#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    magic_square_z3.py - Solve the magic-square problem with z3
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

import sys
import time
from z3 import *

def solve_magic_square(size):
    """Try to a solution for a size-magic square"""
    def column(matrix, i):
        """Get the column i of matrix"""
        return [matrix[j][i] for j in range(size)]

    def get_diagonals(matrix):
        """Get the diagonals of matrix"""
        return ([matrix[i][i] for i in range(size)], [matrix[i][size - i - 1] for i in range(size)])

    def get_constrained_int(x, y, s):
        """Get an Int and add the constraints associated directly in the solver"""
        # Int() is really really slower!
        x = BitVec('x%dy%d' % (x, y), 32)
        s.add(x > 0, x <= size**2)
        return x

    s = Solver()
    magic = (size * (size**2 + 1)) / 2
    matrix = [[get_constrained_int(y, x, s) for y in range(size)] for x in range(size)]

    # Each value must be different
    s.add(Distinct([matrix[i][j] for j in range(size) for i in range(size)]))

    for i in range(size):
        # Sum of each line, column must be equal to magic
        s.add(Sum(matrix[i]) == magic, Sum(column(matrix, i)) == magic)

    # Sum of each diagonal must be equal to magic
    d1, d2 = get_diagonals(matrix)
    s.add(Sum(d1) == magic, Sum(d2) == magic)

    if s.check() == unsat:
        raise Exception('The problem is not sat')

    m = s.model()
    return [[m[val].as_long() for val in line] for line in matrix], magic

def display_magic_square(s, magic):
    """Display the magic square with the solution"""
    print 'Magic value: %d' % magic
    for i in range(len(s)):
        print ('%.3d|' * len(s)) % tuple(s[i])

def main(argc, argv):
    if argc < 2:
        print 'Usage: ./magic_square_z3 <n>'
        return -1

    n = int(argv[1], 10)
    print 'Trying to find a solution for a %d-magic square..' % n
    t1 = time.time()
    s, magic = solve_magic_square(n)
    t2 = time.time()

    print 'Found a solution in %ds:' % (t2 - t1)
    display_magic_square(s, magic)
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))