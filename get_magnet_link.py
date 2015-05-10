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
import re
import ctypes
import getpass
import subtitle
import requests
# https://bitbucket.org/blueluna/transmissionrpc
import transmissionrpc
from torrent_config import *
from bs4 import BeautifulSoup

def look_for_magnet_in_eztv(full_title):
    '''Look for a magnet link @ EZTV for the episode you are looking for'''
    url = "https://eztv.ch/search/"
    # Normalize the full_title, EZTV doesn't use '.' as a separator, but I do
    # Let's just replace them
    payload = {
        'SearchString1': full_title.replace('.', ' '),
        'SearchString': '',
        'search': 'Search'
    }

    req = requests.post(url, data = payload, timeout = 5, verify = False)
    link_title_release, link_magnet = BeautifulSoup(req.content).find_all('a', class_ = lambda x: x in ['epinfo', 'magnet'])[:2]
    assert(link_title_release.get('class') == ['epinfo'] and link_magnet.get('class') == ['magnet'])
    return link_title_release.get_text().replace(' ', '.'), link_magnet.get('href')

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

    full_title = argv[1]
    release_name, magnet_link = look_for_magnet_in_eztv(full_title)
    print release_name
    copy_into_clipboard(magnet_link)
    if raw_input('>> Do you want to transmission-remote the link to your server? [y/n]\n').lower() == 'y':
        server = raw_input('>>> Server?\n') if PREFERED_SERVER == '' else PREFERED_SERVER
        user = raw_input('>>> Username?\n') if PREFERED_USER == '' else PREFERED_USER
        pwd = getpass.getpass()
        tc = transmissionrpc.Client(address = server, user = user, password = pwd)
        print tc.add_torrent(magnet_link)

    if raw_input('>> Do you want to fetch the subs? [y/n]\n').lower() == 'y':
        subtitle.get_subtitle(release_name, 'D:\\')
    
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
