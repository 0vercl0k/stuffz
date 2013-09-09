#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    colissimo.py - Track a parcel with colissimo.fr
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
import urllib
import time
import winsound
from bs4 import BeautifulSoup

def main(argc, argv):
    if argc != 2:
        print './colissimo.py <ID>'
        return 0

    data = None
    while True:
        soup = BeautifulSoup(
            urllib2.urlopen(
                urllib2.Request(
                    'http://www.colissimo.fr/portail_colissimo/suivre.do?language=fr_FR',
                    urllib.urlencode({ 'parcelnumber' : argv[1] })
                )
            ).read()
        )

        x = soup.find(id = 'resultatSuivreDiv').div.text.strip()
        if data == None:
            print 'Init: "%s"' % x
            data = x
        else:
            if x != data:
                print 'New change: %s' % x
                data = x
                winsound.PlaySound(r'C:\Windows\Media\Afternoon\Windows Logon Sound.wav', winsound.SND_FILENAME)

        time.sleep(15 * 60)
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))