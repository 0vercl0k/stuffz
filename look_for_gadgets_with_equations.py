#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    look_for_gadggets_with_equations.py - 
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

# Show case
# Example with several constraints: "I want EAX = EBX = 0 at the end of the gadget execution":
# xor eax, eax ; push eax ; mov ebx, eax ; ret
# xor eax, eax ; xor ebx, ebx ; ret
# xor ebx, ebx ; mov eax, ebx ; push esi ; call  [0x10A1587C]
# [...]
# push 0x00000000 ; call  [0x10A15B98] ; pop edi ; pop ebx ; xor eax, eax ; retn 0x0008 # TODO: Check what's going on here

# Find a way to pivot code execution to the stack: "I want EIP = ESP at the end of the gadget execution":
# add dword ptr [ebx], 2 ; push esp ; ret 
# jmp esp
# pushad ; mov eax, 0xffffffff ; pop ebx ; pop esi ; pop edi ; ret
# [...]

# Find a way to move the stack by at least 1000 bytes: "I want ((ESP >= ESP + 1000) && (ESP < ESP + 2000))"
# add esp, 0x47c ; fldz ; pop ebx ; fchs ; pop esi ; pop edi ; pop ebp ; ret
# ret 0x3ff
# ret 0x78b
# ret 0x789
# xor eax, eax ; add esp, 0x45c ; pop ebx ; pop esi ; pop edi ; pop ebp ; ret

# Find a way to move the stack by at least 1000 bytes & set EAX to 0: "I want ((ESP >= ESP + 1000) && (ESP < ESP + 2000)) && (EAX == 0)"
# xor eax, eax ; add esp, 0x45c ; pop ebx ; pop esi ; pop edi ; pop ebp ; ret

import sys
import operator
from z3 import *

import amoco
import amoco.system.raw
import amoco.system.core
import amoco.arch.x86.cpu_x86 as cpu

def get_cpu_state_from_gadget(code, address_code = 0xdeadbeef):
    p = amoco.system.raw.RawExec(
        amoco.system.core.DataIO(code)
    )
    p.use_x86()
    blocks = list(amoco.lsweep(p).iterblocks())
    assert(len(blocks) > 0)
    mp = amoco.cas.mapper.mapper()
    for block in blocks:
        # If the last instruction a call, we need to "neutralize" its effect
        # in the final mapper, otherwise the mapper thinks the block after that one
        # if actually the inside of the call, which is not the case in our ROP gadgets
        if block.instr[-1].mnemonic.lower() == 'call':
            p.cpu.i_RET(None, block.map)
        mp >>= block.map
    return mp

def get_memory_expressions_from_mapper(mapper):
    exprs = []
    for target, expr in mapper:
        if isinstance(target, amoco.cas.expressions.ptr):
            exprs.append((target, expr))
    return exprs

class SymbolicCpuX86(object):
    '''This is basically our virtual & symbolic x86 CPU.
    You get all the register & a memory store (so yeah not really only a cpu per se)'''
    def __init__(self):
        self.eax, self.ebx, self.ecx, self.edx, self.esi, self.edi, self.eip, self.esp, self.ebp, self.eflags = BitVecs('eax ebx ecx edx esi edi eip esp ebp eflags', 32)
        self.state = {
            'eax' : self.eax,
            'ebx' : self.ebx,
            'ecx' : self.ecx,
            'edx' : self.edx,
            'esi' : self.esi,
            'edi' : self.edi,
            'eip' : self.eip,
            'esp' : self.esp,
            'ebp' : self.ebp,
            'eflags' : self.eflags
        }

        self.mem = Array('mem', BitVecSort(32), BitVecSort(32))
        self.vars = []

        self.op =  {
            '*' : operator.mul,
            '+' : operator.add,
            '-' : operator.sub,
            '&' : operator.and_,
            '|' : operator.or_,
            '^' : operator.xor,
            '~' : operator.inv,
            '%' : operator.mod,
            '<<' : operator.lshift,
            '>>' : LShR,
            '>' : operator.gt,
            '<' : operator.lt,
            # TODO: do that with Z3
            '//' : operator.div, # '\xd1\xf9j\x03P\x8dF\xfa\x8d\x04HP\xff\xd7'
            '>>>' : RotateRight,
            '<<<' : RotateLeft
        }

    def __getitem__(self, key):
        if key in self.state:
            return self.state[key]
        raise KeyError

    def set_address_with_value(self, addr, value):
        self.mem = Store(self.mem, addr, value)
        self.vars.append(value)
        return value

    def reset_mem(self):
        self.mem = Array('mem', BitVecSort(32), BitVecSort(32))
        self.vars = []

    def amoco_expression_to_z3(self, amoco_exp):
        # My memory support sucks & doesn't work -- let's wait the Z3 backend in amoco
        if isinstance(amoco_exp, amoco.cas.expressions.cst):
            # x.base
            return BitVecVal(amoco_exp.value, 32)
        elif isinstance(amoco_exp, amoco.cas.expressions.reg):
            # x.base
            return self.state[amoco_exp.ref]
        elif isinstance(amoco_exp, amoco.cas.expressions.ptr):
            # x.base, x.disp
            return self.amoco_expression_to_z3(amoco_exp.base) + BitVecVal(amoco_exp.disp, 32)
        elif isinstance(amoco_exp, amoco.cas.expressions.mem):
            # x.a
            return self.set_address_with_value(
                self.amoco_expression_to_z3(amoco_exp.a),
                BitVec('mem_%d' % len(self.vars), 32)
            )
        elif isinstance(amoco_exp, amoco.cas.expressions.op):
            return self.op[amoco_exp.op.symbol](
                self.amoco_expression_to_z3(amoco_exp.l),
                self.amoco_expression_to_z3(amoco_exp.r)
            )
        elif isinstance(amoco_exp, int):
            return BitVecVal(amoco_exp, 32)
        else:
            # print type(amoco_exp)
            raise RuntimeError

symbolic_cpu = SymbolicCpuX86()

class SymbolicCpuX86TargetedState(object):
    '''This is the state you want at the end of the gadget execution.
    Use the registers and the memory store to set your constraints.
    Chain them, combine them to suit your needs.'''
    def __init__(self):
        self.state = {}
        self.mem = {}
        self.equiv = {
            'eax' : cpu.eax,
            'ebx' : cpu.ebx,
            'ecx' : cpu.ecx,
            'edx' : cpu.edx,
            'esi' : cpu.esi,
            'edi' : cpu.edi,
            'eip' : cpu.eip,
            'esp' : cpu.esp,
            'ebp' : cpu.ebp,
            'eflags' : cpu.eflags
        }

    def wants(self, register, value_op):
        value, op = value_op
        if isinstance(value, str):
            value = self.equiv[value]

        value = symbolic_cpu.amoco_expression_to_z3(value)
        if register in self.state:
            self.state[register].append((value, op))
        else:
            self.state[register] = [(value, op)]

    def wants_register_equal(self, register, value):
        self.wants(register, (value, operator.eq))

    def wants_register_greater_or_equal(self, register, value):
        self.wants(register, (value, operator.ge))

    def wants_register_greater(self, register, value):
        self.wants(register, (value, operator.gt))

    def wants_register_lesser(self, register, value):
        self.wants(register, (value, operator.lt))

    def does_gadget_meet_constraints(self, symcpu):
        valid = True
        # For registers
        for register, equation_operator in self.state.iteritems():
            register = self.equiv[register]
            l_equation = symbolic_cpu.amoco_expression_to_z3(symcpu[register])
            for r_equation, op in equation_operator:
                if op in (operator.gt, operator.ge, operator.lt, operator.le):
                    # little trick here
                    #   In [42]: from z3 import *
                    #   In [43]: a, b = BitVecs('a b', 32)
                    #   In [44]: prove(UGT((a + 10), (a+3)))
                    #    counterexample
                    #    [a = 4294967287] :((((
                    #   In [65]: prove(((a+10)-(a+3)) > 0)
                    #    proved - yay!

                    if prove_(op(l_equation - r_equation, 0)) == False:
                        valid = False
                        break
                else:
                    if prove_(op(l_equation, r_equation)) == False:
                        valid = False
                        break
        # For memory
        # if valid:
        #     # First generate the state of the memory you want
        #     mem = Array('mem target end', BitVecSort(32), BitVecSort(32))
        #     for mem_location, mem_content in self.mem.iteritems():
        #         mem = Store(mem, mem_location, mem_content)

        #     # Extract mem from the target mapper
        #     mapper_mem = get_memory_expressions_from_mapper(symcpu)

        #     for mem_location, l_equation in self.mem.iteritems():
        #         r_equation = symbolic_cpu.amoco_expression_to_z3(symcpu.mem[mem_location])
        #         if prove_(l_equation == r_equation) == False:
        #             valid = False
        #             break

        return valid

def prove_(f):
    '''Taken from http://rise4fun.com/Z3Py/tutorialcontent/guide#h26'''
    s = Solver()
    s.add(Not(f))
    if s.check() == unsat:
        return True
    return False

def are_cpu_states_equivalent(target, candidate):
    valid = True
    for reg, exp in target.iteritems():
        if prove_(exp == symbolic_cpu.amoco_expression_to_z3(candidate[reg])) == False:
            valid = False
            break

    return valid

def test_arith_assignation():
    print '=' * 50
    print 'Arithmetic/Assignation tests:'
    print '=' * 50
    disass_target, gadget_target = 'mov eax, ebx ; ret 4', '\x89\xd8\xc2\x04\x00'
    sym_target = get_cpu_state_from_gadget(gadget_target)
    cpu_state_end_target_eax = dict(
        (reg, symbolic_cpu.amoco_expression_to_z3(sym_target[reg])) for reg in [cpu.eax]
    )

    # Thanks Dad`! -- http://aurelien.wail.ly/nrop/demos/
    candidates = {
        'add byte ptr [eax], al ; add byte ptr [edi], cl ; add eax, 0xc3d88948 ; xchg ebx, eax ; ret' : '\x00\x00\x00\x0f\x05\x48\x89\xd8\xc3\x87\xd8\xc3',
        'add byte ptr [edi], cl ; add eax, 0xc3d88948 ; xchg ebx, eax ; ret' : '\x00\x0f\x05\x48\x89\xd8\xc3\x87\xd8\xc3',
        # TODO: Implement fadd
        'fadd st0, st3 ; xchg ebx, eax ; pop edi ; pop edi ; ret' : '\xd8\xc3\x87\xd8\x5f\x5f\xc3',
        'mov eax, ebx ; shl eax, 32 ; ret' : '\x89\xd8\xc1\xe0\x20\xc3',
        'mov eax, ebx ; rol eax, 32 ; ret' : '\x89\xd8\xc1\xc0\x20\xc3',
    }

    for disass, code in candidates.iteritems():
        cpu_state_end_candidate = get_cpu_state_from_gadget(code)
        assert(are_cpu_states_equivalent(cpu_state_end_target_eax, cpu_state_end_candidate) == True)
        print ' > "%s" == "%s"' % (disass_target, disass)

    cpu_state_end_target_eax_esp = dict(
        (reg, symbolic_cpu.amoco_expression_to_z3(sym_target[reg])) for reg in [cpu.eax, cpu.esp]
    )
    
    # Conservation of ESP (or not conservation in this case)
    gadget = 'fadd st0, st3 ; xchg ebx, eax ; pop edi ; pop edi ; ret'
    gadget_code = candidates[gadget]
    assert(
        are_cpu_states_equivalent(
            cpu_state_end_target_eax_esp,
            get_cpu_state_from_gadget(gadget_code)
        ) == False
    )

    print ' > "%s" != "%s"' % (disass_target, gadget)
    print '  > %r VS %r' % (
        cpu_state_end_target_eax_esp[cpu.esp],
        symbolic_cpu.amoco_expression_to_z3(get_cpu_state_from_gadget(gadget_code)[cpu.esp])
    )

    disass_target, gadget_target = 'mov eax, 0x1234 ; ret', '\xb8\x34\x12\x00\x00\xc3'
    disass, gadget = 'mov edx, 0xffffedcc ; xor eax, eax ; sub eax, edx ; ret', '\xba\xcc\xed\xff\xff\x31\xc0\x29\xd0\xc3'
    sym_target = get_cpu_state_from_gadget(gadget_target)
    cpu_state_end_target_eax = dict(
        (reg, symbolic_cpu.amoco_expression_to_z3(sym_target[reg])) for reg in [cpu.eax]
    )

    assert(are_cpu_states_equivalent(cpu_state_end_target_eax, get_cpu_state_from_gadget(gadget)) == True)
    print ' > "%s" == "%s"' % (disass_target, disass)

def testing_memory_stuff():
    print '=' * 50
    print 'Memory store / read tests:'
    print '=' * 50
    disass_target, gadget_target = 'mov eax, 0x1234 ; ret', '\xb8\x34\x12\x00\x00\xc3'
    sym_target = get_cpu_state_from_gadget(gadget_target)
    cpu_state_end_target_eax = dict(
        (reg, symbolic_cpu.amoco_expression_to_z3(sym_target[reg])) for reg in [cpu.eax]
    )

    candidates = {
        'push 0xffffedcc ; pop edx ; xor eax, eax ; sub eax, edx ; ret' : '\x68\xcc\xed\xff\xff\x5a\x31\xc0\x29\xd0\xc3',
        'mov [eax], 0x1234 ; mov ebx, [eax] ; xchg eax, ebx ; ret' : '\xc7\x00\x34\x12\x00\x00\x8b\x18\x93\xc3'
    }

    for disass, code in candidates.iteritems():
        cpu_state_end_candidate = get_cpu_state_from_gadget(code)
        # print cpu_state_end_candidate
        # print get_z3_expr(cpu_state_end_candidate[cpu.eax])
        assert(are_cpu_states_equivalent(cpu_state_end_target_eax, cpu_state_end_candidate) == True)
        print ' > "%s" == "%s"' % (disass_target, disass)

def testing():
    test_arith_assignation()
    testing_memory_stuff()

def build_candidates(maxtuple = None):
    candidates = []
    with open(r'D:\Codes\gadgets.txt', 'r') as f:
        i = 0
        for line in f.readlines():
            first_part, second_part = line.split(' ;  ')
            _, disass = first_part.split(':', 1)
            bytes, _ = second_part.split(' (')
            candidates.append([disass, bytes.decode('string_escape')])
            i += 1
            if max(maxtuple, i) != i:
                break
    return candidates

def main(argc, argv):
    amoco.set_quiet()

    testing()
    # return 0
    # candidates = build_candidates(maxtuple = None)
    # print len(candidates)
    candidates = []

    # candidates['add eax, 0xc3d88948 ; xchg rbx, rax ; ret'] = '\x05\x48\x89\xd8\xc3\x87\xd8\xc3'
    # candidates['xor eax, eax ; not eax ; and eax, ebx ; ret'] = '\x31\xc0\xf7\xd0\x21\xd8\xc3'
    # candidates.append(('add esp, 0x3ff ; xor eax, eax', '\x81\xc4\xff\x03\x00\x00\x31\xc0'))
    # candidates['add ebx, dword ptr [edx + eax + 0x43140e0a] ; ret'] = '\x03\x9c\x02\x0a\x0e\x14\x43\xc3'
    # candidates['push ecx ; popad ; pop esp ; ret'] = '\x51\x61\x5c\xc3'

    # candidates.append(('xor eax, eax ; xor ebx, ebx ; xor ecx, ecx', '\x31\xc0\x31\xdb\x31\xc9'))
    # candidates['xor eax, eax ; push eax ; mov ebx, eax ; ret'] = '\x31\xc0\x50\x89\xc3\xc3'
    # candidates['rcr byte ptr [esi+0x48], 0x1 ; xor eax, eax ; not eax ; and eax, ebx ; ret'] = '\xd0\x5e\x48\x31\xc0\xf7\xd0\x21\xd8\xc3'
    # <over> !a32 mov eax, ebx ; ret
    # \x89\xd8\xc3
    
    candidates.append(('inc [eax]', '\xff\x00'))

    # TODO:
    #  Inequations: why do they actually work?:D
    #  Memory

    # Show case: [EAX] = EAX+1
    # cpu_state_end_target = SymbolicCpuX86TargetedState()
    # cpu_state_end_target.mem[amoco.cas.expressions.ptr(cpu.eax)] = amoco.cas.expressions.mem(cpu.eax) + 1

    # Show case: EAX = EBX = 0
    # cpu_state_end_target = SymbolicCpuX86TargetedState()
    # cpu_state_end_target.wants_register_equal('eax', 0)
    # cpu_state_end_target.wants_register_equal('ebx', 0)

    # Show case: EDI = ESI
    # cpu_state_end_target = SymbolicCpuX86TargetedState()
    # cpu_state_end_target.wants_register_equal('edi', 'esi')

    # Show case: ((ESP >= ESP + 1000) && (ESP < ESP + 2000)) && (EAX == 0)
    cpu_state_end_target = SymbolicCpuX86TargetedState()
    cpu_state_end_target.wants_register_greater_or_equal('esp', cpu.esp + 1000)
    cpu_state_end_target.wants_register_lesser('esp', cpu.esp + 2000)
    cpu_state_end_target.wants_register_equal('eax', 0)

    # Show case: Pivot ; EIP = ESP
    # cpu_state_end_target = SymbolicCpuX86TargetedState()
    # cpu_state_end_target.wants_register_equal('eip', 'esp')

    matches = []
    print 'Trying to find equivalents..'
    for disass, bytes in candidates:
        try:
            sym = get_cpu_state_from_gadget(bytes)
            symbolic_cpu.mem = {}
            if cpu_state_end_target.does_gadget_meet_constraints(sym):
                print '  GOT A MATCH with %r' % disass
                matches.append(disass)
        except AssertionError, e:
            pass
        except RuntimeError, e:
            pass
        except Exception, e:
            if str(e) != 'size mismatch':
                print '?? %s with %s:%r' % (str(e), disass, bytes)
            # pass

    print '='*20
    print 'Gadgets equivalent to'
    print cpu_state_end_target
    print '='*20
    print '\n'.join(matches)
    print '='*20
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))