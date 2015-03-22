#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    generate_aes_clean_unique_aabbccdd.py - Takes the unrolled implementation & generate one
#    with unique aa, bb, cc, dd variables ; easier to graph the dependency
#    Copyright (C) 2015 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k
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

def main(argc, argv):
    with open('aes_unrolled_code.raw.clean', 'r') as infile:
        idx = 0
        replace_table = dict(('%s' % i, '%s_%d' % (i, idx) ) for i in 'aa bb cc dd'.split())
        with open('aes_unrolled_code.raw.clean.unique_aabbccdd', 'w') as outfile:
            for line in infile.readlines():
                if '= Tyboxes' in line:
                    outfile.write('unsigned int ')

                for before, after in replace_table.iteritems():
                    line = line.replace(before, after)

                outfile.write(line)

                if ' >> 24' in line:
                    idx += 1
                    replace_table = dict(('%s' % i, '%s_%d' % (i, idx) ) for i in 'aa bb cc dd'.split())

    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))