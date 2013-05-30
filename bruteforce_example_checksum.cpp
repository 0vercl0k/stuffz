/*
    bruteforce_example_checksum.cpp - C++ modular and iterative bruteforce engine.
    Copyright (C) 2013 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <iostream>
#include <string>
#include <cstring>

//thx thaw <3
std::string bf(void (*hashing)(unsigned char*, unsigned int, unsigned char*),
               const unsigned char* hash,
               unsigned int hs,
               const std::string& charset,
               unsigned int min,
               unsigned int max)
{
    std::string result("not found");
    unsigned int* idx = new unsigned int[max];
    unsigned char* input = new unsigned char[hs];
    unsigned char* output = new unsigned char[hs];
    unsigned int charset_size = charset.size() - 1;
    unsigned int size = min;
    unsigned int i;

    for(i = 0; i < size; ++i)
        input[i] = charset[idx[i] = 0];

    while(size <= max)
    {
        hashing(input, size, output);

        if(!memcmp(hash, output, hs))
        {
            result = "";

            for(i = 0; i < size; ++i)
                result += charset[idx[i]];

            break;
        }

        for(i = 0; i < size; ++i)
        {
            if(idx[i] == charset_size)
            {
                input[i] = charset[idx[i] = 0];

                if(i + 1 == size)
                {
                    i = ++size - 1;
                    input[i] = charset[idx[i] = 0];
                    break;
                }
            }
            else
            {
                input[i] = charset[++idx[i]];
                break;
            }
        }
    }

    delete[] idx;
    delete[] input;
    delete[] output;

    return result;
}

void sub_41EC50(unsigned char *in, unsigned int len, unsigned char *out)
{
  unsigned int v1; // edx@1
  unsigned char *v2; // ecx@1
  int v3; // esi@1
  char v4; // al@2

  v2 = in;
  v3 = -559038737;
  v1 = 0;
  do
    v4 = *v2++;
  while ( v4 );
  if ( v2 != in + 1 )
  {
    do
      v3 = 1535553534 * in[v1++] - 942085638 * v3;
    while ( v1 < strlen((const char*)in) );
  }

  *((unsigned int*)out) = v3;
}

int main(int argc, char** argv)
{
    unsigned int hash = 0xC4B1801C;
    std::string charset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789");
    std::cout << bf(sub_41EC50, (const unsigned char*)&hash, 4, charset, 1, 5) << std::endl;
    return 0;
}
