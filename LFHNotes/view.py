#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    view.py - view script abstract
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
import time
import json
import glob
import os

class Chunk(object):
    def __init__(self, address, state, content = 'AA BB CC DD EE FF HH JJ'):
        self.address = address
        assert(state in ['free', 'busy'])
        self.state = state
        self.content = content

    def __str__(self):
        return '<div class="col %s"><span class="address">%.16x</span> <hr> <span class="hexdump"> %s </span></div>' % (
            self.state,
            self.address,
            self.content
        )

class Bucket(object):
    def __init__(self, address, size):
        self.address = address
        self.size = size
        self.chunks = []

    def __str__(self):
        s = '<div class="container"><b> Bucket @%.16x size %d </b><div class="row">' % (self.address, self.size)
        for chunk in self.chunks:
            s += str(chunk)
        s += "</div></div>"
        return s

def parse_json(path, address):
    datas = json.load(open(path))
    LFHHeap = filter(
        lambda x : x['address'] == address,
        datas['LFHs']
    )
    
    if len(LFHHeap) == 0:
        return

    print path
    b = []

    for bucket in LFHHeap[0]['buckets']:
        current_bucket = Bucket(0, bucket['size'])
        b.append(current_bucket)
        for chunk in bucket['chunks']:
            current_bucket.chunks.append(Chunk(chunk['address'], chunk['state'], chunk['content']))

    _, tail = os.path.split(path)
    _, n, _ = tail.split('.')
    with open(r'htmls\testview.%s.html' % n, 'w') as f:
        f.write('''<html>
<head>
    <title></title>
    <link rel="stylesheet" href="..\\style.css">
</head>
<body>
''')
    
        for bucket in b:
            f.write(str(bucket))

        f.write('''</body>
</html>''')

# 00CD0000

def main(argc, argv):
    for path in glob.glob(r'jsons\*'):
        parse_json(path, 0x00D70000)
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
