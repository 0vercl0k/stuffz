#include "utils.hpp"

#include <sstream>

const char * StripPath(const char * path)
{
    const char * file = strrchr(path, '\\');
    if (file)
        return file + 1;
    else
        return path;
}

std::string virtualprotect_flags_to_str(WINDOWS::DWORD flags)
{
	std::string res;
	#define BIT_ENTRY(u) { u, #u }
	struct
	{
		WINDOWS::UCHAR mask;
		WINDOWS::CHAR *flag;
	} info[] = {
		BIT_ENTRY(PAGE_NOACCESS),
		BIT_ENTRY(PAGE_READONLY),
		BIT_ENTRY(PAGE_READWRITE),
		BIT_ENTRY(PAGE_WRITECOPY),
		BIT_ENTRY(PAGE_EXECUTE),
		BIT_ENTRY(PAGE_EXECUTE_READ),
		BIT_ENTRY(PAGE_EXECUTE_READWRITE),
		BIT_ENTRY(PAGE_EXECUTE_WRITECOPY)
	};
	
	for(WINDOWS::DWORD j = 0; j < (sizeof(info) / sizeof(info[0])); ++j)
	{
		if((flags & info[j].mask) == info[j].mask)
		{
			if(res.size() > 0)
				res += '|';
			res += info[j].flag;
		}
	}

	return res;
}

std::string address_to_symbol(ADDRINT address, MODULE_LIST_T &module_list)
{
	std::string target_module("[Unknown]");
	for(MODULE_LIST_T::const_iterator it = module_list.begin(); it != module_list.end(); ++it)
	{
		std::pair<ADDRINT, ADDRINT> bounds(it->second);
		if(address >= bounds.first && address <= bounds.second)
		{
			std::stringstream oss;
			oss << it->first << "+" << std::hex << address - bounds.first;
			target_module = oss.str();
			break;
		}
	}

	return target_module;
}