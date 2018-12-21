#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    normalization.py
#    Copyright (C) 2017 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k
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
import os
from hashlib import sha1

def main(argc, argv):
    if argc != 3:
        print 'normalization.py <dir> <extension without dot>'
        return 0

    dirin = argv[1]
    ext = argv[2]
    for i in os.listdir(dirin):
        filein = os.path.join(dirin, i)
        with open(filein, 'rb') as f:
            data = f.read()
        h = sha1(data).hexdigest()
        fileout = os.path.join(dirin, '%s.%s' % (h, ext))
        if os.path.isfile(fileout):
            if filein != fileout:
                print 'Removing ', filein, 'dupe of', fileout
                os.remove(filein)
        else:
            print 'Renaming', filein, 'to', fileout
            os.rename(filein, fileout)

    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))