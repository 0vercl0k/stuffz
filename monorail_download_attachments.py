#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    monorail_download_attachments.py - Download attachments of a monorail bug
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
from urlparse import urlparse, urljoin
from bs4 import BeautifulSoup

onemeg = 1024 * 1024

def download_file(where, issue_url):
    requests.packages.urllib3.disable_warnings()
    soup = BeautifulSoup(requests.get(issue_url).content)
    links = soup.find_all('a')
    # /p/foo/issues/detail
    path = urlparse(issue_url).path
    # https://bugs.chromium.org/p/foo/issues/
    base = urljoin('https://bugs.chromium.org/', path.replace('detail', ''))
    n_files = 0
    for link in links:
        href = link.attrs.get('href', '')
        if not href.startswith('attachment?'):
            continue

        try:
            r = requests.get(
                # https://bugs.chromium.org/p/foo/issues/attachment?aid=348
                urljoin(base, href),
                timeout = 20, verify = False
            )
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
    parser.add_argument('--project-name', required = True, help = 'name.')
    parser.add_argument('--out', required = True, help = 'Directory where files will get downloaded.')
    args = parser.parse_args()

    pool = multiprocessing.Pool(processes = multiprocessing.cpu_count())
    download_file_worker = functools.partial(download_file, args.out)
    n_files, n_issues, start = 0, 0, 0
    for i in range(100000):
        url = 'https://bugs.chromium.org/p/%s/issues/list' % args.project_name
        soup = BeautifulSoup(
            requests.get(
                url, params = {'num' : 1000, 'start' : 0, 'can' : 1}
            ).content
        )
        start += 1000
        tds = soup.find_all('td', attrs = {'class' : 'id col_0'})
        bug_urls = []
        for td in tds:
            bug_urls.append('https://bugs.chromium.org%s' % td.a.attrs['href'])

        if len(bug_urls) == 0:
            break

        for url, n in pool.imap_unordered(download_file_worker, bug_urls):
            n_issues += 1
            n_files += n
            print '[*] Downloaded', n_files, 'files (queried', n_issues, 'issues from', i, 'pages)\r',

    pool.close()
    pool.join()
    print '[+] Downloaded', n_files, 'files (queried', n_issues, 'issues).'

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
