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
#ifndef HOOKING_HPP
#define HOOKING_HPP

#include "platform.h"

#include <windows.h>

/* Custom types */
// ntdll.KiUserExceptionDispatcher signature
typedef VOID (NTAPI *KiUserExceptionDispatcher_t)(PEXCEPTION_RECORD ExceptionRecord, PCONTEXT Context);

// kernel32.UnhandledExceptionFilter signature
// typedef LONG (WINAPI *UnhandledExceptionFilter_t)(struct _EXCEPTION_POINTERS *ExceptionInfo);

/* Function declaration */
// The hook of KiUserExceptionDispatcher: it aims to log all the exception happening in the process
VOID NTAPI KiUserExceptionDispatcher(PEXCEPTION_RECORD ExceptionRecord, PCONTEXT Context);

// Set the hook via the detours API
VOID SetHook();

// Unset the hook via the detours API
VOID UnsetHook();

#endif