#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    lzw_odbg2.py - LZW implementation. I did this script because the same implementation
#    is used in OllyDBG2.
#    Copyright (C) 2013 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k
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
import struct

def int2bitstring(n, nb):
    '''
    >>> int2bitstring(0x101, 8)
    >>> '00000001'
    >>> int2bitstring(0x101, 9)
    >>> '100000001'
    '''
    r = ''
    for i in range(nb - 1, -1, -1):
        r += '1' if ((n >> i) & 1) else '0'
    return r

def bitstring2bytes(b):
    '''
    >>> bitstring2bytes('000000000000000100000010')
    >>> '\x00\x01\x02'
    '''
    bytes = ''
    for i in range(len(b) / 8):
        idx = i*8
        bytes += chr(int(b[idx : idx + 8], 2))
    return bytes

def bitstring2int(b):
    '''
    >>> bitstring2int('001010100')
    >>> 84
    '''
    r = 0
    b = list(reversed(b))
    for i in range(len(b)):
        r += (1 << i) if b[i] == '1' else 0
    return r

def bytes2bitstring(by):
    '''
    >>> bytes2bitstring('\x01\x02')
    >>> '0000000100000010'
    '''
    bits = ''
    for b in by:
        bits += int2bitstring(ord(b), 8)
    return bits

def lzw_compress(clear_data):
    '''Python implementation of a simple Lempel-Ziv-Welch with code words starting
    at 9 bits until 14'''
    # Initialize the dictionary to contain all strings of length one.
    dictionary = map(chr, range(0x100))
    w, bits, nbits, maxbits = '', '', 9, 14
    for c in clear_data:
        # Buffer input characters in a sequence ω until ω + next characteris not in the dictionary.
        if (w + c) in dictionary:
            w += c
        # Emit the code for ω, and add ω + next character to the dictionary. Start buffering again with the next character.
        else:
            if len(dictionary) >= (1 << nbits):
                nbits += 1

            bits += int2bitstring(dictionary.index(w), nbits)
            dictionary.append(w + c)
            w = c

        # Reset if the dictionary is too big
        if len(dictionary) >= (1 << maxbits):
            dictionary = map(chr, range(0x100))
            nbits = 9

    # Don't forget the last data
    bits += int2bitstring(dictionary.index(w), nbits)

    if (len(bits) % 8) != 0:
        bits += '0' * (8 - (len(bits) % 8))

    return bitstring2bytes(bits)

def lzw_decompress(compressed_data):
    '''Python implementation of a simple Lempel-Ziv-Welch with code words starting
    at 9 bits until 14'''
    dictionary, dictionary_size = map(chr, range(0x100)), 256
    w, nbits, maxbits, i = '', 9, 14, 0
    bits, result = bytes2bitstring(compressed_data), ''
    while i < len(bits):
        if dictionary_size >= (1 << nbits):
            nbits += 1

        # We won't have enough bits!
        if (i + nbits) > len(bits):
            break

        c = bitstring2int(bits[i : i + nbits])
        if c < len(dictionary):
            entry = dictionary[c]
        elif c == len(dictionary):
            entry = w + w[0]
        else:
            raise Exception('corrupted somehow')

        result += entry
        if (w + entry[0]) not in dictionary:
            dictionary.append(w + entry[0])

        w = entry
        dictionary_size += 1
        i += nbits

        # Reset if the dictionary is too big
        if dictionary_size >= (1 << maxbits):
            dictionary, dictionary_size = map(chr, range(0x100)), 256
            w, nbits, maxbits = '', 9, 14

    return result

def odbg2_lzw_compress(data):
    '''Python implementation of ollydbg!Compress'''
    header = '\nCpd' + struct.pack('<I', len(data))
    return header + lzw_compress(data)

def odbg2_lzw_decompress(data):
    '''Python implementation of ollydbg!Decompress'''
    return lzw_decompress(data[8 : ])

def main(argc, argv):
    # Tests for the compression
    print 'COMPRESSION'.center(80, '=')
    for name in 'small small2 big'.split():
        print ('Compression: %s' % name).center(80, '=')
        clear_data = open('tests\\%s.clear.bin' % name, 'rb').read()
        print 'Len clear data: %d bytes' % len(clear_data)
        compressed_data_computed = odbg2_lzw_compress(clear_data)
        print 'Len compressed data computed: %d bytes' % len(compressed_data_computed)
        compressed_data_read = open('tests\\%s.compressed.bin' % name, 'rb').read()
        print 'Len compressed data read: %d bytes' % len(compressed_data_read)
        print 'Same output ?', compressed_data_computed == compressed_data_read
        if (compressed_data_computed == compressed_data_read) == False:
            raise Exception('A test failed')

    # Tests for the decompression
    print 'DECOMPRESSION'.center(80, '=')
    for name in 'small small2 big'.split():
        print ('Decompression: %s' % name).center(80, '=')
        compressed_data = open('tests\\%s.compressed.bin' % name, 'rb').read()
        print 'Len compressed data: %d bytes' % len(compressed_data)
        clear_data_computed = odbg2_lzw_decompress(compressed_data)
        print 'Len clear data computed: %d bytes' % len(clear_data_computed)
        clear_data_read = open('tests\\%s.clear.bin' % name, 'rb').read()
        print 'Len clear data read: %d bytes' % len(clear_data_read)
        print 'Same output ?', clear_data_computed == clear_data_read
        if (clear_data_computed == clear_data_read) == False:
            raise Exception('A test failed')

    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
