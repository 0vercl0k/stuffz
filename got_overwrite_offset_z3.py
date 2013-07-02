#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    got_overwrite_offset_z3.py - How you can use Z3 to smash a got entry in some exploitation task.
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

import sys
from z3 import *

# I was reading https://twitter.com/ekse0x/status/347422267690598401, and @ekse0x could have solved the challenge
# using Z3. So it was a perfect occasion to write a little script instead of "bruteforcing" the variable i.
# The idea is:
#   mov [0x0804A100+0x88*i], controled
# And you want to smash a got entry :-), let's ask Z3!

def main(argc, argv):
    base = 0x0804A100
    addresses = {
      'read' : 0x0804A010,
      'printf' : 0x0804A014,
      'puts' : 0x0804A030,
      'exit' : 0x0804A03C
    }

    i = BitVec('i', 32)
    for k, v in addresses.iteritems():
        s = Solver()
        s.add((base + (i * 0x88)) == v)
        if s.check() == sat:
            m = s.model()
            print 'You can smash %s with i=%#.8x' % (k, m[i].as_long())

    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
