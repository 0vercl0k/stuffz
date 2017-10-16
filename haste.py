#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    haste.py - Dummy haste client.
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

import os
import sys
import requests
import json
from urlparse import urlparse
from config import haste_server

def main(argc, argv):
    if argc != 2:
        print './haste.py <file>'
        return 0

    server_url = haste_server
    data = open(argv[1], 'r').read()
    r = requests.post('%s/documents' % server_url, data = data)
    if '@' in server_url:
        u = urlparse(server_url)
        _, host = u.netloc.split('@')
        server_url = '%s://%s%s' % (u.scheme, host, u.path)

    print '%s%s' % (server_url, json.loads(r.text)['key'])
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
