#include <windows.h>
#include <stdio.h>

int main()
{
    LoadLibrary("user32.dll");

    printf("Understand phook's internals par 0vercl0k.\n");

    __asm("int3;");

    //Test d'un api o� l'on d�finit des actions suppl�mentaires
    Beep( 750, 300 );

    //Un api simplement redirig�
    GetProcAddress(GetModuleHandle("user32.dll"), "MessageBoxA");

    return 0;
}
