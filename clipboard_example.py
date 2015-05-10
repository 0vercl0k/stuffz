#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    clipboard_example.py -
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

def copy_into_clipboard(data):
    strcpy = ctypes.cdll.msvcrt.strcpy
    OpenClipboard = ctypes.windll.user32.OpenClipboard
    SetClipboardData = ctypes.windll.user32.SetClipboardData
    EmptyClipboard = ctypes.windll.user32.EmptyClipboard
    CloseClipboard = ctypes.windll.user32.CloseClipboard
    GlobalAlloc = ctypes.windll.kernel32.GlobalAlloc
    GlobalLock = ctypes.windll.kernel32.GlobalLock
    GlobalUnlock = ctypes.windll.kernel32.GlobalUnlock
    GMEM_DDESHARE = 0x2000 

    OpenClipboard(None)
    EmptyClipboard()
    hMem = GlobalAlloc(GMEM_DDESHARE, len(data) + 1)
    hData = GlobalLock(hMem)
    strcpy(ctypes.c_char_p(hData), data)
    GlobalUnlock(hMem)
    SetClipboardData(1, hMem)
    CloseClipboard()

def main(argc, argv):
    copy_into_clipboard('yoyoyoy')
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
