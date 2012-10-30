#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    extract_audio_from_video_with_vlc.py - Extract and save the audio content from videos thanks to VLC
#    Copyright (C) 2012 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k
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
from subprocess import call

VLC_PATH = r'C:\Program Files (x86)\VideoLAN\VLC\vlc.exe'

def main(argc, argv):
    if argc == 1:
        print 'Usage: ./extract_audio_from_video.py <path dir video> [<dest path audio>]'
        return 0

    src = os.path.abspath(argv[1])
    dst = src if argc < 3 else os.path.abspath(argv[2])
    assert(os.path.isdir(src) and os.path.isdir(dst))

    for root, dirs, files in os.walk(src):
        for f in files:
            src_file = os.path.join(root, f)
            dst_file = os.path.join(dst, f) + '.wav'

            print 'Extracting audio from "%s" to "%s"..' % (src_file, dst_file)
            # http://wiki.videolan.org/Extract_audio
            args = [VLC_PATH] + '-I dummy --no-sout-video --sout-audio --no-sout-rtp-sap --no-sout-standard-sap --ttl=1 --sout-keep --sout'.split(' ')
            args += ['#transcode{acodec=s16l,channels=2}:std{access=file,mux=wav,dst=%s}' % dst_file, "%s" % src_file, 'vlc://quit']
            call(args)
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
