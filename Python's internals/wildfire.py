#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    wildfire.py - Self-modifying Python bytecode: w.i.l.d.f.i.r.e
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

# Debugging tips:
# Bytecode fetching:
#     .text:1E011329                  fetch_opcode:                          ; CODE XREF: PyEval_EvalFrameEx+47CA6j
#     .text:1E011329                                                         ; PyEval_EvalFrameEx+47CB0j ...
#     .text:1E011329 0F B6 06         movzx   eax, byte ptr [esi] ; Here is the bytecode and the current instruction
#     .text:1E01132C 46               inc     esi
#     .text:1E01132D 83 F8 5A         cmp     eax, 5Ah        ; test if the bytecode got an argument or not
#     .text:1E011330 89 44 24 18      mov     [esp+98h+var_80], eax
#     .text:1E011334 7C 4F            jl      short bytecode_without_argument
#     .text:1E011336 0F B6 5E 01      movzx   ebx, byte ptr [esi+1] ; Take the two bytes after the instruction,
#     .text:1E011336                                          ; and make a short value (in ebx)
#     .text:1E01133A 0F B6 0E         movzx   ecx, byte ptr [esi]
#     .text:1E01133D 83 C6 02         add     esi, 2
#     .text:1E011340 C1 E3 08         shl     ebx, 8
#     .text:1E011343 03 D9            add     ebx, ecx
# End-of the VM's stack at [ESP-0xC]


# WOOOOTZ it works!
#     Windows, Python 2.6.6 x86
#     D:\python very_understandable_function.Py266.pyc
#         Hello, Windows-7-6.1.7601-SP1 (32bit) 
#         I like doing stuff with number: 10
#         31337
#         31338
#         31339
# [...]
#         dont care!
#     Linux, Python 2.6.6 x86
#     overclok@theokoles:~/tmp$ python2.6 very_understandable_function.Py266.pyc
#         Hello, Linux-2.6.32-5-686-i686-with-debian-6.0 (32bit)
#         I like doing stuff with number: 10
#         31337
#         31338
#         31339
# [...]
#         dont care!
#     Linux, Python 2.6.6 x64
#     overclok@spartacus:/tmp$ python2.6 very_understandable_function.Py266.pyc
#         Hello, Linux-2.6.32-5-xen-amd64-x86_64-with-debian-6.0.2 (64bit)
#         I like doing stuff with number: 10
#         31337
#         31338
#         31339
# [...]
#         dont care!

import sys
import types
import string
import dis
import random
import marshal
import struct
import platform
from py_compile import MAGIC
import opcode

def very_understandable_function():
    def get_eleet():
        return 31337

    import platform
    print 'Hello, %s (%s)' % (platform.platform(), platform.architecture()[0])
    r = 10
    print 'I like doing stuff with number: %r' % (r % 42)
    
    for i in range(r):
        print i + get_eleet()

    if (r % 10):
        print 'wUuUUt'
    else:
        print 'dont care!'

    with open('success', 'w') as f:
        f.write('yoooo seems to work bra!')

    return 0xdeadbeef

def encrypt(s):
    return ''.join(chr((ord(c) + 1) & 0xff) for c in s)

def opcodes_to_bytecode(opcodes):
    """Kind of bytecode compiler \o/"""
    bytecode = ''
    for instr in opcodes:
        if instr[0] in opcode.opmap:
            bytecode += chr(opcode.opmap.get(instr[0]))
            if len(instr) > 1:
                bytecode += struct.pack('<H', instr[1])
        else:
            bytecode += instr[0]
    return bytecode

def craft_pyc_via_func_object(function_object):
    """Craft directly a .pyc file with your code object inside"""
    varnames = []
    code_object = function_object.func_code
    c = code_object.co_code
    names = [ function_object.__name__ ]
    consts = [ code_object ]
    stub_instrs = opcodes_to_bytecode([
        ('LOAD_CONST', consts.index(code_object)),
        ('MAKE_FUNCTION', 0),
        ('STORE_NAME', names.index(function_object.__name__)),
        ('LOAD_NAME', names.index(function_object.__name__)),
        ('CALL_FUNCTION', 0),
        ('RETURN_VALUE', )
    ])

    stub_object = types.CodeType(
        0, 0, 1, 0,
        stub_instrs,
        tuple(consts), tuple(names), tuple(varnames),
        '', '', 137, ''
    )

    name = '%s.Py%s.pyc' % (
        function_object.__name__,
        ''.join(platform.python_version_tuple())
    )

    with open(name, 'wb') as f:
        f.write(MAGIC)
        f.write(struct.pack('<I', 0xBA0BAB))
        marshal.dump(stub_object, f)
        f.flush()

def generate_random_strings():
    """Generate a random string"""
    charset = map(chr, range(0, 0x100))
    return ''.join(random.choice(charset) for i in range(random.randint(10, 100)))

def find_absolute_instr(code, i_init = 0, end = None):
    """Find in code the instructions that use absolute reference, and
    returns the offsets of those instructions.
    Really useful when you want to relocate a code, you just have to patch
    the 2bytes with your relocation offset."""
    i = i_init
    absolute_refs = []
    if end == None:
        end = len(code)

    while i < end:
        byte = ord(code[i])
        i += 1

        if byte >= opcode.HAVE_ARGUMENT:
            absolute_offset = struct.unpack('<H', code[i : i + 2])[0]
            if byte in opcode.hasjabs:
                absolute_refs.append(i)

            i += 2

    return absolute_refs

class UniqueList(list):
    """Set doens't have a .index method, so here a class doing the job"""
    def append(self, r):
        if not list.__contains__(self, r):
            list.append(self, r)

    def extend(self, it):
        for i in it:
            self.append(i)

def add_encryption_layer(f, number_layer):
    """Add number_layer layers to the function f"""
    c = f.func_code
    original_bytecode = c.co_code

    encryption_marker = '\xBA\x0B\xBA\xBE'
    names = UniqueList(c.co_names)
    varnames = UniqueList(c.co_varnames)
    consts = UniqueList(c.co_consts)
    decryption_layers = []
    relocation_offset = 0
    absolute_jmp_infos = find_absolute_instr(original_bytecode)

    print '    Instructions with absolute offsets found in the original bytecode: %r' % absolute_jmp_infos
    print '    Preparing all the decryption layers..'
    for _ in range(number_layer):
        varnames_to_obfuscated_varnames = {
            'code' : generate_random_strings(),
            'idx_marker' : generate_random_strings(),
            'code_to_decrypt': generate_random_strings(),
            'code_decrypted' : generate_random_strings(),
            'memmove' : generate_random_strings(),
            'c_char' : generate_random_strings(),
            'padding_marker' : generate_random_strings(),
            'padding_size' : generate_random_strings()
        }

        const_to_obfuscated_const = {
            'MARKER' : generate_random_strings()
        }

        names.extend([
            f.__name__,
            'ctypes',
            'memmove',
            'c_char',
            'func_code',
            'co_code',
            'rfind',
            'id',
            'len',
            'chr',
            'ord',
            'from_address',
            'raw',
            'find'
        ])

        varnames.extend(varnames_to_obfuscated_varnames.values())

        consts.extend([
            const_to_obfuscated_const['MARKER'],
            len(const_to_obfuscated_const['MARKER']),
            -1,
            ('memmove', 'c_char'),
            '',
            0xff,
            'ABCDEFGH',
            100
        ])

        stub_decrypt_instrs = [
            ('JUMP_FORWARD', len(encryption_marker)),
            (encryption_marker, ),

            # from ctypes import memmove, c_char
            ('LOAD_CONST', consts.index(-1)),                               # __import__ level argument
            ('LOAD_CONST', consts.index(('memmove', 'c_char'))),            # __import__ fromlist argument
            ('IMPORT_NAME', names.index('ctypes')),
            ('IMPORT_FROM', names.index('memmove')),
            ('STORE_FAST', varnames.index(varnames_to_obfuscated_varnames['memmove'])),
            ('IMPORT_FROM', names.index('c_char')),
            ('STORE_FAST', varnames.index(varnames_to_obfuscated_varnames['c_char'])),
            ('POP_TOP', ),

            # padding_marker = 'ABCDEFGH'
            ('LOAD_CONST', consts.index('ABCDEFGH')),
            ('STORE_FAST', varnames.index(varnames_to_obfuscated_varnames['padding_marker'])),

            # padding_size = (c_char * 100).from_address(id(padding_marker)).raw.find(padding_marker)
            ('LOAD_FAST', varnames.index(varnames_to_obfuscated_varnames['c_char'])),
            ('LOAD_CONST', consts.index(100)),
            ('BINARY_MULTIPLY', ),
            ('LOAD_ATTR', names.index('from_address')),
            ('LOAD_GLOBAL', names.index('id')),
            ('LOAD_FAST', varnames.index(varnames_to_obfuscated_varnames['padding_marker'])),
            ('CALL_FUNCTION', 1),
            ('CALL_FUNCTION', 1),
            ('LOAD_ATTR', names.index('raw')),
            ('LOAD_ATTR', names.index('find')),
            ('LOAD_FAST', varnames.index(varnames_to_obfuscated_varnames['padding_marker'])),
            ('CALL_FUNCTION', 1),
            ('STORE_FAST', varnames.index(varnames_to_obfuscated_varnames['padding_size'])),

            # code = decryption_layer.func_code.co_code
            ('LOAD_GLOBAL', names.index(f.__name__)),
            ('LOAD_ATTR', names.index('func_code')),
            ('LOAD_ATTR', names.index('co_code')),
            ('STORE_FAST', varnames.index(varnames_to_obfuscated_varnames['code'])),

            # idx_marker = code.rfind('MARKER')
            ('LOAD_FAST', varnames.index(varnames_to_obfuscated_varnames['code'])),
            ('LOAD_ATTR', names.index('rfind')),
            ('LOAD_CONST', consts.index(const_to_obfuscated_const['MARKER'])),
            ('CALL_FUNCTION', 1),
            ('STORE_FAST', varnames.index(varnames_to_obfuscated_varnames['idx_marker'])),

            # code_to_decrypt = code[idx_marker + 6 : ]
            ('LOAD_FAST', varnames.index(varnames_to_obfuscated_varnames['code'])),
            ('LOAD_FAST', varnames.index(varnames_to_obfuscated_varnames['idx_marker'])),
            ('LOAD_CONST', consts.index(len(const_to_obfuscated_const['MARKER']))),
            ('BINARY_ADD', ),
            # Implements TOS = TOS1[TOS:]
            ('SLICE+1', ),
            ('STORE_FAST', varnames.index(varnames_to_obfuscated_varnames['code_to_decrypt'])),

            # code_decrypted = ''
            ('LOAD_CONST', consts.index('')),
            ('STORE_FAST', varnames.index(varnames_to_obfuscated_varnames['code_decrypted'])),
            
            # for c in code_to_decrypt:
            #     code_decrypted += chr((ord(c) - 1) & 0xff)
            ('SETUP_LOOP', 1),
            ('LOAD_FAST', varnames.index(varnames_to_obfuscated_varnames['code_to_decrypt'])),
            ('GET_ITER', ),
            
            ('FOR_ITER', 33),
            ('LOAD_FAST', varnames.index(varnames_to_obfuscated_varnames['code_decrypted'])),
            ('ROT_TWO', ),
            ('LOAD_GLOBAL', names.index('chr')),
            ('ROT_TWO', ),
            # ord(c)
            ('LOAD_GLOBAL', names.index('ord')),
            ('ROT_TWO', ),
            ('CALL_FUNCTION', 1),
            # + (-1)
            ('LOAD_CONST', consts.index(-1)),
            ('BINARY_ADD', ),
            # & 0xff
            ('LOAD_CONST', consts.index(0xff)),
            ('BINARY_AND', ),
            # chr()
            ('CALL_FUNCTION', 1),
            # code_decrypted += chr()
            ('BINARY_ADD', ),
            ('STORE_FAST', varnames.index(varnames_to_obfuscated_varnames['code_decrypted'])),
            ('JUMP_ABSOLUTE', 126),
            ('POP_BLOCK', ),

            # memmove(id(code) + padding_size + idx_marker + len(marker), code_decrypted, len(code_decrypted))
            # id(code)
            ('LOAD_FAST', varnames.index(varnames_to_obfuscated_varnames['memmove'])),
            ('LOAD_GLOBAL', names.index('id')),
            ('LOAD_FAST', varnames.index(varnames_to_obfuscated_varnames['code'])),
            ('CALL_FUNCTION', 1),
            # + padding_size
            ('LOAD_FAST', varnames.index(varnames_to_obfuscated_varnames['padding_size'])),
            ('BINARY_ADD', ),
            # + idx_marker
            ('LOAD_FAST', varnames.index(varnames_to_obfuscated_varnames['idx_marker'])),
            ('BINARY_ADD', ),
            # + len(marker)
            ('LOAD_CONST', consts.index(len(const_to_obfuscated_const['MARKER']))),
            ('BINARY_ADD', ),
            # Push code_decrypted
            ('LOAD_FAST', varnames.index(varnames_to_obfuscated_varnames['code_decrypted'])),
            # len(code_decrypted)
            ('LOAD_GLOBAL', names.index('len')),
            ('LOAD_FAST', varnames.index(varnames_to_obfuscated_varnames['code_decrypted'])),
            ('CALL_FUNCTION', 1),
            # memmove call!
            ('CALL_FUNCTION', 3),
            ('POP_TOP', ),

            # Don't forgot to jump over the marker
            ('JUMP_FORWARD', len(const_to_obfuscated_const['MARKER'])),
            (const_to_obfuscated_const['MARKER'], )
        ]

        stub_decrypt_opcodes = opcodes_to_bytecode(stub_decrypt_instrs)

        relocation_offset += len(stub_decrypt_opcodes)
        decryption_layers.append(bytearray(stub_decrypt_opcodes))

    # First, patch the absolute references in the original bytecode
    # Note: the original_relocated_bytecode is valid only when it will be prepended by the X layerz
    print '    Relocate the original bytecode (size of all the stubs: %d bytes)' % relocation_offset
    original_relocated_bytecode = bytearray(original_bytecode)

    for patch_offset in absolute_jmp_infos:
        print '    Patching absolute instruction at offset %.8x' % patch_offset
        off = struct.unpack(
            '<H',
            str(original_relocated_bytecode[patch_offset : patch_offset + 2])
        )[0]
        off += relocation_offset
        original_relocated_bytecode[patch_offset : patch_offset + 2] = struct.pack('<H', off)

    # Why 7? It's the size of the 2 first instruction of our payload
    # We don't want to desynchronize our "disassembler"
    # Let's find absolute instruction only in the 170 first bytes, we don't want to
    # search stuff in the final marker ;)
    absolute_jmps_stub = find_absolute_instr(
        str(decryption_layers[0]),
        7,
        170
    )
    stub_relocation_offset = 0
    for layer in reversed(decryption_layers):
        for patch_offset in absolute_jmps_stub:
            off = struct.unpack(
                '<H',
                str(layer[patch_offset : patch_offset + 2])
            )[0]

            off += stub_relocation_offset
            layer[patch_offset : patch_offset + 2] = struct.pack('<H', off)

        stub_relocation_offset += len(layer)

    print '    Now assemble the layers..'
    
    final_bytecode = str(original_relocated_bytecode)
    for layer in decryption_layers:
        final_bytecode = str(layer) + encrypt(final_bytecode)

    print '    Final payload size: %d' % len(final_bytecode)
    f.func_code = types.CodeType(
        c.co_argcount, len(varnames), max(c.co_stacksize, 10), c.co_flags,
        final_bytecode,
        tuple(consts), tuple(names), tuple(varnames),
        c.co_filename, c.co_name, c.co_firstlineno, c.co_lnotab
    )

def main(argc, argv):
    print '1. Adding the decryption layers...'
    add_encryption_layer(very_understandable_function, 200)
    
    print '2. Generation of the .pyc file..'
    craft_pyc_via_func_object(very_understandable_function)

    print '3. Calling the resulting function, to see if it works'
    print 
    print hex(very_understandable_function())
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))