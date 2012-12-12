#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    nqueens.py - Solve the nqueens problem thanks to recursivity & z3 (constraint programming)
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

from time import time
from pprint import pprint
from z3 import *
import sys

def good_move(i, j, solutions):
    """Is it an allowed move ?"""
    for x, y in solutions:
        # a queen can't be on the same column / line / diag
        if x == i or y == j or abs(x - i) == abs(y - j):
            return False
    return True

def recurse_nqueens(n, ni, solution_list):
    """A queen can't be placed on the same diag/col/lin of an other"""
    i, j = 0, 0
    while i < n:
        while good_move(i, j, solution_list) == False and j < n:
            j += 1

        if j != n:
            if ni + 1 == n:
                return [(i, j)]

            r = recurse_nqueens(n, ni + 1, solution_list + [(i, j)])
            if r != None:
                return r + [(i, j)]
        else:
            j = 0
        i += 1
    return None

def nqueens(n):
    """Solves the problem of the nqueens thanks to recursivity/backtracking
    and returns the coordinates of the queens"""
    return recurse_nqueens(n, 0, [])

def abs_z3(a):
    """Get the absolute value of a Z3 variable"""
    return If(a >= 0, a, -a)

def nqueens_constraint_programming(n):
    """Solves the problem of the nqueens thanks to constraint programming/z3"""
    columns = [Int('c%d' % i) for i in range(n)]
    lines = [Int('l%d' % i) for i in range(n)]
    s = Solver()

    for i in range(n):
        s.add(columns[i] >= 0,columns[i] < n, lines[i] >= 0, lines[i] < n)

    for i in range(n - 1):
        for j in range(i + 1, n):
            s.add(columns[i] != columns[j])
            s.add(lines[i] != lines[j])
            s.add(abs_z3(columns[i] - columns[j]) != abs_z3(lines[i] - lines[j]))

    if s.check() == unsat:
        raise Exception('Unsat bitch')

    m = s.model()
    return [(m[x].as_long(), m[y].as_long()) for x, y in zip(columns, lines)]

def nqueens_constraint_programming_opti(n):
    """Solves the problem of the nqueens thanks to constraint programming/z3 & a little trick"""
    columns = [Int('c%d' % i) for i in range(n)]
    # optimization trick: we set each column at a specific value, 0..N, it avoids a lot of useless constraint
    # thx fireboot!
    lines = range(n)
    s = Solver()

    for i in range(n):
        # each queen must be in the chessboard's limits
        s.add(columns[i] >= 0, columns[i] < n)

    for i in range(n - 1):
        for j in range(i + 1, n):
            s.add(columns[i] != columns[j])
            s.add(lines[i] != lines[j])
            s.add(abs_z3(columns[i] - columns[j]) != abs(lines[i] - lines[j]))

    if s.check() == unsat:
        raise Exception('Unsat bitch')

    m = s.model()
    return [(m[x].as_long(), y) for x, y in zip(columns, lines)]


def display_solutions(s):
    chessboard = [[0] * len(s) for i in range(len(s))]
    for x,y in s:
        chessboard[x][y] = 1
    pprint(chessboard)

def main(argc, argv):
    if argc != 2:
        print 'Usage: nqueens <n>'
        return 0

    implementations = [
        nqueens_constraint_programming_opti,
        nqueens_constraint_programming,
        nqueens
    ]

    for implementation in implementations:
        n = int(argv[1], 10)
        t1 = time()
        q = implementation(n)
        t2 = time()
        display_solutions(q)
        print 'With %s: %fs, %r' % (implementation.__name__, t2 - t1, q)

    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
