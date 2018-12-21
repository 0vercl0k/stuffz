#include <windows.h>
#define DLLEXPORT __declspec (dllexport)

void doTheFuckingStuff()
{
       MessageBox(NULL, "BEEP IZ EVIL", "BEEP IZ EVIL", MB_OK);
       return;
}

DLLEXPORT BOOL _stdcall _Beep(DWORD a, DWORD b)
{
          doTheFuckingStuff();
          return Beep(a,b);
}
