#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    download_electro_playlists_kix.py - Don't let the bass get ya!
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
import urllib2
import re
import json
import os
import sys
from bs4 import *
from urllib import unquote
from urlparse import urlparse

def download(directory, filename, link):
    """Download a file and save it on your filesystem"""
    if os.path.exists(directory) == False:
        os.mkdir(directory)

    where = os.path.join(directory, filename)
    # check if the file doesn't already exist, if it is save some bandwidth & skip!
    if os.path.exists(where) == True:
        return

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    print '> Starting to download "%s"..' % filename
    try:
        with open(where, 'wb') as f:
            r = opener.open(link)
            while True:
                c = r.read(8192)
                if not c:
                    break
                sys.stdout.write('.')
                f.write(c)
    except Exception, e:
        print str(e)
        return
    print '\n>> Downloaded', filename, 'in ', where

def main(argc, argv):
    if argc != 3:
        print './rip_electro_playlists <link> <where>'
        return -1

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    soup = BeautifulSoup(opener.open(argv[1]).read())
    for link in soup.find_all('script', type = 'text/javascript', text = re.compile('^AudioPlayer.embed')):
        _, j = link.text.split(' ', 1)
        link = unquote(
            json.loads(
                j.replace('soundFile', '"soundFile"').replace(');', '')
            )['soundFile']
        )
        path = urlparse(link).path.encode('ascii', 'ignore')
        filename = path[path.rfind('/') + 1 :]
        download(argv[2], filename, link)
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))