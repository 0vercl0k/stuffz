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
        '1,1' : bins[7 : 14],
        '-1,1' : bins[ : 7],
        '1,0' : bins[14 : ]
    }

    projections['-1,1'].reverse()
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

def solve_mojette_grid(projections):
    """Solve the grid thanks to z3py"""
    # each bin is numeroted from 0 to 23 starting at the left bottom
    bins = [Int('b%d' % i) for i in range(24)]
    s = Solver()

    # each bin must be in the range [0 - 9]
    for bin in bins:
        s.add(bin < 10, bin >= 0)

    # Little schema of the bins indexes:
    #         |00|
    #      |01|02|03|
    #    |04|05|06|07|08|
    # |09|10|11|12|13|14|15|
    #    |16|17|18|19|20|
    #      |21|22|23|

    idx = {
        '1,1' : [
            # indexes of the bins constrainted by the first projection: 1,1
            [0, 3, 8, 15],
            [2, 7, 14],
            [1, 6, 13, 20],
            [5, 12, 19],
            [4, 11, 18, 23],
            [10, 17, 22],
            [9, 16, 21]
        ],

        '1,0' : [
            # indexes of the bins constrainted by the second projection: 1,0
            [9],
            [16, 10, 4],
            [21, 17, 11, 5, 1],
            [22, 18, 12, 6, 2, 0],
            [23, 19, 13, 7, 3],
            [20, 14, 8],
            [15]
        ],

        '-1,1' : [
            # indexes of the bins constrainted by the third projection: -1,1
            [0, 1, 4, 9],
            [2, 5, 10],
            [3, 6, 11, 16],
            [7, 12, 17],
            [8, 13, 18, 21],
            [14, 19, 22],
            [15, 20, 23]
        ]
    }

    for projection_angle, bins_constraints in idx.iteritems():
        idx_projection = 0
        for bins_idx in bins_constraints:
            bins_csts = map(lambda bin_idx: bins[bin_idx], bins_idx)
            if len(bins_csts) > 1:
                s.add(reduce(operator.add, bins_csts) == projections[projection_angle][idx_projection])
            else:
                s.add(bins_csts[0] == projections[projection_angle][idx_projection])

            idx_projection += 1

    if s.check() == unsat:
        raise Exception('The model is not sat, i guess something went wrong.')

    m = s.model()
    return [m[bin].as_long() for bin in bins]

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