/*
    ___________.__               _________              __  .__              .__   
    \__    ___/|  |__   ____    /   _____/ ____   _____/  |_|__| ____   ____ |  |  
      |    |   |  |  \_/ __ \   \_____  \_/ __ \ /    \   __\  |/    \_/ __ \|  |  
      |    |   |   Y  \  ___/   /        \  ___/|   |  \  | |  |   |  \  ___/|  |__
      |____|   |___|  /\___  > /_______  /\___  >___|  /__| |__|___|  /\___  >____/
                    \/     \/          \/     \/     \/             \/     \/  
                    ExceptionMonitorDll - This dll is injected by the process spawner part
                    of the project in order to perform the exception monitoring.

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
#include "main.hpp"
#include "hooking.hpp"
#include "config.hpp"

#include <detours.h>

CRITICAL_SECTION critical_section = {0};

/*
   Some useful links:
       * http://openrce-snippets.googlecode.com/svn-history/r27/trunk/standalone/ExcpHook/src/ExcpHook.cpp
       * http://www.piotrbania.com/all/efilter/efilter.c
*/

DWORD WINAPI sleeping_thread(LPVOID lpParameter)
{
    Sleep(SLEEP_TIMEOUT);

    // Time to kill the process man, but be sure the second thread isn't writing the report!
    EnterCriticalSection(&critical_section);

    // BRAAAAA
    TerminateProcess(GetCurrentProcess(), 0);
    return 0;
}

__declspec(dllexport) BOOL __stdcall DllMain(
  _In_  HINSTANCE hinstDLL,
  _In_  DWORD fdwReason,
  _In_  LPVOID lpvReserved
)
{
    switch(fdwReason) 
    { 
        case DLL_PROCESS_ATTACH:
        {
            // Set the hook on ntdll.KiUserExceptionDispatch
            DetourRestoreAfterWith();
            SetHook();

            DWORD tid = 0;

            // Initialize the critical section which be used to synchronize
            InitializeCriticalSection(&critical_section);

            // Creating the sleeping thread
            CreateThread(
                NULL,
                0,
                sleeping_thread,
                NULL,
                0,
                &tid
            );

            break;
        }

        case DLL_PROCESS_DETACH:
        {  
            UnsetHook();
            break;
        }
    }

    return TRUE;  // Successful DLL_PROCESS_ATTACH.
}