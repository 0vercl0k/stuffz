#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    tiny_symbolic_execution_engine_z3.py - Really tiny symbolic execution engine to defeat the home-made 32 bits adder:
#    https://github.com/0vercl0k/stuffz/blob/master/llvm-funz/llvm-cpp-frontend-home-made-32bits-adder.cpp
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
sys.path.append(r'C:\Program Files (x86)\z3-430\bin')
from z3 import *
from idc import *

def prove_(f):
    '''Taken from http://rise4fun.com/Z3Py/tutorialcontent/guide#h26'''
    s = Solver()
    s.add(Not(f))
    if s.check() == unsat:
        return True
    return False

class EquationId(object):
    def __init__(self, id_):
        self.id = id_

    def __repr__(self):
        return 'EID:%d' % self.id

class Disassembler(object):
    '''A simple class to decode easily instruction in IDA'''
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.eip = start

    def _decode_instr(self):
        '''Returns mnemonic, dst, src'''
        mnem = GetMnem(self.eip)
        x = []
        for i in range(2):
            ty = GetOpType(self.eip, i)
            # cst
            if 5 <= ty <= 7:
                x.append(GetOperandValue(self.eip, i))
            else:
                x.append(GetOpnd(self.eip, i))

        return [mnem] + x

    def get_next_instruction(self):
        '''This is a convenient generator, you can iterator through
        each instructions easily'''
        while self.eip != self.end:
            yield self._decode_instr()
            self.eip += ItemSize(self.eip)

class SymbolicExecutionEngine(object):
    '''The symbolic execution engine is the class that will
    handle the symbolic execution. It will keep a track of the 
    different equations encountered, and the CPU context at each point of the program.

    The symbolic variables have to be found by the user (or using data-taing). This is not
    the purpose of this class.

    We are lucky, we only need to handle those operations & encodings:
        . mov:
            . mov reg32, reg32
            . mov reg32, [mem]
            . mov [mem], reg32
            . mov reg32, cst
        . shr:
            . shr reg32, cst
        . shl:
            . shl reg32, cst
        . and:
            . and reg32, cst
            . and reg32, reg32
        . xor:
            . xor reg32, cst
        . or:
            . or reg32, reg32
        . add:
            . add reg32, reg32
            . add reg32, cst

    We also don't care about:
        . EFLAGS
        . branches
        . smaller registers (16/8 bits)
    Long story short: it's perfect ; that environment makes really easy to play with symbolic execution.'''
    def __init__(self, start, end):
        # This is the CPU context at each time
        # The value of the registers are index in the equations dictionnary
        self.ctx = {
            'eax' : None,
            'ebx' : None,
            'ecx' : None,
            'edx' : None,
            'esi' : None,
            'edi' : None,
            'ebp' : None,
            'esp' : None,
            'eip' : None
        }

        # The address where the symbolic execution will start
        self.start = start

        # The address where the symbolic execution will stop
        self.end = end

        # Our disassembler
        self.disass = Disassembler(start, end)

        # This is the memory that can be used by the instructions to save temporary values/results
        self.mem = {}

        # Each equation must have a unique id
        self.idx = 0

        # The symbolic variables will be stored there
        self.sym_variables = []

        # Each equation will be stored here
        self.equations = {}

        # Number of instructions emulated
        self.ninstrs = 0

    def _check_if_reg32(self, r):
        '''XXX: make a decorator?'''
        return r.lower() in self.ctx

    def _push_equation(self, e):
        idx = EquationId(self.idx)
        self.equations[idx] = e
        self.idx += 1
        return idx

    def set_reg_with_equation(self, r, e):
        if self._check_if_reg32(r) == False:
            return

        self.ctx[r] = self._push_equation(e)

    def get_reg_equation(self, r):
        if self._check_if_reg32(r) == False:
            return

        if isinstance(self.ctx[r], EquationId):
            return self.equations[self.ctx[r]]
        else:
            return self.ctx[r]

    def run(self):
        '''Run from start address to end address the engine'''
        for mnemonic, dst, src in self.disass.get_next_instruction():
            if (self.ninstrs % 5000) == 0 and self.ninstrs > 0:
                print '%d instructions, %d equations so far...' % (self.ninstrs, len(self.equations))

            if mnemonic == 'mov':
                # mov reg32, imm32
                if dst in self.ctx and isinstance(src, (int, long)):
                    self.ctx[dst] = src
                # mov reg32, reg32
                elif src in self.ctx and dst in self.ctx:
                    self.ctx[dst] = self.ctx[src]
                # mov reg32, [mem]
                elif (src.find('var_') != -1 or src.find('arg') != -1) and dst in self.ctx:
                    if src not in self.mem:
                        # A non-initialized location is trying to be read, we got a symbolic variable!
                        sym = BitVec('arg%d' % len(self.sym_variables), 32)
                        self.sym_variables.append(sym)
                        print 'Trying to read a non-initialized area, we got a new symbolic variable: %s' % sym
                        self.mem[src] = self._push_equation(sym)
                    
                    self.ctx[dst] = self.mem[src]
                # mov [mem], reg32
                elif dst.find('var_') != -1 and src in self.ctx:
                    self.mem[dst] = self.ctx[src]
                else:
                    raise Exception('This encoding of "mov" is not handled.')
            elif mnemonic == 'shr':
                # shr reg32, cst
                if dst in self.ctx and isinstance(src, (int, long)):
                    self.set_reg_with_equation(dst, self.get_reg_equation(dst) >> src)
                else:
                    raise Exception('This encoding of "shr" is not handled.')
            elif mnemonic == 'shl':
                # shl reg32, cst
                if dst in self.ctx and isinstance(src, (int, long)):
                    self.set_reg_with_equation(dst, self.get_reg_equation(dst) << src)
                else:
                    raise Exception('This encoding of "shl" is not handled.')
            elif mnemonic == 'and':
                # and reg32, cst
                if isinstance(src, (int, long)):
                    x = src
                # and reg32, reg32
                elif src in self.ctx:
                    x = self.get_reg_equation(src)
                else:
                    raise Exception('This encoding of "and" is not handled.')

                self.set_reg_with_equation(dst, self.get_reg_equation(dst) & x)
            elif mnemonic == 'xor':
                # xor reg32, cst
                if dst in self.ctx and isinstance(src, (int, long)):
                    if self.ctx[dst] not in self.equations:
                        self.ctx[dst] ^= src
                    else:
                        self.set_reg_with_equation(dst, self.get_reg_equation(dst) ^ src)
                else:
                    raise Exception('This encoding of "xor" is not handled.')
            elif mnemonic == 'or':
                # or reg32, reg32
                if dst in self.ctx and src in self.ctx:
                    self.set_reg_with_equation(dst, self.get_reg_equation(dst) | self.get_reg_equation(src))
                else:
                    raise Exception('This encoding of "or" is not handled.')
            elif mnemonic == 'add':
                # add reg32, reg32
                if dst in self.ctx and src in self.ctx:
                    self.set_reg_with_equation(dst, self.get_reg_equation(dst) + self.get_reg_equation(src))
                # add reg32, cst
                elif dst in self.ctx and isinstance(src, (int, long)):
                    self.set_reg_with_equation(dst, self.get_reg_equation(dst) + src)
                else:
                    raise Exception('This encoding of "add" is not handled.')
            else:
                print mnemonic, dst, src
                raise Exception('This instruction is not handled.')

            self.ninstrs += 1

    def _simplify_additions(self, eq):
        '''The idea in this function is to help Z3 to simplify our big bitvec-arithmetic
        expression. It's simple, in eq we have a big expression with two symbolic variables (arg0 & arg1)
        and a lot of bitvec arithmetic. Somehow, the simplify function is not clever enough to reduce the
        equation.

        The idea here is to use the prove function in order to see if we can simplify an equation by an addition of the
        symbolic variables.'''
        # The two expressions are equivalent ; we got a simplification!
        if prove_(Sum(self.sym_variables) == eq):
            return Sum(self.sym_variables)

        return eq

    def get_reg_equation_simplified(self, reg):
        eq = self.get_reg_equation(reg)
        eq = simplify(self._simplify_additions(eq))
        return eq


def main():
    '''Here we will try to attack the semantic-preserving obfuscations
    I talked about in "Obfuscation of steel: meet my Kryptonite." : http://0vercl0k.tuxfamily.org/bl0g/?p=260.

    The idea is to defeat those obfuscations using a tiny symbolic execution engine.'''
    # sym = SymbolicExecutionEngine(0x804845A, 0x0804A17C) # for simple adder
    sym = SymbolicExecutionEngine(0x804823C, 0x08072284) # adder kryptonized
    print 'Launching the engine..'
    sym.run()
    print 'Done. %d equations built, %d assembly lines emulated, %d virtual memory cells used' % (len(sym.equations), sym.ninstrs, len(sym.mem))
    print 'CPU state at the end:'
    print sym.ctx
    print 'Retrieving and simplifying the EAX register..'
    eax = sym.get_reg_equation_simplified('eax')
    print 'EAX=%r' % eax
    return 1

if __name__ == '__main__':
    main()