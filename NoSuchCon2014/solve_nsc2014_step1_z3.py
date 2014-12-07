#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    solve_nsc2014_step1_z3.py - Solve the MIPS crackme released for NoSuchCon2014
#    with Z3 & symbolic execution.
#    Associated blogpost on doar-e:
#    https://doar-e.github.io/blog/2014/10/11/taiming-a-wild-nanomite-protected-mips-binary-with-symbolic-execution-no-such-crackme
#
#    Copyright (C) 2014 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k
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
#    Example of a run:
#      PS D:\Codes\NoSuchCon2014> python .\solve_nsc2014_step1_z3.py
#      ==================================================
#      Tests OK -- you are fine to go
#      ==================================================
#      > Instantiating the symbolic execution engine..
#      > Generating dynamically the code of the son & reorganizing/cleaning it..
#      > Configuring the virtual environement..
#      > Running the code..
#      > Instantiating & configuring the solver..
#      > Solving..
#      > Constraints solvable, here are the 6 DWORDs:
#       a = 0xFE446223
#       b = 0xBA770149
#       c = 0x75BA5111
#       d = 0x78EA3635
#       e = 0xA9D6E85F
#       f = 0xCC26C5EF
#      > Serial: 322644EF941077AB1115AB575363AE87F58E6D9AFE5C62CC

import sys
import os
from z3 import *

import mini_mips_symexec_engine
import memory
import code
import struct

def to_SMT2(f, status='unknown', name='', logic=''):
    '''https://stackoverflow.com/questions/14628279/z3-convert-z3py-expression-to-smt-lib2'''
    v = (Ast * 0)()
    return Z3_benchmark_to_smtlib_string(f.ctx_ref(), name, logic, status, '', 0, v, f.as_ast())


def emu_generate_magic_from_son_pc(emu, print_final_state = False):
    '''This block genereates a magic 32-bits value based on the son $pc'''
    emu.code = code.block_generate_magic_from_pc_son
    emu.run(print_final_state = print_final_state)

def emu_generate_new_pc_for_son(emu, print_final_state = False):
    '''This block computes the new PC address for the child'''
    emu.code = code.block_compute_new_pc_from_magic_high
    emu.run(print_final_state = print_final_state)

def extract_equation_of_function_that_generates_magic_value():
    '''Here we do some magic to transform our mini MIPS emulator
    into a symbolic execution engine ; the purpose is to extract
    the formula of the function generating the 32-bits magic value'''

    x = mini_mips_symexec_engine.MiniMipsSymExecEngine('function_that_generates_magic_value.log')
    x.debug = False
    x.enable_z3 = True
    pc_son = BitVec('pc_son', 32)
    n_break = BitVec('n_break', 32)
    x.stack['pc_son'] =  pc_son
    x.stack['var_300'] = n_break
    emu_generate_magic_from_son_pc(x, print_final_state = False)
    compute_magic_equation = x.gpr['v0']
    with open(os.path.join('formulas', 'generate_magic_value_from_pc_son.smt2'), 'w') as f:
        f.write(to_SMT2(compute_magic_equation, name = 'generate_magic_from_pc_son'))

    return pc_son, n_break, simplify(compute_magic_equation)

var_magic, var_n_break, expr_magic = [None]*3
def generate_magic_from_son_pc_using_z3(pc_son, n_break):
    '''Generates the 32 bits magic value thanks to the output
    of the symbolic execution engine: run the analysis once, extract
    the complete equation & reuse it as much as you want'''
    global var_magic, var_n_break, expr_magic
    if var_magic is None and var_n_break is None and expr_magic is None:
        var_magic, var_n_break, expr_magic = extract_equation_of_function_that_generates_magic_value()
    
    return substitute(
        expr_magic,
        (var_magic, BitVecVal(pc_son, 32)),
        (var_n_break, BitVecVal(n_break, 32))
    ).as_long()

def extract_equation_of_function_that_generates_new_son_pc():
    '''Extract the formula of the function generating the new son's $pc'''

    x = mini_mips_symexec_engine.MiniMipsSymExecEngine('function_that_generates_new_son_pc.log')
    x.debug = False
    x.enable_z3 = True
    tmp_pc = BitVec('magic', 32)
    n_loop = BitVec('n_loop', 32)
    x.stack['tmp_pc'] = tmp_pc
    x.stack['var_2F0'] = n_loop
    emu_generate_new_pc_for_son(x, print_final_state = False)
    compute_pc_equation = simplify(x.gpr['v0'])
    with open(os.path.join('formulas', 'generate_new_pc_son.smt2'), 'w') as f:
        f.write(to_SMT2(compute_pc_equation, name = 'generate_new_pc_son'))

    return tmp_pc, n_loop, compute_pc_equation

var_new_pc, var_n_loop, expr_new_pc = [None]*3
def generate_new_pc_from_magic_high(magic_high, n_loop):
    global var_new_pc, var_n_loop, expr_new_pc
    if var_new_pc is None and var_n_loop is None and expr_new_pc is None:
        var_new_pc, var_n_loop, expr_new_pc = extract_equation_of_function_that_generates_new_son_pc()
    return substitute(
        expr_new_pc,
        (var_new_pc, BitVecVal(magic_high, 32)),
        (var_n_loop, BitVecVal(n_loop, 32))
    ).as_long()

def generate_new_pc_from_pc_son_using_z3(pc_son, n_break):
    '''Generate the new program counter from the address where the son SIGTRAP'd and
    the number of SIGTRAP the son encountered'''
    loop_n = (n_break / 101)
    magic = generate_magic_from_son_pc_using_z3(pc_son, n_break)
    idx = None
    for i in range(len(memory.pcs)):
        if (memory.pcs[i] & 0xffffffff) == magic:
            idx = i
            break

    assert(idx != None)
    return generate_new_pc_from_magic_high(memory.pcs[idx] >> 32, loop_n)

def regression_tests():
    '''The code is quite dense & hacky ; it also relies on a lot of different formulaes / z3 expression
    to generate the correct serial, so here we are just making sure we have the values we expect :).
    Trust me: this little function saved me hours of debugging when I was modifying critical part of the code'''

    assert(generate_magic_from_son_pc_using_z3(0x4022bc, 0) == 0xcd0e99ae)
    assert(generate_magic_from_son_pc_using_z3(0x4022bc, 0x94) == 0x2d4f035c)
    assert(generate_magic_from_son_pc_using_z3(0x4022bc, 0xcd) == 0x51c72d51)
    assert(generate_magic_from_son_pc_using_z3(0x4022bc, 0x17a) == 0x7ae7ae50)
    assert(generate_magic_from_son_pc_using_z3(0x4022bc, 0x1a4) == 0x36e2899e)

    assert(generate_new_pc_from_pc_son_using_z3(0x40228c, 0) == 0x402290)
    assert(generate_new_pc_from_pc_son_using_z3(0x40228c, 0x65) == 0x402fe8)
    assert(generate_new_pc_from_pc_son_using_z3(0x40228c, 0xca) == 0x402548)

    x = mini_mips_symexec_engine.MiniMipsSymExecEngine('regression_tests.log')
    x.stack_offsets['var_30'] = 24
    x.gpr['fp'] = 0x7fff6cb0
    start_addr = x.gpr['fp'] + x.stack_offsets['var_30'] + 8

    x.code = code.block_code_of_son_reordered_loop_unrolled
    x.mem[start_addr +  0] = 0x11111111
    x.mem[start_addr +  4] = 0x11111111
    x.mem[start_addr +  8] = 0x11111111
    x.mem[start_addr + 12] = 0x11111111
    x.mem[start_addr + 16] = 0x11111111
    x.mem[start_addr + 20] = 0x11111111

    x.run()

    assert(x.mem[start_addr +  0] == 0xf0eac3cb)
    assert(x.mem[start_addr +  4] == 0xaf7e9746)
    assert(x.mem[start_addr +  8] == 0x3d5562b4)

def generate_son_code_reordered(debug = False):
    '''This functions puts in the right order the son's block of codes without
    relying on the father to set a new $pc value when a break is executed in the son.
    With this output we are good to go to create a nanomites-less binary:
      - We don't need the father anymore (he was driving the son)
      - We have the code in the right order, so we can also remove the break instructions
    It will also be quite useful when we want to execute symbolic-ly its code.
    '''
    def parse_line(l):
        addr_seg, instr, _ = l.split(None, 2)
        _, addr = addr_seg.split(':')
        return int('0x%s' % addr, 0), instr

    son_code = code.block_code_of_son
    next_break = 0
    n_break = 0
    cleaned_code = []
    for _ in range(6):
        for z in range(101):
            i = 0
            while i < len(son_code):
                line = son_code[i]
                addr, instr = parse_line(line)
                if instr == 'break' and (next_break == addr or z == 0):
                    break_addr = addr
                    new_pc = generate_new_pc_from_pc_son_using_z3(break_addr, n_break)
                    n_break += 1
                    if debug:
                        print '; Found the %dth break (@%.8x) ; new pc will be %.8x' % (z, break_addr, new_pc)
                    state = 'Begin'
                    block = []
                    j = 0
                    while j < len(son_code):
                        line = son_code[j]
                        addr, instr = parse_line(line)
                        if state == 'Begin':
                            if addr == new_pc:
                                block.append(line)
                                state = 'Log'
                        elif state == 'Log':
                            if instr == 'break':
                                next_break = addr
                                state = 'End'
                            else:
                                block.append(line)
                        elif state == 'End':
                            break
                        else:
                            pass
                        j += 1

                    if debug:
                        print ';', '='*25, 'BLOCK %d' % z, '='*25
                        print '\n'.join(block)
                    cleaned_code.extend(block)
                    break
                i += 1

    return cleaned_code

def get_serial():
    print '> Instantiating the symbolic execution engine..'
    x = mini_mips_symexec_engine.MiniMipsSymExecEngine('decrypt_serial.log')
    x.enable_z3 = True

    print '> Generating dynamically the code of the son & reorganizing/cleaning it..'
    # If you don't want to generate it dynamically like a sir, I've copied a version inside
    # code.block_code_of_son_reordered_loop_unrolled :-)
    x.code = generate_son_code_reordered()

    print '> Configuring the virtual environement..'
    x.gpr['fp'] = 0x7fff6cb0
    x.stack_offsets['var_30'] = 24
    start_addr = x.gpr['fp'] + x.stack_offsets['var_30'] + 8
    # (gdb) x/6dwx $s8+24+8
    # 0x7fff6cd0:     0x11111111      0x11111111      0x11111111      0x11111111     0x11111111      0x11111111
    a, b, c, d, e, f = BitVecs('a b c d e f', 32)
    x.mem[start_addr +  0] = a
    x.mem[start_addr +  4] = b
    x.mem[start_addr +  8] = c
    x.mem[start_addr + 12] = d
    x.mem[start_addr + 16] = e
    x.mem[start_addr + 20] = f

    print '> Running the code..'
    x.run()

    for i in range(6):
        with open(os.path.join('formulas', 'input_dword_%d.smt2' % i), 'w') as f_:
            f_.write(to_SMT2(x.mem[start_addr + i*4], name = 'input_dword_%d' % i))

    print '> Instantiating & configuring the solver..'
    s = Solver()
    s.add(
        x.mem[start_addr +   0] == 0x7953205b, x.mem[start_addr +   4] == 0x6b63616e,
        x.mem[start_addr +   8] == 0x20766974, x.mem[start_addr +  12] == 0x534e202b, 
        x.mem[start_addr +  16] == 0x203d2043, x.mem[start_addr +  20] == 0x5d20333c,
    )

    print '> Solving..'
    if s.check() == sat:
        print '> Constraints solvable, here are the 6 DWORDs:'
        m = s.model()
        for i in (a, b, c, d, e, f):
            print ' %r = 0x%.8X' % (i, m[i].as_long())

        print '> Serial:', ''.join(('%.8x' % m[i].as_long())[::-1] for i in (a, b, c, d, e, f)).upper()
    else:
        print '! Constraints unsolvable'

def main(argc, argv):
    '''Ready for war.'''
    regression_tests()
    print '=' * 50
    print 'Tests OK -- you are fine to go'
    print '=' * 50
    get_serial()
    print '=' * 50
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))