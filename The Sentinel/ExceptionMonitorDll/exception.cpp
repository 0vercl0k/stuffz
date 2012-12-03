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
#include "exception.hpp"
#include "toolbox.hpp"
#include "config.hpp"

#include <distorm.h>
#include <cstdio>
#include <string>

PCHAR ExceptionCodeToString(DWORD code)
{
    switch(code)
    {
        case EXCEPTION_ACCESS_VIOLATION: return "EXCEPTION_ACCESS_VIOLATION";
        case EXCEPTION_ARRAY_BOUNDS_EXCEEDED: return "EXCEPTION_ARRAY_BOUNDS_EXCEEDED";
        case EXCEPTION_BREAKPOINT: return "EXCEPTION_BREAKPOINT";
        case EXCEPTION_DATATYPE_MISALIGNMENT: return "EXCEPTION_DATATYPE_MISALIGNMENT";
        case EXCEPTION_FLT_DENORMAL_OPERAND: return "EXCEPTION_FLT_DENORMAL_OPERAND";
        case EXCEPTION_FLT_DIVIDE_BY_ZERO: return "EXCEPTION_FLT_DIVIDE_BY_ZERO";
        case EXCEPTION_FLT_INEXACT_RESULT: return "EXCEPTION_FLT_INEXACT_RESULT";
        case EXCEPTION_FLT_INVALID_OPERATION: return "EXCEPTION_FLT_INVALID_OPERATION";
        case EXCEPTION_FLT_OVERFLOW: return "EXCEPTION_FLT_OVERFLOW";
        case EXCEPTION_FLT_STACK_CHECK: return "EXCEPTION_FLT_STACK_CHECK";
        case EXCEPTION_FLT_UNDERFLOW: return "EXCEPTION_FLT_UNDERFLOW";
        case EXCEPTION_ILLEGAL_INSTRUCTION: return "EXCEPTION_ILLEGAL_INSTRUCTION";
        case EXCEPTION_IN_PAGE_ERROR: return "EXCEPTION_IN_PAGE_ERROR";
        case EXCEPTION_INT_DIVIDE_BY_ZERO: return "EXCEPTION_INT_DIVIDE_BY_ZERO";
        case EXCEPTION_INT_OVERFLOW: return "EXCEPTION_INT_OVERFLOW";
        case EXCEPTION_INVALID_DISPOSITION: return "EXCEPTION_INVALID_DISPOSITION";
        case EXCEPTION_NONCONTINUABLE_EXCEPTION: return "EXCEPTION_NONCONTINUABLE_EXCEPTION";
        case EXCEPTION_PRIV_INSTRUCTION: return "EXCEPTION_PRIV_INSTRUCTION";
        case EXCEPTION_SINGLE_STEP: return "EXCEPTION_SINGLE_STEP";
        case EXCEPTION_STACK_OVERFLOW: return "EXCEPTION_STACK_OVERFLOW";
        default: return "UNKNOWN";
    }
}

VOID log_exception(PEXCEPTION_RECORD ExceptionRecord, PCONTEXT Context)
{   
    char image_path[MAX_PATH] = {0}, *command_line = GetCommandLine(), *executable_name = NULL;
    DWORD pid = GetCurrentProcessId();
    FILE* f = NULL;
    static std::string report_path;

    // Sometimes this exception is raised during the loading of a process, ignore it
    if(ExceptionRecord->ExceptionCode == 0x000006ba)
        return;

    GetModuleFileName(
        NULL,
        (char*)image_path,
        MAX_PATH
    );

    executable_name = strrchr(image_path, '\\') + 1;

    if(report_path.size() == 0)
        report_path = generate_unique_report_path(executable_name, (DWORD)ExceptionRecord->ExceptionAddress);

    errno_t err = fopen_s(&f, report_path.c_str(), "a");
    if(err != 0)
        return;

    fprintf(f, "\n\n--Exception detected--\n");
    fprintf(f, "ExceptionRecord: %#.8x Context: %#.8x\n", ExceptionRecord, Context);
    fprintf(f, "Image Path: %s\n", image_path);
    fprintf(f, "Command Line: %s\n", command_line);
    fprintf(f, "PID: %#.8x\n", pid);
    fprintf(f, "Exception Code: %#.8x (%s)\n", ExceptionRecord->ExceptionCode, ExceptionCodeToString(ExceptionRecord->ExceptionCode));
    fprintf(f, "Exception Address: %#.8x\n", ExceptionRecord->ExceptionAddress);
    
    if(ExceptionRecord->ExceptionCode == EXCEPTION_ACCESS_VIOLATION && ExceptionRecord->NumberParameters >= 2)
    {       
        char *type;
        switch(ExceptionRecord->ExceptionInformation[0])
        {
            case 0:
            {
                type = "READ";
                break;
            }

            case 1:
            {
                type = "WRITE";
                break;
            }
            
            case 8:
            {
                type = "EXEC";
                break;
            }
            
            default:
            {
                type = "UNKNOW";
                break;
            }
        }

        fprintf(f, "Access Violation Type: %s\n", type);
        fprintf(f, "Accessed Memory Address: %.8x\n", ExceptionRecord->ExceptionInformation[1]);
    }

    // CONTEXT dumping now
    fprintf(f, "EAX: 0x%.8x EDX: 0x%.8x ECX: 0x%.8x EBX: 0x%.8x\n", Context->Eax, Context->Edx, Context->Ecx, Context->Ebx);
    fprintf(f, "ESI: 0x%.8x EDI: 0x%.8x ESP: 0x%.8x EBP: 0x%.8x\n", Context->Esi, Context->Edi, Context->Esp, Context->Ebp);
    fprintf(f, "EIP: 0x%.8x\n", Context->Eip);
    fprintf(f, "EFLAGS: 0x%.8x\n", Context->EFlags);

    fprintf(f, "\nStack:");
    for(unsigned int i = 0; i < 8; ++i)
    {
        if(IsBadReadPtr((const void*)Context->Esp, sizeof(unsigned int)) == 0)
        {
            if(i % 4 == 0)
                fprintf(f, "\n");

            fprintf(f, "0x%.8x", *(PDWORD)(Context->Esp + sizeof(unsigned int)*i));
            if(i + 1 < 8)
                fprintf(f, " ");
        }
        else
            break;
    }
    fprintf(f, "\n");

    if(IsBadReadPtr((const void*)Context->Eip, SIZE_BIGGEST_X86_INSTR * MAX_INSTRUCTIONS) == 0)
    {
        _DecodeResult res;
        _OffsetType offset = Context->Eip;
        _DecodedInst decodedInstructions[MAX_INSTRUCTIONS] = {0};
        unsigned int decodedInstructionsCount = 0;

        res = distorm_decode(
            offset,
            (const unsigned char*)Context->Eip,
            MAX_INSTRUCTIONS * SIZE_BIGGEST_X86_INSTR,
            Decode32Bits,
            decodedInstructions,
            MAX_INSTRUCTIONS,
            &decodedInstructionsCount
        );

        if(res == DECRES_SUCCESS || res == DECRES_MEMORYERR)
        {
            fprintf(f, "\nDisassembly:\n");
            for(unsigned int i = 0; i < decodedInstructionsCount; ++i)
            {
			    fprintf(
                    f,
                    "%.8I64x (%.2d) %-24s %s%s%s\n",
                    decodedInstructions[i].offset,
                    decodedInstructions[i].size,
                    (char*)decodedInstructions[i].instructionHex.p,
                    (char*)decodedInstructions[i].mnemonic.p,
                    decodedInstructions[i].operands.length != 0 ? " " : "",
                    (char*)decodedInstructions[i].operands.p
               );
            }
        }
    }

    fclose(f);
}