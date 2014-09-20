#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    disassembler_ql_chall.py - HACKY disassembler designed for Quarkslab's custom compiler
#    It has been tested only with this challenge -- don't expect it to work elsewhere
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
import dis
import marshal

def dis_ql(x, store_fast = False):
    '''Makes dis.dis work with the custom opcodes'''
    custom_opmap = {
        'RETURN_VALUE' : 0x1b,
        'INPLACE_ADD' : 0x3c,
        'BINARY_XOR' : 0x4e,
        'GET_ITER' : 0x53,
        'POP_TOP' : 0x54,
        'INPLACE_SUBTRACT' : 0x55,
        'YIELD_VALUE' : 0x59,
        'FOR_ITER' : 0x5d,
        'STORE_GLOBAL' : 0x61,
        
        'LOAD_CONST'   : 0x64,
        'LOAD_CONST2'  : 0xa0,
        'LOAD_CONST3'  : 0xc8,
        'LOAD_CONST4'  : 0xea,
        'LOAD_CONST5'  : 0xb2,
        'LOAD_CONST6'  : 0x91,
        'LOAD_CONST7'  : 0x9e,
        'LOAD_CONST8'  : 0xd4,
        'LOAD_CONST9'  : 0xdd,
        'LOAD_CONST10' : 0xd5,
        'LOAD_CONST11' : 0xcc,
        'LOAD_CONST12' : 0x78,
        'LOAD_CONST14' : 0x5b,
        'LOAD_CONST15' : 0x97,

        'BUILD_LIST' : 0x67,
        'LOAD_ATTR' : 0x6a,
        'COMPARE_OP' : 0x6b,
        'JUMP_FORWARD' : 0x6e,
        'JUMP_ABSOLUTE' : 0x71,
        'POP_JUMP_IF_FALSE' : 0x72,
        'MAKE_FUNCTION' : 0x77,
        'LOAD_GLOBAL' : 0x7c,
        'CALL_FUNCTION' : 0x86,

        'LOAD_FAST' : 0x8f,
    }
    if store_fast:
        custom_opmap['STORE_FAST'] = 0x87
    else:
        custom_opmap['LOAD_CONST16'] = 0x87

    custom_opmap_rev = dict((v, k) for k, v in custom_opmap.iteritems())
    custom_opname = list()
    values = sorted(custom_opmap.values(), reverse = True)
    biggest_key = values[0]
    for i in range(biggest_key + 1):
        if i in values:
            custom_opname.append(custom_opmap_rev[i])
        else:
            custom_opname.append('(%d)' % i)

    custom_hasname = list()
    custom_hasconst = list()
    custom_hasjrel = list()
    custom_haslocal = list()
    custom_hascompare = list()

    for k, v in custom_opmap.iteritems():
        # Little hack to handle every LOAD_CONST
        if k.startswith('LOAD_CONST'):
            k = 'LOAD_CONST'

        if dis.opmap[k] in dis.hasname:
            custom_hasname.append(v)
        if dis.opmap[k] in dis.hasconst:
            custom_hasconst.append(v)
        if dis.opmap[k] in dis.hasjrel:
            custom_hasjrel.append(v)
        if dis.opmap[k] in dis.haslocal:
            custom_haslocal.append(v)
        if dis.opmap[k] in dis.hascompare:
            custom_hascompare.append(v)

    dis.opname = custom_opname
    dis.opmap = custom_opmap
    dis.hasname = custom_hasname
    dis.hasconst = custom_hasconst
    dis.hasjrel = custom_hasjrel
    dis.haslocal = custom_haslocal
    dis.hascompare = custom_hascompare
    dis.EXTENDED_ARG = 0xff # dunno!
    return dis.dis(x)

def main(argc, argv):
    # part 1
    p1 = marshal.loads('c\x00\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00C\x00\x00\x00s\x14\x00\x00\x00d\x01\x00\x87\x00\x00|\x00\x00d\x01\x00<a\x00\x00|\x00\x00\x1b(\x02\x00\x00\x00Ni\x01\x00\x00\x00(\x01\x00\x00\x00t\x04\x00\x00\x00True(\x01\x00\x00\x00t\x0e\x00\x00\x00Robert_Forsyth(\x00\x00\x00\x00(\x00\x00\x00\x00s\x10\x00\x00\x00obfuscate/gen.pyt\x03\x00\x00\x00foo\x05\x00\x00\x00s\x06\x00\x00\x00\x00\x01\x06\x02\n\x01')
    dis_ql(p1, store_fast = True)
    print '=' * 80

    # part 2
    p2 = marshal.loads('\x63\x00\x00\x00\x00\x00\x00\x00\x00\x1d\x00\x00\x00\x43\x00\x00\x00\x73\x8b\x00\x00\x00\x7c\x00\x00\x64\x01\x00\x6b\x03\x00\x72\x19\x00\x7c\x00\x00\x64\x02\x00\x55\x61\x00\x00\x6e\x6e\x00\x7c\x01\x00\x6a\x02\x00\x64\x03\x00\x6a\x03\x00\x64\x04\x00\x77\x00\x00\xa0\x05\x00\xc8\x06\x00\xa0\x07\x00\xb2\x08\x00\xa0\x09\x00\xea\x0a\x00\xa0\x0b\x00\x91\x08\x00\xa0\x0c\x00\x9e\x0b\x00\xa0\x0d\x00\xd4\x08\x00\xa0\x0e\x00\xd5\x0f\x00\xa0\x10\x00\xdd\x11\x00\xa0\x07\x00\xcc\x08\x00\xa0\x12\x00\x78\x0b\x00\xa0\x13\x00\x87\x0f\x00\xa0\x14\x00\x5b\x15\x00\xa0\x16\x00\x97\x17\x00\x67\x1a\x00\x53\x86\x01\x00\x86\x01\x00\x86\x01\x00\x54\x64\x00\x00\x1b\x28\x18\x00\x00\x00\x4e\x69\x03\x00\x00\x00\x69\x01\x00\x00\x00\x74\x00\x00\x00\x00\x63\x01\x00\x00\x00\x02\x00\x00\x00\x04\x00\x00\x00\x73\x00\x00\x00\x73\x1f\x00\x00\x00\x8f\x00\x00\x5d\x15\x00\x87\x01\x00\x7c\x00\x00\x8f\x01\x00\x64\x00\x00\x4e\x86\x01\x00\x59\x54\x71\x03\x00\x64\x01\x00\x1b\x28\x02\x00\x00\x00\x69\x0d\x00\x00\x00\x4e\x28\x01\x00\x00\x00\x74\x03\x00\x00\x00\x63\x68\x72\x28\x02\x00\x00\x00\x74\x02\x00\x00\x00\x2e\x30\x74\x01\x00\x00\x00\x5f\x28\x00\x00\x00\x00\x28\x00\x00\x00\x00\x73\x10\x00\x00\x00\x6f\x62\x66\x75\x73\x63\x61\x74\x65\x2f\x67\x65\x6e\x2e\x70\x79\x73\x09\x00\x00\x00\x3c\x67\x65\x6e\x65\x78\x70\x72\x3e\x16\x00\x00\x00\x73\x02\x00\x00\x00\x06\x00\x69\x4b\x00\x00\x00\x69\x62\x00\x00\x00\x69\x7f\x00\x00\x00\x69\x2d\x00\x00\x00\x69\x59\x00\x00\x00\x69\x65\x00\x00\x00\x69\x68\x00\x00\x00\x69\x43\x00\x00\x00\x69\x7a\x00\x00\x00\x69\x41\x00\x00\x00\x69\x78\x00\x00\x00\x69\x63\x00\x00\x00\x69\x6c\x00\x00\x00\x69\x5f\x00\x00\x00\x69\x7d\x00\x00\x00\x69\x6f\x00\x00\x00\x69\x61\x00\x00\x00\x69\x64\x00\x00\x00\x69\x6e\x00\x00\x00\x28\x04\x00\x00\x00\x74\x04\x00\x00\x00\x54\x72\x75\x65\x74\x09\x00\x00\x00\x71\x75\x61\x72\x6b\x73\x6c\x61\x62\x74\x06\x00\x00\x00\x61\x70\x70\x65\x6e\x64\x74\x04\x00\x00\x00\x6a\x6f\x69\x6e\x28\x00\x00\x00\x00\x28\x00\x00\x00\x00\x28\x00\x00\x00\x00\x73\x10\x00\x00\x00\x6f\x62\x66\x75\x73\x63\x61\x74\x65\x2f\x67\x65\x6e\x2e\x70\x79\x74\x03\x00\x00\x00\x66\x6f\x6f\x11\x00\x00\x00\x73\x06\x00\x00\x00\x00\x02\x0c\x01\x0d\x02')
    dis_ql(p2, store_fast = False)
    print '=' * 80

    # part 2.generator
    dis_ql(p2.co_consts[4], store_fast = False)
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))