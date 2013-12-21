/*
#
#    ccompiler.c - Just a simple C compiler using libtcc
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
#    Compile with:
#    gcc ccompiler.c -o ccompiler -ldl -I. -std=c99 libtcc.a
*/
#include <libtcc.h>
#include <tcc.h>
#include <stdio.h>

int main(int argc, char* argv[])
{
    TCCState *s = NULL;
    unsigned char *p = NULL;

    if(argc != 2)
    {
        printf("./ccompiler <c code>\n");
        return 0;
    }

    s = tcc_new();
    if(s == NULL)
        return 0;

    tcc_set_output_type(s, TCC_OUTPUT_MEMORY);
    if(tcc_compile_string(s, argv[1]) == -1)
        return 0;

    if (tcc_relocate(s, TCC_RELOCATE_AUTO) < 0)
        return 0;

    for(unsigned int i = 0; i < text_section->data_offset; ++i)
        printf("\\x%.2x", text_section->data[i]);
    
    tcc_delete(s);
    return 0;
}
