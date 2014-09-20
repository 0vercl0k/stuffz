#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    bf_with_lambdas_cleaned.py
#    Copyright (C) 2014 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k
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
    tab0 = [1375, 1368, 1294, 1293, 1373, 1295, 1290, 1373, 1290, 1293, 1280, 1368, 1368,1294, 1293, 1368, 1372, 1292, 1290, 1291, 1371, 1375, 1280, 1372, 1281, 1293,1373, 1371, 1354, 1370, 1356, 1354, 1355, 1370, 1357, 1357, 1302, 1366, 1303,1368, 1354, 1355, 1356, 1303, 1366, 1371]
    tab1 = [1373, 1281, 1288, 1373, 1290, 1294, 1375, 1371,1289, 1281, 1280, 1293, 1289, 1280, 1373, 1294, 1289, 1280, 1372, 1288, 1375,1375, 1289, 1373, 1290, 1281, 1294, 1302, 1372, 1355, 1366, 1372, 1302, 1360, 1368, 1354, 1364, 1370, 1371, 1365, 1362, 1368, 1352, 1374, 1365, 1302]

    func = (
        lambda g, c, d: 
        (
            lambda x: (
                x.__setitem__('$', ''.join([(x['chr'] if ('chr' in x) else chr)((x['_'] if ('_' in x) else x)) for x['_'] in (x['s'] if ('s' in x) else s)[::-1]])),
                x
            )[-1]
        )
        (
            (
                lambda x: 
                    (lambda f, x: f(f, x))
                (
                    (
                        lambda __, x: 
                        (
                            (lambda x: __(__, x))
                            (
                                # i += 1
                                (
                                    lambda x: (
                                        x.__setitem__('i', ((x['i'] if ('i' in x) else i) + 1)),
                                        x
                                    )[-1]
                                )
                                (
                                    # s += [c ^ l[i]]
                                    (
                                        lambda x: (
                                            x.__setitem__('s', (
                                                    (x['s'] if ('s' in x) else s) +
                                                    [((x['l'] if ('l' in x) else l)[(x['i'] if ('i' in x) else i)] ^ (x['c'] if ('c' in x) else c))]
                                                )
                                            ),
                                            x
                                        )[-1]
                                    )
                                    (x)
                                )
                            )
                            # if ((x['g'] % 4) and (x['i'] < len(l))) else x
                            if (((x['g'] if ('g' in x) else g) % 4) and ((x['i'] if ('i' in x) else i)< (x['len'] if ('len' in x) else len)((x['l'] if ('l' in x) else l))))
                            else x
                        )
                    ),
                    x
                )
            )
            # Returns { 'g':g, 'c':c, 'd':d, '!':zip(tab1, tab0), 'l':zip(tab1, tab0), l1':tab1, 'l0':tab0, 'i': 0, 'j': 1302, '!':0, 's':[] }
            (
                (
                    lambda x: (
                        x.__setitem__('!', []),
                        x.__setitem__('s', x['!']),
                        x
                    )[-1]
                )
                # Returns { 'g':g, 'c':c, 'd':d, '!':zip(tab1, tab0), 'l':zip(tab1, tab0), l1':tab1, 'l0':tab0, 'i': 0, 'j': 1302, '!':0}
                (
                    (
                        lambda x: (
                            x.__setitem__('!', ((x['d'] if ('d' in x) else d) ^ (x['d'] if ('d' in x) else d))),
                            x.__setitem__('i', x['!']),
                            x
                        )[-1]
                    )
                    # Returns { 'g' : g, 'c', 'd': d, '!':zip(tab1, tab0), 'l':zip(tab1, tab0), l1':tab1, 'l0':tab0, 'i': (1371, 1302), 'j': 1302}
                    (
                        (
                            lambda x: (
                                x.__setitem__('!', [(x['j'] if ('j' in x) else j) for x[ 'i'] in (x['zip'] if ('zip' in x) else zip)((x['l0'] if ('l0' in x) else l0), (x['l1'] if ('l1' in x) else l1)) for x['j'] in (x['i'] if ('i' in x) else i)]),
                                x.__setitem__('l', x['!']),
                                x
                            )[-1]
                        )
                        # Returns { 'g' : g, 'c', 'd': d, '!':tab1, 'l1':tab1, 'l0':tab0}
                        (
                            (
                                lambda x: (
                                    x.__setitem__('!', tab1),
                                    x.__setitem__('l1', x['!']),
                                    x
                                )[-1]
                            )
                            # Return { 'g' : g, 'c', 'd': d, '!' : tab0, 'l0':tab0}
                            (
                                (
                                    lambda x: (
                                        x.__setitem__('!', tab0),
                                        x.__setitem__('l0', x['!']),
                                        x
                                    )[-1]
                                )
                                ({ 'g': g, 'c': c, 'd': d, '$': None})
                            )
                        )
                    )
                )
            )
        )['$']
    )
    
    for i in range(0x1000):
        try:
            ret = func(1, i, 0)
            if 'quarks' in ret:
                print ret
        except:
            pass
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
