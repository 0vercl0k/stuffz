/*
    ___________.__               _________              __  .__              .__   
    \__    ___/|  |__   ____    /   _____/ ____   _____/  |_|__| ____   ____ |  |  
      |    |   |  |  \_/ __ \   \_____  \_/ __ \ /    \   __\  |/    \_/ __ \|  |  
      |    |   |   Y  \  ___/   /        \  ___/|   |  \  | |  |   |  \  ___/|  |__
      |____|   |___|  /\___  > /_______  /\___  >___|  /__| |__|___|  /\___  >____/
                    \/     \/          \/     \/     \/             \/     \/  

    Copyright (C) 2012 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
*/
#include "hooking.hpp"
#include "exception.hpp"

#include <detours.h>

/* Global variable */
// The address of the real ntdll.KiUserExceptionDispatcher
KiUserExceptionDispatcher_t TrueKiUserExceptionDispatcher = (KiUserExceptionDispatcher_t)DetourFindFunction(
    "ntdll.dll",
    "KiUserExceptionDispatcher"
);

// The address of the real kernel32.UnhandledExceptionFilter
// UnhandledExceptionFilter_t TrueUnhandledExceptionFilter = (UnhandledExceptionFilter_t)DetourFindFunction(
//    "kernel32.dll",
//    "UnhandledExceptionFilter"
// );

extern CRITICAL_SECTION critical_section;

// LONG WINAPI UnhandledExceptionFilter_(struct _EXCEPTION_POINTERS *ExceptionInfo)
// {
//     /* If we reached there, it is a good (good for us, bad for the coder/program :)) sign, report it! */
//     EnterCriticalSection(&critical_section);
//     log_exception(ExceptionInfo->ExceptionRecord, ExceptionInfo->ContextRecord);
//     LeaveCriticalSection(&critical_section);

//     TerminateProcess(GetCurrentProcess(), 0);
//     return 0;
// }

VOID __declspec(naked) NTAPI KiUserExceptionDispatcher(PEXCEPTION_RECORD ExceptionRecord, PCONTEXT Context)
{
    /* Taken from the Excep's detours sample */
    __asm
    {
        xor     eax, eax                ; // Create fake return address on stack.
        push    eax                     ; // (Generally, we are called by the kernel.)

        push    ebp                     ; // Prolog
        mov     ebp, esp                ;
        sub     esp, __LOCAL_SIZE       ;
    }

    EnterCriticalSection(&critical_section);
    log_exception(ExceptionRecord, Context);
    LeaveCriticalSection(&critical_section);
    
    __asm
    {
        mov     ebx, ExceptionRecord    ;
        mov     ecx, Context            ;
        push    ecx                     ;
        push    ebx                     ;
        mov     eax, [TrueKiUserExceptionDispatcher];
        jmp     eax                     ;
        //
        // The above code should never return.
        //
        int     3                       ; // Break!
        mov     esp, ebp                ; // Epilog
        pop     ebp                     ;
        ret                             ;
    }
}

VOID SetHook()
{
    DetourTransactionBegin();
            
    DetourUpdateThread(GetCurrentThread());
    DetourAttach(
        (PVOID*)&TrueKiUserExceptionDispatcher,
        KiUserExceptionDispatcher 
    );
    
    /*
        Imagine a process with a stack-buffer overflow protected by the GS Cookie.
        The stack frame is overunned, security_check_cookie is called, it detects something wrong,
        it calls report_gs_failure, and it kills your process.

        -> You've missed one interesting (?) bug.
    
        Solution:
        Hook the kernel32.UnhandledExceptionFilter (will be called by _report_gs_failure or by the program itself (?) but only if everything goes wrong, so good for us.)

        Update: That doesn't work anymore cf http://doar-e.github.io/blog/2013/10/12/having-a-look-at-the-windows-userkernel-exceptions-dispatcher/
    */
    // DetourAttach(
    //     (PVOID*)&TrueUnhandledExceptionFilter,
    //     UnhandledExceptionFilter_
    // );

    DetourTransactionCommit();
}

VOID UnsetHook()
{
    DetourTransactionBegin();

    DetourUpdateThread(GetCurrentThread());
    DetourDetach(
        (PVOID*)&TrueKiUserExceptionDispatcher,
        KiUserExceptionDispatcher
    );
    
    // DetourDetach(
    //     (PVOID*)&TrueUnhandledExceptionFilter,
    //     UnhandledExceptionFilter_
    // );

    DetourTransactionCommit();
}