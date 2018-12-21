#include <windows.h>
#include <stdio.h>
#include <tlhelp32.h>
#include <string.h>

typedef int(*MSGBOX)(HWND,LPCTSTR,LPCTSTR,UINT);
int MessageBox_pwnd(HWND hWnd,LPCTSTR lpText,LPCTSTR lpCaption,UINT uType);
DWORD adressePrologue;
void hotPatchingInTls();


int main(int argc,char* argv[])
{
    MessageBox(NULL,"test","test",MB_OK);
    return 0;
}

int MessageBox_pwnd(HWND hWnd,LPCTSTR lpText,LPCTSTR lpCaption,UINT uType)
{
    MSGBOX MessageBox_true;
    MessageBox_true = (MSGBOX)adressePrologue;

    return MessageBox_true(NULL,"lolz","lolz",MB_OK);
}

void hotPatchingInTls()
{
    DWORD ancienneProtection;
    short int* adresseMessageBoxA = (short int*)GetProcAddress(LoadLibrary("user32.dll"),"MessageBoxA");
    adressePrologue = (DWORD)((PUCHAR)adresseMessageBoxA + 2); // on passe outre du mov edi,edi, ou maintenant notre short jmp

    VirtualProtect(adresseMessageBoxA,2,PAGE_READWRITE,&ancienneProtection);
    *adresseMessageBoxA = (short int)0xF9EB;
    VirtualProtect(adresseMessageBoxA,2,ancienneProtection,&ancienneProtection);

    VirtualProtect(((PUCHAR)adresseMessageBoxA - 5) , 5 , PAGE_READWRITE,&ancienneProtection);
    memcpy(((PUCHAR)adresseMessageBoxA - 5),"\xE9\x5E\x0D\x03\x82",5);
    VirtualProtect(((PUCHAR)adresseMessageBoxA - 5) , 5 , ancienneProtection,&ancienneProtection);
}
