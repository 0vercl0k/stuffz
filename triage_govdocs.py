#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    triage_govdocs.py - Triage all the files found in the govdocs zip files
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
import zipfile
import os

# http://downloads.digitalcorpora.org/corpora/files/govdocs1/zipfiles/

def main(argc, argv):
    if argc != 3:
        print './%s <base dir> <base dir out>' % argv[0]
        return 0

    base = argv[1]
    base_out = argv[2]
    if not os.path.isdir(base):
        print base, 'needs to be a folder'
        return 0

    if not os.path.isdir(base_out):
        print 'Creating', base_out
        os.mkdir(base_out)

    for file_ in os.listdir(base):
        if not file_.endswith('.zip'):
            continue
        file_ = os.path.join(base, file_)
        with zipfile.ZipFile(file_) as z:
            print '[*] Handling', file_
            for filepath in z.namelist():
                _, filename = os.path.split(filepath)
                if '.' not in filename:
                    continue
                _, ext = os.path.splitext(filename)
                folderout = os.path.join(base_out, ext)
                if not os.path.isdir(folderout):
                    print '[*] Creating', folderout, '\r',
                    os.mkdir(folderout)
                fileout = os.path.join(folderout, filename)
                if os.path.isfile(fileout):
                    continue
                print '[*] Extracting', filename, 'to', folderout, '\r',
                with open(fileout, 'wb') as fout:
                    fout.write(z.read(filepath))

    print '[+] Done!'
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))