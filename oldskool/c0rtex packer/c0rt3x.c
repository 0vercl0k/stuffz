#include <windows.h>
#include <string.h>
#include <stdio.h>

int main(int argc, char* argv[])
{
    /* Déclaration variables */

    int nbrSection,i;

    HANDLE handleBin,handleBinMappingObject,handleBinMappe;
    PUCHAR imgBase;

    DWORD entryPoint,offsetLoader,adresseBaseSection1;
    PDWORD adresseFinSection;
    PUCHAR adresseDebutSection1Raw,adresseFinSection1Raw;

    PIMAGE_DOS_HEADER      imgDosHeader;
    PIMAGE_NT_HEADERS      imgNtHeader;
    PIMAGE_SECTION_HEADER  imgSectionHeader;

    char loader[] = {

        0xB8 , 0x00 , 0x00 , 0x00 , 0x00 , //MOV EAX,00000000 adresse complete du point d'entré.
        0xBE , 0x00 , 0x00 , 0x00 , 0x00 , //MOV ESI,00000000 l'offset.
        0xBF , 0x00 , 0x00 , 0x00 , 0x00 , //MOV EDI,00000000 la premiere section.
        0xEB , 0x05 , //JMP SHORT loader.00401012
        0x4E , //DEC ESI
        0x80 , 0x34 , 0x37 , 0x13 , //XOR BYTE PTR DS:[EDI+ESI],13
        0x0B , 0xF6 , //OR ESI,ESI
        0x75 , 0xF7 , //JNZ SHORT loader.0040100D
        0xFF , 0xE0 ,//JMP EAX
        0x00 , 0x13 , 0x37 , 0x00 //signature
                        };

    /*                       */
    /* File mapping */

    handleBin = CreateFile(argv[1] , GENERIC_ALL , FILE_SHARE_READ|FILE_SHARE_WRITE , NULL , OPEN_EXISTING , 0 , 0);
    handleBinMappingObject = CreateFileMapping(handleBin , NULL , PAGE_READWRITE , 0 , 0 , NULL);
    handleBinMappe = MapViewOfFile(handleBinMappingObject , FILE_MAP_ALL_ACCESS , 0 ,0 , 0);

    if(handleBinMappe == NULL)
        return 0;

    /*              */


    printf("C0rt3x packer par 0vercl0k.\n\n");

    imgDosHeader = (PIMAGE_DOS_HEADER)handleBinMappe;

    if(imgDosHeader->e_magic != IMAGE_DOS_SIGNATURE)//'MZ'
        return 0;

    imgNtHeader = (PIMAGE_NT_HEADERS)((PUCHAR)imgDosHeader + imgDosHeader->e_lfanew);

    if(imgNtHeader->Signature != IMAGE_NT_SIGNATURE)
        return 0;

    imgBase = (PUCHAR)imgNtHeader->OptionalHeader.ImageBase;

    printf("- PE valide.\n");

    nbrSection = imgNtHeader->FileHeader.NumberOfSections;
  
    printf("- Loading sections.\n");

    /* test */

    PDWORD adresseIAT = (PDWORD)((PUCHAR)imgNtHeader + imgNtHeader->OptionalHeader.DataDirectory[1].VirtualAddress);
    int size = imgNtHeader->OptionalHeader.DataDirectory[1].Size / sizeof(IMAGE_IMPORT_DESCRIPTOR);
    printf("%d apis loaded.\n",size);

    /*      */

    imgSectionHeader        = (PIMAGE_SECTION_HEADER)((PUCHAR)imgNtHeader + sizeof(IMAGE_NT_HEADERS));

    if( *(PDWORD)((PUCHAR)handleBinMappe + imgSectionHeader->PointerToRawData + imgSectionHeader->SizeOfRawData - 8) == 0x00371300 )
    {
        printf("\nSignature presente, package impossible.\n");
        return 0;
    }

    printf("- Ajout du flag +write sur la 1ere section.\n");

    *(&imgSectionHeader->Characteristics) = (imgSectionHeader->Characteristics) | IMAGE_SCN_MEM_WRITE;

    adresseFinSection          = (PDWORD)((PUCHAR)handleBinMappe + imgSectionHeader->PointerToRawData + imgSectionHeader->SizeOfRawData - 4);
    adresseDebutSection1Raw    = (PUCHAR)handleBinMappe + imgSectionHeader->PointerToRawData;
    adresseFinSection1Raw      = (PUCHAR)handleBinMappe + imgSectionHeader->PointerToRawData + imgSectionHeader->SizeOfRawData;

    /* Infos Loader */

    offsetLoader            = (DWORD)(imgSectionHeader->Misc.VirtualSize );
    adresseBaseSection1     = (DWORD)((PUCHAR)imgBase + imgSectionHeader->VirtualAddress);
    entryPoint              = (DWORD)(imgBase + imgNtHeader->OptionalHeader.AddressOfEntryPoint);

    /*             */

    printf("- Scan de la premiere section a la recherche de place pour implenter le loader.\n\n");

    for( i = 0 ; i < (int)(sizeof(loader)/4) ; i++)
    {
        printf(".");
        if(*adresseFinSection != 0)
            return 0;
        adresseFinSection--;
    }

    printf("\n\nEspace Ok.\n");
    printf("- Encryptage de la 1ere section..\n");
    for(  ; adresseDebutSection1Raw < adresseFinSection1Raw ; adresseDebutSection1Raw++)
        *adresseDebutSection1Raw ^= 0x13;

    printf("- Generation du loader.\n");

    /* Génération du loader */

    memcpy((void*)&loader[1],&entryPoint,4);
    memcpy((void*)&loader[6],&offsetLoader,4);
    memcpy((void*)&loader[11],&adresseBaseSection1,4);

    /*                      */

    printf("- Ecriture du loader.\n");

    for(i = 0 ; i < (int)sizeof(loader) ; i++)
        *((PUCHAR)adresseFinSection+i) = loader[i];

    printf("- Redirection du point d'entre.\n");

    /* EntryPoint = Section1.VirtualAddress + OffsetLoader */

    *(&imgNtHeader->OptionalHeader.AddressOfEntryPoint) = (DWORD)(imgSectionHeader->VirtualAddress + (((PUCHAR)adresseFinSection - (DWORD)handleBinMappe - imgSectionHeader->PointerToRawData)));


    /*                                                     */


    printf("Executable Packe avec succes.\n");


    /* Clean */

    UnmapViewOfFile(handleBinMappe);
    CloseHandle(handleBinMappingObject);

    /*       */

    return 1;
}
