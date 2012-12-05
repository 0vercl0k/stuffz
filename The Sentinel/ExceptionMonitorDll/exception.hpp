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
#ifndef EXCEPTION_HPP
#define EXCEPTION_HPP

#include "platform.h"

#include <windows.h>

/* Function declaration */
// Give the string representation of an ExceptionCode
PCHAR ExceptionCodeToString(DWORD code);

// The unhandled exception filter: if we get to that, we kill the process
LONG WINAPI unhandled_exception_filter(struct _EXCEPTION_POINTERS *ExceptionInfo);

// Generate the exception report holding important information like the CPU context, the disassembly, etc.
VOID log_exception(PEXCEPTION_RECORD ExceptionRecord, PCONTEXT Context);

#endif