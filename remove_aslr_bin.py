#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    remove_aslr_bin.py - This script simply unset/set the IMAGE_DLL_CHARACTERISTICS_DYNAMIC_BASE flag in the PE header.
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
import pefile

IMAGE_DLL_CHARACTERISTICS_DYNAMIC_BASE  = 0x40

def main(argc, argv):
    if argc != 2:
        print 'Usage: ./remove_aslr_bin.py <bin>'
        return 0

    pe = pefile.PE(argv[1])

    if (pe.OPTIONAL_HEADER.DllCharacteristics & IMAGE_DLL_CHARACTERISTICS_DYNAMIC_BASE) != 0:
        print 'Disabling the ASLR..'
        pe.OPTIONAL_HEADER.DllCharacteristics &= ~IMAGE_DLL_CHARACTERISTICS_DYNAMIC_BASE
    else:
        print 'Enabling the ASLR..'
        pe.OPTIONAL_HEADER.DllCharacteristics |= IMAGE_DLL_CHARACTERISTICS_DYNAMIC_BASE

    pe.write(filename = '%s.patched.exe' % argv[1])
    print 'Done.'
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))