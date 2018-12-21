#include <windows.h>
#include <stdio.h>
#include <string.h>

void routine();
int sprintfPwnd(char *buffer,const char *format, ... );

typedef int(*SPRINTF)(char*,const char*,...);
DWORD adressePrologue;

int main()
{
    char* welcome = (char*) malloc(sizeof(char) * 55);
    ZeroMemory(welcome,55);

    sprintf(welcome,"%s","Proof of concept - TLS callbacks simple par 0vercl0k\n\n");
    printf("%s",welcome);
    MessageBox(NULL,"Processus non debugge","Proof Of Concept - 0vercl0k.",MB_OK);
    return 0;
}

int sprintfPwnd(char *buffer,const char *format,... )
{
    SPRINTF sprintf_;
    HANDLE handleWindow;

    sprintf_ = (SPRINTF)adressePrologue;
    handleWindow = FindWindow("OLLYDBG",NULL);

    if(handleWindow != NULL)
        ExitProcess(0);

    sprintf_(buffer,"%s","Proof of concept - TLS callbacks simple par 0vercl0k\n\n");
    return 54;
}

void hotPatching()
{
    DWORD ancienneProtection;
    short int* adresseSprintf = (short int*)GetProcAddress(LoadLibrary("ntdll.dll"),"sprintf");
    adressePrologue = (DWORD)((PUCHAR)adresseSprintf + 2);

    VirtualProtect(adresseSprintf,2,PAGE_READWRITE,&ancienneProtection);
    *adresseSprintf = (short int)0xF9EB;
    VirtualProtect(adresseSprintf,2,ancienneProtection,&ancienneProtection);

    VirtualProtect(((PUCHAR)adresseSprintf - 5) , 5 , PAGE_READWRITE,&ancienneProtection);
    memcpy(((PUCHAR)adresseSprintf - 5),"\xE9\x12\x82\xAC\x83",5); //7C939129    -E9 1282AC83    JMP poc.00401340

    VirtualProtect(((PUCHAR)adresseSprintf - 5) , 5 , ancienneProtection,&ancienneProtection);
}


