#ifndef _TOOLBOX_
#define _TOOLBOX

#include <windows.h>
#include <stdio.h>

#define SUCCESS 0
#define FAIL    1

#define IsASuccess(x) (x == SUCCESS)
#define IsAFailure(x) (x == FAIL)

#define _DBG_(x)    printf("[DEBUG] %s\r\n", x)
#define _ERROR_()   { printf("[ERROR] An error occured in %s|%d : GetLastError() = 0x%x.\r\n", __FILE__, __LINE__, (unsigned int)GetLastError()); return FAIL; }
#define _ERROR1_(x) { printf("[ERROR] An error occured '%s'.\r\n", x); return FAIL; }


#endif
