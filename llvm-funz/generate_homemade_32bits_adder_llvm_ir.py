#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    generate_homemade_32bits_adder_llvm_ir.py - Generate a home made 32bits adder in LLVM IR
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

def Instruction(type_, name, LO, RO, nindent = 4):
    """Return a LLVM IR instruction"""
    types = {
        'shr' : 'LShr',
        'shl' : 'Shl',
        'or' : 'Or',
        'and' : 'And',
        'add' : 'Add',
        'xor' : 'Xor'
    }
    assert(type_ in types.keys())

    instr = '%sllvm::Instruction *%s = llvm::BinaryOperator::Create%s(%s, %s);' % (
        ' ' * nindent,
        name,
        types[type_],
        LO,
        RO
    )

    instr += '\n'
    instr += '%sbbl->getInstList().push_back(%s);' % (
        ' ' * nindent,
        name
    )
    return instr

def GetInt32(x):
    """Get a constant 32 bits integer"""
    return 'llvm::ConstantInt::get(Int32Ty, %d)' % x

def generate_32bits_adder_llvm():
    """Generate the 32 bits LLVM IR adder"""
    print 'void insert_32bits_adder(llvm::BasicBlock *bbl, llvm::Value *A, llvm::Value *B)\n{'
    for i in range(32):
        # %1 = LO >> %d
        # %2 = %1 & 1
        print Instruction('shr', 'LO_RShifted%d' % i, 'A', GetInt32(i))
        print Instruction('and', 'LO_RShiftedAnded%d' % i, 'LO_RShifted%d' % i, GetInt32(1))
        LO = 'LO_RShiftedAnded%d' % i
        # %3 = ~%2
        print Instruction('xor', 'LO_RShiftedAndedNoted%d' % i, LO, GetInt32(1))
        NotLO = 'LO_RShiftedAndedNoted%d' % i

        # %4 = RO >> %d
        # %5 = %4 & 1
        print Instruction('shr', 'RO_RShifted%d' % i, 'B', GetInt32(i))
        print Instruction('and', 'RO_RShiftedAnded%d' % i, 'RO_RShifted%d' % i, GetInt32(1))
        RO = 'RO_RShiftedAnded%d' % i
        # %6 = ~%5
        print Instruction('xor', 'RO_RShiftedAndedNoted%d' % i, RO, GetInt32(1))
        NotRO = 'RO_RShiftedAndedNoted%d' % i

        Cin = 'Cout%d' % (i - 1)
        NotCin = 'NotCout%d' % (i - 1)

        if i == 0:
            Cin = GetInt32(0)
            NotCin = 'llvm::ConstantInt::get(Int32Ty, %d)' % 1

        # Now compute R
        # 1. And(NotLO, RO, NotCin)
        print Instruction('and', 'R_And01%d' % i, NotLO, RO)
        print Instruction('and', 'R_And02%d' % i, 'R_And01%d' % i, NotCin)

        # 2. And(LO, NotRO, NotCin)
        print Instruction('and', 'R_And11%d' % i, LO, NotRO)
        print Instruction('and', 'R_And12%d' % i, 'R_And11%d' % i, NotCin)

        # 3. And(NotLO, NotRO, Cin)
        print Instruction('and', 'R_And21%d' % i, NotLO, NotRO)
        print Instruction('and', 'R_And22%d' % i, 'R_And21%d' % i, Cin)

        # 4. And(LO, RO, Cin)
        print Instruction('and', 'R_And31%d' % i, LO, RO)
        print Instruction('and', 'R_And32%d' % i, 'R_And31%d' % i, Cin)

        # Or(1., 2., 3., 4.)
        print Instruction('or', 'R_Or0%d' % i, 'R_And02%d' % i, 'R_And12%d' % i)
        print Instruction('or', 'R_Or1%d' % i, 'R_And22%d' % i, 'R_And32%d' % i)
        print Instruction('or', 'R%d' % i, 'R_Or0%d' % i, 'R_Or1%d' % i)

        # Finally compute Cout
        # 1. And(NotLO, RO, Cin)
        print Instruction('and', 'Cout_And01%d' % i, NotLO, RO)
        print Instruction('and', 'Cout_And02%d' % i, 'Cout_And01%d' % i, Cin)

        # 2. And(LO, NotRO, Cin)
        print Instruction('and', 'Cout_And11%d' % i, LO, NotRO)
        print Instruction('and', 'Cout_And12%d' % i, 'Cout_And11%d' % i, Cin)

        # 3. And(LO, RO, NotCin)
        print Instruction('and', 'Cout_And21%d' % i, LO, RO)
        print Instruction('and', 'Cout_And22%d' % i, 'Cout_And21%d' % i, NotCin)

        # 4. And(LO, RO, Cin)
        print Instruction('and', 'Cout_And31%d' % i, LO, RO)
        print Instruction('and', 'Cout_And32%d' % i, 'Cout_And31%d' % i, Cin)

        # Or(1., 2., 3., 4.)
        print Instruction('or', 'Cout_Or0%d' % i, 'Cout_And02%d' % i, 'Cout_And12%d' % i)
        print Instruction('or', 'Cout_Or1%d' % i, 'Cout_And22%d' % i, 'Cout_And32%d' % i)
        print Instruction('or', 'Cout%d' % i, 'Cout_Or0%d' % i, 'Cout_Or1%d' % i)
        # NotCount
        print Instruction('xor', 'NotCout%d' % i, 'Cout%d' % i, GetInt32(1))

    # Shift each bit according to its position in the final DWORD
    for i in range(32):
        print Instruction('shl', 'R%d_LShifted' % i, 'R%d' % i, GetInt32(i))
    
    # Make the intermediate additions to obtain the final result
    for i in range(31):
        if i == 0:
            print Instruction('add', 'R_Tmp%d' % i, 'R%d_LShifted' % i, 'R%d_LShifted' % (i + 1))
        elif i == 30:
            print Instruction('add', 'FinalResult', 'R_Tmp%d' % (i - 1), 'R%d_LShifted' % (i + 1))
        else:
            print Instruction('add', 'R_Tmp%d' % i, 'R_Tmp%d' % (i - 1), 'R%d_LShifted' % (i + 1))

    print '}'

def main(argc, argv):
    generate_32bits_adder_llvm()
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
