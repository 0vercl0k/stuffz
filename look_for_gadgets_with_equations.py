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

'''Show case
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
'''

import sys
import operator
import amoco
import amoco.system.raw
import amoco.system.core
import amoco.cas.smt
import amoco.arch.x86.cpu_x86 as cpu
import argparse
import multiprocessing
import time
import traceback

from z3 import *
from amoco.cas.expressions import *

class Constraint(object):
    '''A constraint is basically a `src` that can be a register or a memory location,
    an operator & an equation.
    Note that you can also supply your own comparaison operator as soon as it takes two things in input & return a boolean.

    Here is an example:
        * src = esp, operator = '=', constraint = eax + 100
          - It basically means that you want that ESP = EAX + 100 at the end of the execution of the gadget

        * src = esp, operator = '<', constraint = esp + 100
          - It basically means that you want that ESP < ESP + 100 at the end of the execution of the gadget
    '''
    def __init__(self, src, constraint, op = operator.eq):
        self.src = src
        self.constraint = constraint
        self.operator = op

def sym_exec_gadget_and_get_mapper(code, address_code = 0xdeadbeef):
    '''This function gives you a ``mapper`` object from assembled `code`. `code` will basically be
    our assembled gadgets.

    Note that `call`s will be neutralized in order to not mess-up the symbolic execution (otherwise the instruction just
    after the `call is considered as the instruction being jumped to).
    
    From this ``mapper`` object you can reconstruct the symbolic CPU state after the execution of your gadget.

    The CPU used is x86, but that may be changed really easily, so no biggie.'''
    p = amoco.system.raw.RawExec(
        amoco.system.core.DataIO(code), cpu
    )
    blocks = list(amoco.lsweep(p).iterblocks())
    assert(len(blocks) > 0)
    mp = amoco.cas.mapper.mapper()
    for block in blocks:
        # If the last instruction is a call, we need to "neutralize" its effect
        # in the final mapper, otherwise the mapper thinks the block after that one
        # is actually 'the inside' of the call, which is not the case with ROP gadgets
        if block.instr[-1].mnemonic.lower() == 'call':
            p.cpu.i_RET(None, block.map)
        mp >>= block.map
    return mp

def prove_(f):
    '''Taken from http://rise4fun.com/Z3Py/tutorialcontent/guide#h26'''
    s = Solver()
    s.add(Not(f))
    if s.check() == unsat:
        return True
    return False

def get_preserved_gpr_from_mapper(mapper):
    '''Returns a list with the preserved registers in `mapper`'''
    # XXX: Is there a way to get that directly from `cpu` without knowing the architecture?
    gpr = [ cpu.eax, cpu.ebx, cpu.ecx, cpu.edx, cpu.esi, cpu.edi, cpu.ebp, cpu.esp, cpu.eip ]
    return filter(lambda reg: prove_(mapper[reg].to_smtlib() == reg.to_smtlib()), gpr)

def get_preserved_gpr_from_mapper_str(mapper):
    '''Returns a clean string instead of a list of expressions'''
    preserved_gprs = get_preserved_gpr_from_mapper(mapper)
    return ', '.join(str(r) for r in preserved_gprs)

def are_cpu_states_equivalent(target, candidate):
    '''This function tries to compare a set of constraints & a symbolic CPU state. The idea
    is simple:
        * `target` is basically a list of `constraints`
        * `candidate` is a `mapper` instance

    Every constraints inside target are going to be checked against the mapper `candidate`,
    if they are all satisfied, it returns True, else False.'''
    valid = True
    for constraint in target:
        reg, exp, op = constraint.src, constraint.constraint, constraint.operator
        if op in (operator.gt, operator.ge, operator.lt, operator.le):
            # little trick here
            #   In [42]: from z3 import *
            #   In [43]: a, b = BitVecs('a b', 32)
            #   In [44]: prove(UGT((a + 10), (a+3)))
            #    counterexample
            #    [a = 4294967287] :((((
            #   In [65]: prove(((a+10)-(a+3)) > 0)
            #    proved - yay!
            valid = prove_(op(0, exp.to_smtlib() - candidate[reg].to_smtlib()))
        else:
            valid = prove_(op(exp.to_smtlib(), candidate[reg].to_smtlib()))

        if valid == False:
            break

    return valid

def extract_things_from_mapper(mapper, op, *things):
    '''Extracts whatever you want from a mapper & build a Constraint instance so that you can directly feed
    those ones in `are_cpu_states_equivalent`.'''
    return [ Constraint(thing, mapper[thing], op) for thing in things ]

def extract_things_from_mapper_eq(mapper, *things):
    return extract_things_from_mapper(mapper, operator.eq, *things)

def test_arith_assignation():
    print 'Arithmetic/Assignation tests'.center(100, '=')
    disass_target, gadget_target = 'mov eax, ebx ; ret 4', '\x89\xd8\xc2\x04\x00'
    
    # We generate the mapper for the final state we want to reach
    # In that state we may be interested in only one or two registers ; whatever, you extract what you want from it
    target_mapper = sym_exec_gadget_and_get_mapper(gadget_target)
    
    # We pick the registers (& their amoco expressions) we are interested in inside the final ``mapper``
    cpu_state_end_target_eax = extract_things_from_mapper_eq(target_mapper, cpu.eax)

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
        cpu_state_end_candidate = sym_exec_gadget_and_get_mapper(code)
        assert(are_cpu_states_equivalent(cpu_state_end_target_eax, cpu_state_end_candidate) == True)
        print ' > "%s" == "%s"' % (disass_target, disass)

    cpu_state_end_target_eax_esp = extract_things_from_mapper_eq(target_mapper, cpu.eax, cpu.esp)

    # Conservation of ESP (or not in this case)
    gadget = 'fadd st0, st3 ; xchg ebx, eax ; pop edi ; pop edi ; ret'
    gadget_code = candidates[gadget]
    assert(
        are_cpu_states_equivalent(
            cpu_state_end_target_eax_esp,
            sym_exec_gadget_and_get_mapper(gadget_code)
        ) == False
    )

    print ' > "%s" != "%s"' % (disass_target, gadget)
    csts_eax, csts_esp = cpu_state_end_target_eax_esp
    print '  > %r VS %r' % (
        csts_esp.constraint.to_smtlib(),
        sym_exec_gadget_and_get_mapper(gadget_code)[cpu.esp].to_smtlib()
    )

    disass_target, gadget_target = 'mov eax, 0x1234 ; ret', '\xb8\x34\x12\x00\x00\xc3'
    disass, gadget = 'mov edx, 0xffffedcc ; xor eax, eax ; sub eax, edx ; ret', '\xba\xcc\xed\xff\xff\x31\xc0\x29\xd0\xc3'
    target_mapper = sym_exec_gadget_and_get_mapper(gadget_target)

    cpu_state_end_target_eax = extract_things_from_mapper_eq(target_mapper, mem(cpu.eax))
    assert(are_cpu_states_equivalent(cpu_state_end_target_eax, sym_exec_gadget_and_get_mapper(gadget)) == True)
    print ' > "%s" == "%s"' % (disass_target, disass)

def test_memory_stuff():
    print 'Memory store / read tests:'.center(100, '=')
    disass_target, gadget_target = 'mov eax, 0x1234 ; ret', '\xb8\x34\x12\x00\x00\xc3'
    target_mapper = sym_exec_gadget_and_get_mapper(gadget_target)
    cpu_state_end_target_eax = extract_things_from_mapper_eq(target_mapper, cpu.eax)

    candidates = {
        'push 0xffffedcc ; pop edx ; xor eax, eax ; sub eax, edx ; ret' : '\x68\xcc\xed\xff\xff\x5a\x31\xc0\x29\xd0\xc3',
        'mov [eax], 0x1234 ; mov ebx, [eax] ; xchg eax, ebx ; ret' : '\xc7\x00\x34\x12\x00\x00\x8b\x18\x93\xc3'
    }

    for disass, code in candidates.iteritems():
        cpu_state_end_candidate = sym_exec_gadget_and_get_mapper(code)
        assert(are_cpu_states_equivalent(cpu_state_end_target_eax, cpu_state_end_candidate) == True)
        print ' > "%s" == "%s"' % (disass_target, disass)

    cpu_state_end_target_esp = [ Constraint(cpu.esp, mem(cpu.ebp, 32) + 8) ]
    candidates = {
        # https://twitter.com/NicoEconomou/status/527555631017107456 -- thanks @NicoEconomou! 
        'leave ; setl cl ; mov eax, ecx ; pop edi ; pop ebx ; pop esi ; leave ; ret' : '\xc9\x0f\x9c\xc1\x89\xc8\x5f\x5b\x5e\xc9\xc3',
    }
    for disass, code in candidates.iteritems():
        cpu_state_end_candidate = sym_exec_gadget_and_get_mapper(code)
        assert(are_cpu_states_equivalent(cpu_state_end_target_esp, cpu_state_end_candidate) == True)
        print ' > "%s" == "%s"' % (disass_target, disass)

    disass_target, gadget_target = 'add [eax], 4 ; ret', '\x83\x00\x04\xc3'
    target_mapper = sym_exec_gadget_and_get_mapper(gadget_target)
    cpu_state_end_target_mem_eax = extract_things_from_mapper_eq(target_mapper, mem(cpu.eax, 32))
    candidates = {
        'inc [eax] ; mov ebx, eax ; push ebx ; mov esi, [esp] ; add [esi], 3 ; mov ebx, [esi] ; mov [eax], ebx ; ret' : '\xff\x00\x89\xc3\x53\x8b\x34\x24\x83\x06\x03\x8b\x1e\x89\x18\xc3',
        'inc [eax] ; push eax ; mov esi, [esp] ; add [esi], 3 ; mov ebx, [esi] ; mov [eax], ebx ; ret' : '\xff\x00\x50\x8b\x34\x24\x83\x06\x03\x8b\x1e\x89\x18\xc3',
    }

    for disass, code in candidates.iteritems():
        cpu_state_end_candidate = sym_exec_gadget_and_get_mapper(code)
        assert(are_cpu_states_equivalent(cpu_state_end_target_mem_eax, cpu_state_end_candidate) == True)
        print ' > "%s" == "%s"' % (disass_target, disass)

    disass_target = 'EIP = [ESP + 0x24]'
    cpu_state_end_target_eip = [ Constraint(cpu.eip, mem(cpu.esp + 0x24, 32)) ]
    candidates = {
        'add esp, 0x24 ; ret' : '\x83\xc4\x24\xc3'
    }

    for disass, code in candidates.iteritems():
        cpu_state_end_candidate = sym_exec_gadget_and_get_mapper(code)
        assert(are_cpu_states_equivalent(cpu_state_end_target_eip, cpu_state_end_candidate) == True)
        print ' > "%s" == "%s"' % (disass_target, disass)

    disass_target = 'ESP = [ESP + 0x24]'
    cpu_state_end_target_esp = [ Constraint(cpu.esp, mem(cpu.esp + 0x24, 32)) ]
    candidates = {
        'add esp, 0x24 ; mov esp, [esp]' : '\x83\xc4\x24\x8b\x24\x24'
    }

    for disass, code in candidates.iteritems():
        cpu_state_end_candidate = sym_exec_gadget_and_get_mapper(code)
        print '  >', cpu_state_end_candidate[cpu.esp], 'VS', cpu_state_end_target_esp[0].constraint
        assert(are_cpu_states_equivalent(cpu_state_end_target_esp, cpu_state_end_candidate) == True)
        print ' > "%s" == "%s"' % (disass_target, disass)

def test_inequation():
    pass

def test_preserved_registers():
    pass

def testing():
    test_arith_assignation()
    test_memory_stuff()
    test_inequation()
    test_preserved_registers()

def build_candidates(f, maxtuple = None):
    '''Gets all the gadgets (both assembly & disassembly) from `f` & return them'''
    candidates = []
    for line in f.readlines():
        if ' ;  ' not in line:
            continue

        first_part, second_part = line.split(' ;  ')
        _, disass = first_part.split(':', 1)
        bytes, _ = second_part.split(' (')

        candidates.append([disass, bytes.decode('string_escape')])
        if maxtuple != None and len(candidates) == maxtuple:
            break

    return candidates

class HandleCandidate(object):
    '''This class is here because partial functions are not pickable ;
    so you can't use them with multiprocessing.Pool in Py27.
    This functor kind of workaround that nicely!'''
    def __init__(self, targeted_state, g_list):
        self.targeted_state = targeted_state
        self.g_list = g_list

    def __call__(self, candidate):
        disass, bytes = candidate
        try:
            candidate_mapper = sym_exec_gadget_and_get_mapper(bytes)
            if are_cpu_states_equivalent(self.targeted_state, candidate_mapper) == True:
                self.g_list.append((disass, get_preserved_gpr_from_mapper_str(candidate_mapper)))
        except AssertionError, e:
            pass
        except RuntimeError, e:
            pass
        except Exception, e:
            if str(e) != 'size mismatch':
                print '?? %s with %s:%r' % (str(e), disass, bytes)
                traceback.print_exc()
            # pass

def main():
    parser = argparse.ArgumentParser(description = 'Find a suitable ROP gadget via custom constraints.')
    parser.add_argument('--run-tests', action = 'store_true', help = 'Run the unit tests')
    parser.add_argument('--file', type = argparse.FileType('r'), help = 'The files with every available gadgets you have')
    parser.add_argument('--nprocesses', type = int, default = 2)
    
    amoco.set_quiet()
    # Disable aliasing -- mov [eax], ebx ; mov [ebx], 10; jmp [eax]
    # Here we assume that eax & ebx are different. Without assume_no_aliasing, we would have eip <- M32$2(eax)
    amoco.cas.mapper.mapper.assume_no_aliasing = True

    args = parser.parse_args()
    if args.run_tests:
        testing()

    if args.file is None:
        if args.run_tests is None:
            parser.print_help()
        return 0

    candidates = build_candidates(args.file, maxtuple = None)
    print '> Found %d candidates' % len(candidates)
    # TODO:
    #  Inequations: why do they actually work?:D
    # Add preserved registers

    # Show case: Pivot ; EIP = ESP
    # cpu_state_end_target = SymbolicCpuX86TargetedState()
    # cpu_state_end_target.wants_register_equal('eip', 'esp')

    # cpu_state_end_target = { cpu.esp : mem(cpu.esp + 0x24, 32) }
    
    # Show case: [EAX] = EAX+1
    # targeted_state = [
    #     Constraint(mem(cpu.eax, 32), cpu.eax + 1)
    # ]

    # Show case: EAX = EBX = 0
    # XXX: Try if (EAX = 0, EBX = 0) == (EAX = EBX, EBX = 0)
    # targeted_state = [
    #     Constraint(cpu.eax, cst(0, 32)),
    #     Constraint(cpu.ebx, cst(0, 32))
    # ]

    # Show case: EDI = ESI
    # targeted_state = [
    #     Constraint(cpu.edi, cpu.esi),
    # ]

    # Show case: ((ESP >= ESP + 1000) && (ESP < ESP + 2000)) && (EAX == 0)
    targeted_state = [
        Constraint(cpu.esp, cpu.esp + cst(1000, 32), operator.ge),
        Constraint(cpu.esp, cpu.esp + cst(2000, 32), operator.lt),
        # Constraint(cpu.eax, cst(0, 32))
    ]

    manager = multiprocessing.Manager()
    matches = manager.list()

    print '> Trying to find what you want..'
    t1 = time.time()
    p = multiprocessing.Pool(processes = args.nprocesses)
    job = p.map_async(
        HandleCandidate(targeted_state, matches),
        candidates
    )

    last_idx = 0
    while job.ready() == False:
        job.wait(20)
        len_matches = len(matches)
        print '>> Found %d gadgets so far...' % len_matches
        if last_idx < len_matches:
            for i in range(last_idx, len_matches):
                disass, preserved_gprs = matches[i]
                print '>>>', matches[i], '; Preserved GPRs:', preserved_gprs
                last_idx = len_matches

    print '> Done, found %d matches in %ds!' % (len(matches), time.time() - t1)
    print 'Your constraints'.center(50, '=')
    for constraint in targeted_state:
        print ' >', constraint.src, '->', constraint.constraint

    print 'Successful matches'.center(50, '=')
    for disass, preserved_gprs in matches:
        print ' >', disass, '; Preserved GPRs:', preserved_gprs

    return 1

if __name__ == '__main__':
    sys.exit(main())