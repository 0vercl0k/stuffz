#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    sourceforge_download_attachments.py - Dump attachments of a sourceforge bug
#    tracker.
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
import os
import urllib2
import hashlib
import multiprocessing
import argparse
from bs4 import BeautifulSoup

class DownloadFileWorker(object):
    def __init__(self, where):
        self.where = where

    def __call__(self, url):
        try:
            soup = BeautifulSoup(urllib2.urlopen(url).read())
            attachments = soup.find_all(
                'div', attrs = {'class' : 'attachment_thumb'}
            )

            for attachment in attachments:
                attachment_url = 'https://sourceforge.net%s' % attachment.a.attrs['href']
                u = urllib2.urlopen(attachment_url, timeout = 20)
                # if it has a Content-Length header, then we check if
                # the file is too big or not
                if 'Content-Length' in u.headers and int(u.headers.getheader('Content-Length'), 10) >= (1024*1024):
                    continue

                data = u.read()
                sha1sum = hashlib.sha1(data).hexdigest()
                filepath = os.path.join(self.where, sha1sum)

                # Don't download an already-downloaded file
                if os.path.isfile(filepath):
                    continue

                with open(filepath, 'wb') as f:
                    f.write(data)
        except Exception, e:
            return False, str(e), url

        return True, 'ok', url

def main(argc, argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--project-name', required = True, help = 'The project name.')
    parser.add_argument('--out', required = True, help = 'Directory where files will get downloaded.')
    parser.add_argument('--limit', default = 1000, help = 'Number of bugs displayed per page.')
    args = parser.parse_args()
    for i in range(100000):
        url = 'https://sourceforge.net/p/%s/bugs/?limit=%d&page=%d' % (
            args.project_name, args.limit, i
        )
        print '[*] Querying', url, '..'
        soup = BeautifulSoup(urllib2.urlopen(url).read())
        trs = soup.find_all('tr')
        bug_urls = []
        for tr in trs:
            if 'class' not in tr.attrs:
                continue
            class_ = tr.attrs['class']
            if class_ == ['even', ''] or class_ == ['', '']:
                bug_urls.append('https://sourceforge.net%s' % tr.td.a.attrs['href'])

        if len(bug_urls) == 0:
            break

        pool = multiprocessing.Pool(processes = multiprocessing.cpu_count())
        worker = DownloadFileWorker(args.out)
        for success, _, url in pool.imap_unordered(worker, bug_urls):
            if success:
                print '  [+] Checked', url, '\r',

        pool.close()
        pool.join()

    print '[+] Done.'

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
