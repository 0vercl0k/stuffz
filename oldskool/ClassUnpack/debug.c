#include <stdio.h>
#include <windows.h>

#define DBG 1
#define dprintf  if(DBG)printf

//Macro de Baboon, merci o/
#define OneByteLength 00
#define TwoByteLength 01
#define FourByteLength 3
#define BreakOnExec    0
#define BreakOnWrite   1
#define BreakOnAccess  3
#define GlobalFlag     2
#define LocalFlag      1
#define DR7Flag(_size,_type,flag,HBPnum) (((_size<<2 | _type) << (HBPnum*4 +16)) | (flag <<(HBPnum*2)))

//Variable globale
DEBUG_EVENT dbgEvent = {0};

//Prototype
DWORD goToHW(PDWORD addr, HANDLE hThread);
DWORD goToI3(PDWORD addr, HANDLE hProcess);
PCHAR dumpProcessus(HANDLE hProcess, PCHAR imgBase, PDWORD taille, DWORD oep);
DWORD initialisationDebug();
PDWORD mappeFichier(PCHAR path);

DWORD initialisationDebug()
{
    BOOL ret = FALSE;
    DWORD imgBase = 0;

    while(ret == FALSE)
    {
        WaitForDebugEvent(&dbgEvent, INFINITE);
        switch(dbgEvent.dwDebugEventCode)
        {
            case CREATE_PROCESS_DEBUG_EVENT:
                imgBase = (DWORD)dbgEvent.u.CreateProcessInfo.lpBaseOfImage;
                dprintf("\t[*] ImageBase du processus : 0x%x.\n", (unsigned int)imgBase);
                ret = TRUE;

                ContinueDebugEvent(dbgEvent.dwProcessId, dbgEvent.dwThreadId, DBG_EXCEPTION_NOT_HANDLED);
            break;

            default:
                //L'exception ne sera pas handle par le debugé
                ContinueDebugEvent(dbgEvent.dwProcessId, dbgEvent.dwThreadId, DBG_EXCEPTION_NOT_HANDLED);
            break;
        }
    }
    return imgBase;
}

PDWORD mappeFichier(PCHAR path)
{
    HANDLE hFile, hFileMap, hMapView;

    hFile    = CreateFile(path, GENERIC_WRITE|GENERIC_READ, FILE_SHARE_READ|FILE_SHARE_WRITE, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, 0);
    if(hFile == INVALID_HANDLE_VALUE)
        return NULL;

    hFileMap    = CreateFileMapping(hFile, NULL, PAGE_READWRITE, 0, 0, NULL);
    if(hFileMap == NULL)
     {
        CloseHandle(hFile);
        return NULL;
     }

    hMapView    = MapViewOfFile(hFileMap, FILE_MAP_READ|FILE_MAP_WRITE, 0, 0, 0);
    if(hMapView == NULL)
    {
        CloseHandle(hFile);
        CloseHandle(hFileMap);
        return NULL;
    }

    CloseHandle(hFileMap);
    CloseHandle(hFile);

    return (PDWORD)hMapView;
}

PCHAR dumpProcessus(HANDLE hProcess, PCHAR imgBase, PDWORD taille, DWORD oep)
{
    IMAGE_DOS_HEADER imgDos = {0};
    IMAGE_NT_HEADERS imgPe  = {0};
    PIMAGE_NT_HEADERS pImgPe = NULL;
    PIMAGE_SECTION_HEADER pSection = NULL;
    DWORD nbByte = 0, tailleBin = 0, nbSection = 0, ret;
    PCHAR pDump = NULL;

    ret = ReadProcessMemory(hProcess, imgBase, &imgDos, sizeof(IMAGE_DOS_HEADER), &nbByte);
    if(ret == 0 || nbByte != sizeof(IMAGE_DOS_HEADER))
    {
        dprintf("\t[!] Erreur @ ReadProcessMemory(.., imgBase,..) : 0x%x.\n", (unsigned int)GetLastError());
        return pDump;
    }

    ret = ReadProcessMemory(hProcess, (imgBase + imgDos.e_lfanew), &imgPe, sizeof(IMAGE_NT_HEADERS), &nbByte);
    if(ret == 0 || nbByte != sizeof(IMAGE_NT_HEADERS))
    {
        dprintf("\t[!] Erreur @ ReadProcessMemory(.., imgBase+imgDos.e_lfanew, ..) : 0x%x.\n", (unsigned int)GetLastError());
        return pDump;
    }

    nbSection = imgPe.FileHeader.NumberOfSections;
    pSection = (PIMAGE_SECTION_HEADER)calloc(nbSection, sizeof(IMAGE_SECTION_HEADER));
    if(pSection == NULL)
    {
        dprintf("\t[!] Erreur @ calloc().\n");
        return pDump;
    }

    ret = ReadProcessMemory(hProcess,
                      (imgBase+imgDos.e_lfanew+sizeof(DWORD)+sizeof(IMAGE_FILE_HEADER)+imgPe.FileHeader.SizeOfOptionalHeader),
                      pSection,
                      nbSection*sizeof(IMAGE_SECTION_HEADER),
                      &nbByte);

    if(ret == 0 || nbByte != nbSection*sizeof(IMAGE_SECTION_HEADER))
    {
        dprintf("\t[!] Erreur @ ReadProcessMemory(.., imgBase+imgDos.e_lfanew+sizeof(DWORD)+sizeof(IMAGE_FILE_HEADER)+imgPe.FileHeader.SizeOfOptionalHeader, ..) : 0x%x.\n", (unsigned int)GetLastError());
        free(pSection);
        return pDump;
    }

    pSection += nbSection-1;
    tailleBin = pSection->VirtualAddress + pSection->Misc.VirtualSize;

    pDump = (PCHAR)malloc(sizeof(char)*tailleBin);
    if(pDump == NULL)
    {
        dprintf("\t[!] Erreur @ malloc().\n");
        return pDump;
    }

    ret = ReadProcessMemory(hProcess, imgBase, pDump, tailleBin, &nbByte);
    if(ret == 0 || nbByte != tailleBin)
    {
        dprintf("\t[!] Erreur @ ReadProcessMemory(.., imgBase, ..) : 0x%x.\n", (unsigned int)GetLastError());
        free(pSection);
        free(pDump);
        return NULL;
    }

    if(taille != NULL)
        *taille = tailleBin;

    free(pSection);
    pSection = (PIMAGE_SECTION_HEADER)((PCHAR)pDump+imgDos.e_lfanew+sizeof(DWORD)+sizeof(IMAGE_FILE_HEADER)+imgPe.FileHeader.SizeOfOptionalHeader);
    dprintf("\t[*] Modification des sections headers..\n");
    for(unsigned int i = 0 ; i < nbSection ; i++, pSection++)
    {
        pSection->SizeOfRawData    = pSection->Misc.VirtualSize;
        pSection->PointerToRawData = pSection->VirtualAddress;
    }

    if(oep != 0)
    {
        dprintf("\t[*] Modification de l'entry-point..\n");
        pImgPe = (PIMAGE_NT_HEADERS)(pDump+imgDos.e_lfanew);
        pImgPe->OptionalHeader.AddressOfEntryPoint = oep;
    }

    return pDump;
}

DWORD goToHW(PDWORD addr, HANDLE hThread)
{
    CONTEXT context = {0};
    BOOL ret = FALSE;
    DWORD retour = 0;

    //LOL merci baboon <3
    context.ContextFlags = CONTEXT_DEBUG_REGISTERS|CONTEXT_CONTROL;

    //Recuperation du contexte du thread
    GetThreadContext(hThread, &context);

    //On place le hwbp
    context.Dr0  = (DWORD)addr;
    context.Dr7  = DR7Flag(OneByteLength, BreakOnExec, LocalFlag, 0);

    retour = SetThreadContext(hThread, &context);
    if(retour == 0)
    {
        dprintf("\t[!] Le contexte n'a pu être placé dans le thread.\n");
        return 0;
    }
    dprintf("\t[*] HBP posé.\n");

    ContinueDebugEvent(dbgEvent.dwProcessId, dbgEvent.dwThreadId, DBG_CONTINUE);

    //On attends l'exception
    while(ret == FALSE)
    {
        WaitForDebugEvent(&dbgEvent, INFINITE);
        if(dbgEvent.dwDebugEventCode == EXCEPTION_DEBUG_EVENT)
        {
            if(dbgEvent.u.Exception.ExceptionRecord.ExceptionCode == EXCEPTION_SINGLE_STEP)
                ret = TRUE;
            else
                ContinueDebugEvent(dbgEvent.dwProcessId, dbgEvent.dwThreadId, DBG_CONTINUE);
        }
        else if(dbgEvent.dwDebugEventCode == EXIT_PROCESS_DEBUG_EVENT)
        {
            dprintf("\t[*] Le processus se termine..\n");
            return 0;
        }
        else
            ContinueDebugEvent(dbgEvent.dwProcessId, dbgEvent.dwThreadId, DBG_EXCEPTION_NOT_HANDLED);
    }

    dprintf("\t[*] HBP atteint, nettoyage des debug-registers..\n");

    //Nous venons d'atteindre l'exception, on desactive l'hwbp
    GetThreadContext(hThread, &context);

    context.Dr0 = 0;
    context.Dr7 = 0;

    //To avoid confusion in identifying debug exceptions,
    //debug handlers should clear the register before returning to the interrupted task
    context.Dr6 = 0;

    retour = SetThreadContext(hThread, &context);
    if(retour == 0)
    {
        dprintf("\t[!] Le contexte n'a pu être placé dans le thread.\n");
        return 0;
    }

    return 1;
}

DWORD goToI3(PDWORD addr, HANDLE hProcess)
{
    BOOL ret = FALSE;
    DWORD retour = 0;
    char instru = 0, i3 = 0xCC;


    if(ReadProcessMemory(hProcess, addr, &instru, sizeof(char), &retour) == 0 ||
       WriteProcessMemory(hProcess, addr, &i3, sizeof(char), &retour) == 0)
       {
            dprintf("\t[!] Erreur @ [Read/Write]ProcessMemory().\n");
            return 0;
       }

    dprintf("\t[*] Breakpoint posé.\n");

    ContinueDebugEvent(dbgEvent.dwProcessId, dbgEvent.dwThreadId, DBG_CONTINUE);

    //On attends l'exception
    while(ret == FALSE)
    {
        WaitForDebugEvent(&dbgEvent, INFINITE);
        if(dbgEvent.dwDebugEventCode == EXCEPTION_DEBUG_EVENT)
        {
            if(dbgEvent.u.Exception.ExceptionRecord.ExceptionCode == EXCEPTION_BREAKPOINT)
            {
                dprintf("\t[*] Breakpoint atteint.\n");
                ret = TRUE;
            }
            else
                ContinueDebugEvent(dbgEvent.dwProcessId, dbgEvent.dwThreadId, DBG_EXCEPTION_NOT_HANDLED);
        }
        else if(dbgEvent.dwDebugEventCode == EXIT_PROCESS_DEBUG_EVENT)
        {
            dprintf("\t[*] Le processus se termine..\n");
            return 0;
        }
        else
            ContinueDebugEvent(dbgEvent.dwProcessId, dbgEvent.dwThreadId, DBG_EXCEPTION_NOT_HANDLED);
    }

    dprintf("\t[*] Réécriture de l'instruction précédente..\n");
    WriteProcessMemory(hProcess, addr, &instru, sizeof(char), &retour);
    return 1;
}
