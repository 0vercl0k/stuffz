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
import requests
import time
import os
import winsound
from subprocess import check_output
from bs4 import BeautifulSoup

def gocr_file(inf):
    '''using convert.exe from ImageMagick, and gocr.exe to extract the info'''
    return check_output('convert.exe "%s" pnm:- | gocr049.exe -' % inf, shell = True)

def main(argc, argv):
    if argc != 2:
        print './colissimo.py <ID>'
        return 0

    url_base = 'http://www.colissimo.fr/portail_colissimo/'
    data = None

    while True:
        r = requests.post(
            '%ssuivre.do?language=fr_FR' % url_base,
            { 'parcelnumber' : argv[1] }
        )
        soup = BeautifulSoup(r.text)
        x = soup.find(id = 'resultatSuivreDiv')
        error = x.find('div', **{'class' : 'error'})
        if error != None:
            info = error.text.strip()
        else:
            info = []
            for i in ['Date', 'Libelle', 'site']:
                img_url = url_base + x.find('td', headers = i).img['src']
                with open('tmp.png', 'wb') as f:
                    f.write(requests.get(img_url, cookies = r.cookies).content)
                c = gocr_file('tmp.png').strip().replace('\r\n', ' ')
                if i == 'Date':
                    c = c.replace('I', '/').replace('O', '0')
                info.append('%s: %s' % (i, c))
                os.remove('tmp.png')

            info = ', '.join(info)

        if data == None:
            data = info
            print 'Init: "%s"' % data
        else:
            if info != data:
                data = info
                print 'New change: %s' % data
                winsound.PlaySound(r'C:\Windows\Media\Afternoon\Windows Logon Sound.wav', winsound.SND_FILENAME)

        time.sleep(15 * 60)
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))