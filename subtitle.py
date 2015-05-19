#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    find_subtitles.py - Find some subtitles
#    Copyright (C) 2011 0vercl0k
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
import subprocess
import xmlrpclib
import os
import zipfile
from torrent_config import *

SERVER_API_URL = 'http://api.opensubtitles.org/xml-rpc'

def get_subtitle(full_title, out_dir_base):
    # Login
    server = xmlrpclib.Server(SERVER_API_URL)
    
    # thx - http://code.google.com/p/periscope/source/browse/trunk/periscope/plugins/OpenSubtitles.py
    r = server.LogIn('', '', 'eng', 'periscope')
    token = r['token']
    r = server.SearchSubtitles(token, 
        [
            # http://trac.opensubtitles.org/projects/opensubtitles/wiki/XMLRPC
            {
                'sublanguageid' : 'eng, fre',
                'query' : full_title
            }
        ]
    )
    server.LogOut(token)

    if r['data'] == False:
        print 'No result.'
        return
    
    for entry in r['data']:
        print '[%s downloads - %s] %s -\n %s? [y/n]' % (entry['SubDownloadsCnt'], entry['SubLanguageID'], entry['MovieReleaseName'], entry['ZipDownloadLink'])
        if raw_input('').lower() == 'y':
            out_path = os.path.join(out_dir_base, 'tmp_subtitle.zip')
            devnull = open(os.devnull)
            subprocess.call(
                ['wget',  entry['ZipDownloadLink'], '--no-check-certificate', '-O', out_path],
                stdout = devnull,
                stderr = devnull
            )
            z = zipfile.ZipFile(out_path)
            srt_name = filter(lambda x: x.endswith('.srt'), z.namelist())[0]
            z.extract(srt_name, out_dir_base)
            z.close()
            os.unlink(out_path)
            os.rename(os.path.join(out_dir_base, srt_name), os.path.join(out_dir_base, '%s.srt' % full_title))
            break
    
def main(argc, argv):
    if argc != 2:
        print './subtitle My.Serie.S01E02'
        return 0

    get_subtitle(argv[1], TMP_DIR)
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
