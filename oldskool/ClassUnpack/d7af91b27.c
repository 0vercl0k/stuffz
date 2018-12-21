#define WIN32_LEAN_AND_MEAN
#include "main.h"


HINSTANCE hInst;
DEBUG_EVENT DbgEvt;

DWORD SearchSign(char *Sign,DWORD SignSize,char *Mem ,DWORD MemSize)
{
    DWORD i,j,k;
    for (i=0;i<= MemSize; i++)
    {
        k = 0;
        for (j=0;j<SignSize;j++)
            if (Mem[i+j] != Sign[j])
                break;
            else k++;
        if (k==SignSize)
            return (DWORD)(Mem+i);
    }
    return 0;
}



BOOL CALLBACK DialogProc(HWND hwndDlg, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
    char* path[MAX_PATH] ;
    HANDLE hFile, hMapp;
    char* mapping;
    DWORD  pJmpToOEP ,pCallEdi, BaseAddress,RetnAdd,NumberOfBytesRead;
    HMODULE hModKern;
    PIMAGE_DOS_HEADER pDosHeader;
    PIMAGE_NT_HEADERS pPE;
    PIMAGE_SECTION_HEADER pSection;
    STARTUPINFOA StartupInfo;
    PROCESS_INFORMATION ProcessInfo;
    CONTEXT Context;
    DWORD addrAlloc,AllocSize,addrImportResolver,Sign;
    DWORD addrOEP , addrIT,NumberOfBytesWritten;
    PCHAR PackerMem , Dump;
    DWORD DumpSize;
    OPENFILENAMEA ofn;
    char* filename;

    Context.ContextFlags = CONTEXT_ALL;
    switch(uMsg)
    {
        case WM_INITDIALOG:
            /*
             * TODO: Add code to initialize the dialog.
             */
            return TRUE;

        case WM_CLOSE:
            EndDialog(hwndDlg, 0);
            return TRUE;

        case WM_COMMAND:
            switch(LOWORD(wParam))
            {
                case IDC_BTN_FILE:
                    filename = (char *)malloc(0x200);
                    filename[0] = 0;
                    ofn.lStructSize = sizeof(OPENFILENAMEA);
                    ofn.hwndOwner = hwndDlg;
                    ofn.hInstance = NULL;
                    ofn.lpstrCustomFilter = NULL;
                    ofn.lpstrFileTitle = NULL;
                    ofn.lpstrInitialDir = NULL;
                    ofn.pvReserved = NULL;
                    ofn.dwReserved = 0;
                    ofn.lpstrDefExt= ".dll";
                    ofn.lpstrTitle = "kikoolol";
                    ofn.lpstrFilter = "*.exe\x00";
                    ofn.lpstrFile = (LPSTR)filename;
                    ofn.nMaxFile = 0x200;
                    ofn.Flags = OFN_DONTADDTORECENT | OFN_FILEMUSTEXIST | OFN_EXTENSIONDIFFERENT;
                    if (GetOpenFileNameA(&ofn))
                        SetDlgItemTextA(hwndDlg,IDC_EDT_PATH,ofn.lpstrFile);
                    free(filename);
                    return TRUE;
                case IDC_BTN_QUIT:
                    EndDialog(hwndDlg, 0);
                    return TRUE;

                case IDC_BTN_UNP:
                    GetDlgItemTextA(hwndDlg,IDC_EDT_PATH,(LPSTR)path,MAX_PATH);

                    hFile = CreateFileA((LPCSTR)path, GENERIC_READ , FILE_SHARE_READ , NULL , OPEN_EXISTING , NULL , NULL);
                    if (hFile == INVALID_HANDLE_VALUE)
                    {
                        MessageBoxA(hwndDlg,"Echec lors de l'ouverture du fichier", NULL , MB_ICONERROR);
                        return 0;
                    }
                    hMapp = CreateFileMapping(hFile, NULL , PAGE_READONLY , 0 , 0 , NULL);
                    mapping = (char *)MapViewOfFile(hMapp,FILE_MAP_READ,0,0,0);
                    if (mapping == NULL)
                    {
                        MessageBoxA(hwndDlg,"Echec lors du mapping du fichier", NULL , MB_ICONERROR);
                        CloseHandle(hMapp);
                        CloseHandle(hFile);
                        return 0;
                    }
                    pDosHeader = (PIMAGE_DOS_HEADER)mapping;
                    if (pDosHeader->e_magic != 'ZM')
                    {
                        MessageBoxA(hwndDlg,"Dos header non valide", NULL , MB_ICONERROR);
                        CloseHandle(hMapp);
                        CloseHandle(hFile);
                        return 0;
                    }
                    pPE = (PIMAGE_NT_HEADERS)(pDosHeader->e_lfanew + mapping);
                    if (pPE->Signature != 'EP')
                    {
                        MessageBoxA(hwndDlg,"PE header non valide", NULL , MB_ICONERROR);
                        CloseHandle(hMapp);
                        CloseHandle(hFile);
                        return 0;
                    }
                    pSection = (PIMAGE_SECTION_HEADER)((PCHAR)pPE + sizeof(IMAGE_FILE_HEADER) + pPE->FileHeader.SizeOfOptionalHeader + sizeof(DWORD));
                    do
                    {
                        if (pSection->VirtualAddress == 0)
                        {
                            MessageBoxA(hwndDlg,"La signature .nah n'a pas été trouvé dans les noms des sections", NULL , MB_ICONINFORMATION);
                            CloseHandle(hMapp);
                            CloseHandle(hFile);
                            return 0;
                        }
                        if (*(PDWORD)pSection->Name == 'han.')
                            break;
                        pSection = (PIMAGE_SECTION_HEADER)((PCHAR)pSection + sizeof(IMAGE_SECTION_HEADER));
                    }
                    while (1);
                    CloseHandle(hMapp);
                    CloseHandle(hFile);


                    if (*(DWORD *)(VAToRaw(pPE->OptionalHeader.AddressOfEntryPoint,pPE)+mapping) != 0x87EC8B55 || *(WORD *)(VAToRaw(pPE->OptionalHeader.AddressOfEntryPoint,pPE)+mapping +4) != 0x5DEC)
                    {
                        MessageBoxA(hwndDlg,"La signature 0x55 0x8B 0xEC 0x87 0xEC 0x5D n'a pas été trouvé à l'entry point", NULL , MB_ICONINFORMATION);
                        return TRUE;
                    }

                    StartupInfo.cb = sizeof(STARTUPINFO);
                    StartupInfo.lpReserved = NULL;
                    StartupInfo.lpDesktop = NULL;
                    StartupInfo.lpTitle = NULL;
                    StartupInfo.dwFlags = NULL;
                    StartupInfo.cbReserved2 = 0;
                    StartupInfo.lpReserved2 = NULL;

                    if (CreateProcessA((LPCTSTR)path,NULL,NULL,NULL,FALSE,DEBUG_ONLY_THIS_PROCESS | DEBUG_PROCESS , NULL , NULL , &StartupInfo , &ProcessInfo) == 0)
                    {
                        MessageBoxA(hwndDlg,"La création du processus a échoué", NULL , MB_ICONINFORMATION);
                        return TRUE;
                    }
                    BaseAddress = InitDebug();
                    if (! BaseAddress)
                    {
                        MessageBoxA(hwndDlg,"L'initialisation du deboggage a échouée", NULL , MB_ICONINFORMATION);
                        return TRUE;
                    }
                    // on va d'abord a l'entry point de l'executable
                    Goto((pPE->OptionalHeader.AddressOfEntryPoint + BaseAddress),ProcessInfo.hThread);
                    // on break sur le VirtualAlloc
                    hModKern = GetModuleHandleA("Kernel32");
                    Goto((DWORD)GetProcAddress(hModKern,"VirtualAlloc"),ProcessInfo.hThread);
                    // on recupere l'addresse de retour du call VirtualAlloc ainsi que la taille de la futur page
                    GetThreadContext(ProcessInfo.hThread,&Context);
                    ReadProcessMemory(ProcessInfo.hProcess,(LPCVOID)Context.Esp,&RetnAdd,sizeof(DWORD),&NumberOfBytesRead);
                    if (NumberOfBytesRead != sizeof(DWORD))
                    {
                        MessageBoxA(hwndDlg,"ReadProcessMemory a échouée", NULL , MB_ICONINFORMATION);
                        return TRUE;
                    }
                    ReadProcessMemory(ProcessInfo.hProcess,(LPCVOID)(Context.Esp+8),&AllocSize,sizeof(DWORD),&NumberOfBytesRead);
                    if (NumberOfBytesRead != sizeof(DWORD))
                    {
                        MessageBoxA(hwndDlg,"ReadProcessMemory a échouée", NULL , MB_ICONINFORMATION);
                        return TRUE;
                    }

                    // on recupere la valeure de retour de VirtualAlloc
                    Goto(RetnAdd,ProcessInfo.hThread);
                    GetThreadContext(ProcessInfo.hThread,&Context);
                    addrAlloc = Context.Eax;

                    //on verifie des signatures
                    pJmpToOEP = RetnAdd+0x69;
                    pCallEdi = RetnAdd+0x45;

                    ReadProcessMemory(ProcessInfo.hProcess,(LPCVOID)(pJmpToOEP-2),&Sign,sizeof(DWORD),&NumberOfBytesRead);
                    if (NumberOfBytesRead != sizeof(DWORD))
                    {
                        MessageBoxA(hwndDlg,"ReadProcessMemory a échouée", NULL , MB_ICONINFORMATION);
                        return TRUE;
                    }
                    if(Sign != 0xE0FF5D5B )
                    {
                        MessageBoxA(hwndDlg,"Signature non conforme", NULL , MB_ICONINFORMATION);
                        return TRUE;
                    }

                    //on va jusqu'au call qui se chargera de resoudre les imports

                    Goto(pCallEdi,ProcessInfo.hThread);

                    //une fois qu'on est a ce call, la mémoire allouée a été remplie du code qui se chargera de resoudre les imports
                    //on peut donc la scanner a la recherche d'une signature
                    //on va pour ce faire dumper la page memoire en entier, sa taille etant constante, ca nous facilite le boulot ...
                    PackerMem = (PCHAR)VirtualAlloc(NULL,AllocSize,MEM_COMMIT | MEM_RESERVE,PAGE_READWRITE);
                    ReadProcessMemory(ProcessInfo.hProcess,(LPCVOID)addrAlloc,PackerMem,AllocSize,&NumberOfBytesRead);
                    if (NumberOfBytesRead != AllocSize)
                    {
                        MessageBoxA(hwndDlg,"ReadProcessMemory a échouée", NULL , MB_ICONINFORMATION);
                        return TRUE;
                    }

                    addrImportResolver = SearchSign(PackerSign,sizeof(PackerSign)-1, PackerMem ,AllocSize);
                    if (addrImportResolver == 0)
                    {
                        MessageBoxA(hwndDlg,"La recherche de la signature du resolveur d'import a echoué", NULL , MB_ICONINFORMATION);
                        return TRUE;
                    }
                    addrImportResolver += addrAlloc-(DWORD)PackerMem-5;
                    Goto(addrImportResolver,ProcessInfo.hThread);

                    //là le processus a fini de decrypté le code il nous reste a dumper le bouzin
                    // de plus l'addresse de l'IT se trouve dans Ecx
                    GetThreadContext(ProcessInfo.hThread,&Context);
                    addrIT = Context.Ecx - BaseAddress;
                    Dump = DumpProcess(ProcessInfo.hProcess,(char*)BaseAddress);
                    if (! Dump)
                    {
                        MessageBoxA(hwndDlg,"Le dump a echoué", NULL , MB_ICONINFORMATION);
                        return TRUE;
                    }

                    Goto(pJmpToOEP,ProcessInfo.hThread);
                    GetThreadContext(ProcessInfo.hThread,&Context);
                    addrOEP = Context.Eax - BaseAddress;

                    pDosHeader = (PIMAGE_DOS_HEADER)Dump;
                    pPE = (PIMAGE_NT_HEADERS)(pDosHeader->e_lfanew + Dump);
                    pPE->OptionalHeader.AddressOfEntryPoint = addrOEP;
                    pPE->OptionalHeader.DataDirectory[1].VirtualAddress = addrIT;
                    DumpSize = RebuildDump(Dump);
                    pPE->OptionalHeader.DataDirectory[1].Size = DumpSize;
                    UnmapViewOfFile(mapping);

                    hFile = CreateFileA("unpacked.exe", GENERIC_ALL , 0 , NULL , CREATE_ALWAYS , NULL , NULL);
                    WriteFile(hFile,Dump,DumpSize,&NumberOfBytesWritten,NULL);
                    CloseHandle(hFile);
                    if (NumberOfBytesWritten != DumpSize)
                    {
                        MessageBoxA(hwndDlg,"L'écriture de l'executable unpacké a echoué", NULL , MB_ICONINFORMATION);
                        return TRUE;
                    }
                    MessageBoxA(hwndDlg,"L'écriture de l'executable unpacké a réussi !", NULL , MB_ICONINFORMATION);
                    VirtualFree(Dump,0,MEM_RELEASE);
                    TerminateProcess(ProcessInfo.hProcess,0);
                    return TRUE;
            }
    }

    return FALSE;
}

PCHAR DumpProcess(HANDLE hProcess,char* BaseAddress)
{
    DWORD AllocSize = 0;
    char* Dump;
    IMAGE_DOS_HEADER DosHeader;
    IMAGE_NT_HEADERS PE;
    PIMAGE_SECTION_HEADER pSectionHeaders;
    DWORD i=0;
    DWORD SectionHeadersSize,NumberOfBytesRead;

    ReadProcessMemory(hProcess,BaseAddress,&DosHeader,sizeof(IMAGE_DOS_HEADER),&NumberOfBytesRead);
    if (NumberOfBytesRead != sizeof(IMAGE_DOS_HEADER))
        return 0;
    ReadProcessMemory(hProcess,BaseAddress + DosHeader.e_lfanew,&PE,sizeof(IMAGE_NT_HEADERS),&NumberOfBytesRead);
    if (NumberOfBytesRead != sizeof(IMAGE_NT_HEADERS))
        return 0;
    SectionHeadersSize = sizeof(IMAGE_NT_HEADERS)*PE.FileHeader.NumberOfSections;
    pSectionHeaders = (PIMAGE_SECTION_HEADER)malloc(SectionHeadersSize);
    ReadProcessMemory(hProcess,BaseAddress + DosHeader.e_lfanew + sizeof(IMAGE_FILE_HEADER) + PE.FileHeader.SizeOfOptionalHeader + sizeof(DWORD),pSectionHeaders,SectionHeadersSize,&NumberOfBytesRead);
    if (NumberOfBytesRead != SectionHeadersSize)
    {
        free(pSectionHeaders);
        return 0;
    }

    while ((pSectionHeaders+i+1)->VirtualAddress != 0)
        i ++;

    AllocSize = (pSectionHeaders+i)->VirtualAddress + (pSectionHeaders+i)->Misc.VirtualSize;
    free(pSectionHeaders);

    Dump = (char *)VirtualAlloc(NULL,AllocSize,MEM_COMMIT | MEM_RESERVE,PAGE_READWRITE);

    ReadProcessMemory(hProcess,BaseAddress,Dump,AllocSize,&NumberOfBytesRead);
    if (NumberOfBytesRead != AllocSize)
        return 0;
    return Dump;
}

DWORD RebuildDump(char* Dump)
{
    PIMAGE_DOS_HEADER pDosHeader;
    PIMAGE_NT_HEADERS pPE;
    PIMAGE_SECTION_HEADER pSection;
    PIMAGE_IMPORT_DESCRIPTOR IT;
    DWORD curseur,i;

    //il faut d'abord recopier la table des FirstChunk
    pDosHeader = (PIMAGE_DOS_HEADER)Dump;
    pPE = (PIMAGE_NT_HEADERS)(Dump+pDosHeader->e_lfanew);
    pSection = (PIMAGE_SECTION_HEADER)((PCHAR)pPE + sizeof(IMAGE_FILE_HEADER) + pPE->FileHeader.SizeOfOptionalHeader + sizeof(DWORD));
   /* for (IT = (PIMAGE_IMPORT_DESCRIPTOR)(pPE->OptionalHeader.DataDirectory[1].VirtualAddress + Dump);IT->Characteristics != 0;IT++)
        for (i=0;*(PDWORD)(IT->OriginalFirstThunk + Dump + i) != 0 ; i+=4)
            *(PDWORD)(IT->FirstThunk + Dump + i) = *(PDWORD)(IT->OriginalFirstThunk + Dump + i);
*/
    curseur = pPE->OptionalHeader.SizeOfHeaders;
    //on copie maintenant les sections
    while ((pSection)->VirtualAddress != 0)
    {
        CopyMemory(Dump+curseur,Dump+pSection->VirtualAddress,pSection->Misc.VirtualSize);
        curseur += pSection->Misc.VirtualSize;
        while(Dump[curseur] == 0)
            curseur --;
        curseur = AlignSize(curseur,pPE->OptionalHeader.FileAlignment);
        pSection->SizeOfRawData = curseur - pSection->PointerToRawData;
        pSection ++;
    }
    // on efface le dernier section header
   /* for(i=0;i!=sizeof(IMAGE_SECTION_HEADER)/4;i++)
        (((PDWORD)pSection)[i]) = 0;
    pPE->FileHeader.NumberOfSections --;*/
    return curseur;
}

DWORD AlignSize(DWORD size, DWORD alignement)
{
    return (size%alignement == 0) ? size : ((size / alignement) +1)*alignement;
}

DWORD InitDebug(void)
{
    HANDLE hThread;
    CONTEXT Context;
    DWORD BaseAddress;

    Context.ContextFlags = CONTEXT_ALL;

    while(WaitForDebugEvent(&DbgEvt,INFINITE))
    {
        switch (DbgEvt.dwDebugEventCode)
        {
            case CREATE_PROCESS_DEBUG_EVENT:
                hThread = DbgEvt.u.CreateProcessInfo.hThread;

                BaseAddress = (DWORD)DbgEvt.u.CreateProcessInfo.lpBaseOfImage;

                //on créé une petite exception single step en armant le TrapFlag
                GetThreadContext(hThread,&Context);
                Context.EFlags |= 0x100;
                SetThreadContext(hThread,&Context);

                ContinueDebugEvent(DbgEvt.dwProcessId,DbgEvt.dwThreadId,DBG_CONTINUE);
                break;

            case EXCEPTION_DEBUG_EVENT:
                if (DbgEvt.u.Exception.ExceptionRecord.ExceptionCode != EXCEPTION_SINGLE_STEP)
                {
                    ContinueDebugEvent(DbgEvt.dwProcessId,DbgEvt.dwThreadId,DBG_EXCEPTION_NOT_HANDLED);
                    break;
                }
                return BaseAddress;
                break;

            default:
                ContinueDebugEvent(DbgEvt.dwProcessId,DbgEvt.dwThreadId,DBG_CONTINUE);
                break;
        }

    }
    return 0;
}

int Goto(DWORD addr,HANDLE hThread)
{
    CONTEXT Context;
    int RetnValue;

    Context.ContextFlags = CONTEXT_ALL;

    GetThreadContext(hThread,&Context);
    Context.Dr0 = addr;
    Context.Dr7 |= DR7flag(OneByteLength,BreakOnExec,GlobalFlag | LocalFlag,0);
    SetThreadContext(hThread,&Context);
    RetnValue = WaitForSingleStepExc();
    GetThreadContext(hThread,&Context);
    Context.Dr0 = 0;
    Context.Dr7 = 0;
    SetThreadContext(hThread,&Context);
    if (! RetnValue)
        return 0;
    else
        return 1;
}

int WaitForSingleStepExc(void)
{
    ContinueDebugEvent(DbgEvt.dwProcessId,DbgEvt.dwThreadId,DBG_CONTINUE);
    while(WaitForDebugEvent(&DbgEvt,INFINITE))
    {
        if (DbgEvt.dwDebugEventCode == EXCEPTION_DEBUG_EVENT)
        {
            if (DbgEvt.u.Exception.ExceptionRecord.ExceptionCode == EXCEPTION_SINGLE_STEP)
                return 1;
            else if (DbgEvt.u.Exception.ExceptionRecord.ExceptionCode == EXCEPTION_BREAKPOINT)
                ContinueDebugEvent(DbgEvt.dwProcessId,DbgEvt.dwThreadId,DBG_CONTINUE);
            else
                ContinueDebugEvent(DbgEvt.dwProcessId,DbgEvt.dwThreadId,DBG_EXCEPTION_NOT_HANDLED);
        }
        else
            ContinueDebugEvent(DbgEvt.dwProcessId,DbgEvt.dwThreadId,DBG_CONTINUE);
    }
    return 0;
}


DWORD VAToRaw(DWORD VA,PIMAGE_NT_HEADERS pPE)
{
    PIMAGE_SECTION_HEADER pSection;

    pSection = (PIMAGE_SECTION_HEADER)((PCHAR)pPE + sizeof(IMAGE_FILE_HEADER) + pPE->FileHeader.SizeOfOptionalHeader + sizeof(DWORD));

    do
    {
        if (pSection->VirtualAddress == 0)
            return 0;

        if ((pSection->VirtualAddress <= VA) && ((pSection->VirtualAddress + pSection->SizeOfRawData) >= VA))
            return (VA - pSection->VirtualAddress + pSection->PointerToRawData);
        pSection = (PIMAGE_SECTION_HEADER)((PCHAR)pSection + sizeof(IMAGE_SECTION_HEADER));
    }
    while (1);
}

int APIENTRY WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nShowCmd)
{
    hInst = hInstance;

    // The user interface is a modal dialog box
    return DialogBox(hInstance, MAKEINTRESOURCE(DLG_MAIN), NULL, DialogProc);
}

