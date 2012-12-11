#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    mojette_z3.py - Solve the grid of the day (taken from mojette.net) via z3
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
import urllib2
import operator
import BeautifulSoup
from z3 import *

def get_the_grid_of_the_day():
    """Gets the grid of the day on http://www.mojette.net"""
    data = urllib2.urlopen('http://www.mojette.net/').read()
    bins = map(
        lambda bin: int(bin['value'], 10),
        BeautifulSoup.BeautifulSoup(data).findAll(
            'input',
            {
                'type' : 'text',
                'name' : 'bin',
                'class' : 7
            }
        )
    )

    # ATM: it exists only one type of grid
    assert(len(bins) == 21)

    projections = {
        '-1,1' : bins[7 : 14],
        '1,1' : bins[ : 7],
        '0,-1' : bins[14 : ]
    }

    projections['1,1'].reverse()
    return projections

def display_mojette_grid(bins):
    """Display one type of mojette grid (the only one ATM available on the website)"""
    print '''
      |%d|
    |%d|%d|%d|
  |%d|%d|%d|%d|%d|
|%d|%d|%d|%d|%d|%d|%d|
  |%d|%d|%d|%d|%d|
    |%d|%d|%d|''' % tuple(bins)

# thx baaabz
def create_int_constrainted(name, solver, A, B, C):
    """Each pixel must be in [0 - 9], but you must fill the
    grid with only 3 digit among the range"""
    x = Int(name)
    solver.add(Or(x == A, x == B, x == C))
    return x

def solve_mojette_grid(projections):
    """Solve the grid thanks to z3py
    A bit of terminology:
        - The grid is composed of 24 pixels
        - A projection is composed of bins
        - Each projection is identified by an angle (p, q)"""

    s = Solver()

    # This is the only 3 values we'll use to fill the grid
    A, B, C = Ints('A B C')
    s.add(A >= 0, A <= 9, B >= 0, B <= 9, C >= 0, C <= 9)
    s.add(Distinct(A, B, C))
   
    # Little schema of the pixel indexes:
    #         |00|
    #      |01|02|03|
    #    |04|05|06|07|08|
    # |09|10|11|12|13|14|15|
    #    |16|17|18|19|20|
    #      |21|22|23|
    pixels = [create_int_constrainted('b%d' % i, s, A, B, C) for i in range(24)]

    projections_info = {
        '-1,1' : [
            # indexes of the pixels constrained by the first projection: -1,1
            [0, 3, 8, 15],
            [2, 7, 14],
            [1, 6, 13, 20],
            [5, 12, 19],
            [4, 11, 18, 23],
            [10, 17, 22],
            [9, 16, 21]
        ],

        '0,-1' : [
            # indexes of the pixels constrained by the second projection: 1,0
            [9],
            [16, 10, 4],
            [21, 17, 11, 5, 1],
            [22, 18, 12, 6, 2, 0],
            [23, 19, 13, 7, 3],
            [20, 14, 8],
            [15]
        ],

        '1,1' : [
            # indexes of the pixels constrained by the third projection: -1,1
            [0, 1, 4, 9],
            [2, 5, 10],
            [3, 6, 11, 16],
            [7, 12, 17],
            [8, 13, 18, 21],
            [14, 19, 22],
            [15, 20, 23]
        ]
    }

    for projection_angle, pixels_constrained in projections_info.iteritems():
        idx_projection = 0
        for pixels_idx in pixels_constrained:
            pixels_values = map(lambda pixel_idx: pixels[pixel_idx], pixels_idx)
            s.add(Sum(pixels_values) == projections[projection_angle][idx_projection])
            idx_projection += 1

    if s.check() == unsat:
        raise Exception('The model is not sat, i guess something went wrong.')

    m = s.model()
    return [m[pixel].as_long() for pixel in pixels]

def main(argc, argv):
    print 'Getting the projections from the website..'
    p = get_the_grid_of_the_day()
    print 'Got it, %r' % p

    print 'Now lets move on serious business aka solving..'
    r = solve_mojette_grid(p)

    print 'Alright done, displaying the grid filled..'
    display_mojette_grid(r)
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))