#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    get_magnet_link.py - 
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
import eztv
import re
import ctypes
import subtitle

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
    if argc != 2:
        print './get_magnet_link My.Serie.S01E02'
        return 0

    show_title, _, episode_info = map(lambda x: x.replace('.', ' '), argv[1].rpartition('.'))
    season, episode = map(lambda x: int(x, 10), re.match(r'S(\d+)E(\d+)', episode_info).groups()) 
    e = eztv.EztvAPI().tv_show(show_title).episode(season, episode)
    print e
    copy_into_clipboard(e)
    raw_input('>> Ready to fetch the subs?')
    subtitle.get_subtitle(argv[1], 'D:\\')
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
