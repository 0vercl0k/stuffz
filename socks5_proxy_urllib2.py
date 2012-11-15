#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    socks5_proxy_urllib2.py - Use a SOCK5 proxy with urllib2 thanks to Socksipy
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
import socks
import socket
import urllib2
import json
import functools

# If you want to disable the SOCKS5 proxy we have to remember the original function
socket_function_saved = socket.socket

def enable_socks_proxy():
    """ Enable the SOCKS5 proxy for all the sockets """
    # Don't forgot to start TOR :]
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050)
    socket.socket = socks.socksocket

def disable_socks_proxy():
    """ Restore the original socket function to disable the SOCKS proxy """
    socket.socket = socket_function_saved

def pass_through_proxy(function):
    """ You can use this decorator when you want to use the SOCK5 proxy with a function """
    # functools.wraps aims to have the same function.__name__, __doc__
    # than the f returned by the decorator
    @functools.wraps(function)
    def f(*args, **kwargs):
        enable_socks_proxy()
        r = function(*args, **kwargs)
        disable_socks_proxy()
        return r
    return f

def get_public_ip():
    """ Retrieve your public IP thanks to jsonip.com """
    return json.loads(urllib2.urlopen('http://jsonip.com/').read())['ip']

@pass_through_proxy
def get_public_ip_with_proxy():
    """ get_public_ip version with proxy support """
    return get_public_ip()

def get_new_tor_identity():
    """ Ask the tor controler to get a new identity """
    old_public_ip = get_public_ip_with_proxy()
    new_public_ip = old_public_ip

    ret = True
    while (old_public_ip == new_public_ip):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 9051))

        requests = [
            'AUTHENTICATE ""',
            'SIGNAL NEWNYM',
            'QUIT'
        ]

        for request in requests:
            s.send(request + '\n')
            if s.recv(256).startswith('250') == False:
                ret = False
                break

        s.close()
        new_public_ip = get_public_ip_with_proxy()

    return ret

def main(argc, argv):
    print 'Public IP without SOCKS5 Proxy: %s' % get_public_ip()
    for i in range(5):
        print 'Public IP with SOCKS5 Proxy: %s' % get_public_ip_with_proxy()
        print 'Getting a new identity..'
        if not get_new_tor_identity():
            raise Exception('Please be sure the tor control is launched on the tcp/9051')
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
