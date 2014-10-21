#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    mini_mips_symengine.py - Mini symbolic execution engine used to break
#    NoSuchCon 2014 MIPS crackme done by @elvanderb.
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

import sys
import logging
import os
from z3 import *

class MiniMipsSymExecEngine(object):
    '''This is a simple uncomplete MIPS emulator I wrote to
    solve the NoSuchCon2014 MIPS crackme wrote by @elvanderb.
    The emulator takes an IDA disassembly dump in input, and executes it
    with our virtual MIPS CPU.

    The other cool thing is that it supports Z3 ; that basically means instead
    of manipulating direct value, you can inject in the virtual CPU context
    symbolic variables.

    Obviously only a subset of instructions have been implemented, to be honest
    I only cared to implement the instructions used inside the challenge: so it doesn't
    support neither branches/loops or functions/procedures. Again this wasn't needed
    for the challenge :-).'''
    def __init__(self, trace_name):
        self.gpr = {
            'zero' : 0,
            'at' : 0,
            'v0' : 0,
            'v1' : 0,
            'a0' : 0,
            'a1' : 0,
            'a2' : 0,
            'a3' : 0,
            't0' : 0,
            't1' : 0,
            't2' : 0,
            't3' : 0,
            't4' : 0,
            't5' : 0,
            't6' : 0,
            't7' : 0,
            's0' : 0,
            's1' : 0,
            's2' : 0,
            's3' : 0,
            's4' : 0,
            's5' : 0,
            's6' : 0,
            's7' : 0,
            't8' : 0,
            't9' : 0,
            'k0' : 0,
            'k1' : 0,
            'gp' : 0,
            'sp' : 0,
            's8' : 0,
            'ra' : 0,
            'fp' : 0,

            'lo' : 0,
            'hi' : 0
        }

        self.stack = {}
        self.pc = 0
        self.code = []
        self.mem = {}
        self.stack_offsets = {}
        self.debug = False
        self.enable_z3 = False

        if os.path.exists('traces') == False:
            os.mkdir('traces')

        self.logger = logging.getLogger(trace_name)
        h = logging.FileHandler(
            os.path.join('traces', trace_name),
            mode = 'w'
        )
        h.setFormatter(
            logging.Formatter(
                '%(levelname)s: %(asctime)s %(funcName)s @ l%(lineno)d -- %(message)s',
                datefmt = '%Y-%m-%d %H:%M:%S'
            )
        )
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(h)

    # /!\ THIS IS A PITFALL
    # LShR VS >> in z3
    def _LShR(self, a, b):
        '''Useful hook function if you want to run the emulation
        with/without Z3 as LShR is different from >> in Z3'''
        if self.enable_z3:
            if isinstance(a, long) or isinstance(a, int):
                a = BitVecVal(a, 32)
            if isinstance(b, long) or isinstance(b, int):
                b = BitVecVal(b, 32)
            return LShR(a, b)
        return a >> b

    def _parse_line(self, line):
        '''Parse a MIPS disassembly line (according to IDA's layout)'''
        addr_seg, instr, rest = line.split(None, 2)
        args = rest.split(',')
        for i in range(len(args)):
            if '#' in args[i]:
                args[i], _ = args[i].split(None, 1)

        a0, a1, a2 = map(
            lambda x: x.strip().replace('$', '') if x is not None else x,
            args + [None]*(3 - len(args))
        )
        _, addr = addr_seg.split(':')
        return int(addr, 16), instr, a0, a1, a2

    def _is_gpr(self, x):
        '''Is it a valid GPR name?'''
        return x in self.gpr

    def _is_imm(self, x):
        '''Is it a valid immediate?'''
        x = x.replace('loc_', '0x')
        try:
            int(x, 0)
            return True
        except:
            return False

    def _to_imm(self, x):
        '''Get an integer from a string immediate'''
        if self._is_imm(x):
            x = x.replace('loc_', '0x')
            return int(x, 0)
        return None

    def _is_memderef(self, x):
        '''Is it a memory dereference?'''
        return '(' in x and ')' in x

    def is_stackvar(self, x):
        '''Is is a stack variable?'''
        return ('(fp)' in x and '+' in x) or ('var_' in x and '+' in x)

    def to_stackvar(self, x):
        '''Get the stack variable name'''
        _, var_name = x.split('+')
        return var_name.replace('(fp)', '')

    def debug_print(self, s, arg):
        if self.debug:
            print s % arg

    def step(self):
        '''This is the core of the engine -- you are supposed to implement the semantics
        of all the instructions you want to emulate here.'''
        line = self.code[self.pc]
        addr, instr, a0, a1, a2 = self._parse_line(line)
        if instr == 'sw':
            if self._is_gpr(a0) and self.is_stackvar(a1) and a2 is None:
                var_name = self.to_stackvar(a1)
                self.logger.info('%s = $%s', var_name, a0)
                self.stack[var_name] = self.gpr[a0]
            elif self._is_gpr(a0) and self._is_memderef(a1) and a2 is None:
                idx, base = a1.split('(')
                base = base.replace('$', '').replace(')', '')
                computed_address = self.gpr[base] + self._to_imm(idx)
                self.logger.info('[%s + %s] = $%s', base, idx, a0)
                self.mem[computed_address] = self.gpr[a0]
            else:
                raise Exception('sw not implemented')
        elif instr == 'lw':
            if self._is_gpr(a0) and self.is_stackvar(a1) and a2 is None:
                var_name = self.to_stackvar(a1)
                if var_name not in self.stack:
                    self.logger.info(' WARNING: Assuming %s was 0', (var_name, ))
                    self.stack[var_name] = 0
                self.logger.info('$%s = %s', a0, var_name)
                self.gpr[a0] = self.stack[var_name]
            elif self._is_gpr(a0) and self._is_memderef(a1) and a2 is None:
                idx, base = a1.split('(')
                base = base.replace('$', '').replace(')', '')
                computed_address = self.gpr[base] + self._to_imm(idx)
                if computed_address not in self.mem:
                    value = raw_input(' WARNING %.8x is not in your memory store -- what value is there @0x%.8x?' % (computed_address, computed_address))
                else:
                    value = self.mem[computed_address]
                self.logger.info('$%s = [%s+%s]', a0, idx, base)
                self.gpr[a0] = value
            else:
                raise Exception('lw not implemented')
        elif instr == 'sll':
            if self._is_gpr(a0) and self._is_gpr(a1) and self._is_imm(a2):
                self.logger.info('$%s = $%s << %d', a0, a1, self._to_imm(a2))
                self.gpr[a0] = self.gpr[a1] << self._to_imm(a2)
            elif self._is_gpr(a0) and self._is_imm(a1) and a2 is None:
                self.logger.info('$%s <<= %d', a0, self._to_imm(a1))
                self.gpr[a0] <<= self._to_imm(a1)
            else:
                raise Exception('sll not implemented')
        elif instr == 'sllv':
            if self._is_gpr(a0) and self._is_gpr(a1) and self._is_gpr(a2):
                self.logger.info('$%s = $%s << $%s', a0, a1, a2)
                self.gpr[a0] = self.gpr[a1] << self.gpr[a2]
            elif self._is_gpr(a0) and self._is_gpr(a1) and a2 is None:
                self.logger.info('$%s <<= $%s', a0, a1)
                self.gpr[a0] <<= self.gpr[a1]
            else:
                raise Exception('sllv not implemented')
        elif instr == 'srl':
            if self._is_gpr(a0) and self._is_gpr(a1) and self._is_imm(a2):
                self.logger.info('$%s = $%s >> %d', a0, a1, self._to_imm(a2))
                self.gpr[a0] = self._LShR(self.gpr[a1], self._to_imm(a2))
            elif self._is_gpr(a0) and self._is_imm(a1) and a2 is None:
                self.logger.info('$%s >>= %d', a0, self._to_imm(a1))
                self.gpr[a0] = self._LShR(self.gpr[a0], self._to_imm(a1))
            else:
                raise Exception('srl not implemented')
        elif instr == 'srlv':
            if self._is_gpr(a0) and self._is_gpr(a1) and self._is_gpr(a2):
                self.logger.info('$%s = $%s >> $%s', a0, a1, a2)
                self.gpr[a0] = self._LShR(self.gpr[a1], self.gpr[a2])
            elif self._is_gpr(a0) and self._is_gpr(a1) and a2 is None:
                self.logger.info('$%s >>= $%s', a0, a1)
                self.gpr[a0] = self._LShR(self.gpr[a0], self.gpr[a1])
            else:
                raise Exception('srlv not implemented')
        elif instr == 'nor':
            if self._is_gpr(a0) and self._is_gpr(a1) and self._is_gpr(a2):
                self.logger.info('$%s = ~($%s | $%s)', a0, a1, a2)
                self.gpr[a0] = ~(self.gpr[a1] | self.gpr[a2])
            else:
                raise Exception('nor not implemented')
        elif instr == 'or':
            if self._is_gpr(a0) and self._is_gpr(a1) and self._is_gpr(a2):
                self.logger.info('$%s = $%s | $%s', a0, a1, a2)
                self.gpr[a0] = self.gpr[a1] | self.gpr[a2]
            elif self._is_gpr(a0) and self._is_gpr(a1) and a2 is None:
                self.logger.info('$%s |= $%s', a0, a1)
                self.gpr[a0] |= self.gpr[a1]
            else:
                raise Exception('or not implemented')
        elif instr == 'xor':
            if self._is_gpr(a0) and self._is_gpr(a1) and self._is_gpr(a2):
                self.logger.info('$%s = $%s ^ $%s', a0, a1, a2)
                self.gpr[a0] = self.gpr[a1] ^ self.gpr[a2]
            elif self._is_gpr(a0) and self._is_gpr(a1) and a2 is None:
                self.logger.info('$%s ^= $%s', a0, a1)
                self.gpr[a0] ^= self.gpr[a1]
            else:
                raise Exception('xor not implemented')
        elif instr == 'addu':
            if self._is_gpr(a0) and self._is_gpr(a1) and self._is_gpr(a2):
                self.logger.info('$%s = $%s + $%s', a0, a1, a2)
                self.gpr[a0] = self.gpr[a1] + self.gpr[a2]
            elif self._is_gpr(a0) and self._is_gpr(a1) and a2 is None:
                self.logger.info('$%s += $%s', a0, a1)
                self.gpr[a0] += self.gpr[a1]
            else:
                raise Exception('addu not implemented')
        elif instr == 'addiu':
            if self._is_gpr(a0) and self._is_gpr(a1) and self._is_gpr(a2):
                self.logger.info('$%s = $%s + $%s', a0, a1, a2)
                self.gpr[a0] = self.gpr[a1] + self.gpr[a2]
            elif self._is_gpr(a0) and self._is_gpr(a1) and self._is_imm(a2):
                self.logger.info('$%s = $%s + %d', a0, a1, self._to_imm(a2))
                self.gpr[a0] = self.gpr[a1] + self._to_imm(a2)
            elif self._is_gpr(a0) and self._is_gpr(a1) and self.is_stackvar(a2):
                self.logger.info('$%s = $%s + %s', a0, a1, a2)
                self.gpr[a0] = self.gpr[a1] + self.stack_offsets[self.to_stackvar(a2)]
            elif self._is_gpr(a0) and self._is_imm(a1) and a2 is None:
                self.logger.info('$%s += %d', a0, self._to_imm(a1))
                self.gpr[a0] += self._to_imm(a1)
            else:
                raise Exception('addiu not implemented')
        elif instr == 'la' or instr == 'li':
            if self._is_gpr(a0) and self._is_imm(a1) and a2 is None:
                self.logger.info('$%s = 0x%.8x', a0, self._to_imm(a1))
                self.gpr[a0] = self._to_imm(a1)
            else:
                raise Exception('la | li not implemented')
        elif instr == 'subu':
            if self._is_gpr(a0) and self._is_gpr(a1) and a2 is None:
                self.logger.info('$%s -= $%s', a0, a1)
                self.gpr[a0] -= self.gpr[a1]
            elif self._is_gpr(a0) and self._is_gpr(a1) and self._is_gpr(a2):
                self.logger.info('$%s = $%s - $%s', a0, a1, a2)
                self.gpr[a0] = self.gpr[a1] - self.gpr[a2]
            else:
                raise Exception('subu not implemented')
        elif instr == 'multu':
            if self._is_gpr(a0) and self._is_gpr(a1) and a2 is None:
                self.logger.info('$lo = ($%s * $%s) & 0xffffffff', a0, a1)
                self.logger.info('$hi = ($%s * $%s) >> 32', a0, a1)
                if self.enable_z3:
                    # /!\ THIS IS A PITFALL
                    # If you just multiply two vectors of the same size, you won't have any overflow
                    # So your $hi will be *always* zero, which is bad
                    # Trust me I had to debug a loooooot of time before identifying this bug
                    # inside my symbolic execution engine.
                    # The trick is just to use bigger vectors & extract the high / low part
                    # job done.
                    a0bis, a1bis = self.gpr[a0], self.gpr[a1]
                    if isinstance(a0bis, int) or isinstance(a0bis, long):
                        a0bis = BitVecVal(a0bis, 32)
                    if isinstance(a1bis, int) or isinstance(a1bis, long):
                        a1bis = BitVecVal(a1bis, 32)

                    a064 = ZeroExt(32, a0bis)
                    a164 = ZeroExt(32, a1bis)
                    r = a064 * a164
                    self.gpr['lo'] = Extract(31, 0, r)
                    self.gpr['hi'] = Extract(63, 32, r)
                else:
                    x = self.gpr[a0] * self.gpr[a1]
                    self.gpr['lo'] = x & 0xffffffff
                    self.gpr['hi'] = self._LShR(x, 32)
            else:
                raise Exception('multu not implemented')
        elif instr == 'mfhi':
            if self._is_gpr(a0) and a1 is None and a2 is None:
                self.logger.info('$%s = $hi', a0)
                self.gpr[a0] = self.gpr['hi']
            else:
                raise Exception('mfhi not implemented')
        elif instr == 'lui':
            if self._is_gpr(a0) and self._is_imm(a1) and a2 is None:
                self.logger.info('$%s = %d', a0, self._to_imm(a1) << 16)
                self.gpr[a0] = self._to_imm(a1) << 16
            else:
                raise Exception('lui not implemented')
        elif instr == 'move':
            if self._is_gpr(a0) and self._is_gpr(a1) and a2 is None:
                self.logger.info('$%s = $%s', a0, a1)
                self.gpr[a0] = self.gpr[a1]
        else:
            raise Exception('instr: %r not implemented' % repr(instr))

        for k, v in self.gpr.iteritems():
            if isinstance(v, int) or isinstance(v, long):
                self.gpr[k] = v & 0xffffffff
            else:
                self.gpr[k] = simplify(self.gpr[k])

    def run(self, print_final_state = False):
        '''Run the code!'''
        self.pc = 0
        for line in self.code:
            if line == '' or line.startswith(';'):
                self.pc += 1
                continue
            self.step()
            self.pc += 1

        if print_final_state == False:
            return

        logging.info('CPU STATE:')
        reg_lines = [
            'zero     at       v0       v1       a0       a1       a2       a3',
            't0       t1       t2       t3       t4       t5       t6       t7',
            's0       s1       s2       s3       s4       s5       s6       s7',
            't8       t9       k0       k1       gp       sp       s8       ra'
        ]
        for reg_line in reg_lines:
            logging.info(
                ' '.join('%s:0x%.8x' % (reg_name, self.gpr[reg_name]) for reg_name in reg_line.split(None))
            )

        logging.info('STACK STATE:')
        logging.info('%r', self.stack)

def main(argc, argv):
    print '=' * 50
    sym = MiniMipsSymExecEngine('donotcare.log')
    # DO NOT FORGET TO ENABLE Z3 :)
    sym.enable_z3 = True
    a = BitVec('a', 32)
    sym.stack['var'] = a
    sym.stack['var2'] = 0xdeadbeef
    sym.stack['var3'] = 0x31337
    sym.code = '''.doare:DEADBEEF                 lw      $v0, 0x318+var($fp)  # Load Word
.doare:DEADBEEF                 lw      $v1, 0x318+var2($fp)  # Load Word
.doare:DEADBEEF                 subu    $v0, $v1, $v0    #
.doare:DEADBEEF                 li      $v1, 0x446F8657  # Load Immediate
.doare:DEADBEEF                 multu   $v0, $v1         # Multiply Unsigned
.doare:DEADBEEF                 mfhi    $v1              # Move From HI
.doare:DEADBEEF                 subu    $v0, $v1         # Subtract Unsigned'''.split('\n')
    sym.run()

    print 'Symbolic mode:'
    print 'Resulting equation: %r' % sym.gpr['v0']
    print 'Resulting value if `a` is 0xdeadb44: %#.8x' % substitute(
        sym.gpr['v0'], (a, BitVecVal(0xdeadb44, 32))
    ).as_long()

    print '=' * 50
    emu = MiniMipsSymExecEngine('donotcare.log')
    emu.stack = sym.stack
    emu.stack['var'] = 0xdeadb44
    sym.stack['var2'] = 0xdeadbeef
    sym.stack['var3'] = 0x31337
    emu.code = sym.code
    emu.run()

    print 'Emulator mode:'
    print 'Resulting value when `a` is 0xdeadb44: %#.8x' % emu.gpr['v0']
    print '=' * 50
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))