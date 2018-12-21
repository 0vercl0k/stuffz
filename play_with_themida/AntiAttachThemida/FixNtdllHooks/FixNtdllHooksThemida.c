/*
#
#    FixNtdllHooksThemida.c - Themida implements some anti-attach features by hooking
#    ntdll!DbgBreakPoint & ntdll!DbgUiRemoteBreakin, fix those hooks :).
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
#include <windows.h>
#include <stdio.h>

int main(int argc, char* argv[])
{
    unsigned int pid_to_patch = 0, oldprot = 0;
    void *dbguiremotebreakin = 0, *dbgbreakpoint = 0;
    HANDLE hProcess = INVALID_HANDLE_VALUE;
    /*
        0:000> !for_each_module !chkimg @#ModuleName
        [...]
        6 errors : ntdll (7718879c-7720fdc8)

        0:000> !chkimg ntdll -d
            7718879c - ntdll!DbgBreakPoint
            [ cc:c3 ]
            7720fdc4-7720fdc8  5 bytes - ntdll!DbgUiRemoteBreakin (+0x87628)
            [ 6a 08 68 18 fe:e9 94 a4 fb ff ]
    */
    if(argc != 2)
    {
        printf("./FixNtdllHooksThemida <pid>\n");
        return EXIT_FAILURE;
    }

    pid_to_patch = atoi(argv[1]);

    dbguiremotebreakin = (void*)GetProcAddress(GetModuleHandle("ntdll"), "DbgUiRemoteBreakin");
    dbgbreakpoint = (void*)GetProcAddress(GetModuleHandle("ntdll"), "DbgBreakPoint");
    hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid_to_patch);
    if(hProcess == NULL)
        return 0;

    printf("Process opened, patching ntdll!DbgUiRemoteBreakin (%#.8x)..\n", dbguiremotebreakin);
    VirtualProtectEx(hProcess, dbguiremotebreakin, 5, PAGE_EXECUTE_READWRITE, &oldprot);
    WriteProcessMemory(hProcess, dbguiremotebreakin, dbguiremotebreakin, 5, NULL);
    VirtualProtectEx(hProcess, dbguiremotebreakin, 5, oldprot, &oldprot);

    printf("patching ntdll!DbgBreakPoint (%#.8x)..\n", dbgbreakpoint);
    VirtualProtectEx(hProcess, dbgbreakpoint, 1, PAGE_EXECUTE_READWRITE, &oldprot);
    WriteProcessMemory(hProcess, dbgbreakpoint, dbgbreakpoint, 1, NULL);
    VirtualProtectEx(hProcess, dbgbreakpoint, 1, oldprot, &oldprot);

    CloseHandle(hProcess);
    return 0;
}
