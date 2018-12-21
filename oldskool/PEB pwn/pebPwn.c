#include <stdio.h>
#include <windows.h>

#define PROCESS_TEST "./test.exe"
#define DLL_HOOK "./pebPwn.dll"

int InjectDllInProcess(long, char*);


int main(int argc, char* argv[])
{
    int retour = 0;
    PROCESS_INFORMATION processInfo = {0};
    STARTUPINFO startInfo = {0};

    printf("[-- Peb pwn par 0vercl0k. --]\n\n");

    retour = CreateProcess(PROCESS_TEST,
                           NULL,
                           NULL,
                           NULL,
                           FALSE,
                           CREATE_SUSPENDED,
                           NULL,
                           NULL,
                           &startInfo,
                           &processInfo
                           );
    if(retour)
        printf("[x] Creation du processus, thread principal suspendu.\n");
    else
    {
        printf("[!] Creation du processus impossible.\n");
        return 0;
    }

    printf("\t [ INFOS ]   : PID            : 0x%x/%d.\n", (unsigned int)processInfo.dwProcessId, (int)processInfo.dwProcessId);
    printf("\t               Handle Process : 0x%x/%d.\n", (unsigned int)processInfo.hProcess, (int)processInfo.hProcess);
    printf("\t               TID            : 0x%x/%d.\n", (unsigned int)processInfo.dwThreadId, (int)processInfo.dwThreadId);
    printf("\t               Handle Thread  : 0x%x/%d.\n", (unsigned int)processInfo.hThread, (int)processInfo.hThread);

    if(InjectDllInProcess(processInfo.dwProcessId, DLL_HOOK))
        printf("[x] La dll a ete injectee avec succes dans le processus.\n");
    else
    {
        printf("[!] La dll n'a pu etre injectee.\n");
        goto clean;
    }

    printf("[?] Relancement du thread?\n");
    getchar();

    if(ResumeThread(processInfo.hThread) == (DWORD)-1)
    {
        printf("[!] Relancement du thread impossible.\n");
        goto clean;
    }
    else
        printf("[x] Thread relance avec succes.\n");

    clean:
    CloseHandle(processInfo.hThread);
    CloseHandle(processInfo.hProcess);

    return 1;
}

int InjectDllInProcess(long pidProcAInjecter , char* fullPathDll)
{
    long sizeString = strlen(fullPathDll)+1;
    int ret = 0;
    HANDLE hProcess = NULL, hRemoteThread = NULL;
    DWORD tid = 0;
    LPVOID pMem = NULL;
    LPTHREAD_START_ROUTINE pLoadLibraryA = NULL;

    hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pidProcAInjecter);
    if(hProcess == NULL)
        return 0;

    pMem = VirtualAllocEx(hProcess, NULL, sizeString, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
    if(pMem == NULL)
        return 0;

    ret = WriteProcessMemory(hProcess, pMem, fullPathDll, sizeString, 0);
    if(ret == 0)
        return 0;

    pLoadLibraryA = (LPTHREAD_START_ROUTINE)GetProcAddress(GetModuleHandle("kernel32.dll"), "LoadLibraryA");
    hRemoteThread = CreateRemoteThread(hProcess, NULL, 0, pLoadLibraryA, pMem, 0, &tid);
    if(hRemoteThread == NULL)
        return 0;

    WaitForSingleObject(hRemoteThread, INFINITE);
    VirtualFreeEx(hProcess, pMem, 0, MEM_DECOMMIT);

    CloseHandle(hProcess);
    CloseHandle(hRemoteThread);

    return 1;
}
