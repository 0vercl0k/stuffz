#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    3_generate_c_algorithm_via_execution_trace.py - NoSuchCon 2013 FSM to extract
#    the algorithm in C.
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

import re

def address_to_sym(addr):
    i = int(addr, 16)
    if 0x00617000 <= i <= 0x0061700f:
        return 'key[0x%x]' % (i & 0xf)

    if 0x00617010 <= i <= 0x0061701f:
        return 'out[0x%x]' % (i & 0xf)

    return addr

def normalize_addr(addr):
    tmp = ''
    if addr.startswith('0x'):
        tmp = addr[2 : ]
    else:
        tmp = addr

    if len(tmp) != 8:
        tmp = tmp.rjust(8, '0')

    tmp = tmp.upper()
    return '0x' + tmp

def get_value(register_or_address, line):
    ret = ''
    is_int = False
    try:
        int(register_or_address, 16)
        is_int = True
    except:
        pass

    if is_int:
        ret = register_or_address
    # It's directly an address
    elif register_or_address.startswith('Oppida_NSC_Challenge_2013'):
        _, addr = register_or_address.split('.')
        ret = normalize_addr(addr)
    # It's a register
    else:
        _, tmp = line.split('%s=' % register_or_address)
        ret = normalize_addr(tmp[: 8])

    return address_to_sym(normalize_addr(ret))

lines = open('1_execution_trace.txt').readlines()
i = 0
state = 'read'
counter = 0

reg32_src = ''
reg32_src_value = ''
reg32_src2_value = ''
handlers_table_or_table_address = ''

tables = set()
handlers_tables = set()
sixteenbit_tables = set()
operations = []

while i < len(lines):
    line = lines[i].strip()
    if line == '' or line.startswith('#') or line.startswith('*'):
        i += 1
        continue

    if state == 'read':
        # On cherche un referencement d'un pointeur dans un registre c'est le debut d'une ecriture
        pattern = 'MOV [A-Z]{2},BYTE PTR \[(.+)\]'

        match = re.search(pattern, line)
        if match:
            reg32_src_value = get_value(match.group(1), line)
            score = 0
            pattern_1 = 'MOV ([A-Z]{3}),DWORD PTR \[([A-Z]{3})\+(.+)\]'
            pattern_2 = 'ADD ([A-Z]{3}),Oppida_NSC_Challenge_2013\.([A-F0-9]+)'

            for j in range(15):                   
                match = re.search(pattern_1, lines[i + j])
                if match:
                    reg32 = get_value(match.group(2), lines[i + j])
                    if reg32.startswith('0x000000') == False:
                        score += 2
                    else:
                        break

                match = re.search(pattern_2, lines[ i + j])
                if match:
                    reg32 = get_value(match.group(1), lines[i + j])
                    if reg32.startswith('0x000000') == False:
                        score += 2
                    else:
                        break

            if score >= 2:
                print 'Seems like a 16bits table: %r' % line
                state = 'sixteen_bits'
            else:
                state = 'handler_or_table'

            counter += 1
    elif state == 'handler_or_table':
        # Dans cet etat on recherche si on va avoir a faire a une table de handler
        # ou si on va avoir une table tout cours
        pattern_table_1 = 'MOV ([A-Z]{3}),DWORD PTR \[([A-Z]{3})\+Oppida_NSC_Challenge_2013\.([A-F0-9]+)\]'
        pattern_table_2 = 'ADD ([A-Z]{3}),Oppida_NSC_Challenge_2013\.([A-F0-9]+)'

        pattern_handler_1 = 'LEA ([A-Z]{3}),\[([A-Z]{3})\*4\+Oppida_NSC_Challenge_2013\.([A-F0-9]+)\]'
        pattern_handler_2 = 'PUSH DWORD PTR \[([A-Z]{3})\*4\+Oppida_NSC_Challenge_2013\.([A-F0-9]+)\]'
        pattern_handler_3 = 'JMP DWORD PTR \[([A-Z]{3})\*4\+Oppida_NSC_Challenge_2013\.([A-F0-9]+)\]'

        match = re.search(pattern_table_1, line)
        if match:
            handlers_table_or_table_address = normalize_addr(match.group(3))
            state = 'table'
        match = re.search(pattern_table_2, line)
        if match:
            handlers_table_or_table_address = normalize_addr(match.group(2))
            state = 'table'

        match = re.search(pattern_handler_1, line)
        if match:
            handlers_table_or_table_address = normalize_addr(match.group(3))
            state = 'handler'
        match = re.search(pattern_handler_2, line)
        if match:
            handlers_table_or_table_address = normalize_addr(match.group(2))
            state = 'handler'
        match = re.search(pattern_handler_3, line)
        if match:
            handlers_table_or_table_address = normalize_addr(match.group(2))
            state = 'handler'

    elif state == 'handler':
        # Maintenant on doit trouver la prochaine ecriture
        pattern = 'MOV BYTE PTR \[(.+)\],[A-Z0-9]{1,2}'
        match = re.search(pattern, line)

        if match:
            dest = get_value(match.group(1), line)

            print '*%s = %s[*%s]()' % (
                dest,
                handlers_table_or_table_address,
                reg32_src_value
            )

            handlers_tables.add(handlers_table_or_table_address)
            operations.append((dest, handlers_table_or_table_address, (reg32_src_value, )))
            state = 'read'
    elif state == 'table':
        # Maintenant on doit trouver la prochaine ecriture
        pattern = 'MOV BYTE PTR \[(.+)\],[A-Z0-9]{1,2}'
        match = re.search(pattern, line)

        if match:
            dest = get_value(match.group(1), line)

            print '*%s = %s[*%s]' % (
                dest,
                handlers_table_or_table_address,
                reg32_src_value
            )

            tables.add(handlers_table_or_table_address)
            operations.append((dest, handlers_table_or_table_address, (reg32_src_value, )))
            state = 'read'
    elif state == 'sixteen_bits':
        # Maintenant on recherche la seconde lecture
        pattern = 'MOV ([A-Z]{2}),BYTE PTR \[(.+)\]'
        match = re.search(pattern, line)
        if match:
            reg32_src2_value = get_value(match.group(2), line)
            state = 'sixteen_bits_fetch_in_table'
    elif state == 'sixteen_bits_fetch_in_table':
        patterns = [
            'MOV ([A-Z]{3}),DWORD PTR \[[A-Z]{3}\+(.+)\]',
            'ADD ([A-Z]{3}),Oppida_NSC_Challenge_2013\.([A-F0-9]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                handlers_table_or_table_address = get_value(match.group(2), line)
                state = 'sixteen_bits_write'
    elif state == 'sixteen_bits_write':
        pattern = 'MOV BYTE PTR \[(.+)],([A-Z]{2})'
        match = re.search(pattern, line)
        if match:
            dest = get_value(match.group(1), line)
            print '*%s = %s[*%s << 8 + %s]' % (
                dest,
                handlers_table_or_table_address,
                reg32_src_value,
                reg32_src2_value
            )
            sixteenbit_tables.add(handlers_table_or_table_address)
            operations.append((dest, handlers_table_or_table_address, (reg32_src_value, reg32_src2_value)))
            state = 'read'
    else:
        pass

    i += 1

print 'EOF - %d' % counter
if tables.intersection(handlers_tables) != set([]):
    print 'WEIRD T & HT'

if tables.intersection(sixteenbit_tables) != set([]):
    print 'WEIRD T & T16'
    print tables.intersection(sixteenbit_tables)

if handlers_tables.intersection(sixteenbit_tables) != set([]):
    print 'WEIRD HT & T16'

print 'Now generating the .c file..'
with open('algorithm_extracted_with_fsm.c', 'w') as f:
    # define time!
    for address in tables:
        f.write('#define T_%s ((PUCHAR)%s)\n' % (address[2 :], address))

    f.write('\n')
    
    for address in handlers_tables:
        f.write('#define TH_%s ((PUCHAR)%s)\n' % (address[2 :], address))
    
    f.write('\n')

    for address in sixteenbit_tables:
        f.write('#define T16_%s ((PUCHAR)%s)\n' % (address[2 : ], address))

    f.write('VOID Algo(UCHAR key[16], UCHAR out[16])\n{\n')
    for a, b, c in operations:
        f.write('\t')
        if a.startswith('key') == False and a.startswith('out') == False:
            f.write('*(PUCHAR)')

        f.write('%s = ' % a)
        
        if b in tables:
            f.write('T_')
        elif b in handlers_tables:
            f.write('TH_')
        else:
            f.write('T16_')

        f.write('%s[' % b[2 : ])

        if len(c) == 1:
            if c[0].startswith('key') == False and c[0].startswith('out') == False:
                f.write('*(PUCHAR)')
            f.write('%s' % c)
        else:
            f.write('(')
            src1, src2 = c
            if src1.startswith('key') == False and src1.startswith('out') == False:
                f.write('*(PUCHAR)')

            f.write('%s << 8) + ' % src1)
            if src2.startswith('key') == False and src2.startswith('out') == False:
                f.write('*(PUCHAR)')

            f.write('%s' % src2)
        f.write('];\n')

    f.write('}')
