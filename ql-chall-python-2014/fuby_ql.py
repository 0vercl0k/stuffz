#!/usr/bin/env python

"""
  Decompiles a .pyc or .pyo file into a human-readable .py source file.
  >> Hacked a bit to decompile Quarkslab's 2014 security challenge
  >> by Axel "@0vercl0k" Souchet

  fupy is free software: you can redistribute it and/or modify
  it under the terms of the GNU Lesser General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
 
  fupy is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU Lesser General Public License for more details.
 
  You should have received a copy of the GNU Lesser General Public License
  along with fupy. If not, see <http://www.gnu.org/licenses/>.

  Contact: Guillaume Delugre <guillaume (at) security-labs (dot) org>
"""

import sys
import imp, dis, opcode, marshal
import types
import __builtin__

class Statement:
  """ Python generic statement. """
  def __init__(self, indent_level = 0):
    self.indent_level = indent_level

  def set_indent_level(self, level):
    self.indent_level = level

  def make_indent(self, indent):
    return indent * self.indent_level

  def __eq__(self, s):
    if isinstance(s, Statement):
      saved_indent_levels = self.indent_level, s.indent_level
      self.set_indent_level(0)
      s.set_indent_level(0)
      if hasattr(self, 'parenthesize'):
        saved_self_parenthesize = self.parenthesize
        self.parenthesize = True
      if hasattr(s, 'parenthesize'):
        saved_other_parenthesize = s.parenthesize  
        s.parenthesize = True

      equals = self.write(' ') == s.write(' ')

      self.set_indent_level(saved_indent_levels[0])
      s.set_indent_level(saved_indent_levels[1])
      if hasattr(self, 'parenthesize'):
        self.parenthesize = saved_self_parenthesize
      if hasattr(s, 'parenthesize'):
        self.parenthesize = saved_other_parenthesize
      return equals
    else:
      return False

  def __ne__(self, s):
    return not (self == s)

  @staticmethod
  def auto_indent(writer):
    def do_indent(self, indent = ''):
      return indent * self.indent_level + writer(self, indent)
    return do_indent

class Block(Statement):
  """ Python compound statement. Contains one or more indented block of statements.
  Can be
    - if/elif/else 
    - for in..else
    - while..else
    - try..except..else..finally
    - with
    - def
    - class
  """
  def __init__(self, statements = [], indent_level = 0):
    Statement.__init__(self, indent_level)
    self.statements = statements
    for statement in statements:
      statement.set_indent_level(self.indent_level + 1)

  def append_statement(self, statement):
    self.statements.append(statement)
    statement.set_indent_level(self.indent_level + 1)

  def set_indent_level(self, level):
    Statement.set_indent_level(self, level)
    for statement in self.statements:
      statement.set_indent_level(level + 1)

  def replace_statements(self, match, new, rec = False):
    for i, statement in enumerate(self.statements):
      if rec and isinstance(statement, Block):
        statement.replace_statements(match, new, rec)
      if match(statement):
        self.statements[i] = new(statement)
        self.statements[i].set_indent_level(self.indent_level + 1)

  def delete_statements(self, match, rec = False):
    pos = []
    for i, statement in enumerate(self.statements):
      if rec and isinstance(statement, Block):
        statement.delete_statements(cond)
      if match(statement):
        pos.insert(0, i)
    for i in pos:
      self.statements.pop(i)
    if len(self.statements) == 0:
      self.append_statement(Pass())

  def write(self, indent = ''):
    # Reduce conditional blocks to assert statements when possible
    i = 0
    while i < len(self.statements):
      s = self.statements[i]
      next = i < len(self.statements) - 1 and self.statements[i + 1]
      if isinstance(s, If) and not isinstance(next, Elif):
        if len(s.statements) == 1 and isinstance(s.statements[0], Raise) and s.statements[0].exception == Variable('AssertionError'):
          self.statements[i] = Assert(s.expr.expr if isinstance(s.expr, UnaryOp) and s.expr.op == 'not ' else UnaryOp('not ', s.expr), s.statements[0].param)
          self.statements[i].set_indent_level(self.indent_level + 1)
          if isinstance(next, Else):
            self.statements.pop(i + 1)
            self.statements[i+1:i+2] = next.statements
            for statement in next.statements:
              statement.set_indent_level(self.indent_level + 1)
        elif isinstance(next, Else) and len(next.statements) == 1 and isinstance(next.statements[0], Raise) and next.statements[0].exception == Variable('AssertionError'):
          self.statements[i] = Assert(s.expr, next.statements[0].param)
          self.statements[i].set_indent_level(self.indent_level + 1)
          self.statements.pop(i + 1)
          self.statements[i+1:i+2] = s.statements
          for statement in s.statements:
            statement.set_indent_level(self.indent_level + 1)
      i = i + 1
      
    if len(self.statements) == 0:
      self.append_statement(Pass())
    return "\n".join([statement.write(indent) for statement in self.statements])

class Expression(Statement):
  """ Python generic expression. """
  def __hash__(self):
    return hash(id(self))

class ExpressionList(Expression):
  """ List of expressions : expr1, expr2, ... """
  def __init__(self, exprs = None):
    Expression.__init__(self)
    if exprs:
      self.exprs = exprs
    else:
      self.exprs = []

  def append(self, expr):
    self.exprs.append(expr)

  @Statement.auto_indent
  def write(self, indent = ''):
    return ", ".join([expr.write() for expr in self.exprs])

class ConditionalExpression(Expression):
  """ Conditional expression : expr1 if cond else expr2 """
  def __init__(self, if_expr, cond_expr, else_expr):
    Expression.__init__(self)
    self.if_expr = if_expr
    self.cond_expr = cond_expr
    self.else_expr = else_expr

  @Statement.auto_indent
  def write(self, indent = ''):
    return self.if_expr.write() + " if " + self.cond_expr.write() + " else " + self.else_expr.write()

class Assignment(Expression):
  """ Assignement expr1 = expr2 """
  def __init__(self, left, right):
    Expression.__init__(self)
    self.left = left
    self.right = right

  @Statement.auto_indent
  def write(self, indent = ''):
    return self.left.write() + " = " + self.right.write()

class GetAttr(Expression):
  """ Expression attribute expr.attr """
  def __init__(self, expr, attr):
    Expression.__init__(self)
    self.base = expr
    if isinstance(self.base, BinaryOp):
      self.base.parenthesize = True
    self.attr = attr

  @Statement.auto_indent
  def write(self, indent = ''):
    return self.base.write() + "." + self.attr

class Variable(Expression):
  """ Expression as variable name """
  def __init__(self, name):
    Expression.__init__(self)
    self.name = name

  def __hash__(self):
    return hash(self.name)

  def __eq__(self, other):
    return isinstance(other, Variable) and (self.name == other.name)

  def __ne__(self, other):
    return not (self == other)

  @Statement.auto_indent
  def write(self, indent = ''):
    return self.name

class Constant(Expression):
  """ Expression as constant (e.g "foo", (1,2,x)) """
  def __init__(self, value):
    Expression.__init__(self)
    self.value = value

  def __hash__(self):
    return hash(self.value)

  def __eq__(self, other):
    return isinstance(other, Constant) and (self.value == other.value)

  def __ne__(self, other):
    return not (self == other)

  @Statement.auto_indent
  def write(self, indent = ''):
    if isinstance(self.value, types.ListType):
      values = [ value.write() if isinstance(value, Expression) else repr(value) for value in self.value ]
      out = "[" + ", ".join(values) + "]"
    elif isinstance(self.value, types.TupleType):
      values = [ value.write() if isinstance(value, Expression) else repr(value) for value in self.value ]
      out = "(" + ", ".join(values)
      if len(values) == 1:
        out += ","
      out += ")"
    elif isinstance(self.value, types.DictType):
      couples = []
      for key, value in self.value.iteritems():
        key = key.write() if isinstance(key, Expression) else repr(key)
        value = value.write() if isinstance(value, Expression) else repr(value)
        couples.append(key + ": " + value)
      out = "{" + ", ".join(couples) + "}"
    elif isinstance(self.value, set):
      values = [ value.write() if isinstance(value, Expression) else repr(value) for value in self.value ]
      out = "{" + ", ".join(values) + "}"
    else:
      out = repr(self.value)
    return out

class Comprehension(Expression):
  """ Comprehension expression : expr1 for vars in expr2 """
  def __init__(self, expr, variables, iterable, if_expr = None):
    Expression.__init__(self)
    self.expr = expr
    self.variables = variables
    self.iterable = iterable
    self.if_expr = if_expr

  @Statement.auto_indent
  def write(self, indent = ''):
    var_list = ", ".join([var.write() for var in self.variables])
    out = self.expr.write() + " for " + var_list + " in " + self.iterable.write()
    if self.if_expr:
      out += " if " + self.if_expr.write()
    return out

class TypedComprehension(Expression):
  """ List/set/dict comprehensions """
  def __init__(self, comp):
    Expression.__init__(self)
    self.comp = comp

class ListComprehension(TypedComprehension):
  """ List comprehension : [expr1 for vars in expr2] """
  @Statement.auto_indent
  def write(self, indent = ''):
    return '[' + self.comp.write() + ']'

class SetComprehension(TypedComprehension):
  """ Set comprehension : {expr1 for vars in expr2} """
  @Statement.auto_indent
  def write(self, indent = ''):
    return '{' + self.comp.write() + '}'

class DictComprehensionEntry:
  """ Entry in dict comprehension : key_expr : value_expr """
  def __init__(self, key_expr, value_expr):
    self.key_expr = key_expr
    self.value_expr = value_expr

  def write(self, indent = ''):
    return self.key_expr.write() + ' : ' + self.value_expr.write()

class DictComprehension(TypedComprehension):
  """ Dict comprehension : { key_expr : value_expr for vars in expr } """
  @Statement.auto_indent
  def write(self, indent = ''):
    return '{' + self.comp.write() + '}'

class Generator(Expression):
  """ Generator expression : (expr1 for vars in expr2) """
  def __init__(self, comp):
    Expression.__init__(self)
    self.comp = comp
    self.parenthesize = True

  @Statement.auto_indent
  def write(self, indent = ''):
    out = ''
    if self.parenthesize:
      out += '('
    out += self.comp.write()
    if self.parenthesize:
      out += ')'
    return out

class UnaryOp(Expression):
  """ Expression with unary operator (e.g ~expr) """
  def __init__(self, op, expr):
    Expression.__init__(self)
    self.op = op
    self.expr = expr
    self.parenthesize = False
    if isinstance(self.expr, BinaryOp) or isinstance(self.expr, UnaryOp):
      if self.expr.precedence() < self.precedence():
        self.expr.parenthesize = True

  def precedence(self):
    return PythonDecompiler.unary_operator_precedences[self.op]

  @Statement.auto_indent
  def write(self, indent = ''):
    out = ''
    if self.parenthesize:
      out += '('
    out += self.op + self.expr.write()  
    if self.parenthesize:
      out += ')'
    return out

class UnaryConvert(Expression):
  """ Expression with convert operator (`expr`) """
  def __init__(self, expr):
    Expression.__init__(self)
    self.expr = expr

  @Statement.auto_indent
  def write(self, indent = ''):
    return '`' + self.expr.write()  + '`'

class BinaryOp(Expression):
  """ Expression with binary operator (e.g expr1 == expr2) """
  def __init__(self, left, op, right):
    Expression.__init__(self)
    self.op = op
    self.left = left
    self.right = right
    self.parenthesize = False
    logical_ops = ( 'and', 'or' )
    if self.op in logical_ops:
      neg_op = logical_ops[1-logical_ops.index(self.op)]
      if isinstance(self.left, BinaryOp) and self.left.op == neg_op:
        self.left.parenthesize = True
      if isinstance(self.right, BinaryOp) and self.right.op == neg_op:
        self.right.parenthesize = True
    else:
      if isinstance(self.left, BinaryOp) or isinstance(self.left, UnaryOp):
        if self.left.precedence() < self.precedence():
          self.left.parenthesize = True
      if isinstance(self.right, BinaryOp) or isinstance(self.right, UnaryOp):
        if self.precedence() == self.right.precedence() and not self.commutative():
          self.right.parenthesize = True
        elif self.right.precedence() < self.precedence():
          self.right.parenthesize = True
  
  def commutative(self):
    return self.op in PythonDecompiler.commutative_operators

  def precedence(self):
    return PythonDecompiler.binary_operator_precedences[self.op]

  def first(self):
    if isinstance(self.left, BinaryOp):
      return self.left.first
    else:
      return self.left

  def last(self):
    if isinstance(self.right, BinaryOp):
      return self.right.last
    else:
      return self.right

  @Statement.auto_indent
  def write(self, indent = ''):
    out = ''
    if self.parenthesize:
      out += '('
    out += self.left.write() + " " + self.op + " " + self.right.write()
    if self.parenthesize:
      out += ')'
    return out

class BinarySubscr(Expression):
  """ Expression expr1[expr2]. """
  def __init__(self, base_expr, index_expr):
    Expression.__init__(self)
    self.base_expr = base_expr
    if isinstance(self.base_expr, BinaryOp):
      self.base_expr.parenthesize = True
    self.index_expr = index_expr

  @Statement.auto_indent
  def write(self, indent = ''):
    return self.base_expr.write() + "[" + self.index_expr.write() + "]"

class FunctionCall(Expression):
  """ Function call expression : expr(expr1, expr2, param = expr3) """
  def __init__(self, expr, pos_args = [], key_args = {}, var_args = None, kwvar_args = None):
    Expression.__init__(self)
    self.function = expr
    self.pos_args = pos_args
    self.key_args = key_args
    self.var_args = var_args
    self.kwvar_args = kwvar_args
    # rare case where generator does not need parenthesises
    if len(self.key_args) == 0 and len(self.pos_args) == 1 and isinstance(self.pos_args[0], Generator):
      self.pos_args[0].parenthesize = False

  @Statement.auto_indent
  def write(self, indent = ''):
    args = ", ".join([arg.write() for arg in self.pos_args ])
    if len(self.key_args) > 0:
      if len(args) > 0:
        args += ", "
      keys = self.key_args.keys()
      keys.sort()
      args += ", ".join([key + " = " + self.key_args[key].write() for key in keys])
    if self.var_args:
      if len(args) > 0:
        args += ", "
      args += '*' + self.var_args.write()
    if self.kwvar_args:
      if len(args) > 0:
        args += ", "
      args += '**' + self.kwvar_args.write()
    return self.function.write() + "(" + args + ")"

class Slice(Expression):
  """ Slice expression : start:stop:step """
  def __init__(self, start = None, stop = None, step = None):
    Expression.__init__(self)
    self.start = start
    self.stop = stop
    self.step = step

  @Statement.auto_indent
  def write(self, indent = ''):
    out = ''
    if self.start != None and self.start != Constant(None):
      out += self.start.write()
    out += ':'
    if self.stop != None and self.stop != Constant(None):
      out += self.stop.write()
    if self.step != None and self.step != Constant(None):
      out += ':' + self.step.write()
    return out

class Yield(Expression):
  """ Yield expression. """
  def __init__(self, expr):
    Statement.__init__(self)
    self.expr = expr

  @Statement.auto_indent
  def write(self, indent = ''):
    return "yield " + self.expr.write()

class Lambda(Expression):
  """ Lambda expression: lambda args: expr """
  def __init__(self, args, default_args, statements):
    Expression.__init__(self)
    self.args = args
    self.default_values = default_args
    self.statements = statements
    self.__remove_returns()

  def __remove_returns(self):
    for i, statement in enumerate(self.statements):
      if isinstance(statement, Return):
        self.statements[i] = statement.expr
      elif isinstance(statement, Block):
        statement.replace_statements(match = (lambda s: isinstance(s, Return)), new = (lambda s: s.expr), rec = True)

  @Statement.auto_indent
  def write(self, indent = ''):
    args = []
    first_default = len(self.args) - len(self.default_values)
    for i in range(0, first_default):
      args.append(self.args[i])
    for i in range(first_default, len(self.args)):
      args.append(self.args[i] + " = " + self.default_values[i - first_default].write())
    out = "(lambda " + ", ".join([str(arg) for arg in args]) + ": "
    out += "; ".join([ statement.write() for statement in self.statements ]) + ")"
    return out

class With(Block):
  """ With block : with expr as var: statements """
  def __init__(self, expr, var, statements):
    Block.__init__(self, statements)
    self.expr = expr
    self.var = var

  @Statement.auto_indent
  def write(self, indent):
    out = "with " + self.expr.write()
    if self.var:
      out += " as " + self.var.write()
    out += ":\n" 
    out += Block.write(self, indent)
    return out

class For(Block):
  """ For block : for variables in expr: statements """
  def __init__(self, variables, expr, statements):
    Block.__init__(self, statements)
    self.variables = variables
    self.expr = expr

  @Statement.auto_indent
  def write(self, indent):
    var_list = ", ".join([ var.write() for var in self.variables ]) 
    return "for " + var_list + " in " + self.expr.write() + ":\n" + Block.write(self, indent)

class While(Block):
  """ While block: while expr: statements """
  def __init__(self, expr, statements):
    Block.__init__(self, statements)
    self.expr = expr

  @Statement.auto_indent
  def write(self, indent):
    return "while " + self.expr.write() + ":\n" + Block.write(self, indent)

class If(Block):
  """ If block: if expr: statements """
  def __init__(self, expr, statements):
    Block.__init__(self, statements)
    self.expr = expr

  @Statement.auto_indent
  def write(self, indent):
    return "if " + self.expr.write() + ":\n" + Block.write(self, indent)

class Elif(Block):
  """ Elif block: elif expr: statements
  Can appear after an If statement or another Elif statement.
  """
  def __init__(self, expr, statements):
    Block.__init__(self, statements)
    self.expr = expr

  @Statement.auto_indent
  def write(self, indent):
    return "elif " + self.expr.write() + ":\n" + Block.write(self, indent)

class Else(Block):
  """ Else block: else: statements
  Can appear after If, Elif, For, While, Try statements.
  """
  @Statement.auto_indent
  def write(self, indent):
    return "else:\n" + Block.write(self, indent)

class Try(Block):
  """ Try block """

  def __init__(self, statements):
    Block.__init__(self, statements)

  @Statement.auto_indent
  def write(self, indent):
    return "try:\n" + Block.write(self, indent)

class Except(Block):
  """ Except block: except exc as name: statements """

  def __init__(self, statements, exc = None, as_name = None):
    Block.__init__(self, statements)
    self.exc = exc
    self.as_name = as_name

  @Statement.auto_indent
  def write(self, indent):
    out = "except" 
    if self.exc:
      out += ' ' + self.exc.write()
    if self.as_name:
      out += " as " + self.as_name.write()
    out += ":\n"
    out += Block.write(self, indent)
    return out

class Finally(Block):
  """ Finally block """

  @Statement.auto_indent
  def write(self, indent):
    return "finally:\n" + Block.write(self, indent)

class DocString(Statement):
  """ Docstring comment. """
  def __init__(self, comment):
    Statement.__init__(self)
    self.comment = comment

  @Statement.auto_indent
  def write(self, indent):
    lines = self.comment.split("\n")
    indented_lines = [ self.make_indent(indent) + line.lstrip() for line in lines[1:] ]
    return '"""' + "\n".join(lines[0:1] + indented_lines) + '"""'

class ClassDefinition(Block):
  """ Class definition block: class name(superclasses): statements """
  def __init__(self, name, supers, statements):
    Block.__init__(self, statements)
    self.name = name
    self.supers = supers
    self.docstring = None
    docstrings = filter(
      lambda s: isinstance(s, Assignment) and s.left == Variable('__doc__'), 
      self.statements
    )
    if len(docstrings) > 0:
      self.docstring = DocString(docstrings[0].right.value)
      self.docstring.set_indent_level(self.indent_level + 1)
    self.delete_statements(
      match = lambda s: isinstance(s, Return) or isinstance(s, Assignment) and (s.left == Variable('__module__') or s.left == Variable('__doc__')), 
      rec = False
    )
    methods = filter(
      lambda s: isinstance(s, FunctionDefinition),
      self.statements
    )
    for method in methods:
      self.unmangle(method) 
         
  def unmangle(self, method):
    if method.name[0:1] == '_' and method.name[1:len(self.name)+1] == self.name:
      method.name = method.name[len(self.name)+1:]

  def set_indent_level(self, level):
    Block.set_indent_level(self, level)
    if self.docstring:
      self.docstring.set_indent_level(level + 1)

  @Statement.auto_indent
  def write(self, indent):
    out = "class " + self.name
    if len(self.supers) > 0:
      supers = ", ".join([superclass.write() for superclass in self.supers])
      out += "(" + supers + ")"
    out += ":\n"
    if self.docstring:
      out += self.docstring.write(indent) + "\n"
    out += Block.write(self, indent)
    if len(self.statements) > 0 and not isinstance(self.statements[-1], FunctionDefinition) and not isinstance(self.statements[-1], ClassDefinition):
      out += "\n"
    return out

class FunctionDefinition(Block):
  """ Function definition block: 
    def func(args, arg_n = default_arg_1, arg_n+1 = default_arg_2): statements 
  """
  def __init__(self, name, args, default_args, varargs, kwvarargs, statements):
    Block.__init__(self, statements)
    self.name = name
    self.args = args
    self.default_values = default_args
    self.varargs = varargs
    self.kwvarargs = kwvarargs
    self.docstring = None
    if len(statements) > 0 and statements[-1].write('') == 'return':
      statements.pop()

  def set_docstring(self, string):
    self.docstring = DocString(string)
    self.docstring.set_indent_level(self.indent_level + 1)

  def set_indent_level(self, level):
    Block.set_indent_level(self, level)
    if self.docstring:
      self.docstring.set_indent_level(level + 1)

  @Statement.auto_indent
  def write(self, indent):
    args = []
    first_default = len(self.args) - len(self.default_values)
    for i in range(0, first_default):
      args.append(self.args[i])
    for i in range(first_default, len(self.args)):
      args.append(self.args[i] + " = " + self.default_values[i - first_default].write())
    out = "def " + self.name + "(" + ", ".join(args)
    if self.varargs:
      if len(args) > 0:
        out += ", "
      out += "*" + self.varargs
    if self.kwvarargs:
      if len(args) > 0 or self.varargs:
        out += ", "
      out += "**" + self.kwvarargs
    out += "):\n"
    if self.docstring:
      out += self.docstring.write(indent) + "\n"
    out += Block.write(self, indent) + "\n"
    return out

class Import(Statement):
  """ Import statement.
  Equivalent to 
    module = __import__('module', fromlist = None, level = -1).
  """
  def __init__(self, module, as_name = None):
    Statement.__init__(self)
    self.module = module
    self.as_name = as_name

  @Statement.auto_indent
  def write(self, indent = ''):
    out = "import " + '.'.join(self.module.path)
    if self.as_name:
      out += " as " + self.as_name.write()
    return out

class ImportFrom(Statement):
  """ Import from statement.
  Equivalent to 
    name = __import__('module', fromlist = None, level = -1).name.
  """
  def __init__(self, module, name, as_name = None):
    Statement.__init__(self)
    self.module = module
    self.name = name
    self.as_name = as_name

  @Statement.auto_indent
  def write(self, indent = ''):
    out = "from " + '.'.join(self.module.path) + " import " + self.name.write()
    if self.as_name:
      out += " as " + self.as_name.write()
    return out

class Assert(Statement):
  """ Assert statement.
  Equivalent to 
    if not expr: raise AssertionError(message)
  """
  def __init__(self, expr, message = None):
    Statement.__init__(self)
    self.expr = expr
    self.message = message

  @Statement.auto_indent
  def write(self, indent = ''):
    out = "assert " + self.expr.write()
    if self.message:
      out += ", " + self.message.write()
    return out

class Print(Statement):
  """ Print statement. """
  def __init__(self, expr_list = None):
    Statement.__init__(self)
    if expr_list:
      self.expr_list = expr_list
    else:
      self.expr_list = ExpressionList()
    self.new_line = False

  @Statement.auto_indent
  def write(self, indent = ''):
    out = "print " + self.expr_list.write()
    if not self.new_line:
      out += ","
    return out

class ExtendedPrint(Statement):
  """ Extended print statement. """
  def __init__(self, filedesc, expr_list = None):
    Statement.__init__(self)
    self.filedesc = filedesc
    if expr_list:
      self.expr_list = expr_list
    else:
      self.expr_list = ExpressionList()
    self.new_line = False

  @Statement.auto_indent
  def write(self, indent = ''):
    out = "print >> " + self.filedesc.write() + ", " + self.expr_list.write()
    if not self.new_line:
      out += ","
    return out

class Break(Statement):
  """ break statement. """
  @Statement.auto_indent
  def write(self, indent = ''):
    return "break"

class Continue(Statement):
  """ continue statement. """
  @Statement.auto_indent
  def write(self, indent = ''):
    return "continue"

class Return(Statement):
  """ return statement. """
  def __init__(self, expr = None):
    Statement.__init__(self)
    self.expr = expr

  @Statement.auto_indent
  def write(self, indent = ''):
    out = "return"
    if self.expr != None and self.expr != Constant(None):
      out += " " + self.expr.write()
    return out

class Global(Statement):
  """ global statement """
  def __init__(self, var):
    Statement.__init__(self)
    self.var = var

  @Statement.auto_indent
  def write(self, indent = ''):
    return "global " + self.var.write()

class Del(Statement):
  """ del statement. """
  def __init__(self, expr):
    Statement.__init__(self)
    self.expr = expr

  @Statement.auto_indent
  def write(self, indent = ''):
    return "del " + self.expr.write()

class Raise(Statement):
  """ raise statement. """
  def __init__(self, exception = None, param = None, trace = None):
    Statement.__init__(self)
    self.exception = exception
    self.param = param
    self.trace = trace

  @Statement.auto_indent
  def write(self, indent = ''):
    out = "raise"
    if self.exception != None:
      out += " " + self.exception.write()
      if self.param != None:
        out += ", " + self.param.write()
        if self.trace != None:
          out += ", " + self.trace.write()
    return out

class Decorator(Statement):
  """ Function decorator. """
  def __init__(self, expr):
    Statement.__init__(self)
    self.expr = expr
    
  @Statement.auto_indent
  def write(self, indent = ''):
    return "@" + self.expr.write()

class Exec(Statement):
  """ exec statement. """
  def __init__(self, expr, global_vars, local_vars):
    Statement.__init__(self)
    self.expr = expr
    self.global_vars = global_vars
    self.local_vars = local_vars

  @Statement.auto_indent
  def write(self, indent = ''):
    out = "exec " + self.expr.write()
    if self.global_vars != Constant(None):
      out += " in " + self.global_vars.write()
      if self.local_vars != Constant(None):
        out += ", " + self.local_vars.write()
    return out

class Pass(Statement):
  """ pass statement. """
  @Statement.auto_indent
  def write(self, indent = ''):
    return "pass"

class PythonProgram(Block):
  """ Python program. This is what we wish to reconstruct.
  The python source is considered as a block of statements.
  """
  def __init__(self, statements):
    Block.__init__(self, statements, -1)
    self.delete_statements(match = lambda s: isinstance(s, Return), rec = False)
    docstrings = filter(
      lambda s: isinstance(s, Assignment) and s.left == Variable('__doc__'), 
      self.statements
    )
    if len(docstrings) > 0:
      statements.insert(0, DocString(docstrings[0].right.value))
    self.delete_statements(
      match = lambda s: isinstance(s, Assignment) and s.left == Variable('__doc__'), 
      rec = False
    )

class PythonExceptionClass:
  """
  Internally used by the decompiler to represent the current exception class.
  """
  def write(self, indent = ''):
    return '.CurrentExceptionClass'
 
class PythonExceptionInstance:
  """
  Internally used by the decompiler to represent the current exception instance.
  """
  def write(self, indent = ''):
    return '.CurrentException'
 
class PythonImportedModule:
  """
  Internally used by the decompiler to represent an imported module.
  """
  def __init__(self, name):
    self.path = name.split('.')

class PythonImportedModuleAttr:
  """
  Internally used by the decompiler to represent an imported module name.
  """
  def __init__(self, module, name):
    self.module = module
    self.name = name

class PythonCompiledFunction:
  """
  Internally used by the decompiler to represent a function made out of a precompiled code object.
  """
  def __init__(self, code, default_args):
    self.code = code
    self.default_args = default_args

class PythonCompiledGenerator:
  """
  Internally used by the decompiler to represent a precompiled generator object.
  """
  def __init__(self, code):
    self.code = code

class PythonCompiledComprehension:
  """
  Internally used by the decompiler to represent set and dict comprehensions.
  """
  def __init__(self, code):
    self.code = code

class PythonCompiledFunctionCall:
  """
  Internally used by the decompiler to represent a call to a precompiled function.
  """
  def __init__(self, compiled):
    self.function = compiled

class PythonCompiledClass:
  """
  Internally used by the decompiler to represent a compiled class object.
  """
  def __init__(self, supers, code):
    self.supers = supers
    self.code = code

class PythonIterator:
  """
  Internally used by the decompiler to represent a volatile iterator.
  """
  def __init__(self, expr):
    self.expr = expr
    self.walked = False
    self.alive = True
    self.exhausted_addr = None

class PythonIterate:
  """
  Internally used by the decompiler to mark a next() call on a volatile iterator.
  """
  def __init__(self, iterator, addr):
    self.iterator = iterator
    self.addr = addr

class PythonOpenedComprehension(Statement):
  """
  Fake statement. Internally used by the decompiler for reconstructing comprehensions.
  """
  def __init__(self, comp):
    self.init = comp
    self.current = comp.comp # Comprehension component in type comprehension

class PythonBlockFinalizer(Block):
  """
  Internally used by the decompiler to represent Else statements of loops.
  """

class PythonBasicBlock:
  """
  Internally used by the decompiler to analyze control flows.
  """
  def __init__(self, addr):
    self.addr = addr
    self.children = set()   # direct children
    self.parents = set()    # direct parents
    self.ancestors = None
    self.end_addr = 0

  def add_child(self, block):
    self.children.add(block)
    block.parents.add(self)

  def remove_child(self, block):
    if block in self.children:
      self.children.remove(block)
      block.parents.remove(self)

  def get_ancestors(self, walked = None):
    if walked is None:
      walked = set()
    if self.ancestors:
      return self.ancestors
    else:
      self.ancestors = set()
      for parent in self.parents:
        if parent not in walked:
          walked.add(parent)
          self.ancestors |= parent.get_ancestors(walked)
      self.ancestors |= self.parents
      return self.ancestors

  def __hash__(self):
    return hash(self.addr)

  # Block are compared by their starting and ending addresses only
  def __eq__(self, block):
    assert isinstance(block, PythonBasicBlock)
    return self.addr == block.addr 

  def __ne__(self, block):
    return not (self == block)

  def __lt__(self, block):
    assert isinstance(block, PythonBasicBlock)
    return self.addr < block.addr

class PythonUnpackedSequence:
  """
  Internally used by the decompiler to represent an unpacked sequence.
  """
  def __init__(self, expr, size):
    self.expr = expr
    self.size = size
    self.variables = [ None ] * size
    self.nested = False
    self.parent = None
    self.parent_index = None

  def bind(self, index, var):
    self.variables[index] = var

  def is_complete(self):
    return all(self.variables)

class PythonUnpackedValue:
  """
  Internally used by the decompiler to represent an unpacked value from a sequence.
  """
  def __init__(self, sequence, index):
    self.sequence = sequence
    self.index = index

class PythonWithEnter:
  """
  Internally used by the decompiler to represent a return value from __enter__.
  Used in with statements.
  """
  def __init__(self, expr):
    self.expr = expr

class PythonWithExit:
  """
  Internally used by the decompiler to represent a pointer to __exit__.
  Used in with statements.
  """

class PythonCompiledObjectFile:
  """
  Helper class for opening Python compiled object files (.pyc or .pyo)
  """
  
  version_by_magic = {
    '\xb3\xf2\r\n' : 2.5,
    '\xd1\xf2\r\n' : 2.6,
    '\x03\xf3\r\n' : 2.7
  }
  
  def __init__(self, path):
    fp = open(path, 'rb')

    try:
      self.magic = fp.read(4)
      if self.magic != imp.get_magic():
        raise Exception("Magic constant does not match with current Python version.")

      self.timestamp = fp.read(4)
      self.code = marshal.load(fp)      
      if not isinstance(self.code, types.CodeType):
        raise TypeError("Cannot find main code object.")

    finally:
      fp.close()
      
  def python_version(self):
    return self.version_by_magic[self.magic]

class PythonDecompilerError(Exception):
  def __init__(self, message, addr = None, opname = None, arg = None):
    Exception.__init__(self, message)
    self.addr = addr
    self.opname = opname
    self.arg = arg

  def __str__(self):
    info = "Decompilation error: %s" % self.message
    if self.addr and self.opname:
      info += " [address: %d, instruction: %s" % (self.addr, self.opname)
    if self.arg:
      info += " (%s)" % repr(self.arg)
    info += "]"
    return info

class PythonDecompiler:
  binary_operators = {
    'ADD' : '+',
    'SUBTRACT' : '-',
    'MULTIPLY' : '*',
    'DIVIDE' : '/',
    'TRUE_DIVIDE' : '/',
    'FLOOR_DIVIDE' : '//',
    'MODULO' : '%',
    'POWER' : '**',
    'LSHIFT' : '<<',
    'RSHIFT' : '>>',
    'AND' : '&',
    'OR' : '|',
    'XOR' : '^'
  }

  unary_operators = {
    'POSITIVE' : '+',
    'NEGATIVE' : '-',
    'NOT' : 'not ',
    'INVERT' : '~'
  }

  binary_operator_precedences = {
    'or' : 1,
    'and' : 2,
    'in' : 4, 'not in' : 4, 'is' : 4, 'is not' : 4,
    '<' : 4, '<=' : 4, '>' : 4, '>=' : 4, '<>' : 4, '!=' : 4, '==' : 4,
    '|' : 5,
    '^' : 6,
    '&' : 7,
    '<<' : 8, '>>' : 8,
    '+' : 9, '-' : 9,
    '*' : 10, '/' : 10, '//' : 10, '%' : 10,
    '**' : 12,
    'exception match' : 13
  }

  commutative_operators = ( '+', '*', '&', '^', '|', '!=', '==', '<>' )
  comparison_operators = ( '<', '<=', '==', '!=', '<>', '>=', '>' )

  unary_operator_precedences = {
    'not ' : 3,
    '+' : 11, '-' : 11, '~' : 11
  }

  conditional_jump_insns = ( 
    'POP_JUMP_IF_TRUE', 
    'POP_JUMP_IF_FALSE', 
    'JUMP_IF_TRUE_OR_POP', 
    'JUMP_IF_FALSE_OR_POP',
    'JUMP_IF_TRUE',   # < 2.7
    'JUMP_IF_FALSE'   # < 2.7
  )
  
  conditional_insns = ( 
    'POP_JUMP_IF_TRUE', 
    'POP_JUMP_IF_FALSE', 
    'JUMP_IF_TRUE_OR_POP', 
    'JUMP_IF_FALSE_OR_POP',
    'JUMP_IF_TRUE',   # < 2.7
    'JUMP_IF_FALSE',  # < 2.7
    
    'SETUP_FINALLY',  # finally clause
    'SETUP_EXCEPT',   # except clause
  )

  jump_insns = ( 
    'POP_JUMP_IF_TRUE', 
    'POP_JUMP_IF_FALSE', 
    'JUMP_IF_TRUE_OR_POP', 
    'JUMP_IF_FALSE_OR_POP',
    'JUMP_IF_TRUE',   # < 2.7
    'JUMP_IF_FALSE',  # < 2.7
    'JUMP_FORWARD',
    'JUMP_ABSOLUTE',
    'CONTINUE_LOOP',
    # XXX: BREAK_LOOP ??? Need to keep track of loop blocks
    'FOR_ITER',       # finally clause
    'SETUP_FINALLY',  # finally clause
    'SETUP_WITH',     # finally clause
    'SETUP_EXCEPT',   # except clause
    'SETUP_LOOP'
  )

  CODE_FLAG_OPTIMIZED = 1
  CODE_FLAG_NEWLOCALS = 2
  CODE_FLAG_VARARGS = 4
  CODE_FLAG_KWVARARGS = 8
  CODE_FLAG_NESTED = 16
  CODE_FLAG_GENERATOR = 32
  CODE_FLAG_NOFREE = 64

  WHY_NOT = 1
  WHY_EXCEPT = 2
  WHY_RERAISE = 4
  WHY_RETURN = 8
  WHY_BREAK = 16
  WHY_CONTINUE = 32
  WHY_YIELD = 64

  def __init__(self, path):
    if path == 'whocares':
      self.pyc = None
      self.target_version = 2.7
    else:
      self.pyc = PythonCompiledObjectFile(path)
      self.target_version = self.pyc.python_version()
    self.global_vars = set()

  def __disassemble_insn_at(self, bytecode, i):
    """ Return tuple ( opcode, operand, addr_of_next ) from a bytecode string. """
    if ord(bytecode[i:i+1]) == opcode.EXTENDED_ARG:
      ext = (ord(bytecode[i+1:i+2]) << 16) | (ord(bytecode[i+2:i+3]) << 24)
      i = i + 3
    else:
      ext = 0

    op = ord(bytecode[i:i+1])
    arg = None
    if op >= opcode.HAVE_ARGUMENT:
      arg = ord(bytecode[i+1:i+2]) | (ord(bytecode[i+2:i+3]) << 8) | ext
      i = i + 2

    i = i + 1
    return (op, arg, i)

  def __disassemble(self, code):
    """ Return list of tuples ( address, opname, operand, size of instruction ) from a code object. """
    insns = []
    bytecode = code.co_code
    cells = code.co_cellvars + code.co_freevars
    i = 0
    r14d_magic_flag = False
    while i < len(bytecode):
      op_addr = i
      op, arg, i = self.__disassemble_insn_at(bytecode, i)
      idx = arg
      if arg != None:
        if op in opcode.hasconst:
          arg = code.co_consts[arg] 
        elif op in opcode.hasname:
          arg = code.co_names[arg]  
        elif op in opcode.haslocal:
          arg = code.co_varnames[arg]
        elif op in opcode.hascompare:
          arg = opcode.cmp_op[arg]
        elif op in opcode.hasjrel:
          arg = arg + i
        elif op in opcode.hasfree:
          arg = cells[arg]
      # Handle the magic switch flipping & the hybrid opcode
      name = opcode.opname[op]
      if name == 'LOAD_CONST_OR_STORE_FAST':
        # The hybrid opcode: when the switch is not flipped, it is a STORE_FAST
        if r14d_magic_flag == False:
            name = 'STORE_FAST'
            arg = code.co_varnames[idx]
        # When it is, it is a LOAD_CONST
        else:
            name = 'LOAD_CONST'
            arg = code.co_consts[idx]

      if name == 'LOAD_CONST_AND_FLIP_SWITCH':
        # we flip the switch
        name = 'LOAD_CONST'
        r14d_magic_flag = True
      else:
        r14d_magic_flag = False

      if name.startswith('LOAD_CONST'):
        name = 'LOAD_CONST'
      insns.append((op_addr, name, arg, i - op_addr))
    return insns

  def disassemble(self):
    disass = ""
    for addr, opname, arg, _ in self.__disassemble(self.pyc.code):
      disass += "    @%.4d:    %s (%s)\n" % (addr, opname.ljust(20), arg)
    return disass

  def __jmp_to_insn_at(self, insns, addr):
    # Jump to end ( addr of last insn + size of last insn )
    if addr >= self.__last_addr(insns):
      return len(insns)
    i = 0
    while i < len(insns):
      if insns[i][0] == addr:
        break
      i = i + 1
    else:
      raise Exception("Jump to %d out of bounds [%d..%d]" % (addr, self.__first_addr(insns), self.__last_addr(insns)))
    return i

  def __first_addr(self, insns):
    if len(insns) > 0:
      return insns[0][0]
    else:
      return None

  def __last_addr(self, insns):
    if len(insns) > 0:
      return insns[-1][0] + insns[-1][3]
    else:
      return None

  def __next_addr(self, insns, addr):
    n = self.__jmp_to_insn_at(insns, addr)
    return insns[n][0] + insns[n][3]

  def __decompile(self, code):
    """ Decompile a code object.
    Return a list of Statements.
    """
    #if __debug__:
      #print 'Disassembling %s:' % code.co_name
      #dis.dis(code)
      #print '_' * 80
    insns = self.__disassemble(code)
    return self.__decompile_block(insns, [])[1]

  def __decompile_loop(self, insns, stack):
    """ Decompile a loop statement.
        Return ( next_addr, statements )
    """
    next_addr, statements = self.__decompile_block(insns, stack)
    else_block = None
    assert(len(statements) > 0)

    #
    # var = iterate over iterator => for loop
    #
    if isinstance(statements[0], Assignment) and isinstance(statements[0].right, PythonIterate):
      iterate = statements[0].right
      iterator = iterate.iterator
      if isinstance(statements[0].left, ExpressionList):
        var = statements[0].left.exprs
      else:
        var = [ statements[0].left ]
      expr = iterator.expr
      if isinstance(statements[-1], PythonBlockFinalizer):
        else_block = Else(statements.pop().statements)
      loop = For(var, expr, statements[1:])
    #
    # while loop
    #
    else:
      if len(statements) == 1 and isinstance(statements[0], If):
        if_block = statements.pop(0)
        if isinstance(if_block.statements[-1], PythonBlockFinalizer):
          else_block = Else(if_block.statements.pop().statements)
        loop = While(if_block.expr, if_block.statements)
      else:
        if isinstance(statements[-1], PythonBlockFinalizer):
          else_block = Else(statements.pop().statements)
        loop = While(Constant(True), statements)

    # Remove extraneous continue statement
    if len(loop.statements) > 1 and isinstance(loop.statements[-1], Continue):
      loop.statements.pop()

    # Reached end of for loop before cleaning the block (e.g. because of a return statement)
    if isinstance(loop, For) and iterator.alive:
      # Finalize the block, cleanup the stack
      next_addr, finalize_stmts = self.__decompile_block(insns[self.__jmp_to_insn_at(insns, iterate.addr):], stack)
      if len(finalize_stmts) > 0 and isinstance(finalize_stmts[-1], PythonBlockFinalizer):
        else_block = Else(finalize_stmts.pop().statements)
    # Escape while loop
    elif isinstance(loop, While) and next_addr is None or next_addr == self.__first_addr(insns):
      next_addr = self.__last_addr(insns) # escape loop

    loop_stmts = [ loop ]
    if else_block:
      loop_stmts.append(else_block)

    return (next_addr, loop_stmts)

  def __decompile_with(self, expr, finally_addr, insns, stack):
    """ Decompile a with block.
    Return (next_addr, with_block).
    """
    end_with = self.__jmp_to_insn_at(insns, finally_addr)
    _, statements = self.__decompile_block(insns[:end_with], stack)
    var = None
    if len(statements) > 0 and isinstance(statements[0], Assignment) and isinstance(statements[0].right, PythonWithEnter):
      var = statements.pop(0).left
    if len(statements) > 0 and isinstance(statements[-1], PythonBlockFinalizer):
      statements.pop()
    with_block = With(expr, var, statements)
    
    # cleanup with
    #stack.pop() 
    #stack.pop() 

    # finally cleanup
    next_addr, _ = self.__decompile_block(insns[end_with:], stack)
    
    return ( next_addr, with_block )

  def __create_basic_blocks(self, start_addr, insns, blocks):
    """ Recursively create basic blocks """
    addr = start_addr
    block = PythonBasicBlock(addr)
    blocks[addr] = block
    if len(insns) == 0:
      block.end_addr = addr
      return block
    i = 0
    while i < len(insns):
      addr, opname, arg, opsize = insns[i]
      if i > 0 and addr in blocks: # break if we enter existing block
        block.add_child(blocks[addr])
        break
      elif opname == 'RETURN_VALUE' or opname == 'RAISE_VARARGS':
        break  
      elif opname in self.jump_insns or i == len(insns) - 1:
        if opname in self.jump_insns:
          if opname in self.conditional_insns:
            if arg < start_addr: # outer loop iteration, probably a continue statement
              if not arg in blocks:
                blocks[arg] = PythonBasicBlock(arg)
                blocks[arg].end_addr = arg
              block.add_child(blocks[arg])
            addr_list = ( arg, addr + opsize )
          else: # unconditional jump
            if arg < start_addr: # outer loop iteration, probably a continue statement
              if not arg in blocks:
                blocks[arg] = PythonBasicBlock(arg)
                blocks[arg].end_addr = arg
              block.add_child(blocks[arg])
              #break
            addr_list = ( arg, )
        else:
          addr_list = ( addr + opsize, )
        targets = [
          blocks[dest] if dest in blocks
          else self.__create_basic_blocks(dest, insns[self.__jmp_to_insn_at(insns, dest):], blocks)
          for dest in addr_list
        ]
        for target in targets:
          prev_blocks = sorted(filter(lambda b: b < target, blocks.values()), key=lambda b: b.addr)
          if len(prev_blocks) > 0 and prev_blocks[-1].end_addr >= target.addr: # block split
            prev_block = prev_blocks[-1]
            prev_block.end_addr = insns[self.__jmp_to_insn_at(insns, target.addr) - 1][0]
            for child in set(prev_block.children):
              prev_block.remove_child(child) # clear edges
            prev_block.add_child(target)
          block.add_child(target)
        break
      i = i + 1

    block.end_addr = addr
    return block

  def __find_convergent_block(self, src_blocks, blocks, walked):
    """ Recursively find first basic block reachable by all paths from src_blocks
        and for which a parent has exactly one children.
        This basic block is characteristic of the end of a conditional statement.

        Return None if no such basic block exists.
    """
    if len(blocks) == 0:
      return None

    for block in blocks:
      #print 'current block : ',
      #print block.addr
      #print 'parents : ',
      #print [ p.addr for p in block.parents ]
      if any(len(p.children) == 1 for p in block.parents):
        for src_block in src_blocks:
          if not walked.issubset(block.get_ancestors()):
            break
        else:
          return block

    walked |= blocks
    # set of all children of current blocks, minus already walked blocks
    children = reduce(lambda c1, c2: c1 | c2, [ b.children for b in blocks ]) - walked
    return self.__find_convergent_block(src_blocks, children, walked)

  def __reduce_conditional_blocks(self, stmts):
    """ Reduce conditional blocks """
    repass = True
    while repass:
      repass = False
      i = 0
      while i < len(stmts):
        if isinstance(stmts[i], If) or isinstance(stmts[i], Elif):
          j = i + 1
          while j < len(stmts):
            if isinstance(stmts[j], If) or isinstance(stmts[j], Elif):
              # (el)if x: z elif y: z => (el)if x or y: z
              if stmts[i].statements == stmts[j].statements:
                stmts[i].expr = BinaryOp(stmts[i].expr, 'or', stmts[j].expr)
                stmts.pop(j)
                repass = True
                continue
            j = j + 1
        i = i + 1

      i = 0
      while i < len(stmts):
        # if x:         if x and y: | if x:         if not x or y:
        #   if y:   =>    foo       |   if y:   =>    z
        #     foo       z           |     z 
        #   [z]                     | else:
        # z                         |   z
        if isinstance(stmts[i], If) or isinstance(stmts[i], Elif):
          if len(stmts[i].statements) > 0 and isinstance(stmts[i].statements[0], If):
            if i < len(stmts) - 1 and isinstance(stmts[i+1], Else):
              if stmts[i].statements[0].statements == stmts[i+1].statements:
                stmts[i].expr = BinaryOp(UnaryOp('not ', stmts[i].expr), 'or', stmts[i].statements[0].expr)
                stmts[i].statements = stmts.pop(i+1).statements
                repass = True
                continue
            if stmts[i].statements[1:] == stmts[1-len(stmts[i].statements):] or stmts[i].statements[1:] == stmts[i+1:] or len(stmts[i].statements) == 1: 
              stmts[i].expr = BinaryOp(stmts[i].expr, 'and', stmts[i].statements[0].expr) 
              stmts[i].statements = stmts[i].statements[0].statements
              repass = True
              continue
        i = i + 1

    return stmts

  def __factorize_condition(self, expr):
    """ Factorize a logical expression """
    ops = ( 'and', 'or' )
    repass = True
    while repass:
      repass = False
      if isinstance(expr, BinaryOp) and expr.op in ops:
        neg_op = ops[1-ops.index(expr.op)]
        expr.left = self.__factorize_condition(expr.left)
        expr.right = self.__factorize_condition(expr.right)
        #
        # (x < y) and (y < z) = x < y < z
        #
        #if expr.op == 'and' and isinstance(expr.left, BinaryOp) and isinstance(expr.right, BinaryOp) and expr.right.op in self.comparison_operators and expr.left.op in self.comparison_operators and expr.left.last == expr.right.first:
        #  expr = BinaryOp(expr.left, expr.right.op, expr.right.right)
        #  expr.left.parenthesize = expr.parenthesize = False
        
        #
        # (x and y) or (z and y) = (x or z) and y
        #
        if isinstance(expr.left, BinaryOp) and isinstance(expr.right, BinaryOp) and expr.right.op == expr.left.op == neg_op and expr.left.right == expr.right.right:
          expr = BinaryOp(BinaryOp(expr.left.left, expr.op, expr.right.left), neg_op, expr.right.right)
          repass = True
          continue
        #
        # (x and (y or z)) or z = (x and y) or z
        #
        elif isinstance(expr.left, BinaryOp) and expr.left.op == neg_op and isinstance(expr.left.right, BinaryOp) and expr.left.right.op == expr.op and expr.left.right.right == expr.right:
          expr = BinaryOp(BinaryOp(expr.left.left, neg_op, expr.left.right.left), expr.op, expr.right)
          repass = True
          continue

      elif isinstance(expr, UnaryOp) and expr.op == 'not ':
        expr.expr = self.__factorize_condition(expr.expr)
        #
        # not (not x) = x
        #
        if isinstance(expr.expr, UnaryOp) and expr.expr.op == 'not ':
          expr = expr.expr.expr
          repass = True
          continue
        #
        # not ((not x) and (not y)) = x or y
        # not ((not x) or (not y)) = x and y
        #
        elif isinstance(expr.expr, BinaryOp) and expr.expr.op in ops:
          if isinstance(expr.expr.left, UnaryOp) and isinstance(expr.expr.right, UnaryOp):
            if expr.expr.left.op == expr.expr.right.op == 'not ':
              expr = BinaryOp(expr.expr.left, ops[1-ops.index(expr.expr.op)], expr.expr.right)
              repass = True
              continue
    return expr

  def __detect_end_of_statement(self, insns):
    """ Find the next address after a conditional statement """
    blocks = {}
    #print 'creating basic blocks at ' + str(insns[0][0])
    first_block = self.__create_basic_blocks(self.__first_addr(insns), insns, blocks)
    #print 'src_blocks : ',
    #print [ b.addr for b in first_block.children]

    if len(first_block.children) == 1:
      end_block = None
    else:
      end_block = self.__find_convergent_block(first_block.children, first_block.children, set())
    #print 'result : ',
    #if end_block:
    #  print end_block.addr
    #else:
    #  print None

    # Couldn't find a final block
    if not end_block:
      # Check if one destination address resumes to start of loop (continue)
      for b in first_block.children:
        if b.addr <= self.__first_addr(insns):
          end_addr = b.addr
          break
      else:
        end_addr = self.__last_addr(insns)
    else:
      end_addr = end_block.addr

    if end_addr <= self.__first_addr(insns):
      last_addr = self.__last_addr(insns)  
    else:
      last_addr = end_addr

    #print 'bounds : [' + str(insns[0][0]) + ', ' + str(insns[-1][0] + insns[-1][3]) + ']'
    #print 'end_addr = ' + str(end_addr)
    #print 'last_addr = ' + str(last_addr)
    return (end_addr, last_addr)

  # The horror show is about to begin
  def __decompile_condition(self, insns, stack):
    """ Decompile a if/elif/else block.
    Return (next_addr, statements)
    """
    end_addr, last_addr = self.__detect_end_of_statement(insns)

    addr, opname, target, opsize = insns[0]
    if opname[0:8] == 'POP_JUMP':
      cond_expr = stack.pop()
      if_stack = stack[:]
      else_stack = stack[:]
      if opname[-8:] == 'IF_FALSE':
        if_addr = addr + opsize
        else_addr = target
      else:
        if_addr = target
        else_addr = addr + opsize
    else:
      cond_expr = stack[-1]
      if_stack = stack[:]
      else_stack = stack[:]
      if opname[5:13] == 'IF_FALSE':
        if_addr = addr + opsize
        else_addr = target
        if opname[-6:] == 'OR_POP':
          if_stack.pop() # OR_POP
      else:
        if_addr = target
        else_addr = addr + opsize
        if opname[-6:] == 'OR_POP':
          else_stack.pop() # OR_POP

    try:
      if_insns = insns[self.__jmp_to_insn_at(insns, if_addr):self.__jmp_to_insn_at(insns, last_addr)]
    except:
      if_insns = []
    try:
      else_insns = insns[self.__jmp_to_insn_at(insns, else_addr):self.__jmp_to_insn_at(insns, last_addr)]
    except:
      else_insns = []

    # Decompile each branch
    _, if_block = self.__decompile_block(if_insns, if_stack)
    if_stmt = If(cond_expr, if_block)
    _, else_block = self.__decompile_block(else_insns, else_stack)
    else_stmt = Else(else_block)

    # Conditional execution paths must set the stack in a consistent state at return.
    # Something wrong happened if this property is not satisfied.
    assert(len(if_stack) == len(else_stack))

    # Empty statements ? Check the stack for remaining values.
    # XXX: multiple expressions on the stack ??? 
    logical_expr = False
    if len(if_stmt.statements) == 0 and len(else_stmt.statements) == 0:
      #i = len(if_stack) - 1;
      #while i >= 0 and (i > len(stack) - 1 or if_stack[i] != stack[i] or else_stack[i] != stack[i]):
      if len(if_stack) > len(stack) or (len(stack) > 0 and len(if_stack) > 0 and (if_stack[-1] != stack[len(if_stack)-1] or else_stack[-1] != stack[len(else_stack)-1])):
        logical_expr = True
        # if x: x else y => x or y
        if if_stmt.expr == if_stack[-1]:
          if_stack[-1] = self.__factorize_condition(BinaryOp(if_stack[-1], "or", else_stack[-1]))
        # if x: y else x => x and y
        elif if_stmt.expr == else_stack[-1]:
          if_stack[-1] = self.__factorize_condition(BinaryOp(else_stack[-1], "and", if_stack[-1]))
        # if x: z else (y and z) => (x or y) and z
        elif isinstance(else_stack[-1], BinaryOp) and else_stack[-1].op == 'and' and if_stack[-1] == else_stack[-1].right:
          if_stack[-1] = self.__factorize_condition(BinaryOp(BinaryOp(if_stmt.expr, 'or', else_stack[-1].left), 'and', if_stack[-1]))
        # if x: (y or z) else: z => (x and y) or z
        elif isinstance(if_stack[-1], BinaryOp) and if_stack[-1].op == 'or' and else_stack[-1] == if_stack[-1].right:
          if_stack[-1] = self.__factorize_condition(BinaryOp(BinaryOp(if_stmt.expr, 'and', if_stack[-1].left), 'or', else_stack[-1]))
        else: # generic conditional expression
          if_stack[-1] = ConditionalExpression(if_stack[-1], self.__factorize_condition(if_stmt.expr), else_stack[-1]) 
        #i = i - 1
    stack[:] = if_stack
    if logical_expr:
      return (end_addr, [])
    
    # Python < 2.7 does not have POP_* instructions.
    # Stack cleaning inside condition blocks can create dummy statements if the expression is a function call.
    if self.target_version < 2.7:
      while len(if_stmt.statements) > 0 and if_stmt.statements[0] == if_stmt.expr:
        if_stmt.statements.pop(0)
      while len(else_stmt.statements) > 0 and else_stmt.statements[0] == if_stmt.expr:
        else_stmt.statements.pop(0)
    
    """
    if expr1: pass
    else: xxx
    
    => if not expr1: xxx
    """
    if len(if_stmt.statements) == 0 and len(else_stmt.statements) > 0:
      if_stmt.expr = UnaryOp('not ', if_stmt.expr)
      if_stmt.statements = else_stmt.statements
      else_stmt.statements = []

    stmts = [ if_stmt ]
    if len(else_stmt.statements) > 0:
      else_stmts = []
      """ if else: if => if elif: """
      if all(isinstance(s, If) or isinstance(s, Elif) or isinstance(s, Else) for s in else_stmt.statements):
        nested_if = else_stmt.statements.pop(0)
        else_stmts.append(Elif(nested_if.expr, nested_if.statements))
        else_stmts.extend(else_stmt.statements)
      else:
        else_stmts.append(else_stmt)
      stmts.extend(else_stmts)
    # reduction of statements
    stmts = self.__reduce_conditional_blocks(stmts)
    # reduction of expression
    for s in stmts:
      if isinstance(s, If) or isinstance(s, Elif):
        s.expr = self.__factorize_condition(s.expr)
    
    return (end_addr, stmts)

  def __decompile_try_catch(self, insns, stack):
    """ Decompile a try/except/else/finally block 
        Return (next_addr, statements)
    """
    end_addr, last_addr = self.__detect_end_of_statement(insns)

    i = 0
    except_addr = finally_addr = None
    while i < len(insns) and insns[i][1] in ('SETUP_EXCEPT', 'SETUP_FINALLY'):
      arg = insns[i][2]
      if insns[i][1] == 'SETUP_EXCEPT':
        except_addr = arg
      else:
        finally_addr = arg
      i = i + 1

    else_stmt = None
    finally_stmt = None
    stmt_end = self.__jmp_to_insn_at(insns, last_addr)
    next_addr, try_block = self.__decompile_block(insns[i:stmt_end], stack[:])
    if len(try_block) > 0 and isinstance(try_block[-1], PythonBlockFinalizer):
      else_block = try_block.pop().statements
      if len(else_block) > 0 and isinstance(else_block[-1], PythonBlockFinalizer):
        else_block.pop()
      if len(else_block) > 0:
        else_stmt = Else(else_block)
    try_stmt = Try(try_block)

    if finally_addr:
      finally_stack = stack[:]
      finally_stack.append(Constant(None))
      next_addr, finally_stmts = self.__decompile_block(insns[self.__jmp_to_insn_at(insns, finally_addr):], finally_stack)
      finally_stmt = Finally(finally_stmts)

    excepts = []
    if except_addr:
      except_stack = stack[:]
      except_stack.append(Constant(None)) # Dummy traceback
      except_stack.append(PythonExceptionInstance())
      except_stack.append(PythonExceptionClass())
      start_excepts = self.__jmp_to_insn_at(insns, except_addr)
      end_excepts = self.__jmp_to_insn_at(insns, last_addr)
      _, except_stmts = self.__decompile_block(
        insns[start_excepts:end_excepts],
        except_stack
      )
      if len(except_stmts) > 0 and isinstance(except_stmts[-1], PythonBlockFinalizer):
        except_stmts.pop()

      if len(except_stmts) == 0:
        excepts.append(Except([]))

      multiple_excepts = False
      for statement in except_stmts:
        if (isinstance(statement, If) or isinstance(statement, Elif)) and isinstance(statement.expr, BinaryOp) and statement.expr.op == 'exception match':
          multiple_excepts = True
          exc_var = None
          if len(statement.statements) > 0 and isinstance(statement.statements[0], Assignment) and isinstance(statement.statements[0].right, PythonExceptionInstance):
            exc_var = statement.statements.pop(0).left
          except_class = statement.expr.left if isinstance(statement.expr.right, PythonExceptionClass) else statement.expr.right
          excepts.append(Except(statement.statements, except_class, exc_var))
        else:
          if not multiple_excepts:
            excepts.append(Except(except_stmts))
          break

    stmts = [ try_stmt ] + excepts
    if else_stmt and len(excepts) > 0:
      stmts.append(else_stmt)
    if finally_stmt:
      stmts.append(finally_stmt)
    if else_stmt and len(excepts) == 0:
      stmts.extend(else_stmt.statements)
    return (next_addr, stmts)

  def __decompile_comprehension(self, code, argument):
    """ Decompile a comprehension implemented as a code object """
    comp_stmts = self.__decompile(code)
    if len(comp_stmts) != 1 or not isinstance(comp_stmts[0], Return):
      if not isinstance(comp_stmts[0].expr, TypedComprehension):
        raise PythonDecompilerError("Cannot decompile comprehension in code object.")
    comp = comp_stmts[0].expr
    iterable = argument.expr
    nested = comp.comp
    while isinstance(nested.expr, Comprehension):
      nested = nested.expr
    nested.iterable = iterable
    return comp

  def __decompile_generator(self, code, argument):
    """ Decompile an anonymous generator """
    gen_stmts = self.__decompile(code)
    
    # convert statements into a one-line generator expression
    def create_generator_from_statements(first, stmts, current):
      for statement in stmts:
        if isinstance(statement, Yield):
          first.expr = statement.expr
          return current
        elif isinstance(statement, For): # < 2.7
          iterable = statement.expr
          var = statement.variables
          if not current.variables:
            current.variables = var
            if not isinstance(iterable, Variable):
              current.iterable = iterable
          else:
            current = Comprehension(current, var, iterable)
          return create_generator_from_statements(first, statement.statements, current)
        elif isinstance(statement, Assignment) and isinstance(statement.right, PythonIterate):
          iterable = statement.right.iterator.expr
          if isinstance(statement.left, ExpressionList):
            var = statement.left.exprs
          else:
            var = [ statement.left ]
          if not current.variables:
            current.variables = var
            if not isinstance(iterable, Variable):
              current.iterable = iterable
          else:
            current = Comprehension(current, var, iterable)
        elif isinstance(statement, If):
          current.if_expr = statement.expr
          return create_generator_from_statements(first, statement.statements, current)
        else:
          raise PythonDecompilerError("Cannot decompile generator, invalid statements")
      raise PythonDecompilerError("Cannot decompile generator, no yield statement")

    iterable = argument.expr
    init = Comprehension(None, None, iterable)
    return Generator(create_generator_from_statements(init, gen_stmts, init))

  def __decompile_block(self, insns, stack):
    """ Core method for decompiling a block of instructions.
        Returns ( next_addr, statements)
    """
    statements = []
    
    n = 0
    while n < len(insns):
      addr, opname, arg, opsize = insns[n]
      n = n + 1
      if opname in self.conditional_jump_insns:
        next_addr, cond_stmts = self.__decompile_condition(insns[n-1:], stack)
        statements.extend(cond_stmts)
        if next_addr is None or next_addr <= self.__first_addr(insns):
          return (next_addr, statements)
        n = self.__jmp_to_insn_at(insns, next_addr)
      elif opname[:7] == 'BINARY_':
        right = stack.pop()
        left = stack.pop()
        if opname == 'BINARY_SUBSCR':
          stack.append(BinarySubscr(left, right))
        elif opname[7:] in self.binary_operators:
          stack.append(BinaryOp(left, self.binary_operators[opname[7:]], right))
        else:
          raise PythonDecompilerError("Unhandled opcode", addr, opname, arg)
      elif opname == 'BREAK_LOOP':
        statements.append(Break())
      elif opname == 'BUILD_CLASS':
        codecall = stack.pop()
        if not isinstance(codecall, PythonCompiledFunctionCall):
          raise PythonDecompilerError(
            "Bad type for first argument of BUILD_CLASS.",
            addr, opname, arg
          )
        supers = stack.pop()
        if not isinstance(supers, Constant):
          raise PythonDecompilerError(
            "Expected constant as second argument of BUILD_CLASS.",
            addr, opname, arg
          )
        name = stack.pop()
        stack.append(PythonCompiledClass(supers.value, codecall.function.code))
      elif opname == 'BUILD_LIST':
        values = []
        for i in range(0, arg):
          values.insert(0, stack.pop())
        stack.append(Constant(values))
      elif opname == 'BUILD_MAP':
        stack.append(Constant({}))
      elif opname == 'BUILD_TUPLE':
        values = []
        for i in range(0, arg):
          values.insert(0, stack.pop())
        stack.append(Constant(tuple(values)))
      elif opname == 'BUILD_SET':
        values = []
        for i in range(0, arg):
          values.append(stack.pop())
        stack.append(Constant(set(values)))
      elif opname == 'BUILD_SLICE':
        step = None
        if arg == 2:
          stop = stack.pop()
          start = stack.pop()
        elif arg == 3:
          step = stack.pop()
          stop = stack.pop()
          start = stack.pop()
        else:
          raise PythonDecompilerError("Invalid argument for BUILD_SLICE.", addr, opname, arg)
        stack.append(Slice(start, stop, step))
      elif opname[:13] == 'CALL_FUNCTION':
        nkey_params = (arg >> 8) & 0xff;
        npos_params = arg & 0xff;
        keywords = {}
        positional_params = []
        var_args = kwvar_args = None
        if opname[13:] == '_VAR':
          var_args = stack.pop()
        elif opname[13:] == '_KW':
          kwvar_args = stack.pop()
        elif opname[13:] == '_VAR_KW':
          kwvar_args = stack.pop()
          var_args = stack.pop()
        for i in range(0, nkey_params):
          key_value = stack.pop()
          key_name = stack.pop()
          keywords[key_name.value] = key_value
        for i in range(0, npos_params):
          positional_params.insert(0, stack.pop())
        func = stack.pop()
        if isinstance(func, PythonCompiledFunction):
          stack.append(PythonCompiledFunctionCall(func))
        elif isinstance(func, PythonCompiledGenerator):
          if npos_params != 1 or not isinstance(positional_params[0], PythonIterator):
            raise PythonDecompilerError("Expected iterator argument for generator.", addr, opname, arg)
          generator = self.__decompile_generator(func.code, positional_params[0])
          stack.append(generator)
        elif isinstance(func, PythonCompiledComprehension):
          if npos_params != 1 or not isinstance(positional_params[0], PythonIterator):
            raise PythonDecompilerError("Expected iterator argument for comprehension.", addr, opname, arg)
          comp = self.__decompile_comprehension(func.code, positional_params[0])
          stack.append(comp)
        else:
          if arg == 1 and isinstance(positional_params[0], PythonCompiledFunction):
            stack.append(positional_params[0])
            statements.append(Decorator(func))
          else:
            stack.append(FunctionCall(func, positional_params, keywords, var_args, kwvar_args))
      elif opname == 'COMPARE_OP':
        right = stack.pop()
        left = stack.pop()
        stack.append(BinaryOp(left, arg, right))
      elif opname == 'CONTINUE_LOOP':
        statements.append(Continue())
        return ( arg, statements )
      elif opname == 'DELETE_ATTR':
        base = stack.pop()
        statements.append(Del(GetAttr(base, arg)))
      elif opname in ( 'DELETE_FAST', 'DELETE_NAME' ):
        statements.append(Del(Variable(arg)))
      elif opname == 'DELETE_GLOBAL':
        if arg not in __builtin__.__dict__:
          self.global_vars.add(Variable(arg))
        statements.append(Del(Variable(arg)))
      elif opname == 'DELETE_SLICE+0':
        statements.append(Del(BinarySubscr(stack.pop(), Slice())))
      elif opname == 'DELETE_SLICE+1':
        expr = stack.pop()
        statements.append(Del(BinarySubscr(stack.pop(), Slice(start = expr))))
      elif opname == 'DELETE_SLICE+2':
        expr = stack.pop()
        statements.append(Del(BinarySubscr(stack.pop(), Slice(stop = expr))))
      elif opname == 'DELETE_SLICE+3':
        stop_expr = stack.pop()
        start_expr = stack.pop()
        statements.append(Del(BinarySubscr(stack.pop(), Slice(start = start_expr, stop = stop_expr))))
      elif opname == 'DELETE_SUBSCR':
        index = stack.pop()
        base = stack.pop()
        statements.append(Del(BinarySubscr(base, index)))
      elif opname == 'DUP_TOP':
        stack.append(stack[-1])
      elif opname == 'DUP_TOPX':
        stack.extend(stack[-arg:])
      elif opname == 'EXEC_STMT':
        global_vars = stack.pop()
        local_vars = stack.pop()
        statements.append(Exec(stack.pop(), global_vars, local_vars))
      elif opname == 'END_FINALLY':
        why = stack.pop()
        if isinstance(why, PythonExceptionClass):
          stack.pop() # exception instance
          stack.pop() # traceback
        return (addr + opsize, statements)
      elif opname == 'FOR_ITER':
        if len(stack) == 0 or (not isinstance(stack[-1], PythonIterator) and not isinstance(stack[-1], Variable)):
          raise PythonDecompilerError("Expected iterator on the stack.", addr, opname, arg)
        iterator = stack[-1]
        if isinstance(iterator, Variable):
          stack[-1] = iterator = PythonIterator(iterator) # cast variable to iterator
        if not iterator.walked:
          iterator.walked = True
          iterator.alive = True
          iterator.exhausted_addr = arg
          stack.append(PythonIterate(iterator, addr))
        else:
          iterator = stack.pop() # remove the iterator from the stack
          iterator.alive = False
          if_expr = None
          if len(statements) > 0 and isinstance(statements[-1], If):
            if len(statements[-1].statements) > 0 and isinstance(statements[-1].statements[0], PythonOpenedComprehension):
              comp = statements[-1].statements[0].current # get comprehension
              if_expr = statements[-1].expr
              statements[-1] = statements[-1].statements[0] # destroy If
          if len(statements) > 1 and isinstance(statements[-1], PythonOpenedComprehension):
            comp = statements[-1].current 
            if isinstance(statements[-2], Assignment):
              assign = statements[-2]
              if isinstance(assign.right, PythonIterate) and assign.right.iterator is iterator:
                iterable = iterator.expr
                if isinstance(assign.left, ExpressionList):
                  var = assign.left.exprs
                else:
                  var = [ assign.left ]
                if comp.variables:
                  comp.expr = Comprehension(comp.expr, var, iterable)
                  statements[-1].current = comp.expr
                else:
                  comp.variables = var
                  comp.iterable = iterable
                if if_expr:
                  statements[-1].current.if_expr = if_expr
                statements.pop(-2) # remove assign
                if len(stack) > 0 and stack[-1] is statements[-1].init:
                  statements.pop() # no more iteration, remove opened comprehension

          n = self.__jmp_to_insn_at(insns, iterator.exhausted_addr)
      elif opname == 'GET_ITER':
        stack.append(PythonIterator(stack.pop()))
      elif opname == 'IMPORT_FROM':
        if len(stack) == 0 or not isinstance(stack[-1], PythonImportedModule):  
          raise PythonDecompilerError("Expected module on the stack.", addr, opname, arg)
        stack.append(PythonImportedModuleAttr(stack[-1], Variable(arg)))
      elif opname == 'IMPORT_NAME':
        fromlist = stack.pop()
        level = stack.pop()
        if fromlist.value is None or isinstance(fromlist.value, list) and len(fromlist.value) == 0:
          stack.append(PythonImportedModule(arg.split('.')[0]))
        else:
          stack.append(PythonImportedModule(arg))
      elif opname == 'IMPORT_STAR':
        if len(stack) == 0 or not isinstance(stack[-1], PythonImportedModule):  
          raise PythonDecompilerError("Expected module on the stack.", addr, opname, arg)
        statements.append(ImportFrom(stack.pop(), Variable('*')))
      elif opname[:8] == 'INPLACE_':
        right = stack.pop()
        left = stack.pop()
        stack.append(BinaryOp(left, self.binary_operators[opname[8:]], right))
      elif opname == 'JUMP_FORWARD':
        if arg <= addr:
          raise PythonDecompilerError("Unexpected jump address in bytecode.", addr, opname, arg)
        n = self.__jmp_to_insn_at(insns, arg)
      elif opname == 'JUMP_ABSOLUTE':
        if arg <= self.__first_addr(insns): # outer loop iteration
          statements.append(Continue()) 
          # can't go any further in this block, let the caller decide where to resume
          return (arg, statements) 
        else:
          jmp_n = self.__jmp_to_insn_at(insns, arg)
          n = jmp_n
      elif opname == 'LIST_APPEND':
        expr = stack.pop()
        list_pos = arg or -1 # 2.7 can specify pos in argument
        stack[-list_pos] = ListComprehension(Comprehension(expr, None, None))
        statements.append(PythonOpenedComprehension(stack[-list_pos]))
      elif opname == 'LOAD_ATTR':
        base = stack.pop()
        if isinstance(base, PythonImportedModule):
          stack.append(PythonImportedModuleAttr(base, Variable(arg)))
        elif isinstance(base, PythonImportedModuleAttr):
          base.module.path.append(base.name.name)
          base.name = Variable(arg)
          stack.append(base)
        else:
          stack.append(GetAttr(base, arg))
      elif opname == 'LOAD_CONST':
        stack.append(Constant(arg))
      elif opname == 'LOAD_GLOBAL':
        stack.append(Variable(arg)) 
      elif opname in ('LOAD_FAST', 'LOAD_NAME', 'LOAD_DEREF', 'LOAD_CLOSURE'):
        stack.append(Variable(arg))
      elif opname == 'LOAD_LOCALS':
        stack.append(FunctionCall(Variable('locals')))
      elif opname in ('MAKE_FUNCTION', 'MAKE_CLOSURE'):
        fcode = stack.pop()
        if opname == 'MAKE_CLOSURE':
          stack.pop() # discard closure cells
        if not isinstance(fcode, Constant) and not isinstance(fcode.value, types.CodeType):
          raise PythonDecompilerError("Expected code object.")
        default_args = []
        code = fcode.value
        for i in range(0, arg):
          default_args.insert(0, stack.pop())
        if code.co_name == '<lambda>':
          args = code.co_varnames[:code.co_argcount]
          stack.append(Lambda(args, default_args, self.__decompile(code)))
        elif code.co_name == '<genexpr>':
          stack.append(PythonCompiledGenerator(code))
        elif code.co_name in ('<setcomp>', '<dictcomp>'):
          stack.append(PythonCompiledComprehension(code))
        else: 
          stack.append(PythonCompiledFunction(code, default_args))
      elif opname == 'MAP_ADD':
        key_expr = stack.pop()
        value_expr = stack.pop()
        stack[-arg] = DictComprehension(Comprehension(DictComprehensionEntry(key_expr, value_expr), None, None))
        statements.append(PythonOpenedComprehension(stack[-arg]))
      elif opname == 'NOP':
        pass
      elif opname == 'POP_BLOCK':
        if n != len(insns):
          next_addr, finalize = self.__decompile_block(insns[n:], stack)
          statements.append(PythonBlockFinalizer(finalize))
          return (next_addr, statements)
      elif opname == 'POP_TOP':
        value = stack.pop()
        if isinstance(value, FunctionCall) or isinstance(value, Yield):
        #if isinstance(value, Expression) and not isinstance(value, Variable) and not isinstance(value, Constant):
          statements.append(value)
      elif opname == 'PRINT_ITEM':
        if len(statements) > 0 and isinstance(statements[-1], Print) and not statements[-1].new_line:
          statements[-1].expr_list.append(stack.pop())
        else:
          statements.append(Print(ExpressionList([stack.pop()])))
      elif opname == 'PRINT_ITEM_TO':
        filedesc = stack.pop()
        if len(statements) > 0 and isinstance(statements[-1], ExtendedPrint) and statements[-1].filedesc == filedesc and not statements[-1].new_line:
          statements[-1].expr_list.append(stack.pop())
        else:
          statements.append(ExtendedPrint(filedesc, ExpressionList([stack.pop()])))
      elif opname == 'PRINT_NEWLINE':
        if len(statements) > 0 and isinstance(statements[-1], Print) and not statements[-1].new_line:
          statements[-1].new_line = True
        else:
          statements.append(Print())
          statements[-1].new_line = True
      elif opname == 'PRINT_NEWLINE_TO':
        filedesc = stack.pop()
        if len(statements) > 0 and isinstance(statements[-1], ExtendedPrint) and statements[-1].filedesc == filedesc and not statements[-1].new_line:
          statements[-1].new_line = True
        else:
          statements.append(ExtendedPrint(filedesc))
          statements[-1].new_line = True
      elif opname == 'RAISE_VARARGS':
        exception = param = trace = None
        if arg == 0:
          pass
        elif arg == 1:
          exception = stack.pop()
        elif arg == 2:
          param = stack.pop()
          exception = stack.pop()
        elif arg == 3:
          trace = stack.pop()
          param = stack.pop()
          exception = stack.pop()
        else:
          raise PythonDecompilerError("Bad number of arguments", addr, opname, arg)
        statements.append(Raise(exception, param, trace))
        return (None, statements)
      elif opname == 'RETURN_VALUE':
        statements.append(Return(stack.pop()))
        return (None, statements) # next instruction unreachable
      elif opname == 'ROT_FOUR':
        tos = stack.pop(); tos1 = stack.pop(); tos2 = stack.pop(); tos3 = stack.pop()
        stack.append(tos); stack.append(tos3); stack.append(tos2); stack.append(tos1)
      elif opname == 'ROT_THREE':
        tos = stack.pop(); tos1 = stack.pop(); tos2 = stack.pop()
        stack.append(tos); stack.append(tos2); stack.append(tos1)
      elif opname == 'ROT_TWO':
        tos = stack.pop(); tos1 = stack.pop()
        stack.append(tos); stack.append(tos1)
      elif opname == 'SET_ADD':
        expr = stack.pop()
        stack[-arg] = SetComprehension(Comprehension(expr, None, None))
        statements.append(PythonOpenedComprehension(stack[-arg]))
      elif opname in ('SETUP_EXCEPT', 'SETUP_FINALLY'):
        next_addr, try_stmts = self.__decompile_try_catch(insns[n-1:], stack)
        statements.extend(try_stmts)
        if next_addr is None or next_addr <= self.__first_addr(insns):
          return (next_addr, statements)
        n = self.__jmp_to_insn_at(insns, next_addr)
      elif opname == 'SETUP_LOOP':
        endloop = self.__jmp_to_insn_at(insns, arg)
        next_addr, loop_stmts = self.__decompile_loop(insns[n:endloop], stack)
        statements.extend(loop_stmts)
        if next_addr is None or next_addr <= self.__first_addr(insns):
          return (next_addr, statements)
        n = self.__jmp_to_insn_at(insns, next_addr)
      elif opname == 'SETUP_WITH':
        with_expr = stack.pop()
        stack.append(Constant(None)) # Dummy why for the finally block
        stack.append(PythonWithExit())
        stack.append(PythonWithEnter(with_expr))
        next_addr, with_block = self.__decompile_with(with_expr, arg, insns[n:], stack)
        statements.append(with_block)
        if next_addr is None or next_addr <= self.__first_addr(insns):
          return (next_addr, statements)
        n = self.__jmp_to_insn_at(insns, next_addr)
      elif opname == 'SLICE+0':
        stack.append(BinarySubscr(stack.pop(), Slice()))
      elif opname == 'SLICE+1':
        expr = stack.pop()
        stack.append(BinarySubscr(stack.pop(), Slice(start = expr)))
      elif opname == 'SLICE+2':
        expr = stack.pop()
        stack.append(BinarySubscr(stack.pop(), Slice(stop = expr)))
      elif opname == 'SLICE+3':
        stop_expr = stack.pop()
        start_expr = stack.pop()
        stack.append(BinarySubscr(stack.pop(), Slice(start = start_expr, stop = stop_expr)))
      elif opname[:6] == 'STORE_':
        store_type = opname[6:]
        if store_type == 'ATTR':
          base = stack.pop()
          value = stack.pop()
          target = GetAttr(base, arg) 
        elif store_type == 'GLOBAL':
          value = stack.pop()
          target = Variable(arg)
          if arg not in __builtin__.__dict__:
            self.global_vars.add(target)
        elif store_type == 'MAP':
          map_const = stack[-3]
          if not isinstance(map_const, Constant) or not isinstance(map_const.value, types.DictType):  
            raise PythonDecompilerError("Expected dict type.", addr, opname, arg)
          key = stack.pop()
          value = stack.pop()
          map_const.value[key] = value
          continue
        elif store_type == 'SLICE+0':
          target = BinarySubscr(stack.pop(), Slice()) 
          value = stack.pop()
        elif store_type == 'SLICE+1':
          start_expr = stack.pop()
          base = stack.pop()
          target = BinarySubscr(base, Slice(start = start_expr)) 
          value = stack.pop()
        elif store_type == 'SLICE+2':
          stop_expr = stack.pop()
          base = stack.pop()
          target = BinarySubscr(base, Slice(stop = stop_expr)) 
          value = stack.pop()
        elif store_type == 'SLICE+3':
          stop_expr = stack.pop()
          start_expr = stack.pop()
          base = stack.pop()
          value = stack.pop()
          target =  BinarySubscr(base, Slice(start = start_expr, stop = stop_expr))
        elif store_type == 'SUBSCR':
          index = stack.pop()
          base = stack.pop()
          value = stack.pop()
          target =  BinarySubscr(base, index)
        elif store_type in ('NAME', 'FAST', 'DEREF'): 
          value = stack.pop()
          target = Variable(arg)
        else:
          raise PythonDecompilerError("Unhandled opcode", addr, opname, arg)
        if isinstance(value, PythonCompiledFunction):
          func = value
          arg_count = func.code.co_argcount
          args = func.code.co_varnames[:arg_count]
          name = arg
          varargs = None
          if (func.code.co_flags & self.CODE_FLAG_VARARGS) != 0:
            varargs = func.code.co_varnames[arg_count]
            arg_count = arg_count + 1
          kwvarargs = None
          if (func.code.co_flags & self.CODE_FLAG_KWVARARGS) != 0:
            kwvarargs = func.code.co_varnames[arg_count]
          funcdef = FunctionDefinition(name, args, func.default_args, varargs, kwvarargs, self.__decompile(func.code))
          if len(func.code.co_consts) > 0 and func.code.co_consts[0]:
            funcdef.set_docstring(func.code.co_consts[0])
          statements.append(funcdef)
        elif isinstance(value, PythonCompiledClass):
          classo = value
          name = arg
          statements.append(ClassDefinition(name, classo.supers, self.__decompile(classo.code)))
        elif isinstance(value, PythonImportedModule):
          if target.name != value.path[-1]:
            statements.append(Import(value, as_name = target))
          else:
            statements.append(Import(value))
        elif isinstance(value, PythonImportedModuleAttr):
          if target != value.name:
            statements.append(ImportFrom(value.module, value.name, as_name = target))
          else:
            statements.append(ImportFrom(value.module, value.name))
        elif isinstance(value, PythonUnpackedValue):
          seq = value.sequence
          seq.bind(value.index, target)
          while seq.nested:
            if seq.is_complete():
              seq.parent.bind(seq.parent_index, Constant(tuple(seq.variables)))
            seq = seq.parent
          if seq.is_complete():
            statements.append(Assignment(ExpressionList(seq.variables), seq.expr))
        else:
          statements.append(Assignment(target, value))
      elif opname[:6] == 'UNARY_':
        if opname == 'UNARY_CONVERT':
          stack.append(UnaryConvert(stack.pop()))
        elif opname[6:] in self.unary_operators:
          stack.append(UnaryOp(self.unary_operators[opname[6:]], stack.pop()))
        else:
          raise PythonDecompilerError("Unhandled opcode", addr, opname, arg)
      elif opname == 'UNPACK_SEQUENCE':
        packed_expr = stack.pop()
        sequence = PythonUnpackedSequence(packed_expr, arg)
        if isinstance(packed_expr, PythonUnpackedValue):
          sequence.nested = True
          sequence.parent = packed_expr.sequence
          sequence.parent_index = packed_expr.index
        for i in range(0, arg):
          stack.append(PythonUnpackedValue(sequence, arg - i - 1))
      elif opname == 'WITH_CLEANUP':
        while not isinstance(stack[-1], PythonWithExit):
          stack.pop() # Reason
        stack.pop() # PythonWithExit
      elif opname == 'YIELD_VALUE':
        stack.append(Yield(stack.pop()))
      else:
        raise PythonDecompilerError("Unhandled opcode", addr, opname, arg)

    if len(insns) > 0:
      return ( self.__last_addr(insns), statements )
    else:
      return ( None, statements )

  def decompile(self, indent = '  ', ql_code = None):
    if ql_code != None and self.pyc == None:
      x = self.__decompile(ql_code)
    else:
      x = self.__decompile(self.pyc.code)
    program = PythonProgram(x)
    if len(self.global_vars) > 0:
      start = isinstance(program.statements[0], DocString) and 1 or 0
      program.statements.insert(start, Global(ExpressionList(list(self.global_vars))))
    return program.write(indent) + "\n"

def decompile_qb(qlcode):
  '''Do a bit of magic to use our own opcode table instead of the
  normal one.
  Once it's done, it will go ahead and decompile ``qlcode``'''
  custom_opmap = {
    'RETURN_VALUE' : 0x1b,
    'INPLACE_ADD' : 0x3c,
    'BINARY_XOR' : 0x4e,
    'GET_ITER' : 0x53,
    'POP_TOP' : 0x54,
    'INPLACE_SUBTRACT' : 0x55,
    'YIELD_VALUE' : 0x59,
    'FOR_ITER' : 0x5d,
    'STORE_GLOBAL' : 0x61,
    
    'LOAD_CONST'   : 0x64,
    'LOAD_CONST_AND_FLIP_SWITCH' : 0xa0,
    'LOAD_CONST3'  : 0xc8,
    'LOAD_CONST4'  : 0xea,
    'LOAD_CONST5'  : 0xb2,
    'LOAD_CONST6'  : 0x91,
    'LOAD_CONST7'  : 0x9e,
    'LOAD_CONST8'  : 0xd4,
    'LOAD_CONST9'  : 0xdd,
    'LOAD_CONST10' : 0xd5,
    'LOAD_CONST11' : 0xcc,
    'LOAD_CONST12' : 0x78,
    'LOAD_CONST14' : 0x5b,
    'LOAD_CONST15' : 0x97,
    'LOAD_CONST_OR_STORE_FAST' : 0x87,

    'BUILD_LIST' : 0x67,
    'LOAD_ATTR' : 0x6a,
    'COMPARE_OP' : 0x6b,
    'JUMP_FORWARD' : 0x6e,
    'JUMP_ABSOLUTE' : 0x71,
    'POP_JUMP_IF_FALSE' : 0x72,
    'MAKE_FUNCTION' : 0x77,
    'LOAD_GLOBAL' : 0x7c,
    'CALL_FUNCTION' : 0x86,
    'LOAD_FAST' : 0x8f,
  }
  custom_opmap_rev = dict((v, k) for k, v in custom_opmap.iteritems())
  custom_opname = list()
  values = sorted(custom_opmap.values(), reverse = True)
  biggest_key = values[0]
  for i in range(biggest_key + 1):
      if i in values:
          custom_opname.append(custom_opmap_rev[i])
      else:
          custom_opname.append('(%d)' % i)

  custom_hasname = list()
  custom_hasconst = list()
  custom_hasjrel = list()
  custom_haslocal = list()
  custom_hascompare = list()

  for k, v in custom_opmap.iteritems():
      # Little hack to handle every LOAD_CONST
      if k.startswith('LOAD_CONST'):
          k = 'LOAD_CONST'

      if opcode.opmap[k] in opcode.hasname:
          custom_hasname.append(v)
      if opcode.opmap[k] in opcode.hasconst:
          custom_hasconst.append(v)
      if opcode.opmap[k] in opcode.hasjrel:
          custom_hasjrel.append(v)
      if opcode.opmap[k] in opcode.haslocal:
          custom_haslocal.append(v)
      if opcode.opmap[k] in opcode.hascompare:
          custom_hascompare.append(v)

  opcode.opname = custom_opname
  opcode.opmap = custom_opmap
  opcode.hasname = custom_hasname
  opcode.hasconst = custom_hasconst
  opcode.hasjrel = custom_hasjrel
  opcode.haslocal = custom_haslocal
  opcode.hascompare = custom_hascompare
  opcode.EXTENDED_ARG = 0xff # dunno!
  pydec = PythonDecompiler('whocares')
  return pydec.decompile(indent = ' '*4, ql_code = qlcode)

def usage():
  print("Usage: %s [options] <pycfile>" % sys.argv[0])
  print("Reverse a Python pyc file back into a human readable form.")
  print(" -h, --help                Display this message.")
  print(" --disass                  Disassemble bytecode only.")
  print(" -i style, --indent=style  Set indentation style (default to 4s).")
  print("                            style is [num]char where char is 's' for spaces or 't' for tabs.")
  print(" -o file, --output=file    Redirect output to file (default to stdout).")

if __name__ == "__main__":
  import getopt
  import re

  try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["help", "disass", "indent=", "output="])
  except getopt.GetoptError:
    usage()
    exit(1)
  
  indent_pattern = ' ' * 4
  disassemble = False
  output = sys.stdout
  for opt, arg in opts:
    if opt in ("-h", "--help"):
      usage()
      exit()
    elif opt in ("--disass"):
      disassemble = True
    elif opt in ("-i", "--indent"):
      m = re.match("^(\d?)(s|t)$", arg) 
      if not m:
        usage()
        exit(1)
      indent_num = int(len(m.group(1)) > 0 and m.group(1) or "1")
      indent_char = {"s":" ", "t": "\t"}[m.group(2)]
      indent_pattern = indent_num * indent_char
    elif opt in ("-o", "--output"):
      try:
        output = open(arg, "w")  
      except IOError:
        print("Error: cannot open '%s' for writing" % arg)
        exit(1)

  if len(args) != 1:
    usage()
    exit(1)

  target = args[0]
  try:
    pydec = PythonDecompiler(target)
    if disassemble:
      dump = pydec.disassemble()
    else:
      dump = pydec.decompile(indent = indent_pattern)
    output.write(dump)
  except PythonDecompilerError as e:
    print("Error: " + str(e))
  finally:
    output.close()
