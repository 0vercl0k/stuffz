#pragma once

#include <string>
#include <map>
#include "pin.H"

namespace WINDOWS
{
    #include <Windows.h>
}

typedef std::map<std::string, std::pair<ADDRINT, ADDRINT>> MODULE_LIST_T;

// Strips the path & returns just the file part
const char * StripPath(const char * path);

// Gets a string representation of the flags passed to VirtualProtect
std::string virtualprotect_flags_to_str(WINDOWS::DWORD flags);

// Gets something like module+offset if address is inside a loaded module
std::string address_to_symbol(ADDRINT address, MODULE_LIST_T &module_list);
