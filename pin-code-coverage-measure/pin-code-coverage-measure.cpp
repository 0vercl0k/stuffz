/*
    pin-code-coverage-measure.cpp - Generate a JSON report with the address of
    each BBL executed.
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
*/
#include <pin.h>
#include <jansson.h>
#include <map>
#include <string>
#include <iostream>
#include <set>


/// Types
typedef std::map<std::string, std::pair<ADDRINT, ADDRINT> > MODULE_BLACKLIST_T;
typedef MODULE_BLACKLIST_T MODULE_LIST_T;
typedef std::map<ADDRINT, UINT32> BASIC_BLOCKS_INFO_T;


///Globals
// The number of the total instruction executed by the program
UINT64 instruction_counter = 0;
// The number of threads
UINT64 thread_counter = 0;
// This is the list of the blacklisted module ; you can find their names & start/end addresses
MODULE_BLACKLIST_T modules_blacklisted;
// For each bbl executed, we store its address and its number of instruction
BASIC_BLOCKS_INFO_T basic_blocks_info;
// For each module loaded, we keep its name & start/end addresses
MODULE_LIST_T module_list;


/// Pintool arguments
// You can specify where the output JSON report will be written
KNOB<std::string> KnobOutputPath(
    KNOB_MODE_WRITEONCE,
    "pintool",
    "o",
    ".",
    "Specify where you want to store the JSON report"
);

// You can set a timeout (in cases the application never ends)
KNOB<std::string> KnobTimeoutMs(
    KNOB_MODE_WRITEONCE,
    "pintool",
    "r",
    "infinite",
    "Set a timeout for the instrumentation"
);


/// Utility functions
// Walk the modules_blacklisted list and check if address belongs to one of the blacklisted module
bool is_address_in_blacklisted_modules(ADDRINT address)
{
    for(MODULE_BLACKLIST_T::const_iterator it = modules_blacklisted.begin(); it != modules_blacklisted.end(); ++it)
    {
        ADDRINT low_address = it->second.first, high_address = it->second.second;
        if(address >= low_address && address <= high_address)
            return true;
    }

    return false;
}

// Check is image_path matches one of the string in the blacklist
bool is_module_should_be_blacklisted(const std::string &image_path)
{
    // If the path of a DLL matches one of the following string, the module won't be instrumented by Pin.
    // This way you can avoid instrumentation of Windows API.
    static char* path_to_blacklist[] = {
        "C:\\Windows\\"
        // "C:\\Windows\\system32\\",
        // "C:\\Windows\\WinSxS\\"
    };

    for(unsigned int i = 0; i < sizeof(path_to_blacklist) / sizeof(path_to_blacklist[0]); ++i)
        if(_strnicmp(path_to_blacklist[i], image_path.c_str(), strlen(path_to_blacklist[i])) == 0)
            return true;

    return false;
}


/// Instrumentation/Analysis functions
// who cares
INT32 Usage()
{
    std::cerr << "This pintool allows you to generate a JSON report that will contain the address of each basic block executed." << std::endl << std::endl;
    std::cerr << std::endl << KNOB_BASE::StringKnobSummary() << std::endl;
    return -1;
}

// Called right before the execution of each basic block with the number of instruction in arg.
VOID PIN_FAST_ANALYSIS_CALL handle_basic_block(UINT32 number_instruction_in_bb, ADDRINT address_bb)
{
    // What's going on under the hood
    // LOG("[ANALYSIS] BBL Address: " + hexstr(address_bb) + "\n");
    basic_blocks_info[address_bb] = number_instruction_in_bb;
    instruction_counter += number_instruction_in_bb;
}

// We have to instrument traces in order to instrument each BBL, the API doesn't have a BBL_AddInstrumentFunction
VOID trace_instrumentation(TRACE trace, VOID *v)
{
    // We don't want to instrument the BBL contained in the Windows API
    if(is_address_in_blacklisted_modules(TRACE_Address(trace)))
        return;

    for(BBL bbl = TRACE_BblHead(trace); BBL_Valid(bbl); bbl = BBL_Next(bbl))
    {
        // What's going on under the hood
        // LOG("[INSTRU] BBL Address: " + hexstr(BBL_Address(bbl)) + ", " + hexstr(BBL_NumIns(bbl)) + "\n");
        
        // Insert a call to handle_basic_block before every basic block, passing the number of instructions
        BBL_InsertCall(
            bbl,
            IPOINT_ANYWHERE,
            (AFUNPTR)handle_basic_block,
            IARG_FAST_ANALYSIS_CALL, // Use a faster linkage for calls to analysis functions. Add PIN_FAST_ANALYSIS_CALL to the declaration between the return type and the function name. You must also add IARG_FAST_ANALYSIS_CALL to the InsertCall. For example:

            IARG_UINT32,
            BBL_NumIns(bbl),

            IARG_ADDRINT,
            BBL_Address(bbl),

            IARG_END
        );
    }
}

// Instrumentation of the modules
VOID image_instrumentation(IMG img, VOID * v)
{
    ADDRINT module_low_limit = IMG_LowAddress(img), module_high_limit = IMG_HighAddress(img); 

    if(IMG_IsMainExecutable(img))
        return;

    const std::string image_path = IMG_Name(img);

    std::pair<std::string, std::pair<ADDRINT, ADDRINT> > module_info = std::make_pair(
        image_path,
        std::make_pair(
            module_low_limit,
            module_high_limit
        )
    );

    module_list.insert(module_info);

    if(is_module_should_be_blacklisted(image_path))
        modules_blacklisted.insert(module_info);
}

VOID save_instrumentation_infos()
{
    /// basic_blocks_info section
    json_t *bbls_info = json_object();
    json_t *bbls_list = json_array();
    json_t *bbl_info = json_object();
    // unique_count field
    json_object_set_new(bbls_info, "unique_count", json_integer(basic_blocks_info.size()));
    // list field
    json_object_set_new(bbls_info, "list", bbls_list);
    for(BASIC_BLOCKS_INFO_T::const_iterator it = basic_blocks_info.begin(); it != basic_blocks_info.end(); ++it)
    {
        bbl_info = json_object();
        json_object_set_new(bbl_info, "address", json_integer(it->first));
        json_object_set_new(bbl_info, "nbins", json_integer(it->second));
        json_array_append_new(bbls_list, bbl_info);
    }

    /// blacklisted_modules section
    json_t *blacklisted_modules = json_object();
    json_t *modules_list = json_array();
    // unique_count field
    json_object_set_new(blacklisted_modules, "unique_count", json_integer(modules_blacklisted.size()));
    // list field
    json_object_set_new(blacklisted_modules, "list", modules_list);
    for(MODULE_BLACKLIST_T::const_iterator it = modules_blacklisted.begin(); it != modules_blacklisted.end(); ++it)
    {
        json_t *mod_info = json_object();
        json_object_set_new(mod_info, "path", json_string(it->first.c_str()));
        json_object_set_new(mod_info, "low_address", json_integer(it->second.first));
        json_object_set_new(mod_info, "high_address", json_integer(it->second.second));
        json_array_append_new(modules_list, mod_info);
    }

    /// modules section
    json_t *modules = json_object();
    json_t *modules_list_ = json_array();
    // unique_count field
    json_object_set_new(modules, "unique_count", json_integer(module_list.size()));
    // list field
    json_object_set_new(modules, "list", modules_list_);
    for(MODULE_BLACKLIST_T::const_iterator it = module_list.begin(); it != module_list.end(); ++it)
    {
        json_t *mod_info = json_object();
        json_object_set_new(mod_info, "path", json_string(it->first.c_str()));
        json_object_set_new(mod_info, "low_address", json_integer(it->second.first));
        json_object_set_new(mod_info, "high_address", json_integer(it->second.second));
        json_array_append_new(modules_list_, mod_info);
    }

    /// Building the tree
    json_t *root = json_object();
    json_object_set_new(root, "basic_blocks_info", bbls_info);
    json_object_set_new(root, "blacklisted_modules", blacklisted_modules);
    json_object_set_new(root, "modules", modules);

    /// Writing the report
    FILE* f = fopen(KnobOutputPath.Value().c_str(), "w");
    json_dumpf(root, f, JSON_COMPACT | JSON_ENSURE_ASCII);
    fclose(f);
}

// Called just before the application ends
VOID pin_is_detached(VOID *v)
{
    save_instrumentation_infos();
    PIN_ExitProcess(0);
}

VOID this_is_the_end(INT32 code, VOID *v)
{
    save_instrumentation_infos();
}

VOID sleeping_thread(VOID* v)
{
    if(KnobTimeoutMs.Value() == "infinite")
        return;

    PIN_Sleep(atoi(KnobTimeoutMs.Value().c_str()));
    PIN_Detach();
}

int main(int argc, char *argv[])
{
    // Initialize PIN library. Print help message if -h(elp) is specified
    // in the command line or the command line is invalid 
    if(PIN_Init(argc,argv))
        return Usage();
    
    /// Instrumentations
    // Register function to be called to instrument traces
    TRACE_AddInstrumentFunction(trace_instrumentation, 0);

    // Register function to be called when the application exits
    PIN_AddFiniFunction(this_is_the_end, 0);
    
    // Register function to be called when a module is loaded
    IMG_AddInstrumentFunction(image_instrumentation, 0);

    /// Other stuffs
    // This routine will be called if the sleeping_thread calls PIN_Detach() (when the time is out)
    PIN_AddDetachFunction(pin_is_detached, 0);

    // Run a thread that will wait for the time out
    PIN_SpawnInternalThread(
        sleeping_thread,
        0,
        0,
        NULL
    );

    // If we are in a wow64 process we must blacklist manually the JMP FAR: stub
    // from being instrumented (each time a syscall is called, it will be instrumented for *nothing*)
    // Its address is in FS:[0xC0] on Windows 7
    ADDRINT wow64stub = __readfsdword(0xC0);
    modules_blacklisted.insert(
        std::make_pair(
            std::string("wow64stub"),
            std::make_pair(
                wow64stub,
                wow64stub
            )
        )
    );

    /// FIRE IN THE HOLE
    // Start the program, never returns
    PIN_StartProgram();
    
    return 0;
}
