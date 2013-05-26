#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    4_extract_quarter_round.py - NoSuchCon 2013 Extract a quarter of a round.
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

class UniqueList(list):
    def append(self, r):
        try:
            list.index(self, r)
        except:
            list.append(self, r)
    def extend(self, r):
        for i in r:
            self.append(i)


def clean(r):
    r = r.replace('[', '')
    r = r.replace(']', '')
    return r

outputs = {
    'out[8]' : [],
    'memory[101]' : [],
    'out[11]' : [],
    'memory[87]' : []
}

inputs = UniqueList()
lines = UniqueList()

for i in range(3):
    f = open('ssa_version_algorithm', 'r')
    for line in reversed(f.readlines()):
        pattern = '(.+) = T[H]?_([A-F0-9]+)\[(.+?)\];'
        pattern_16 = '(.+) = T16_([A-F0-9]+)\[(.+)\]\[(.+)\];'

        match = re.search(pattern, line)
        if match:
            dst = match.group(1)
            table = match.group(2)
            fetched = match.group(3)
            for mem in outputs.keys():
                if dst == mem or dst in outputs[mem]:
                    inputs.append(fetched)
                    lines.append(line)

        match = re.search(pattern_16, line)
        if match:
            dst = match.group(1)
            table = match.group(2)
            fetched1 = match.group(3)
            fetched2 = match.group(4)
            for mem in outputs.keys():
                if dst == mem or dst in outputs[mem]:
                    outputs[mem].extend([
                        fetched1,
                        fetched2
                    ])
                    lines.append(line)

lines = reversed(lines)
# print ''.join(lines)
assert(len(inputs) == 4)

print 'unsigned char %s;' % ','.join('%s_suce' % clean(i) for i in inputs)
for i in range(len(inputs)):
    increment = chr(ord('i') + i)
    print 'for(unsigned int %c = 0; %c < 0x100; ++%c){' % ((increment, ) * 3)
    print '%s = %c;' % (inputs[i], increment)

print ''.join(lines)
print 'if(%s){' % ' && '.join('%s == %s_suce' % (k, clean(k)) for k in outputs.keys())

for input_ in inputs:
    print '%s_suce = %s;' % (clean(input_), input_)

print '}'
for i in range(len(inputs)):
    print '}'