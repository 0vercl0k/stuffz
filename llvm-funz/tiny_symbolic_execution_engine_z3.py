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
sys.path.append(r'C:\Program Files (x86)\Microsoft Research\Z3-4.1\bin')
from z3 import *
from idc import *

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

    We also don't care about:
        . EFLAGS
        . branches
        . register smaller, greater than 32 bits
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

        # Each equation will be stored here
        self.equations = {}

    def _check_if_reg32(self, r):
        '''XXX: make a decorator'''
        return r.lower() in self.ctx

    def _push_equation(self, e):
        self.equations[self.idx] = e
        self.idx += 1
        return (self.idx - 1)

    def set_reg_with_equation(self, r, e):
        if self._check_if_reg32(r) == False:
            return

        self.ctx[r] = self._push_equation(e)

    def get_reg_equation(self, r):
        if self._check_if_reg32(r) == False:
            return

        return self.equations[self.ctx[r]]

    def run(self):
        '''Run from start address to end address the engine'''
        for mnemonic, dst, src in self.disass.get_next_instruction():
            if mnemonic == 'mov':
                # mov reg32, reg32
                if src in self.ctx and dst in self.ctx:
                    self.ctx[dst] = self.ctx[src]
                # mov reg32, [mem]
                elif src.find('var_') != -1 and dst in self.ctx:
                    if src not in self.mem:
                        raise Exception('An non-initialized location (%r) is trying to be read' % src)

                    self.ctx[dst] = self.mem[src]
                # mov [mem], reg32
                elif dst.find('var_') != -1 and src in self.ctx:
                    if dst not in self.mem:
                        self.mem[dst] = None

                    self.mem[dst] = self.ctx[src]
                else:
                    raise Exception('This encoding of "mov" is not handled.')
            elif mnemonic == 'shr':
                # shr reg32, cst
                if dst in self.ctx and type(src) == int:
                    self.set_reg_with_equation(dst, LShR(self.get_reg_equation(dst), src))
                else:
                    raise Exception('This encoding of "shr" is not handled.')
            elif mnemonic == 'shl':
                # shl reg32, cst
                if dst in self.ctx and type(src) == int:
                    self.set_reg_with_equation(dst, self.get_reg_equation(dst) << src)
                else:
                    raise Exception('This encoding of "shl" is not handled.')
            elif mnemonic == 'and':
                x = None
                # and reg32, cst
                if type(src) == int:
                    x = src
                # and reg32, reg32
                elif src in self.ctx:
                    x = self.get_reg_equation(src)
                else:
                    raise Exception('This encoding of "and" is not handled.')

                self.set_reg_with_equation(dst, self.get_reg_equation(dst) & x)
            elif mnemonic == 'xor':
                # xor reg32, cst
                if dst in self.ctx and type(src) == int:
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
                else:
                    raise Exception('This encoding of "add" is not handled.')
            else:
                print mnemonic, dst, src
                raise Exception('This instruction is not handled.')


def simplify_additions(eq):
    '''The idea in this function is to help Z3 to simplify our big bitvec-arithmetic
    expression. It's simple, in eq we have a big expression with two symbolic variables (arg0 & arg1)
    and a lot of bitvec arithmetic.

    We substitute each symbolic variables by the value 0, thus obtaining a constant value.
    The idea is now to check if we can find values for arg0 & arg1 which sat this equation:
        cst + arg0 + arg1 != eq

    If this equation is not sat, it means those equations are equivalent, we got a simplification possible.
    Special thanks to my nasty-monkey @elvanderb for that :).'''
    cst = simplify(
        substitute(
            eq,
            (BitVec('arg0', 32), BitVecVal(0, 32)),
            (BitVec('arg1', 32), BitVecVal(0, 32))
        )
    )

    s = Solver()
    s.add(cst + BitVec('arg0', 32) + BitVec('arg1', 32) != eq)

    # In that case, it means that cst + arg0 + arg1 != eq isn't sat
    # Long story short, the two expressions are equivalent ; we got a simplification!
    if s.check() == unsat:
        # print 'WIN!'
        return cst + BitVec('arg0', 32) + BitVec('arg1', 32)

    return eq


def main():
    '''Here we will try to attack the semantic-preserving obfuscations
    I talked about in "Obfuscation of steel: meet my Kryptonite." : http://0vercl0k.tuxfamily.org/bl0g/?p=260.

    The idea is to defeat those obfuscations using a tiny symbolic execution engine.'''
    sym = SymbolicExecutionEngine(0x8048468, 0x0804A17C)

    # Here we are cheating, we are finding the symbolic variables by hands.
    # That process could be done automatically by using data-tainting (instanciate a symbolic variable
    # each time we got a read access on a non-initialized memory)
    arg0 = BitVec('arg0', 32)
    arg1 = BitVec('arg1', 32)
    # .text:0804845A                 mov     eax, [esp+3DCh+arg_4]
    # .text:08048461                 mov     ecx, [esp+3DCh+arg_0]
    sym.set_reg_with_equation('eax', arg1)
    sym.set_reg_with_equation('ecx', arg0)

    print 'Launching the engine..'
    sym.run()
    print 'Done, retrieving the equation in EAX'
    eax = sym.get_reg_equation('eax')
    print 'Done, now simplifying it..'
    print simplify(simplify_additions(eax))
    return 1

if __name__ == '__main__':
    main()