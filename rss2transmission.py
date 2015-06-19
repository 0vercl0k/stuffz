#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    rss2transmission-daemon.py - Listen to a RSS-torrent feed (ShowRSS) & adds
#    all the things in transmission 
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
import datetime
import sqlite3
import time
import xml.etree.ElementTree as ET
import transmissionrpc
import getpass
import urllib2
import re
from torrent_config import *

class Episode(object):
    def __init__(self, name):
        showrss_regex = '([0-9]{1,2})x([0-9]{1,2})'
        self.name = name
        s = self.name.split()
        tmp = []
        for x in s:
            if re.search(showrss_regex, x) is None:
                tmp.append(x.lower())
            else:
                break
        self.name = ' '.join(tmp)
        r = re.search(showrss_regex, name)
        if r != None and len(r.groups()) == 2:
            self.season = int(r.group(1), 10)
            self.episode = int(r.group(2), 10)
        else:
            raise RuntimeError('Cannot extract the episode & season id from %s' % name)

class DatabaseManager(object):
    def __init__(self, databasepath):
        self.co = sqlite3.connect(databasepath)
        self.co.execute('''
            CREATE TABLE 
            IF NOT EXISTS "ShowRSS" 
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                season INTEGER,
                episode INTEGER,
                date INTEGER
            )'''
        )
        self.co.commit()

    def __del__(self):
        self.co.commit()
        self.co.close()

    def add(self, s):
        e = Episode(s)
        self.co.execute(
            'INSERT INTO "ShowRSS" VALUES(NULL, ?, ?, ?, ?)', (
                e.name, e.season, e.episode, time.time()
            )
        )
        self.co.commit()

    def exists(self, s):
        e = Episode(s)
        c = self.co.cursor()
        c.execute('SELECT count(*) FROM "ShowRSS" WHERE name = ? AND season = ? AND episode = ?', (e.name, e.season, e.episode))
        row = c.fetchone()
        if row[0] == 0:
            return False
        return True

class DownloadHistory(object):
    def __init__(self, log_file):
        self.log = open(log_file, 'a')
        self.header_put = False

    def __write_header(self):
        self.log.write('''
---- LOG : %s -----
''' % datetime.datetime.fromtimestamp(time.time()).strftime('%d/%m/%Y %H:%M'))

    def add(self, name):
        if self.header_put == False:
            self.__write_header()
            self.header_put = True

        self.log.write('Downloaded : %s\n' % name)

    def __del__(self):
        try:
            self.log.close()
        except:
            pass

def main(argc, argv):
    dbmgr = DatabaseManager('./rss2transmission.sqlite3.db')
    downhist = DownloadHistory('./.logz_dl')
    dom = ET.fromstring(
        urllib2.urlopen(PREFERED_RSS_FEED).read()
    )
    server, user, pwd, tc = None, None, None, None
    for item in dom.findall('channel/item'):
        name = item.find('title').text.encode('ascii', errors = 'ignore')
        if not dbmgr.exists(name):
            print '> Adding %s..' % name
            if server is None:
                server = raw_input('>> Server?\n') if PREFERED_SERVER == '' else PREFERED_SERVER
            if user is None:
                user = raw_input('>> Username?\n') if PREFERED_USER == '' else PREFERED_USER
            if pwd is None:
                pwd = getpass.getpass() if PREFERED_PWD == '' else PREFERED_PWD

            if tc is None:
                tc = transmissionrpc.Client(address = server, user = user, password = pwd)

            try:
                print tc.add_torrent(item.find('link').text)
            except transmissionrpc.TransmissionError, e:
                print str(e)
                continue

            dbmgr.add(name)
            downhist.add(name)
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))