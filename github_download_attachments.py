#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    github_download_attachments.py - Download attachments of a github bug
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
import requests
import hashlib
import multiprocessing
import argparse
import ssl
from bs4 import BeautifulSoup

class DownloadFileWorker(object):
    def __init__(self, where):
        self.where = where

    def __call__(self, url):
        # http://thomas-cokelaer.info/blog/2016/01/python-certificate-verified-failed/
        #                                   ¯\_(ツ)_/¯
        ssl._create_default_https_context = ssl._create_unverified_context
        soup = BeautifulSoup(requests.get(url).content)
        links = soup.find_all('a')
        for link in links:
            if len(link.attrs.keys()) != 1 or 'href' not in link.attrs:
                continue
            href = link.attrs['href']
            # Excluse anything else that is not http
            if not href.startswith('http'):
                continue

            # Exclude references to pull requests
            if href.startswith('https://github.com') and '/pull/' in href:
                continue

            try:
                data = requests.get(href, timeout = 20).content
            except Exception, e:
                print '  /!\\ Exception:', e, 'with', href
                continue

            sha1sum = hashlib.sha1(data).hexdigest()
            filepath = os.path.join(self.where, sha1sum)

            # Don't download an already-downloaded file
            if os.path.isfile(filepath):
                continue

            with open(filepath, 'wb') as f:
                f.write(data)
        return True, 'ok', url

def main(argc, argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--project-name', required = True, help = 'user/project-name.')
    parser.add_argument('--out', required = True, help = 'Directory where files will get downloaded.')
    args = parser.parse_args()
    for i in range(100000):
        url = 'https://github.com/%s/issues' % args.project_name
        print '[*] Querying page', i, '..'
        soup = BeautifulSoup(
            requests.get(
                url, params = {'page' : i, 'q' : 'is:issue'}
            ).content
        )
        lis = soup.find_all('li')

        bug_urls = []
        for li in lis:
            if 'id' not in li.attrs:
                continue
            if li.attrs['id'].startswith('issue'):
                bug_urls.append('https://github.com%s' % li.div.a.attrs['href'])

        if len(bug_urls) == 0:
            break

        print '[+] Found', len(bug_urls), 'issues'
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
