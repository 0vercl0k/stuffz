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
import requests
import hashlib
import multiprocessing
import argparse
import functools
from bs4 import BeautifulSoup

onemeg = 1024 * 1024

def download_file(where, issue_url):
    soup = BeautifulSoup(requests.get(issue_url).content)
    attachments = soup.find_all(
        'div', attrs = {'class' : 'attachment_thumb'}
    )

    n_files = 0
    for attachment in attachments:
        attach_url = 'https://sourceforge.net%s' % attachment.a.attrs['href']
        r = requests.get(attach_url, timeout = 20)
        if int(r.headers.get('content-length', 0)) > onemeg:
            continue

        data = r.content
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
    parser.add_argument('--project-name', required = True, help = 'The project name.')
    parser.add_argument('--out', required = True, help = 'Directory where files will get downloaded.')
    args = parser.parse_args()

    pool = multiprocessing.Pool(processes = multiprocessing.cpu_count())
    download_file_worker = functools.partial(download_file, args.out)
    n_files, n_issues = 0, 0
    for i in range(100000):
        url = 'https://sourceforge.net/p/%s/bugs/' % args.project_name
        soup = BeautifulSoup(
            requests.get(
                url, params = {'limit' : 1000, 'page' : i}
            ).content
        )
        trs = soup.find_all('tr')
        bug_urls = []
        for tr in trs:
            class_ = tr.attrs.get('class', [])
            if class_ == ['even', ''] or class_ == ['', '']:
                bug_urls.append('https://sourceforge.net%s' % tr.td.a.attrs['href'])

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
