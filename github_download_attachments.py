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
import functools
from bs4 import BeautifulSoup

onemeg = 1024 * 1024

def download_file(where, issue_url):
    requests.packages.urllib3.disable_warnings()
    soup = BeautifulSoup(requests.get(issue_url).content)
    links = soup.find_all('a')
    n_files = 0
    for link in links:
        if len(link.attrs.keys()) != 1:
            continue

        href = link.attrs.get('href', '')
        # Exclude anything that is not http
        if not href.startswith('http'):
            continue

        # Exclude references to pull requests
        if href.startswith('https://github.com') and '/pull/' in href:
            continue

        try:
            r = requests.get(href, timeout = 20, verify = False)
            if int(r.headers.get('content-length', 0)) > onemeg:
                continue
            data = r.content
        except Exception, e:
            print >> sys.stderr, '  /!\\ Exception:', e, 'with', href
            continue

        if not 0 < len(data) <= onemeg:
            continue

        sha1sum = hashlib.sha1(data).hexdigest()
        filepath = os.path.join(where, sha1sum)

        # Don't download an already-downloaded file
        if os.path.isfile(filepath):
            continue

        n_files += 1
        with open(filepath, 'wb') as f:
            f.write(data)

    return issue_url, n_files

def main(argc, argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--project-name', required = True, help = 'user/project-name.')
    parser.add_argument('--out', required = True, help = 'Directory where files will get downloaded.')
    args = parser.parse_args()

    pool = multiprocessing.Pool(processes = multiprocessing.cpu_count())
    download_file_worker = functools.partial(download_file, args.out)
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
            if not li.attrs.get('id', '').startswith('issue'):
                continue
            bug_urls.append('https://github.com%s' % li.div.a.attrs['href'])

        if len(bug_urls) == 0:
            break

        for url, n in pool.imap_unordered(download_file_worker, bug_urls):
            n_issues += 1
            n_files += n
            print '[*] Downloaded', n_files, 'files (queried', n_issues, 'issues from', i, 'pages)\r',

    pool.close()
    pool.join()
    print '[+] Downloaded', n_files, 'files (queried', n_issues, 'issues)\r',

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
