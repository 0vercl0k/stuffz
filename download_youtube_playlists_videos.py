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

# To run this script, you have to install:
#   * elementtree -- http://effbot.org/zone/element-index.htm#installation
#   * gdata api -- https://gdata-python-client.googlecode.com/files/gdata-2.0.17.zip


import sys
from urllib import urlopen, urlencode
from urlparse import parse_qs, urlparse
from re import findall
import string
import os
import gdata.youtube
import gdata.youtube.service
from pprint import pprint

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
        # Do not forget Youtube want the signature param
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

    # check if the file doesn't already exist, if it is save some bandwidth & skip!
    if os.path.exists(path_out) == True:
        return

    print ' -> Downloading "%s" in "%s"..' % (info['video_title'], path_out)
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

    print 'Initializing the google API..'
    # "Before you can perform any operations with the YouTube Data API, you must initialize a gdata.youtube.service.YouTubeService object"
    yt_service = gdata.youtube.service.YouTubeService()

    # Turn on HTTPS/SSL access
    yt_service.ssl = True

    print 'Retrieving the playlists of %s..' % argv[1]

    # Getting the (public) playlist for a specific user
    playlists = yt_service.GetYouTubePlaylistFeed(username = argv[1])
    for playlist in playlists.entry:
        # Preparing the out directory to store the videos in
        path_out = os.sep.join([base_path, sanitize_title(playlist.title.text)])
        
        # Ensure to create the directory if it doesn't exist
        if os.path.exists(path_out) == False:
            os.mkdir(path_out)

        print '-> Downloading %s ("%s") in %s' % (playlist.title.text, playlist.description.text, path_out)

        # Parsing the html link and retrieve properly the playlist id holded in the variable 'p'
        playlist_id = parse_qs(urlparse(playlist.GetHtmlLink().href).query)['list'][0]

        # Now we want the videos contained by this playlist
        videos = yt_service.GetYouTubePlaylistVideoFeed(playlist_id = playlist_id)
        for video in videos.entry:
            # Let the show begin -- downloadin'
            download_youtube_video(video.GetHtmlLink().href, path_out)
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))