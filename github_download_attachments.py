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
from bs4 import BeautifulSoup

class DownloadFileWorker(object):
    def __init__(self, where):
        self.where = where

    def __call__(self, url):
        requests.packages.urllib3.disable_warnings()
        soup = BeautifulSoup(requests.get(url).content)
        links = soup.find_all('a')
        n_files = 0
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
                data = requests.get(href, timeout = 20, verify = False).content
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
            n_files += 1
        return True, n_files, url

def main(argc, argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--project-name', required = True, help = 'user/project-name.')
    parser.add_argument('--out', required = True, help = 'Directory where files will get downloaded.')
    args = parser.parse_args()
    n_files, n_issues = 0, 0
    for i in range(100000):
        url = 'https://github.com/%s/issues' % args.project_name
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
            if not li.attrs['id'].startswith('issue'):
                continue
            bug_urls.append('https://github.com%s' % li.div.a.attrs['href'])

        if len(bug_urls) == 0:
            break

        pool = multiprocessing.Pool(processes = multiprocessing.cpu_count())
        worker = DownloadFileWorker(args.out)
        for success, n, url in pool.imap_unordered(worker, bug_urls):
            n_issues += 1
            if success:
                n_files += n
                print '[*] Downloaded', n_files, 'files (queried', n_issues, 'issues from', i, 'pages)\r',

        pool.close()
        pool.join()

    print '[+] Done.'

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
