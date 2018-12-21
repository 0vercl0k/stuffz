#include <windows.h>
#include <stdio.h>
#define USAGE "usage : ./%s <serial>\n\n"

typedef void (*INTER)(char*);

int main(int argc , char* argv[])
{
    HINSTANCE pLib = LoadLibrary("MiniVMPar0vercl0k.dll") , pLib2 = LoadLibrary("user32.dll");
    INTER interprete;

    if( pLib == NULL || !argv[1] || pLib2 == NULL)
    {
        printf(USAGE , argv[0]);
        return 0;
    }

    char* good = "good boy.";
    char* bad  = "bad boy.";

    char code[] = "\x15\x00\xFF\xFF\xFF\xFF\x19\x01\x00\x15\x02\x74\x00\x00\x00\x26"
    "\x01\x02\x24\xAA\xAA\xAA\xAA\x12\x00\x19\x01\x00\x15\x02\x61\x00\x00\x00\x26\x01"
    "\x02\x24\xAA\xAA\xAA\xAA\x12\x00\x19\x01\x00\x15\x02\x70\x00\x00\x00\x26\x01\x02"
    "\x24\xAA\xAA\xAA\xAA\x12\x00\x19\x01\x00\x15\x02\x7a\x00\x00\x00\x26\x01\x02\x24"
    "\xAA\xAA\xAA\xAA\x23\xAA\xAA\xAA\xAA\x00\x00\x00\x00\xFF\xFF\xFF\xFF\xEE\xEE\xEE"
    "\xEE\x00\x00\x00\x00\x25\x23\xAA\xAA\xAA\xAA\x00\x00\x00\x00\xFF\xFF\xFF\xFF\xEE"
    "\xEE\xEE\xEE\x00\x00\x00\x00";


    long ptr4 = (long)code + 102;
    long addrMessageBox = (long)GetProcAddress(pLib2 , "MessageBoxA");

    memcpy((void*)(code+2),&argv[1],4);  //adresse de la chaine entré en argument (argv[1])

    memcpy((void*)(code+19),&ptr4,4); //adresse de l'instru messagebox "bad boy"
    memcpy((void*)(code+38),&ptr4,4); //adresse de l'instru messagebox "bad boy"
    memcpy((void*)(code+57),&ptr4,4); //adresse de l'instru messagebox "bad boy"
    memcpy((void*)(code+76),&ptr4,4); //adresse de l'instru messagebox "bad boy"

    memcpy((void*)(code+81),&addrMessageBox,4); //adresse de messageboxa
    memcpy((void*)(code+103),&addrMessageBox,4); //adresse de messageboxa

    memcpy((void*)(code+89),&good,4);     //adresse de la chaine "good boy"
    memcpy((void*)(code+93),&good,4);     //adresse de la chaine "good boy"

    memcpy((void*)(code+111),&bad,4);     //adresse de la chaine "bad boy"
    memcpy((void*)(code+115),&bad,4);     //adresse de la chaine "bad boy"



    interprete = (INTER)GetProcAddress(pLib , "interprete0vercl0kLanguage" );
    printf("[+] Adresse de la fonction : %p.\n", interprete);

    interprete(code);

    FreeLibrary(pLib);
    return 0;
}
