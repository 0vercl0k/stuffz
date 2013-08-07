/*
#
#    kryptonite-crackme.c - Little crackme I used to demonstrate Kryptonite
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
*/

#include <stdio.h>
#include <string.h>

int main(int argc, char* argv[])
{
    unsigned char hexstring[4 * 2 + 1] = {0};
    unsigned int i = 0, j = 0;
    unsigned int values[4] = {0};
    unsigned char s1[64] = {
        0x87, 0xb6, 0xdb, 0x07, 0x45, 0x64, 0x31, 0x5d,
        0x2d, 0x1e, 0x03, 0xbb, 0xb8, 0x06, 0x2b, 0x9b,
        0xe1, 0xb9, 0x15, 0xf7, 0x90, 0x38, 0xa9, 0xbc,
        0x28, 0xbf, 0x1b, 0xdd, 0x8b, 0x1c, 0x9c, 0xf9,
        0x85, 0xce, 0x33, 0x67, 0x84, 0xe6, 0x86, 0xc1,
        0x21, 0x78, 0x0b, 0x6c, 0x2a, 0x2c, 0xe7, 0x22,
        0xb5, 0x59, 0xfb, 0x5e, 0x53, 0x55, 0x01, 0x47,
        0x5f, 0x09, 0x8a, 0x5b, 0xde, 0xc5, 0x4b, 0x72
    }, s2[64] = {
        0x2c, 0xc3, 0x4a, 0x95, 0xfd, 0x80, 0x82, 0xcf,
        0x94, 0x96, 0xd1, 0x7c, 0xb3, 0x8d, 0x45, 0x4e,
        0xe3, 0x4f, 0x6f, 0x02, 0x2e, 0xa9, 0x77, 0x06,
        0xb0, 0x31, 0x5d, 0xd2, 0x7a, 0x92, 0xa8, 0x3f,
        0x07, 0x48, 0xf7, 0x7e, 0x0f, 0xe4, 0x34, 0xfa,
        0x38, 0x2d, 0x7d, 0x5a, 0x52, 0x72, 0xb5, 0xfb,
        0x15, 0x09, 0x58, 0xa1, 0xdb, 0xa0, 0xcd, 0xd4,
        0x7b, 0x6c, 0x30, 0xbb, 0x0b, 0x1e, 0x98, 0x18
    };

    if(argc != 2)
    {
        printf("./kryptonite-crackme <password>\n");
        return 0;
    }

    if(strlen(argv[1]) != 16)
    {
        printf("Your password must be 16 bytes long.\n");
        return 0;
    }

    for(i = 0; i < 4; ++i)
    {
        for(j = 0; j < 4; ++j)
            sprintf(hexstring + j * 2, "%.2x", argv[1][i * 4 + j]);
        
        hexstring[8] = 0;
        values[i] = strtoul(hexstring, NULL, 16);
        memset(hexstring, 0, sizeof(hexstring));
    }

    for(i = 0; i < 64; ++i)
    {
        #define ROTL32(x, n) (((x) << (n)) | ((x) >> (32 - (n))))
        values[0] = ROTL32(values[0] ^ values[3], 1);
        values[1] = ROTL32(values[1] ^ values[2], 2);
        values[2] = ROTL32(values[2] ^ values[3], 3);
        values[3] = ROTL32(values[3] + 0x1337 + (s1[i] & s2[i]), 4);
    }

    if(
        values[0] == 0xcaf07da0 && values[1] == 0x76c29089 &&
        values[2] == 0x3716cdb4 && values[3] == 0x2ed4aaed &&
        (ROTL32((values[0] ^ values[1]) - (values[2] ^ values[3]), 17) ^ (values[0] + values[1] + values[2] + values[3])) == 0xac3fc22b // Was used to generate moaaar obfuscation
    )
        printf("Good job dude! The key is: %s\n", argv[1]);
    else
        printf("Bad boy :(.\n");

    return 1;
}