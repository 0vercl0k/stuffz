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
import transmissionrpc
from torrent_config import *
from bs4 import BeautifulSoup

class Episode(object):
    def __init__(self, release_name, magnet_link):
        self.release_name = release_name.get_text().replace(' ', '.')
        self.magnet_link = magnet_link.get('href')

def look_for_magnet_in_eztv(full_title):
    '''Look for a magnet link @ EZTV for the episode you are looking for'''
    url = 'https://eztv.ag/search/'
    # Normalize the full_title, EZTV doesn't use '.' as a separator, but I do
    # Let's just replace them
    payload = {
        'SearchString1': full_title.replace('.', ' '),
        'SearchString': '',
        'search': 'Search'
    }

    req = requests.post(url, data = payload, timeout = 5, verify = False)
    for tr in BeautifulSoup(req.content).find_all('tr', class_ = 'forum_header_border'):
        links = tr.find_all('a', class_ = lambda x: x in ['epinfo', 'magnet'])
        if len(links) != 2:
            continue
        title_release, magnet = links
        assert(title_release.get('class') == ['epinfo'] and magnet.get('class') == ['magnet'])
        yield Episode(title_release, magnet)     
        
    raise StopIteration

def main(argc, argv):
    if argc != 2:
        print './get_magnet_link My.Serie.S01E02'
        return 0

    full_title = argv[1]
    for episode in look_for_magnet_in_eztv(full_title):
        print episode.release_name
        if raw_input('>> Do you want to transmission-remote the link to your server? [y/n]\n').lower() == 'y':
            server = raw_input('>>> Server?\n') if PREFERED_SERVER == '' else PREFERED_SERVER
            user = raw_input('>>> Username?\n') if PREFERED_USER == '' else PREFERED_USER
            pwd = getpass.getpass()
            tc = transmissionrpc.Client(address = server, user = user, password = pwd)
            print tc.add_torrent(episode.magnet_link)

            if raw_input('>> Do you want to fetch the subs? [y/n]\n').lower() == 'y':
                subtitle.get_subtitle(episode.release_name, 'D:\\')

            break
    
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
