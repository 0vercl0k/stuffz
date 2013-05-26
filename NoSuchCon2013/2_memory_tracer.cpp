/*
    1_memory_tracer.cpp - NoSuchCon 2013 Simple Pin memory tracer.
    Copyright (C) 2013 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k

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
    
    Kudos to @elvanderb for that really awesome-tough-motherfuckin-challenge.
*/

#include <string>
#include <map>
#include <iostream>
#include <iomanip>
#include "pin.H"
extern "C" {
    #include "xed-interface.h"
}

using namespace std;

// Only the address in [s_addr and e_addr] will be instrumented
unsigned int s_addr = 0, e_addr = 0;
FILE *f = NULL;
bool trace_generation_started = false;
std::map<ADDRINT, std::string> instructions_disassembled;

VOID instruction_analysis_read(ADDRINT address, ADDRINT address_memory_read, ADDRINT size_memory_read)
{
    unsigned char *p = (unsigned char*)address_memory_read;
    unsigned int *p2 = (unsigned int*)address_memory_read;

    std::string disass("unknow");
    if(instructions_disassembled.count(address) > 0)
        disass = instructions_disassembled.at(address);

    fprintf(f, "%#.8x %-35s: R %#.8x (%d bytes - ", address, disass.c_str(), address_memory_read, size_memory_read);
    if(size_memory_read == 1)
        fprintf(f, "%.2x", *p);
    else if(size_memory_read == 4)
        fprintf(f, "%#.8x", *p2);
    else
        fprintf(f, "WUUT");

    fprintf(f, ")\n");
}

VOID instruction_analysis_write(ADDRINT address, ADDRINT address_memory_written, ADDRINT size_memory_written)
{
    unsigned char *p = (unsigned char*)address_memory_written;
    unsigned int *p2 = (unsigned int*)address_memory_written;
    std::string disass("unknow");
    if(instructions_disassembled.count(address) > 0)
        disass = instructions_disassembled.at(address);

    fprintf(f, "%#.8x %-35s: W %#.8x (%d bytes - ", address, disass.c_str(), address_memory_written, size_memory_written);
    if(size_memory_written == 1)
        fprintf(f, "%.2x", *p);
    else if(size_memory_written == 4)
        fprintf(f, "%#.8x", *p2);
    else
        fprintf(f, "WUUT");

    fprintf(f, ")\n");
}

VOID instruction_instrumentation(INS ins, VOID *v)
{
    if(INS_Address(ins) == s_addr)
        trace_generation_started = true;

    if(INS_Address(ins) == e_addr)
        trace_generation_started = false;

    if(trace_generation_started)
    {
        std::string disass(INS_Disassemble(ins));
        if(instructions_disassembled.count(INS_Address(ins)) == 0)
            // So we add it!
            instructions_disassembled.insert(
                std::make_pair(
                    INS_Address(ins),
                    disass
                )
            );


        if(INS_IsMemoryRead(ins))
        {
            INS_InsertCall(
                ins,
                IPOINT_BEFORE,
                (AFUNPTR)instruction_analysis_read,

                IARG_ADDRINT, INS_Address(ins),
                IARG_MEMORYREAD_EA,   // Effective address of a memory read, only valid if INS_IsMemoryRead is true.
                IARG_MEMORYREAD_SIZE, // Size in bytes of memory read, repeating ia32 string instructions are treated as a single memory operation.
                IARG_END
            );
        }

        if(INS_IsMemoryWrite(ins))
        {
            INS_InsertCall(
                ins,
                IPOINT_BEFORE,
                (AFUNPTR)instruction_analysis_write,
            
                IARG_ADDRINT, INS_Address(ins),
                IARG_MEMORYWRITE_EA,   // Effective address of a memory write.
                IARG_MEMORYWRITE_SIZE, // Size in bytes of memory write.
                IARG_END
            );
        }
    }
}

int main(int argc, char * argv[])
{
    if (PIN_Init(argc, argv))
        return 0;

    f = fopen("memory_trace.out", "w");

    s_addr = 0x005A83B8;
    e_addr = 0x006163AE;

    // Add the instrumentation callback
    INS_AddInstrumentFunction(instruction_instrumentation, 0);

    // Initialize the XED tables -- one time.
    xed_tables_init();

    PIN_StartProgram();
    
    return 0;
}
