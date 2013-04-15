#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    python_code_hot_patching.py - Have fun with Python function objects (tested successfully on Python 2.7.3 x86/x64)
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

# http://docs.python.org/2/library/dis.html

# Debugging tips:
# Bytecode fetching:
#     .text:1E011329                         fetch_opcode:                           ; CODE XREF: PyEval_EvalFrameEx+47CA6j
#     .text:1E011329                                                                 ; PyEval_EvalFrameEx+47CB0j ...
#     .text:1E011329 0F B6 06                                movzx   eax, byte ptr [esi] ; Here is the bytecode and the current instruction
#     .text:1E01132C 46                                      inc     esi
#     .text:1E01132D 83 F8 5A                                cmp     eax, 5Ah        ; test if the bytecode got an argument or not
#     .text:1E011330 89 44 24 18                             mov     [esp+98h+var_80], eax
#     .text:1E011334 7C 4F                                   jl      short bytecode_without_argument
#     .text:1E011336 0F B6 5E 01                             movzx   ebx, byte ptr [esi+1] ; Take the two bytes after the instruction,
#     .text:1E011336                                                                 ; and make a short value (in ebx)
#     .text:1E01133A 0F B6 0E                                movzx   ecx, byte ptr [esi]
#     .text:1E01133D 83 C6 02                                add     esi, 2
#     .text:1E011340 C1 E3 08                                shl     ebx, 8
#     .text:1E011343 03 D9                                   add     ebx, ecx
# End-of the VM's stack at [ESP-0xC]

import sys
import dis
import types
from ctypes import memmove, c_char
from opcode import opmap

def get_string_object_padding():
    """
    Find at runtime the padding PyStringObject -> PyStringObject.ob_sval:
        typedef struct {        +
            PyObject_VAR_HEAD   |
            long ob_shash;      | We want to know that size
            int ob_sstate;      |
            char ob_sval[1];    +
        } PyStringObject;
    """
    marker = 'ABCDEFGH'
    r = (c_char * 100).from_address(id(marker))
    return r.raw.find(marker)

def instance_function_via_bytecode():
    """
    Instanciate a function object via Python bytecode.
    For a readable version:

        from struct import pack
        from opcode import opmap

        def p(u):
            return pack('<H', u)

        def opcodes_to_bytecode(opcodes):
            bytecode = ''
            for instr in opcodes:
                if isinstance(instr[0], str) == False:
                    bytecode += chr(instr[0])
                    if len(instr) > 1:
                        bytecode += p(instr[1])
                else:
                    bytecode += instr[0]
            return bytecode

        opcodes = [
            (opmap['JUMP_FORWARD'], 23),
            ('I DONT GIVE A SHIIIIIIT', ),

            (opmap['LOAD_FAST'], 0),
            (opmap['LOAD_CONST'], 0),
            (opmap['COMPARE_OP'], 2), # 2 = PyCmp_EQ, see COMPARE_OP case in 
            (opmap['POP_JUMP_IF_FALSE'], 46),

            (opmap['LOAD_CONST'], 1),
            (opmap['PRINT_ITEM'], ),
            (opmap['PRINT_NEWLINE'], ),
            (opmap['JUMP_FORWARD'], 5),

            (opmap['LOAD_CONST'], 2),
            (opmap['PRINT_ITEM'], ),
            (opmap['PRINT_NEWLINE'], ),

            (opmap['LOAD_CONST'], 3),
            (opmap['RETURN_VALUE'], )
        ]

        bytecode = opcodes_to_bytecode(opcodes)
    """
    bytecode = 'n\x17\x00I DONT GIVE A SHIIIIIIT|\x00\x00d\x00\x00k\x02\x00r.\x00d\x01\x00GHn\x05\x00d\x02\x00GHd\x03\x00S'
    # For further infos, check Python/Include/code.h -- PyCodeObject structure
    return types.FunctionType(
        types.CodeType(
            1,                                        # /* arguments, except *args */
            0,                                        # /* local variables */
            2,                                        # /* entries needed for evaluation stack */
            0,                                        # /* CO_..., see below */
            bytecode,                                 # /* instruction opcodes */
            (0xdeadbeef, 'Winner', 'Looser', None),   # /* list (constants used) */
            (),                                       # /* list of strings (names used) */
            ('r', ),                                  # /* tuple of strings (local variable names) */
            '',                                       # /* tuple of strings (free variable names) */
            'outtaspace',                             # /* string (where it was loaded from) */
            137,                                      # /* first source line number */
            ''                                        # /* string (encoding addr<->lineno mapping) See Objects/lnotab_notes.txt for details. */
        ),
        {}
    )

def wild_patch_memory(where, what):
    """I'm free to do whatever I want with my memory.
    You don't mess with me \o/"""
    return memmove(where, what, len(what))

def patch_function_usual_way(w00t):
    """Patch on the fly the code of w00t() with a new code object."""
    c = w00t.func_code
    # co_code is readonly, beware!
    newbytecode = c.co_code
    # Let's find the comparaison
    idx_jmp = newbytecode.find(chr(opmap['POP_JUMP_IF_FALSE']))
    # Yeah, JE/JNE ?!! if my beloved monkey Baboon read this :]]..
    # Patch the code with a NOP to always take the goodboy branch
    newbytecode = c.co_code[: idx_jmp] + chr(opmap['NOP'])*3 + c.co_code[idx_jmp + 3: ]

    # Patch it likes it's hot, Patch it likes it's hot
    w00t.func_code = types.CodeType(
        c.co_argcount, c.co_nlocals, c.co_stacksize, c.co_flags,
        newbytecode,
        c.co_consts, c.co_names, c.co_varnames, c.co_filename,
        c.co_name, c.co_firstlineno, c.co_lnotab
    )

def patch_function_wild_way(w00t):
    """Patch memory via mmemove, hardcore."""
    c = w00t.func_code.co_code
    idx_jmp = c.find(chr(opmap['POP_JUMP_IF_FALSE']))
    wild_patch_memory(
        id(c) + get_string_object_padding() + idx_jmp,
        chr(opmap['POP_TOP']) + chr(opmap['NOP']) * 2
    )

def main(argc, argv):
    print '->> Instanciate the function via Python bytecodes..'
    w00t = instance_function_via_bytecode()

    print '->> Disassembly before any modification:'
    dis.dis(w00t)
    print '->> Here is the normal behaviour of the function:'
    w00t('w1n!')
    w00t(0xdeadbeef)
    print ''

    print '->> First patch: with a code object replacement..'
    patch_function_usual_way(w00t)
    print '->> Disassembly after the patch:'
    dis.dis(w00t)
    print '->> Test if the patch works:'
    w00t('w1n!')
    w00t(0xdeadbeef)
    print ''

    print '->> Restoring the original function..'
    w00t = instance_function_via_bytecode()
    print '->> Second patch: directly modify the bytecode buffer..'
    patch_function_wild_way(w00t)
    print '->> Disassembly after the patch:'
    dis.dis(w00t)
    print '->> Test if the patch works:'
    w00t('w1n!')
    w00t(0xdeadbeef)
    print ''
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))