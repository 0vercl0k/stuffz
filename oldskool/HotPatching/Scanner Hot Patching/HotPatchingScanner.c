#include <stdio.h>
#include <windows.h>
#include <string.h>
#define USAGE "./%s [-all|-one] <api> <dll>\n\n"
int ScanUneApi(char* nomApi,char* nomDll);
int ScanApisDll(char* nomDll);

int main(int argc, char* argv[])
{
    if( argc < 3 )
    {
        printf(USAGE,argv[0]);
        return 0;
    }
    printf("Hot Patching scanner par 0vercl0k -[ http://0vercl0k.blogspot.com .\n");

    if(!strcmp(argv[1],"-one") && argc == 4)
    {
        printf("Scan de votre api.\n");
        if(ScanUneApi(argv[2],argv[3]) == 1)
        {
            printf("Votre api est hot-patchable.\n");
            return 1;
        }
    }
    else if(!strcmp(argv[1],"-all") && argc == 3)
        ScanApisDll(argv[2]);
    else
        printf(USAGE,argv[0]);

    return 0;
}

int ScanUneApi(char* nomApi,char* nomDll)
{
    PUCHAR adresseFonction = 0;
    HANDLE handleLib = LoadLibrary(nomDll);
    int i;

    if(handleLib == NULL)
        return 0;

    adresseFonction = (PUCHAR) GetProcAddress((HINSTANCE)handleLib,nomApi);

    if(adresseFonction == NULL)
        return 0;

    //printf("- Scan de votre api.\n");

    if( *(PUSHORT)adresseFonction == 0xFF8B )
    {
       adresseFonction -= 5;
        for( i = 0 ; i < 5 ; i++)
        {
            if( *(adresseFonction + i) != 0x90 )
                return 0;
        }
        //printf("Votre api est hot-patchable.\n"); //HotPatchingScanner.exe MessageBoxA user32.dll
        return 1;
    }
    //printf("Votre api est unhot-patchable.\n"); //HotPatchingScanner.exe ZwWaitForSingleObject ntdll.dll
    return 0;
}

int ScanApisDll(char* nomDll)
{
    HANDLE handleDll = LoadLibrary(nomDll);
    PIMAGE_DOS_HEADER ptrDosHeader;
    PIMAGE_EXPORT_DIRECTORY ptrExportDirectory;
    PCHAR ptrTableauRVA;
    char* nomFonction;
    int i,j,nombreName;

    if(handleDll == NULL)
        return 0;

    ptrDosHeader = (PIMAGE_DOS_HEADER)handleDll;
    ptrExportDirectory = (PIMAGE_EXPORT_DIRECTORY)( ((PUCHAR)(((PIMAGE_NT_HEADERS)((PUCHAR)ptrDosHeader + ptrDosHeader->e_lfanew))->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_EXPORT].VirtualAddress)) + (DWORD)handleDll );
    ptrTableauRVA = (PCHAR)ptrExportDirectory->AddressOfNames + (DWORD)handleDll;
    nombreName = ptrExportDirectory->NumberOfNames;

    for(i = 0 ; i < nombreName ; i++)
    {
        nomFonction = (PCHAR)((*((PULONG)ptrTableauRVA + i)) + (DWORD)handleDll);
        if(ScanUneApi(nomFonction,nomDll) == 1)
        {
            printf("-Api '%s' hot-patchable.\n",nomFonction);
            j++;
        }
    }
    printf("Soit un total de %d apis sur %d d'hot-patchable dans la librarie '%s' (%d%%).\n",j,nombreName,nomDll,((j*100)/nombreName));
    return 1;
}
