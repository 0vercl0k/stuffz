#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    dps_like.py - A dps like function for your GDB
#    Copyright (C) 2012 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k
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

import gdb
import re

class CommandDumpPointersWithSymbol(gdb.Command):
    '''
    This class aims to do the same thing (approx yeah) as the dps' windbg command does:
        it displays one pointer per line with its symbol (if there is one)

    Usage:
        dps <register or address> <positive int>
        It will display n [D/Q]WORDs pointed by the register/address
    '''

    def __init__(self):
        gdb.Command.__init__(self, 'dps', gdb.COMMAND_STACK)

        self.p_char = gdb.lookup_type('char').pointer()
        self.p_long = gdb.lookup_type('long').pointer()
        self.is_x86 = self.p_long.sizeof == 4

        # retrieve the memory mapping
        self.zones = self._parse_info_files()

    def _get_cpu_register(self, reg):
        '''
        Get the value holded by a CPU register
        '''

        expr = ''
        if reg[0] == '$':
            expr = reg
        else:
            expr = '$' + reg

        try:
            val = self._normalize_long(long(gdb.parse_and_eval(expr)))
        except:
            print "Hum, have you ran the process ? I can't retrieve any register."
            return None
        return val

    def _normalize_long(self, l):
        return (0xffffffff if self.is_x86 else 0xffffffffffffffff) & l

    def _long_to_str(self, l):
        return ('%#.8x' if self.is_x86 else '%#.16x') % l

    def _deref_long_from_addr(self, addr):
        '''
        Get the value pointed by addr
        '''

        # now cast + deref
        val = gdb.Value(addr).cast(self.p_long).dereference()
        return self._normalize_long(long(val))

    def _where_it_points(self, address):
        '''
        Walk out the memory mapping and try to find where the address is pointing
        '''
        info = []
        for zone in self.zones:
            if zone['start'] <= address < zone['end']:
                temp = zone['section_name']

                # NB: it exists gdb.solid_name(addr) to retrieve the sharedlibrary name if the address points in its range
                if zone['module']:
                    temp += '!%s' % zone['module']

                # we know where the address points
                info.append(temp)
                break

        # but let's try to have other/additional info
        r = self._get_additionnal_info(address, zone['section_name'])
        if r:
            info.append(r)

        return info

    def _is_register(self, s):
        '''
        Is it a valid register ?
        '''
        x86_reg = ['eax', 'ebx', 'ecx', 'edx', 'esi', 'edi', 'esp', 'ebp', 'eip']
        x64_reg = ['rax', 'rbx', 'rcx', 'rdx', 'rsi', 'rdi', 'rsp', 'rbp', 'rip'] + ['r%d' % i for i in range(8, 16)]

        if s[0] == '$':
            s = s[1:]

        if s in (x86_reg if self.is_x86 else x64_reg):
            return True
        return False

    def _is_pointing_on_string(self, addr):
        '''
        Is address is a pointer on a string ?
        Only strings with >= 3 characters are allowed
        '''
        # we try to see if addr is a pointer on an ASCII string
        s = gdb.Value(addr).cast(self.p_char)
        try:
            s = s.string()
        except:
            return None

        if len(s) > 3:
            # we consider it as a true string if it has at last 3 characters
            # but we will display only the first 50 chars
            return (s[:50] + '[...]' if len(s) > 50 else s)
        return None

    def _parse_info_files(self):
        '''
        Creates a list of dictionnaries where you can find the start/end of all sharelibrary sections
        '''
        r = gdb.execute('info files', to_string = True)
        zones = []

        for line in r.splitlines():
            if line.find(' is ') == -1:
                continue

            memrange, where = line.split(' is ', 1)
            start, end = memrange.split(' - ', 1)

            section, module = where, ''

            # it's a section in a sharedlibrary
            if where.find(' in ') != -1:
                section, module = where.split(' in ')

            zones.append({
                'start' : int(start.lstrip(), 16),
                'end' : int(end, 16),
                'section_name' : section,
                'module' : module
            })

        return zones

    def _clean_disass(self, disass):
        '''
        Clean the disassembly
        When you have 'mov      eax, [ebx]', it returns 'mov eax, [ebx]'
        '''
        return re.sub(r'\s+', ' ', disass)

    def _get_additionnal_info(self, addr, section):
        '''
        Try to know if the address is a string pointer, if not it try to disassemble the first instruction
        '''
        # before any test, we want to know if the memory is accessible
        try:
            self._deref_long_from_addr(addr)
        except:
            # memory isn't accessible
            return None

        # we try to see if addr is a pointer on an ASCII string
        r = self._is_pointing_on_string(addr)
        if r != None and len(r) > 1:
            # we consider it as a true string
            return 'String(%s)' % repr(r)

        # try to disassembly it
        r = gdb.execute('x/i %#x' % addr, to_string = True)
        function, instr = r.split(':', 1)

        # clean the instruction part
        clean_disass = self._clean_disass(instr)

        # try to obtain the function name
        function_names = re.findall('<(.+)>', function)

        # we prepare the signature 
        signature = clean_disass

        if len(function_names) > 0:
            signature += 'found in "%s"' % function_names[0]

        return signature

    def invoke(self, arg, from_tty):
        '''
        The core of the command
        '''
        arguments = arg.split(' ')
        assert(len(arguments) == 2)

        r, npointers = arguments
        pointer_address = 0

        if self._is_register(r):
            pointer_address = self._get_cpu_register(r)
            if not pointer_address:
                return
        else:
            try:
                # we assume it's an address
                pointer_address = int(r, 16)
            except:
                print 'The first argument should be wether an address or a register, please read the "help dps"'
                return

        for n in range(int(npointers)):
            try:
                value = self._deref_long_from_addr(pointer_address)
            except:
                print 'There is not allocated memory at %s' % self._long_to_str(pointer_address)
                return

            print '%.4d - [%s] = %s - %s' % (n, self._long_to_str(pointer_address), self._long_to_str(value), ' - '.join(self._where_it_points(value)))
            pointer_address += self.p_long.sizeof

CommandDumpPointersWithSymbol()