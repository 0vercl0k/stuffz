#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    download_youtube_playlists_videos.py - Save locally the videos composing your Youtube playlists
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

# ressources:
#     https://developers.google.com/youtube/2.0/reference
#     https://code.google.com/p/gdata-python-client/source/browse/#hg%2Fsrc%2Fgdata%2Fyoutube
#     https://gdata-python-client.googlecode.com/hg/pydocs/gdata.youtube.html

# Testing & Troubleshooting : --> http://gdata.youtube.com/demo/index.html <--


import sys
from urllib2 import urlopen
from urllib import urlencode
from urlparse import parse_qs, urlparse
from time import sleep
import string
import os
import json

def make_request(url):
    return json.loads(urlopen(url).read())

def sanitize_title(s):
    """
    A filename cannot be composed of all the printable characters (on windows, maybe linux files can),
    """
    white_list = [c for c in (string.letters + string.digits + ' ')]
    sanitized_title = ''
    for c in s:
        if c in white_list:
            sanitized_title += c
    return sanitized_title

def get_video_info(video_id):
    """
    Retrieve some useful information concerning the video,
    like the title or where we can get the video file.

    You can also find stuff concerning the encoding format
    available etc.
    """
    args = urlencode({
        'asv': 3,
        'el': 'detailpage',
        'hl': 'en_US',
        'video_id': video_id
    })

    info = {
        'video_url' : '',
        'video_title' : ''
    }

    r = urlopen('https://www.youtube.com/get_video_info?' + args)
    if r:
        content = r.read()
        content_parsed = parse_qs(content)
        fmt_stream_map = parse_qs(content_parsed['url_encoded_fmt_stream_map'][0])

        # Do not forget Youtube wants the signature param
        info['video_url'] = fmt_stream_map['url'][0] + '&signature=' + fmt_stream_map['sig'][0]
        info['video_title'] = sanitize_title(content_parsed['title'][0])
    return info

def download_youtube_video(url, dir_out = '.'):
    """
    Download a video from youtube and save it in dir_out
    """
    # get the video id (properly) holded in the variable "v"
    vid = parse_qs(urlparse(url).query)['v'][0]

    # now get the token id
    info = get_video_info(vid)
    path_out = os.path.join(dir_out, info['video_title'] + '.flv')
    
    print ' -> Downloading "%s" in "%s"..' % (info['video_title'], path_out)

    # check if the file doesn't already exist, if it is save some bandwidth & skip!
    if os.path.exists(path_out) == True:
        print '    -> You already got this song'
        return

    with open(path_out, 'wb') as f:
        r = urlopen(info['video_url'])
        while True:
            c = r.read(8192)
            if not c:
                break
            f.write(c)
    print '  -> DONE'

def main(argc, argv):
    if argc == 1:
        print 'Usage: ./download_youtube_playlists_videos.py <username> [<base_path>]'
        return -1

    # Where we will store the playlists and the tracks on your filesystem -- default is the current path
    base_path = '.' if argc == 2 else argv[2]
    assert(os.path.isdir(base_path))

    print 'Retrieving the playlists of %s..' % argv[1]

    # Getting the (public) playlist for a specific user
    playlists = make_request('https://gdata.youtube.com/feeds/api/users/%s/playlists?alt=json' % argv[1])['feed']['entry']
    for playlist in playlists:

        playlist_title = playlist['title']['$t']
        playlist_desc = playlist['yt$description']['$t']
        playlist_id = playlist['yt$playlistId']['$t']

        # Preparing the out directory to store the videos in
        path_out = os.sep.join([base_path, sanitize_title(playlist_title)])
        
        # Ensure to create the directory if it doesn't exist
        if os.path.exists(path_out) == False:
            os.mkdir(path_out)

        print '-> Downloading %s ("%s") in %s' % (playlist_title, playlist_desc, path_out)

        start_index = 1

        while True: 
            playlist_url = 'https://gdata.youtube.com/feeds/api/playlists/%s?max-results=50&start-index=%d&alt=json' % (playlist_id, start_index)
            
            entries = make_request(playlist_url)['feed']
            if not 'entry' in entries:
                print '-> Fully downloaded the playlist.'
                break

            for entry in entries['entry']:
                # We want the link associated with the type 'text/html'
                link_html = filter(lambda l: l['type'] == 'text/html', entry['link'])[0]
                # Let the show begin -- downloadin'
                download_youtube_video(link_html['href'], path_out)
                start_index += 1

            sleep(1)
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))