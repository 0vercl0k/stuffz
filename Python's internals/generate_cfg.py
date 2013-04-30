#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    generate_cfg.py - Generate the CFG of a Python method.
#    Copyright (C) 2013 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
import opcode
import pygraphviz as pgv
from struct import unpack

def dis(x = None):
    """Disassemble classes, methods, functions, or code."""
    if hasattr(x, 'func_code'):
        name = x.__name__
        x = x.func_code
        disassemble(x, name)

class Instruction(object):
    def __init__(self, address, op, symbol = None):
        self.address = address
        self.opcode = op
        self.mnemonic = opcode.opname[self.opcode]
        self.symbol = symbol
        if isinstance(self.symbol, str):
            self.symbol = self.__html_escape(self.symbol)

    def __html_escape(self, text):
        """Produce entities within text."""
        html_escape_table = {
            '&' : '&amp;',
            '"' : '&quot;',
            "'" : '&apos;',
            '>' : '&gt;',
            '<' : '&lt;',
            '%' : ''
        }
        return ''.join(html_escape_table.get(c, c) for c in text)

    def __str__(self):
        s = '<TR><TD align="left"><FONT color="white">%-20s</FONT>' % (self.mnemonic)
        if self.opcode >= opcode.HAVE_ARGUMENT:
            s += '<FONT color="#73ADAD">%s</FONT>' % self.symbol.ljust(5)
        s += '</TD></TR>'
        return s

class BasicBlock(object):
    def __init__(self):
        self.instructions = []
        self.start_address = None
        self.end_address = None

    def append(self, instr):
        if len(self.instructions) == 0:
            self.start_address = instr.address

        self.instructions.append(instr)
        self.end_address = instr.address

    def __str__(self):
        s  = '<TABLE><TR><TD align="left"><FONT color="#9DD600">off_%.8d:</FONT></TD></TR>' % self.start_address
        s += ''.join(map(str, self.instructions))
        s += '</TABLE>'
        return s

def findlabels(code):
    """
    Detect all offsets in a byte code which are jump targets.
    Return the list of offsets.
    """
    labels = []
    n = len(code)
    i = 0
    while i < n:
        c = code[i]
        op = ord(c)
        i = i+1
        if op >= opcode.HAVE_ARGUMENT:
            oparg = ord(code[i]) + ord(code[i+1])*256
            i = i+2
            label = -1
            if op in opcode.hasjrel:
                label = i+oparg
            elif op in opcode.hasjabs:
                label = oparg
            if label >= 0:
                if label not in labels:
                    labels.append(label)
    return labels

def disassemble(co, name):
    """Disassemble a code object."""
    code = co.co_code
    branch_instruction = opcode.hasjrel + opcode.hasjabs
    nodes = {}
    edges = []

    for label in findlabels(code):
        nodes[label] = BasicBlock()

    i = 0
    extended_arg = 0
    free = co.co_cellvars + co.co_freevars
    current_bbl = BasicBlock()
    while i < len(code):
        op = ord(code[i])
        addr = i
        symbol = None

        i += 1
        if op >= opcode.HAVE_ARGUMENT:
            oparg = unpack('<H', code[i : i + 2])[0] + extended_arg
            extended_arg = 0
            i += 2

            if op == opcode.EXTENDED_ARG:
                extended_arg = oparg << 16

            if op in opcode.hasconst:
                symbol = co.co_consts[oparg]
            elif op in opcode.hasname:
                symbol = co.co_names[oparg]
            elif op in opcode.hasjrel:
                symbol = i + oparg
            elif op in opcode.haslocal:
                symbol = co.co_varnames[oparg]
            elif op in opcode.hascompare:
                symbol = opcode.cmp_op[oparg]
            elif op in opcode.hasfree:
                symbol = free[oparg]
            else:
                symbol = oparg

        ins = Instruction(addr, op, repr(symbol))
        current_bbl.append(ins)

        if op == opcode.opmap['RETURN_VALUE']:
            nodes[current_bbl.start_address] = current_bbl
            break

        # Is-it a branch instruction ? Or Does it exist a futur BBL ?
        if op in branch_instruction or i in nodes:
            dst = oparg
            # If it is a relative branchment, we compute the dest address
            if op in opcode.hasjrel:
                dst += i

            # Push our current BBL into the nodes list
            nodes[current_bbl.start_address] = current_bbl

            color_branch_taken_if_jmp, color_branch_if_no_jmp = 'blue', 'blue'
            if op in branch_instruction:
                if opcode.opname[op].find('JUMP_IF_FALSE') != -1:
                    color_branch_taken_if_jmp = 'green'
                    color_branch_if_no_jmp = 'red'
                elif opcode.opname[op].find('JUMP_IF_TRUE') != -1:
                    color_branch_taken_if_jmp = 'red'
                    color_branch_if_no_jmp = 'green'

                # Add an edge between the current_bbl and the destination
                edges.append((current_bbl.start_address, dst, color_branch_taken_if_jmp))

            # If the branchment instruction isn't a pure jump (non-conditionnal)
            # We also add an edge with the next futur BBL
            if opcode.opname[op] not in ['JUMP_ABSOLUTE', 'JUMP_FORWARD']:
                edges.append((current_bbl.start_address, i, color_branch_if_no_jmp))

            if i in nodes:
                current_bbl = nodes[i]
            else:
                current_bbl = BasicBlock()

    G = pgv.AGraph(directed = True) # Yeah, it's better oriented.
    G.graph_attr.update({
        'splines' : 'true',
        'label' : 'Control Flow Graph of: %s' % repr(name)
    })

    G.node_attr.update({
        'style' : 'filled',
        'shape' : 'box',
        'color' : '#2D2D2D',
        'fontname' : 'Consolas Bold', # monospace font ftw!
        'fontsize' : 9,
        'nojustify' : 'true'
    })

    G.edge_attr.update({
        'color' : 'blue',
        'dir' : 'forward',
        'arrowsize' : 1
    })

    for bbl_id, bbl in nodes.iteritems():
        G.add_node(bbl_id, label = '<%s>' % bbl)

    for src, dst, color in edges:
        G.add_edge(src, dst, color = color)

    G.layout('dot')
    G.draw(name + '_cfg.svg', prog = 'dot', args = '-Ln20 -LC2')

def testing_1(a, b, c):
    if a == (c + 1):
        print 'lul'
    else:
        if b == 3 and z == 2:
            print 'lole'
        else:
            print 'test!'

def testing_2():
    i = 0
    while i < 10:
        print 'wut'

def main(argc, argv):
    dis(testing_1)
    dis(testing_2)
    dis(dis)
    dis(disassemble)
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
