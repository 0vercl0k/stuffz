#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    udd.py - Parse OllyDbg2's UDD files
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
# References:
#     - 0:000> x ollydbg!*tagged*
#     - 004acdd0   ollydbg!Savetaggedrecord
#     - 004aceec   ollydbg!Createtaggedfile
#     - 004ad018   ollydbg!Finalizetaggedfile
#     - 004ad38c   ollydbg!Gettaggedrecordsize
#     - 004ad470   ollydbg!Gettaggedfiledata
#     - 004ad520   ollydbg!Closetaggedfile
#     - 004ad548   ollydbg!Opentaggedfile
#     - 004af48c   ollydbg!sub_4AF48C
#     - https://pyudd.googlecode.com/svn/trunk/pyudd.py But kinda outdated


import sys
import struct
import os
from ctypes import *

HDR_MAGIC = 'Mod\x00'

def sprint(n, s):
    '''Print with spaces prefixed'''
    print ' ' * n, s

def ssprint(n, s):
    '''Print with spaces prefixed'''
    print ' ' * n, s,

def hexdump(src, length = 16, sep = '.'):
    '''Taken from https://gist.github.com/7h3rAm/5603718'''
    FILTER = ''.join((len(repr(chr(x))) == 3) and chr(x) or sep for x in range(256))
    lines = []
    for c in xrange(0, len(src), length):
        chars = src[c:c+length]
        hex = ' '.join('%02x' % ord(x) for x in chars)
        if len(hex) > 24:
            hex = '%s %s' % (hex[:24], hex[24:])
        printable = ''.join('%s' % ((ord(x) <= 127 and FILTER[ord(x)]) or sep) for x in chars)
        lines.append('%08x:  %-*s  |%s|\n' % (c, length*3, hex, printable))
    return ''.join(lines)

def strtochex(s):
    return ''.join('\\x%.2x' % ord(i) for i in s)

class Record(Structure):
    '''A record is composed of a magic value that defines the type of the record,
    then you have the size of the record, finally the raw data'''
    _fields_ = [
        ('magic', c_int32),
        ('size', c_int32),
        # content
    ]

class t_jmpdata(Structure):
    '''Descriptor of recognized jump or call'''
    _pack_ = 1
    _fields_ = [
        ('from_', c_int32),
        ('dest', c_int32),
        ('type', c_ubyte)
    ]

class t_metadata(Structure):
    '''Descriptor of .NET MetaData table'''
    _pack_ = 1
    _fields_ = [
        ('base', c_int32),     # Location in memory or NULL if absent
        ('rowcount', c_int32), # Number of rows or 0 if absent
        ('rowsize', c_int32),  # Size of single row, bytes, or 0
        ('nameoffs', c_int32), # Offset of name field
        ('namesize', c_int32)  # Size of name or 0 if absent
    ]

class t_patch_hdr(Structure):
    _pack_ = 1
    _fields_ = [
        ('addr', c_int32),  # Base address of patch in memory
        ('size', c_int32),  # Size of patch, bytes
        ('type_', c_int32), # Type of patch, set of TY_xxx
        # uchar  orig[PATCHSIZE];
        # uchar  mod[PATCHSIZE];
    ]

class dt_case(Structure):
    '''Switch exit descriptor DT_CASE'''
    _pack_ = 1
    _fields_ = [
        ('addr', c_int32),   # In our case an addr value is before a dt_case. Seems to be the default case
        ('swbase', c_int32), # Address of a switch descriptor
        ('type_', c_int32),  # Switch type, set of CASE_xxx
        ('ncase', c_int32)   # Number of cases (1..64, 0: default)
        # ulong          value[NSWCASE];       // List of cases for exit
    ]

class t_hexstr_hdr(Structure):
    '''Data for hex/text search'''
    _pack_ = 1
    _fields_ = [
        ('n', c_int32),    # Data length, bytes
        ('nmax', c_int32), # Maximal data length, bytes
        # uchar  data[HEXLEN];  // Data
        # uchar  mask[HEXLEN];  // Mask, 0 bits are masked
    ]

class t_nameinfo(Structure):
    '''Header of name/data record (MI_NAME)'''
    _pack_ = 1
    _fields_ = [
        ('offs', c_int32), # Offset in module
        ('type_', c_ubyte) # Name/data type, one of NM_xxx/DT_xxx
    ]

class FILETIME(Structure):
    _pack_ = 1
    _fields_ = [
        ('low', c_int32),
        ('high', c_int32)
    ]

class t_fileinfo(Structure):
    '''Length, date, CRC (MI_FILEINFO)'''
    _pack_ = 1
    _fields_ = [
        ('size', c_int32),      # Length of executable file
        ('filetime', FILETIME), # Time of last modification
        ('crc', c_int32),       # CRC of executable file
        ('issfx', c_int32),     # Whether self-extractable
        ('sfxentry', c_int32)   # Offset of original entry after SFX
    ]

class t_bpmem(Structure):
    '''Memory breakpoints'''
    _pack_  = 1
    _fields_ = [
        ('addr', c_int32),  # Address of breakpoint
        ('size', c_int32),  # Size of the breakpoint, bytes
        ('type_', c_int32), # Type of breakpoint, TY_xxx+BP_xxx
        ('limit', c_int32), # Original pass count (0 if not set)
        ('count', c_int32)  # Actual pass count
    ]

class t_bphard(Structure):
    '''Hardware breakpoints'''
    _pack_ = 1
    _fields_ = [
        ('index', c_int32),       # Index of the breakpoint (0..NHARD-1)
        ('dummy', c_int32),       # Must be 1
        ('type_', c_int32),       # Type of the breakpoint, TY_xxx+BP_xxx
        ('addr', c_int32),        # Address of breakpoint
        ('size', c_int32),        # Size of the breakpoint, bytes
        ('fnindex', c_int32),     # Index of predefined function
        ('limit', c_int32),       # Original pass count (0 if not set)
        ('count', c_int32),       # Actual pass count
        ('actions', c_int32),     # Actions, set of BA_xxx
        ('modbase', c_int32),     # Module base, used by .udd only
        ('path', (c_wchar * 260)) # Full module name, used by .udd only
    ]

class sd_pred(Structure):
    '''Descriptor of predicted data'''
    _pack_ = 1
    _fields_ = [
        ('addr', c_int32),     # Address of predicted command
        ('mode', c_ushort),    # Combination of PRED_xxx
        ('espconst', c_int32), # Offset of ESP to original ESP
        ('ebpconst', c_int32), # Offset of EBP to original ESP
        ('resconst', c_int32)  # Constant in result of execution
    ]

class dt_switch_hdr(Structure):
    '''Switch descriptor DT_SWITCH'''
    _pack_ = 1
    _fields_ = [
        ('casemin', c_int32),      # Minimal case
        ('casemax', c_int32),      # Maximal case
        ('type_', c_int32),        # Switch type, set of CASE_xxx
        ('nexit', c_int32),        # Number of exits including default
        # #define NSWEXIT 256      // Max no. of switch exits, incl. default
        # ulong exitaddr[NSWEXIT]; // List of exits (point to dt_case)
    ]

class t_procdata(Structure):
    '''Description of procedure'''
    _pack_ = 1
    _fields_ = [
        ('addr', c_int32),            # Address of entry point
        ('size', c_int32),            # Size of simple procedure or 1
        ('type_', c_int32),           # Type of procedure, TY_xxx/PD_xxx
        ('retsize', c_int32),         # Size of return (if PD_RETSIZE)
        ('localsize', c_int32),       # Size of reserved locals, 0 - unknown
        ('savedebp', c_int32),        # Offset of cmd after PUSH EBP, 0 - none
        ('features', c_int32),        # Type of known code, RAW_xxx
        ('generic', (c_char * 12)),  # Generic name (without _INTERN_)
        ('narg', c_int32),            # No. of stack DWORDs (PD_NARG/VARARG)
        ('nguess', c_int32),          # Number of guessed args (if PD_NGUESS)
        ('npush', c_int32),           # Number of pushed args (if PD_NPUSH)
        ('usedarg', c_int32),         # Min. number of accessed arguments
        ('preserved', c_ubyte),       # Preserved registers
        ('argopt', (c_ubyte * 7))     # Guessed argument options, AO_xxx
    ]

class t_bpoint(Structure):
    '''INT3 breakpoints'''
    _pack_ = 1
    _fields_ = [
        ('addr', c_int32),     # Address of breakpoint
        ('size', c_int32),     # Must be 1
        ('type_', c_int32),    # Type of breakpoint, TY_xxx+BP_xxx
        ('fnindex', c_ushort), # Index of predefined function
        ('cmd', c_ubyte),      # First byte of original command
        ('patch', c_ubyte),    # Used only in .udd files
        ('limit', c_int32),    # Original pass count (0 if not set)
        ('count', c_int32),    # Actual pass count
        ('actions', c_int32)   # Actions, set of BA_xxx
    ]

def breakpoint_type_to_access(ty):
    '''0x00200000|0x00400000|0x00800000 -> rwx'''
    flags = [
        (0x00200000, 'r'),
        (0x00400000, 'w'),
        (0x00800000, 'x')
    ]
    return ''.join(a if (ty & mask) == mask else '-' for mask, a in flags)

def flags_to_str(t, flags):
    return '|'.join(m for mask, m in flags if (t & mask) == mask)

def nm_to_str(n):
    types = {
        0x00 : 'NM_NONAME', # Means that name is absent
        0x21 : 'NM_LABEL', # User-defined label
        0x22 : 'NM_EXPORT', # Exported name
        0x23 : 'NM_DEEXP', # Demangled exported name
        0x24 : 'DT_EORD', # Exported ordinal (ulong)
        0x25 : 'NM_ALIAS', # Alias of NM_EXPORT
        0x26 : 'NM_IMPORT', # Imported name (module.function)
        0x27 : 'NM_DEIMP', # Demangled imported name
        0x28 : 'DT_IORD', # Imported ordinal (struct dt_iord)
        0x29 : 'NM_DEBUG', # Name from debug data
        0x2A : 'NM_DEDEBUG', # Demangled name from debug data
        0x2B : 'NM_ANLABEL', # Name added by Analyser
        0x30 : 'NM_COMMENT', # User-defined comment
        0x31 : 'NM_ANALYSE', # Comment added by Analyser
        0x32 : 'NM_MARK', # Important parameter
        0x33 : 'NM_CALLED', # Name of called function
        0x34 : 'DT_ARG', # Name and type of argument or data
        0x35 : 'DT_NARG', # Guessed number of arguments at CALL
        0x36 : 'NM_RETTYPE', # Type of data returned in EAX
        0x37 : 'NM_MODCOMM', # Automatical module comments
        0x38 : 'NM_TRICK', # Parentheses of tricky sequences
        0x40 : 'DT_SWITCH', # Switch descriptor (struct dt_switch)
        0x41 : 'DT_CASE', # Case descriptor (struct dt_case)
        0x42 : 'DT_MNEMO', # Alternative mnemonics data (dt_mnemo)
        0x44 : 'NM_DLLPARMS', # Parameters of Call DLL dialog
        0x45 : 'DT_DLLDATA', # Parameters of Call DLL dialog
        0x4A : 'DT_DBGPROC', # t_function from debug, don't save!
        0x51 : 'NM_INT3COND', # INT3 breakpoint condition
        0x52 : 'NM_INT3EXPR', # Expression to log at INT3 breakpoint
        0x53 : 'NM_INT3TYPE', # Type used to decode expression
        0x54 : 'NM_MEMCOND', # Memory breakpoint condition
        0x55 : 'NM_MEMEXPR', # Expression to log at memory break
        0x56 : 'NM_MEMTYPE', # Type used to decode expression
        0x57 : 'NM_HARDCOND', # Hardware breakpoint condition
        0x58 : 'NM_HARDEXPR', # Expression to log at hardware break
        0x59 : 'NM_HARDTYPE', # Type used to decode expression
        0x60 : 'NM_LABELSAV', # NSTRINGS last user-defined labels
        0x61 : 'NM_ASMSAV', # NSTRINGS last assembled commands
        0x62 : 'NM_ASRCHSAV', # NSTRINGS last assemby searches
        0x63 : 'NM_COMMSAV', # NSTRINGS last user-defined comments
        0x64 : 'NM_WATCHSAV', # NSTRINGS last watch expressions
        0x65 : 'NM_GOTOSAV', # NSTRINGS last GOTO expressions
        0x66 : 'DT_BINSAV', # NSTRINGS last binary search patterns
        0x67 : 'NM_CONSTSAV', # NSTRINGS last constants to search
        0x68 : 'NM_STRSAV', # NSTRINGS last strings to search
        0x69 : 'NM_ARGSAV', # NSTRINGS last arguments (ARGLEN!)
        0x6A : 'NM_CURRSAV', # NSTRINGS last current dirs (MAXPATH!)
        0x6F : 'NM_SEQSAV', # NSTRINGS last sequences (DATALEN!)
        0x70 : 'NM_RTCOND1', # First run trace pause condition
        0x71 : 'NM_RTCOND2', # Second run trace pause condition
        0x72 : 'NM_RTCOND3', # Third run trace pause condition
        0x73 : 'NM_RTCOND4', # Fourth run trace pause condition
        0x74 : 'NM_RTCMD1', # First run trace match command
        0x75 : 'NM_RTCMD2', # Second run trace match command
        0x76 : 'NM_RANGE0', # Low range limit
        0x77 : 'NM_RANGE1' # High range limit
    }
    return types[n] if n in types else 'Unknown'

descriptions = {
    '\nNst' : '.NET streams (t_netstream)', # XXX: Create the record handler
    '\nJdt' : 'Jump data',
    '\nMdt' : '.NET MetaData tables (t_metadata)',
    '\nSav' : 'Save area (t_savearea)', # XXX: Enhance record handler ?
    '\nBsv' : 'Last entered binary search patterns',
    '\nPat' : 'Patch data (compressed t_patch)',
    '\nCas' : 'Case (addr+dt_case)',
    '\nDat' : 'Name or data (t_nameinfo)',
    '\nFcr' : 'Length, date, CRC (t_fileinfo)',
    '\nCbr' : 'Call bracket', # XXX: RTFM nested data
    '\nLbr' : 'Loop bracket', # XXX: RTFM nested data
    '\nBpm' : 'Memory breakpoint (t_bpmem)',
    '\nBph' : 'Hardware breakpoint (t_bphard)',
    '\nPrd' : 'Predicted command execution results',
    '\nMne' : 'Decoding of mnemonics (addr+dt_mnemo)',
    '\nPlg' : 'Plugin prefix descriptor', # XXX: IIRC it's a data zone specific to each plugin (if he needs to)
    '\nSwi' : 'Switch (addr+dt_switch)',
    '\nWtc' : 'Watch in watch window',
    '\nPrc' : 'Procedure data (set of t_procdata)',
    '\nRtc' : 'Run trace pause condition', # XXX: Create the record handler..
    '\nIn3' : 'INT3 breakpoint (t_bpoint)',
    '\nMba' : 'Module base, size and path',
    '\nAna' : 'Record with analysis data', # XXX: Create the record handler..
    '\nLsa' : 'Last entered strings (t_nameinfo)',
    '\nEnd' : 'End of file dudies!'
}

def read_record(f):
    record = Record.from_buffer(bytearray(f.read(sizeof(Record))))
    content = f.read(record.size)
    return struct.pack('<I', record.magic), record.size, content

def handle_mdt_record(size, content):
    '''This record seems to store information related to .NET MetaData tables. More precisely
    with t_module.metadata'''
    assert(size == 1024)
    nbelem = size / sizeof(t_metadata)
    sprint(4, 'Found %d element' % nbelem)
    arrayTy = (t_metadata * nbelem)
    for e in arrayTy.from_buffer(bytearray(content)):
        sprint(5, 'Base: %.8x, Rowcount: %.8x (%d), Nameoffs: %.8x (%d)' % (e.base, e.rowcount, e.rowsize, e.nameoffs, e.namesize))

def handle_jdt_record(size, content):
    '''This record seems to store information related to JMP/CALL information found in the module. More precisely
    with t_module.jmps.jmpdata'''
    types = {
        1 : 'JMP',
        2 : 'JZ',
        3 : 'JMP table[reg32 * 4]',
        4 : 'RET',
        5 : 'CALL'
    }
    nbelem = size / sizeof(t_jmpdata)
    sprint(4, 'Found %d element' % nbelem)
    arrayTy = (t_jmpdata * nbelem)
    for e in arrayTy.from_buffer(bytearray(content)):
        # from is a RVA
        # dest is a VA
        sprint(5, '@%.8x -> %.8x (%s)' % (e.from_, e.dest, types[e.type] if e.type in types else e.type))

def handle_sav_record(size, content):
    '''Dont really know what this is'''
    for line in hexdump(content).strip().split('\n'):
        sprint(4, line)

def handle_pat_record(size, content):
    '''This record contains information related to the different patches you did'''
    hdr = t_patch_hdr.from_buffer(bytearray(content))
    codes = []
    for i in range(2):
        idx_code = sizeof(t_patch_hdr) + i * hdr.size
        codes.append(content[idx_code : idx_code + hdr.size])
    sprint(4, '@%.8x (%d bytes) %s -> %s' % (hdr.addr, hdr.size, strtochex(codes[0]), strtochex(codes[1])))

def handle_cas_record(size, content):
    '''This record keeps information related to SWITCH/>CASE< statements found by
    ollydbg's analyser'''
    dt = dt_case.from_buffer(bytearray(content))
    flags = [
        (0x01, 'CASE_CASCADED'), # Cascaded IF
        (0x02, 'CASE_HUGE'),     # Huge switch, some cases are lost
        (0x04, 'CASE_DEFAULT'),  # Has default (is default for dt_case)
        (0x10, 'CASE_ASCII'), # Intreprete cases as ASCII characters
        (0x20, 'CASE_MSG'),   # Interprete cases as WM_xxx
        (0x40, 'CASE_EXCPTN'), # Interprete cases as exception codes
        (0x80, 'CASE_SIGNED'), # Interprete cases as signed
    ]
    if dt.ncase > 0:
        arrayTy = (c_int32 * dt.ncase)
        array = arrayTy.from_buffer(bytearray(content[sizeof(dt_case) :]))
        cases = '(%s)' % ','.join(hex(i) for i in array)
    else:
        cases = ''
    sprint(4, 'Switch/>case< @%.8x (default case @%.8x), %s %s' % (dt.swbase, dt.addr, flags_to_str(dt.type_, flags), cases))

def handle_bsv_record(size, content):
    '''This record contains your lasts binary search pattern'''
    h = t_hexstr_hdr.from_buffer(bytearray(content))
    idx_base = sizeof(t_hexstr_hdr)
    sprint(4, 'Binary search (ID: %d, %d bytes): %r' % (h.n, h.nmax, content[idx_base : idx_base + h.nmax]))

def handle_dat_record(size, content):
    '''This record contains names/data infos'''
    n = t_nameinfo.from_buffer(bytearray(content))
    st = nm_to_str(n.type_)
    ssprint(4, '@%.8x %s' % (n.offs, st))
    if st != 'Unknown':
        idx_base = sizeof(t_nameinfo)
        if st in 'NM_ANLABEL NM_LABEL NM_CALLED NM_MARK NM_RETTYPE NM_ANALYSE':
            sprint(0, repr(content[idx_base :]))
        elif st in 'DT_ARG':
            name, ty = content[idx_base : ].split('\x00', 1)
            ty = ty.replace('\x00', '')
            sprint(0, '%s -> %s' % (name, ty))
        else:
            print ''
            for line in hexdump(content).strip().split('\n'):
                sprint(4, line)

def handle_fcr_record(size, content):
    '''This record contains global information concerning the executable file'''
    t = t_fileinfo.from_buffer(bytearray(content))
    sprint(4, 'Executable file length: %.8x bytes (crc: %.8x), Is SFX ? %s (sfxentry: %.8x)' % (t.size, t.crc, t.issfx, t.sfxentry))

def handle_cbr_record(size, content):
    '''bla'''
    for line in hexdump(content).strip().split('\n'):
        sprint(4, line)

def handle_lbr_record(size, content):
    '''bla'''
    for line in hexdump(content).strip().split('\n'):
        sprint(4, line)

def handle_bpm_record(size, content):
    '''This record stores your memory breakpoints.'''
    b = t_bpmem.from_buffer(bytearray(content))
    sprint(4, 'MEMBP @%.8x (%d bytes, %s)' % (b.addr, b.size, breakpoint_type_to_access(b.type_)))

def handle_bph_record(size, content):
    '''This record holds info related to the hardware breakpoints you set'''
    b = t_bphard.from_buffer(bytearray(content))
    sprint(4, 'HWBP ID %d (%d bytes) @%.8x %s (%s)' % (b.index, b.size, b.addr, breakpoint_type_to_access(b.type_), b.path))

def handle_prd_record(size, content):
    '''This record holds information about the predictions made by ollydbg's analyser. Beware
    it is *really* log consuming'''
    flags = [
        (0x8000, 'PRED_SHORTSP'), # Offset of ESP is 1 byte, .udd only
        (0x4000, 'PRED_SHORTBP'), # Offset of EBP is 1 byte, .udd only
        (0x0400, 'PRED_ESPRET'),  # Offset of ESP backtraced from return
        (0x0200, 'PRED_ESPOK'),   # Offset of ESP valid
        (0x0100, 'PRED_EBPOK'),   # Offset of EBP valid
        (0x0080, 'PRED_REL'),     # Result constant fixuped or relative
        (0x0020, 'PRED_VALID'),   # Result constant valid
        (0x0010, 'PRED_ADDR'),    # Result is address
        (0x0008, 'PRED_ORIG'),    # Result is based on original register
    ]
    nentry = struct.unpack_from('<I', content)[0]
    sprint(4, '%d prediction entries' % nentry)
    idx = 4
    for i in range(nentry):
        addr, mo = struct.unpack_from('<IH', content, idx)
        espconst, ebpconst, res = None, None, None
        idx += 6
        mode = flags_to_str(mo, flags)
        if 'PRED_ESPOK' in mode:
            if 'PRED_SHORTSP' in mode:
                espconst = struct.unpack_from('<B', content, idx)[0]
                idx += 1
            else:
                espconst = struct.unpack_from('<I', content, idx)[0]
                idx += 4

        if 'PRED_EBPOK' in mode:
            if 'PRED_SHORTBP' in mode:
                ebpconst = struct.unpack('<B', content[idx : idx + 1])[0]
                idx += 1
            else:
                ebconst = struct.unpack_from('<I', content, idx)[0]
                idx += 4

        if 'PRED_VALID' in mode:
            res = struct.unpack_from('<I', content, idx)[0]
            idx += 4

        s = ['Predicted command @%.8x (%s)' % (addr, mode)]
        if espconst is not None:
            s.append('offset of ESP to original ESP: %.8x' % espconst)
        if ebpconst is not None:
            s.append('offset of EBP to original ESP: %.8x' % ebpconst)
        if res is not None:
            s.append('constant in result of execution: %.8x' % res)

        sprint(5, ', '.join(s))

def handle_mne_record(size, content):
    '''This record holds information related to mnemonic (more precisely on jumps)'''
    addr, f = struct.unpack_from('<IB', content)
    # Flags indicating alternative forms of assembler mnemonics.
    flags = [
        (1, 'MF_JZ'), # JZ, JNZ instead of JE, JNE
        (2, 'MF_JC')  # JC, JNC instead of JAE, JB
    ]
    mode = '|'.join(m for mask, m in flags if (f & mask) == mask)
    sprint(4, '%s JMP @%.8x' % (mode, addr))

def handle_swi_record(size, content):
    '''This record keeps information related to >SWITCH</CASE statements found by
    ollydbg's analyser'''
    addr = struct.unpack_from('<I', content)[0]
    idx = 4
    d = dt_switch_hdr.from_buffer(bytearray(content[idx :]))
    flags = [
        (0x00000001, 'CASE_CASCADED'), # Cascaded IF
        (0x00000002, 'CASE_HUGE'),     # Huge switch, some cases are lost
        (0x00000004, 'CASE_DEFAULT'),  # Has default (is default for dt_case)
        (0x00000010, 'CASE_ASCII'),    # Intreprete cases as ASCII characters
        (0x00000020, 'CASE_MSG'),      # Interprete cases as WM_xxx
        (0x00000040, 'CASE_EXCPTN'),   # Interprete cases as exception codes
        (0x00000080, 'CASE_SIGNED'),   # Interprete cases as signed
    ]
    sprint(4, '>Switch</case infos @%.8x (case min/max: %.8x/%.8x, %s)' % (addr, d.casemin, d.casemax, flags_to_str(d.type_, flags)))

def handle_wtc_record(size, content):
    '''This record holds the watch expressions you added.'''
    sprint(4, 'Watch expression %s' % (content[4 :]))

def handle_prc_record(size, content):
    '''This record holds information related to the procedure found'''
    nentry = size / 64
    sprint(4, '%d entry' % nentry)
    idx = 0
    for i in range(nentry):
        p = t_procdata.from_buffer(bytearray(content[idx : ]))
        idx += sizeof(t_procdata)
        sprint(5, 'Procedure %r @%.8x: Reserved %d bytes, size of return: %d' % (p.generic, p.addr, p.localsize, p.retsize))

def handle_rtc_record(size, content):
    '''This record holds information related to the pause condition of the run trace'''
    for line in hexdump(content).strip().split('\n'):
        sprint(4, line)

def handle_in3_record(size, content):
    '''This record holds information related to the software breakpoints you put'''
    b = t_bpoint.from_buffer(bytearray(content))
    cond = None
    s = ['INT3 BP @%.8x' % (b.addr)]
    if size >= sizeof(t_bpoint) and content[sizeof(t_bpoint)] != '\x00':
        s.append(repr(content[sizeof(t_bpoint) :].replace('\x00', '')))

    sprint(4, ', '.join(s))

def handle_mba_record(size, content):
    '''This record holds information related to modules'''
    base, size = struct.unpack_from('<II', content)
    idx = 8
    sprint(4, '%s @%.8x (%.8x bytes)' % (content[idx :], base, size))

def handle_ana_record(size, content):
    '''This record holds information retrieved by the analyser. BTW: huge mess'''
    for line in hexdump(content).strip().split('\n'):
        sprint(4, line)

def handle_lsa_record(size, content):
    '''This record keeps an historic of the last strings you entered'''
    offset, ty = struct.unpack_from('<IB', content)
    idx = 5
    sprint(4, '%s @%.8x (%s)' % (content[idx :], offset, nm_to_str(ty)))

def handle_end_record(size, content):
    '''This is the end record'''
    pass

def dispatch(magic, size, content):
    dispatch_table = {
        '\nJdt' : handle_jdt_record,
        '\nMdt' : handle_mdt_record,
        '\nSav' : handle_sav_record,
        '\nPat' : handle_pat_record,
        '\nCas' : handle_cas_record,
        '\nBsv' : handle_bsv_record,
        '\nDat' : handle_dat_record,
        '\nFcr' : handle_fcr_record,
        '\nCbr' : handle_cbr_record,
        '\nLbr' : handle_lbr_record,
        '\nBpm' : handle_bpm_record,
        '\nBph' : handle_bph_record,
        '\nPrd' : handle_prd_record,
        '\nMne' : handle_mne_record,
        '\nSwi' : handle_swi_record,
        '\nWtc' : handle_wtc_record,
        '\nPrc' : handle_prc_record,
        '\nRtc' : handle_rtc_record,
        '\nIn3' : handle_in3_record,
        '\nMba' : handle_mba_record,
        '\nAna' : handle_ana_record,
        '\nLsa' : handle_lsa_record,
        '\nEnd' : handle_end_record
    }

    if magic in dispatch_table:
        return dispatch_table[magic](size, content)
    else:
        return None

def display_useful_infos(filename):
    '''Extract hardware bp, software bp, memory bp, patch, watch'''
    allowed_records = 'Pat Bsv Fcr Bpm Bph Wtc In3 Lsa'.split(' ')
    with open(filename, 'rb') as f:
        f.seek(0, os.SEEK_END)
        fsize = f.tell()
        f.seek(0, os.SEEK_SET)
        i = 0
        while i < fsize:
            magic, size, content = read_record(f)
            if magic.strip() in allowed_records or magic.strip() == 'Prd':
                print ('Read a record %r of size %d bytes (off: %.8x). ' % (magic, size, i) + (descriptions[magic] if magic in descriptions else ''))
                if magic.strip() != 'Prd':
                    dispatch(magic, size, content)
            i += 8 + size

def main(argc, argv):
    display_useful_infos('ollydbg.udd')
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))