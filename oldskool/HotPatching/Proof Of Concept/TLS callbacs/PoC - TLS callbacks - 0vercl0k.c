#include <windows.h>
#include <stdio.h>

void routine();


int main()
{
    printf("%s","Proof of concept - TLS callbacks simple par 0vercl0k\n\n");
    MessageBox(NULL,"Processus non debugge","Proof Of Concept - 0vercl0k.",MB_OK);
    return 0;
}

void callback()
{
    PIMAGE_DOS_HEADER imgDosHeader;
    PIMAGE_NT_HEADERS imgNtHeader;

    imgDosHeader = (PIMAGE_DOS_HEADER)(GetModuleHandle(NULL));
    imgNtHeader = (PIMAGE_NT_HEADERS)((PUCHAR)imgDosHeader + imgDosHeader->e_lfanew);

    PUCHAR entryPoint = (PUCHAR)imgDosHeader + (imgNtHeader->OptionalHeader.AddressOfEntryPoint);

    if(*entryPoint == 0xCC)
        ExitProcess(0);
}


