#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    idapy_color_diff_from_jsons.py - Color the differences between two execution JSON reports
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

import json
import idc
import idaapi
from collections import defaultdict

def color(ea, nbins, c = 0xFF0000):
    '''Color 'nbins' instructions starting from ea'''
    for _ in range(nbins):
        idaapi.del_item_color(ea)
        idaapi.set_item_color(ea, c)
        ea += idc.ItemSize(ea)

def main():
    report = json.load(open(r'D:\Codes\pin-code-coverage-measure\vlc_1.json'))
    l1 = report['basic_blocks_info']['list']
    report = json.load(open(r'D:\Codes\pin-code-coverage-measure\vlc_2.json'))
    l2 = report['basic_blocks_info']['list']

    addresses_l1 = set(r['address'] for r in l1)    
    addresses_l2 = set(r['address'] for r in l2)
    dic_l2 = dict((k['address'], k['nbins']) for k in l2)

    diff = addresses_l2 - addresses_l1
    print '%d bbls in the first execution' % len(addresses_l1)
    print '%d bbls in the second execution' % len(addresses_l2)
    print 'Differences between the two executions: %d bbls' % len(diff)
    
    assert(len(addresses_l1) < len(addresses_l2))

    funcs = defaultdict(list)
    for i in diff:
        try:
            color(i, dic_l2[i])
            funcs[get_func(i).startEA].append(i)
        except Exception, e:
            print 'fail %s' % str(e)

    print 'A total of %d different sub:' % len(funcs)
    for s in funcs.keys():
        print '%x' % s

    print 'done'    
    return 1

if __name__ == '__main__':
    main()