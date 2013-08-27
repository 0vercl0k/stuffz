#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    idapy_color_path_from_json.py - Color the path taken by the program from a JSON report
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

def color(ea, nbins, c = 0xFFFFFF):
    '''Color 'nbins' instructions starting from ea'''
    for _ in range(nbins):
        idaapi.del_item_color(ea)
        idaapi.set_item_color(ea, c)
        ea += idc.ItemSize(ea)

def main():
    report = json.load(open(r'D:\Codes\pin-code-coverage-measure\test.json'))
    for i in report['basic_blocks_info']['list']:
        print '%x' % i['address'],
        try:
            color(i['address'], i['nbins'])
            print 'ok'
        except:
            print 'fail'
    print 'done'    
    return 1

if __name__ == '__main__':
    main()