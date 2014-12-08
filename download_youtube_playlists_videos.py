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
import multiprocessing

p_name = multiprocessing.current_process().name

class VideoDownloader:
    """ This class aims to download easily a Youtube video and to keep it on your filesystem. """

    def __init__(self, video_link, where = '.'):
        """
        video_link: is the URL of your video
        where: A relative / absolute path of where the video will be stored

        Example:
        >>> VideoDownloader('http://www.youtube.com/watch?v=e2-6dYPEBw4', '/tmp').download()
        """
        self.video_link = video_link

        # get the video id (properly) holded in the variable "v"
        self.video_id = parse_qs(urlparse(self.video_link).query)['v'][0]

        info = self.__get_video_info(self.video_id)
        self.title = info['video_title']
        self.where = os.path.join(where, self.title + '.flv')
        self.video_ddl_link = info['video_url']
    
    def __sanitize_title(self, s):
        """ Only keep the alphanum characters on the filename """
        white_list = list(string.letters + string.digits + ' ')
        return filter(lambda c: c in white_list, s)

    def __get_video_info(self, video_id):
        """
        Retrieve some useful information concerning a video,
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

        content = urlopen('https://www.youtube.com/get_video_info?' + args).read()
        content_parsed = parse_qs(content)
        fmt_stream_map = parse_qs(content_parsed['url_encoded_fmt_stream_map'][0])

        # Do not forget Youtube wants the signature param
        # XXX: 08/12/2014 ; sig is not there anymore, it seems to work without it
        info['video_url'] = fmt_stream_map['url'][0] # + '&signature=' + fmt_stream_map['sig'][0]
        info['video_title'] = self.__sanitize_title(content_parsed['title'][0])
        return info

    def download(self):
        """ Download a Youtube video and save it on your filesystem """   
        # check if the file doesn't already exist, if it is save some bandwidth & skip!
        if os.path.exists(self.where) == True:
            return 'Already Downloaded', self.title

        print '[%s] Starts to download "%s"..' % (p_name, self.title)
        try:
            with open(self.where, 'wb') as f:
                r = urlopen(self.video_ddl_link)
                while True:
                    c = r.read(8192)
                    if not c:
                        break
                    f.write(c)
        except Exception, e:
            return str(e), self.title
        return 'Downloaded', self.title

def download_video(args):
    """ A simple wrapper of VideoDownloader to use with a process pool """
    link = args['link']
    where = args['where']
    try:
        return VideoDownloader(link, where).download()
    except Exception, e:
        print '[%s] Got an exception when trying to download "%s"' % (p_name, link) 
        return 'Failed', link

class PlaylistDownloader:
    """ This class aims to download easily a Youtube playlist with a pool of worker processes. """

    def __init__(self, playlist_link, where = '.', max_process = 3):
        """
        Example:
        >>> PlaylistDownloader('http://www.youtube.com/playlist?list=PL5A00B9A56C4B60E5', '/tmp/AOTP', 4).download()
        """
        self.playlist_link = playlist_link
        self.workers = multiprocessing.Pool(processes = max_process)

        # Get the playlist id in the 'list' variable
        self.playlist_id = parse_qs(urlparse(self.playlist_link).query)['list'][0]

        # Get the title of the playlist and its description
        s = self.__make_request()
        self.title = s['title']['$t']
        self.description = s['subtitle']['$t']
        self.where = os.path.join(where, self.__sanitize_title(self.title))

    def __sanitize_title(self, s):
        """ Only keep the alphanum characters on the filename """
        white_list = list(string.letters + string.digits + ' ')
        return filter(lambda c: c in white_list, s)

    def __make_request(self, start_index = 1):
        """ Retrieve a JSON content somewhere on the internet """
        url_playlist_api = 'https://gdata.youtube.com/feeds/api/playlists/%s?max-results=50&start-index=%d&alt=json' % (self.playlist_id, start_index)
        return json.loads(urlopen(url_playlist_api).read())['feed']
    
    def download(self):
        """ Multithread downloading of all the 
        song of your playlist """
        # Ensure to create the directory if it doesn't exist
        if os.path.exists(self.where) == False:
            os.mkdir(self.where)

        print '[%s] Iterating %s ("%s")..' % (p_name, self.title, self.description)
        start_index = 1
        work_todo = []

        while True:
            entries = self.__make_request(start_index)
            if not 'entry' in entries:
                break

            for entry in entries['entry']:
                # We want the link associated with the type 'text/html'
                link_html = filter(lambda l: l['type'] == 'text/html', entry['link'])[0]

                task = {
                    'link' : link_html['href'],
                    'where' : self.where
                }

                if not task in work_todo:
                    work_todo.append(task)

                start_index += 1

        print '[%s] %d songs fetched, WORKERS ARE YOU READY ? AOUUU AOUU' % (p_name, len(work_todo))
        results = self.workers.map(download_video, work_todo)

        print '[%s] Fully downloaded the playlist.' % p_name
        self.workers.terminate()
        self.workers.join()

class UserPlaylistsDownloader:
    """ This class aims to download easily all the playlists of a Youtube user via its nickname """

    def __init__(self, username, where = '.'):
        """
        Example:
        >>> UserPlaylistsDownloader('doublebubble66', '/tmp/').download()
        """
        self.username = username
        self.where = where

    def __sanitize_title(self, s):
        """ Only keep the alphanum characters on the filename """
        white_list = list(string.letters + string.digits + ' ')
        return filter(lambda c: c in white_list, s)

    def __make_request(self):
        url_user_api = 'https://gdata.youtube.com/feeds/api/users/%s/playlists?alt=json' % self.username
        return json.loads(urlopen(url_user_api).read())['feed']

    def download(self):
        """ Download all the playlists of an user """
        playlists = self.__make_request()
        for playlist in playlists['entry']:
            link_html = filter(lambda l: l['type'] == 'text/html', playlist['link'])[0]
            PlaylistDownloader(link_html['href'], self.where).download()


def main(argc, argv):
    if argc == 1:
        print 'Usage: ./download_youtube_playlists_videos.py <username> [<base_path>]'
        return -1

    # Where we will store the playlists and the tracks on your filesystem -- default is the current directory
    base_path = '.' if argc == 2 else argv[2]
    assert(os.path.isdir(base_path))

    print 'Retrieving the playlists of %s..' % argv[1]
    UserPlaylistsDownloader(argv[1], base_path).download()
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
