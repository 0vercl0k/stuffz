#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    optimize_rop_add_gadgets_z3.py - How you can use Z3 to solve some ROP problem.
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

#    Special thanks to @Myst3rie for giving me the idea, you rock man :).

# The context:
#     I have several ROP gadgets that add a specific value to a specific register like this one:
#         add eax, 0xC9F4458B
#         add eax, 0x0FCF
#         add eax, 0x13B2
#     But I have to initialize EAX with another specific value and each byte of this value must be in the range [0x20, 0x7f].
#     Finally, I want that EAX equals 0xB00BDEAD (imagine it's the address of a .got entry for example).
#     Here is how I tried to solve the problem in the more optimized way via Z3.

import sys
from z3 import *

def ascii_printable(x):
    return And(0x20 <= (x & 0xff), (x & 0xff) <= 0x7f)

def linear_combination(x, y):
    tmp = 0
    for i in range(len(x)):
        tmp = tmp + (x[i] * y[i])
    return tmp

def main(argc, argv):
    model_final = None
    smallest_sum = 0xffffffff

    add_gadgets_values = [
        0xC9F4458B,
        0xDEADBEEF,
        0x0FCF,
        0x13B2,
        0x1337,
        0x42
    ]

    while True:
        s = Solver()
        magic = BitVec('magic', 32)
        gadgets = [BitVec('gadget%d' % i, 32) for i in range(len(add_gadgets_values))]

        # As I said, the EAX init must be a value with all bytes ASCII printable
        for i in range(4):
            s.add(ascii_printable((magic >> (i * 8))))

        for i in gadgets:
            s.add(ULT(i, smallest_sum))

        # Let's do our linear combination
        s.add((magic + linear_combination(gadgets, add_gadgets_values)) == 0xB00BDEAD)

        s.add(ULT(sum(gadgets), smallest_sum))

        if s.check() == sat:
            m = s.model()
            model_final = m
            sumfinal = sum(m[i].as_long() for i in gadgets) & 0xffffffff

            print 'Found a sum: %d' % sumfinal
            smallest_sum = sumfinal
        else:
            break

    assert(model_final != None)
    print 'Here is the optimal solution:'
    print '\t1. So, initialize EAX to the following value: %#.8x' % model_final[magic].as_long()
    n = 2

    for i in range(len(gadgets)):
        times = model_final[gadgets[i]].as_long()
        if times > 0:
            print '\t%d. Then, use the "ADD EAX, %#.8x" gadget %d times' % (
                n,
                add_gadgets_values[i],
                times
            )
            n += 1
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
