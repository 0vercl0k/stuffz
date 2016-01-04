#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    rename_functions_from_debug_logs.py - Uses debug outputs to rename functions
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

# I was looking at a binary that defined a `log_debug_info` method that basically wouldn't do anything
# but a lot of time debug messages would still be embedded in the binary itself -- turns out a lot of those debug
# messages start with the name of the method they are used in; see these examples:

# .text:00000001400160A4                 lea     r9, r ; "CCodecEnumerator::CodecInterfaceArrival"
# .text:00000001400160B7                 call    log_debug_info

# .text:00000001400161ED                 lea     r9, aCcodecenumer_4 ; "CCodecEnumerator::FindCodecFromSymLink"
# .text:00000001400161FB                 call    log_debug_trace

# The idea of this script is just to walk log_debug_trace's xrefs & backward scan from the call until finding a string
# that will be used to rename the function

'''
Examples of output:
   -> Found: 0x140001008L CH_ScoConnectionDown
   -> Found: 0x14000114cL CH_ConnectionRequest
   -> Found: 0x1400011c4L CH_DisconnectionRequest
   -> Found: 0x140002014L ConnectAsAvSource
   -> Found: 0x140002014L ConnectAsAvSource
   -> Found: 0x140002f40L GKI_exit
   -> Found: 0x1400039a4L SubdeviceChange
   -> Found: 0x14000974cL BtStackInterface::BtHwStopRendering
   [...]
'''

import sys
from idaapi import *
from idc import *

def main(argc, argv):
    debug_log_routines = (0x1400026E4, 0x1400024B8, 0x14001417C)
    for debug_routine_addr in debug_log_routines:
        for xref in CodeRefsTo(debug_routine_addr, 0):
            instr_addr = xref
            for _ in range(10):
                print '  -> Scanning back', hex(instr_addr)
                # Oboi, `yrp` you rock man.
                instr_addr = DecodePreviousInstruction(instr_addr).ea
                if GetMnem(instr_addr) == 'lea' and GetOpnd(instr_addr, 0) == 'r9' and GetOpType(instr_addr, 1) == o_mem:
                    s = GetString(
                        GetOperandValue(instr_addr, 1),
                        -1,
                        ASCSTR_C
                    )

                    try:
                        function_addr = idaapi.get_func(instr_addr).startEA
                    except:
                        print '  /!\\ There is no function defined, create one:', hex(instr_addr)
                        break

                    # XXX: we assume the lea instruction will be something like `lea r9, address`
                    # But in fact, if we have a register instead of the absolute address, we need to trace it back where it comes from
                    # It does sound annoying to do in IDAPython though :'
                    print '   -> Found:', hex(function_addr), s
                    MakeName(function_addr, s.replace('~', 'dtor_'))
                    break
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))