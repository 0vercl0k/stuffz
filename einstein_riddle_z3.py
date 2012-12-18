#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    einstein_riddle_z3.py - Solve the Einstein's riddle to step into the 2% :)).
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
from z3 import *

# Thx to alpounet for the idea!

def solve_einstein_stuff():
    """Solve this stuff: http://www.davar.net/MATH/PROBLEMS/EINSTEIN.HTM"""
    def column(matrix, i):
        """Get the column i of matrix"""
        return [matrix[j][i] for j in range(5)]

    def instanciate_int_constrained(name, s):
        x = Int(name)
        # Each int represent an index in p[name]
        s.add(x >= 0, x <= 4)
        return x

    p = {
        'color' : ('Yellow', 'Green', 'Blue', 'Red', 'White'),
        'nationality' : ('Brit', 'Dane', 'German', 'Norwegian', 'Swede'),
        'beverage': ('Beer', 'Coffee', 'Milk', 'Tea', 'Water'),
        'smoke' : ('Blue Master', 'Dunhill', 'Pall Mall', 'Prince', 'Blend'),
        'pet' : ('Cat', 'Bird', 'Dog', 'Fish', 'Horse')
    }

    s = Solver()
    color, nationality, beverage, smoke, pet = range(5)
    houses = [[instanciate_int_constrained('%s%d' % (prop, n), s) for prop in p.keys()] for n in range(5)]

    for i in range(5):
        # Each column must have different values
        s.add(Distinct(column(houses, i)))

    # Time to feed the solver with hints
    # 1. The Brit lives in a red house.
    s.add(Or([And(houses[i][nationality] == p['nationality'].index('Brit'), houses[i][color] == p['color'].index('Red')) for i in range(5)]))

    # 2. The Swede keeps dogs as pets.
    s.add(Or([And(houses[i][nationality] == p['nationality'].index('Swede'), houses[i][pet] == p['pet'].index('Dog')) for i in range(5)]))

    # 3. The Dane drinks tea.
    s.add(Or([And(houses[i][nationality] == p['nationality'].index('Dane'), houses[i][beverage] == p['beverage'].index('Tea')) for i in range(5)]))

    # 4. The green house is on the left of the white house (next to it).
    s.add(Or([And(houses[i][color] == p['color'].index('Green'), houses[i + 1][color] == p['color'].index('White')) for i in range(4)]))

    # 5. The green house owner drinks coffee.
    s.add(Or([And(houses[i][color] == p['color'].index('Green'), houses[i][beverage] == p['beverage'].index('Coffee')) for i in range(5)]))

    # 6. The person who smokes Pall Mall rears birds.
    s.add(Or([And(houses[i][smoke] == p['smoke'].index('Pall Mall'), houses[i][pet] == p['pet'].index('Bird')) for i in range(5)]))
    
    # 7. The owner of the yellow house smokes Dunhill.
    s.add(Or([And(houses[i][color] == p['color'].index('Yellow'), houses[i][smoke] == p['smoke'].index('Dunhill')) for i in range(5)]))
    
    # 8. The man living in the house right in the center drinks milk.
    s.add(houses[2][beverage] == p['beverage'].index('Milk'))

    # 9. The Norwegian lives in the first house.
    s.add(houses[0][nationality] == p['nationality'].index('Norwegian'))

    # 10. The man who smokes blend lives next to the one who keeps cats.
    s.add(Or(
        And(houses[0][smoke] == p['smoke'].index('Blend'), houses[1][pet] == p['pet'].index('Cat')),
        And(houses[1][smoke] == p['smoke'].index('Blend'), Or(houses[0][pet] == p['pet'].index('Cat'), houses[2][pet] == p['pet'].index('Cat'))),
        And(houses[2][smoke] == p['smoke'].index('Blend'), Or(houses[1][pet] == p['pet'].index('Cat'), houses[3][pet] == p['pet'].index('Cat'))),
        And(houses[3][smoke] == p['smoke'].index('Blend'), Or(houses[2][pet] == p['pet'].index('Cat'), houses[4][pet] == p['pet'].index('Cat'))),
        And(houses[4][smoke] == p['smoke'].index('Blend'), houses[3][pet] == p['pet'].index('Cat')),
    ))

    # 11. The man who keeps horses lives next to the man who smokes Dunhill.
    s.add(
        Or(
            And(houses[0][pet] == p['pet'].index('Horse'), houses[1][smoke] == p['smoke'].index('Dunhill')),
            And(houses[1][pet] == p['pet'].index('Horse'), Or(houses[0][smoke] == p['smoke'].index('Dunhill'), houses[2][smoke] == p['smoke'].index('Dunhill'))),
            And(houses[2][pet] == p['pet'].index('Horse'), Or(houses[1][smoke] == p['smoke'].index('Dunhill'), houses[3][smoke] == p['smoke'].index('Dunhill'))),
            And(houses[3][pet] == p['pet'].index('Horse'), Or(houses[2][smoke] == p['smoke'].index('Dunhill'), houses[4][smoke] == p['smoke'].index('Dunhill'))),
            And(houses[4][pet] == p['pet'].index('Horse'), houses[3][smoke] == p['smoke'].index('Dunhill'))
        )
    )

    # 12. The owner who smokes Blue Master drinks beer.
    s.add(Or([And(houses[i][smoke] == p['smoke'].index('Blue Master'), houses[i][beverage] == p['beverage'].index('Beer')) for i in range(5)]))
    
    # 13. The German smokes Prince.
    s.add(Or([And(houses[i][nationality] == p['nationality'].index('German'), houses[i][smoke] == p['smoke'].index('Prince')) for i in range(5)]))
    
    # 14. The Norwegian lives next to the blue house.
    s.add(
        Or
        (
            And(houses[0][nationality] == p['nationality'].index('Norwegian'), houses[1][color] == p['color'].index('Blue')),
            And(houses[0][nationality] == p['nationality'].index('Norwegian'), Or(houses[0][color] == p['color'].index('Blue'), houses[2][color] == p['color'].index('Blue'))),
            And(houses[0][nationality] == p['nationality'].index('Norwegian'), Or(houses[1][color] == p['color'].index('Blue'), houses[3][color] == p['color'].index('Blue'))),
            And(houses[0][nationality] == p['nationality'].index('Norwegian'), Or(houses[2][color] == p['color'].index('Blue'), houses[4][color] == p['color'].index('Blue'))),
            And(houses[4][nationality] == p['nationality'].index('Norwegian'), houses[3][color] == p['color'].index('Blue'))
        )
    )

    # 15. The man who smokes blend has a neighbor who drinks water.
    s.add(
        Or
        (
            And(houses[0][smoke] == p['smoke'].index('Blend'), houses[1][beverage] == p['beverage'].index('Water')),
            And(houses[1][smoke] == p['smoke'].index('Blend'), Or(houses[0][beverage] == p['beverage'].index('Water'), houses[2][beverage] == p['beverage'].index('Water'))),
            And(houses[2][smoke] == p['smoke'].index('Blend'), Or(houses[1][beverage] == p['beverage'].index('Water'), houses[3][beverage] == p['beverage'].index('Water'))),
            And(houses[3][smoke] == p['smoke'].index('Blend'), Or(houses[2][beverage] == p['beverage'].index('Water'), houses[4][beverage] == p['beverage'].index('Water'))),
            And(houses[4][smoke] == p['smoke'].index('Blend'), houses[3][beverage] == p['beverage'].index('Water'))
        )
    )

    if s.check() == unsat:
        raise Exception('Hmm the system does not seem solvable, I guess one of the constraint is wrong.')

    m = s.model()
    solution = [[m[case].as_long() for case in line] for line in houses]

    for i in range(5):
        print 'Color: %s, Nationality: %s, Beverage: %s, Smoke: %s, Pet: %s' % (
            p['color'][solution[i][color]],
            p['nationality'][solution[i][nationality]],
            p['beverage'][solution[i][beverage]],
            p['smoke'][solution[i][smoke]],
            p['pet'][solution[i][pet]]
        )

def main(argc, argv):
    solve_einstein_stuff()
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))