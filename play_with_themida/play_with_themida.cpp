#include "pin.H"
namespace WINDOWS
{
    #include <Windows.h>
}
#include <iostream>
#include <sstream>
#include <fstream>
#include <map>
#include <string>
#include <set>
#include <cstring>
#include <algorithm>

#include "instlib.H"
#include "utils.hpp"

/* ================================================================== */
// Global variables 
/* ================================================================== */
#define ACQUIRE_PIN_LOCK() PIN_GetLock(&lock, tid + 1)
#define RELEASE_PIN_LOCK() PIN_ReleaseLock(&lock)
#define INVALID_HANDLE_VALUE_ ((WINDOWS::HANDLE)(WINDOWS::LONG_PTR)-1)

typedef std::map<std::string, std::pair<ADDRINT, ADDRINT>> MODULE_LIST_T;
typedef WINDOWS::HANDLE (__stdcall *CreateThread_t)(
  _In_opt_   WINDOWS::LPSECURITY_ATTRIBUTES lpThreadAttributes,
  _In_       WINDOWS::SIZE_T dwStackSize,
  _In_       WINDOWS::LPTHREAD_START_ROUTINE lpStartAddress,
  _In_opt_   WINDOWS::LPVOID lpParameter,
  _In_       WINDOWS::DWORD dwCreationFlags,
  _Out_opt_  WINDOWS::LPDWORD lpThreadId
);


PIN_LOCK lock;

std::ostream * out = &cerr;
MODULE_LIST_T module_list;
std::ofstream TraceFile;

bool virtual_protect_hook_set = false;
bool get_command_line_hook_set = false;
bool createtoolhel32snapshot_hook_set = false;
bool createthread_hook_set = false;
bool registerclassexw_hook_set = false;

std::vector<WINDOWS::HANDLE> h_to_kill;

/* ===================================================================== */
// Utilities
/* ===================================================================== */
WINDOWS::DWORD WINAPI do_nothin_yo(WINDOWS::LPVOID lpParameter)
{
	WINDOWS::Sleep(100000);
	return EXIT_SUCCESS;
}

INT32 Usage()
{
    *out << "This little pintool aims at studying a bit defense capabalities of Themida " << endl << endl;
    *out << KNOB_BASE::StringKnobSummary() << endl;
    return -1;
}

WINDOWS::HANDLE __stdcall MyCreateThread(
  CreateThread_t CreateThread,
  _In_opt_   WINDOWS::LPSECURITY_ATTRIBUTES lpThreadAttributes,
  _In_       WINDOWS::SIZE_T dwStackSize,
  _In_       WINDOWS::LPTHREAD_START_ROUTINE lpStartAddress,
  _In_opt_   WINDOWS::LPVOID lpParameter,
  _In_       WINDOWS::DWORD dwCreationFlags,
  _Out_opt_  WINDOWS::LPDWORD lpThreadId
)
{
	THREADID tid = PIN_GetTid();
	ACQUIRE_PIN_LOCK();

	WINDOWS::HANDLE ret = NULL;

	std::string thread_routine_symbol(address_to_symbol((ADDRINT)*lpStartAddress, module_list));

	LOG(
		"[MyCreateThread][" + decstr(tid) + "] CreateThread(" + hexstr((UINT32)lpThreadAttributes) + ", " + hexstr((UINT32)dwStackSize) +  ", " +
		thread_routine_symbol + ", " + hexstr((UINT32)lpParameter) + ", " + 
		hexstr((UINT32)dwCreationFlags) +  ", " + hexstr((UINT32)lpThreadId) + ")\n"
	);

	ret = CreateThread(
		lpThreadAttributes,
		dwStackSize,
		lpStartAddress,
		lpParameter,
		dwCreationFlags,
		lpThreadId
	);

	if(thread_routine_symbol.find("copytransmanager") != std::string::npos)
	{
		// Watch dog?
		LOG("[MyCreateThread][" + decstr(tid) + "] Looks a watchdog, adding to the tokill\n");
		h_to_kill.push_back(ret);
	}

	LOG("[MyCreateThread][" + decstr(tid) + "] TID is " + decstr((UINT32)*lpThreadId) + "\n");
	
	clean:
	RELEASE_PIN_LOCK();
	return ret;
}

/* ===================================================================== */
// Analysis routines
/* ===================================================================== */
WINDOWS::DWORD b = 0;
VOID PIN_FAST_ANALYSIS_CALL before_registerclassexw(THREADID tid)
{
	ACQUIRE_PIN_LOCK();
	b++;
	if(b == 3)
	{
		LOG("Killing the previously identified watchdogs..\n");
		for(auto &h : h_to_kill)
		{
			LOG("Killing " + decstr((UINT32)h) + "\n");
			//WINDOWS::TerminateThread(h, 0);
		}

		LOG("Detaching now..\n");
		PIN_Detach();
	}
	RELEASE_PIN_LOCK();
}

VOID PIN_FAST_ANALYSIS_CALL before_virtuaprotect(THREADID tid, ADDRINT *address, WINDOWS::SIZE_T *size, WINDOWS::DWORD *new_protect, WINDOWS::PDWORD *p_old_protect)
{
	ACQUIRE_PIN_LOCK();

	std::string target_module(address_to_symbol(*address, module_list));
	std::stringstream oss;
	oss << '"';
	for(WINDOWS::DWORD i = 0; i < min(5, *size); ++i)
	{
		WINDOWS::UCHAR *p = (WINDOWS::UCHAR*)address;
		WINDOWS::UCHAR tmp[5] = {0};
		sprintf((CHAR*)tmp, "\\x%.2x", p[i]);
		oss << tmp;
	}

	if(min(5, *size) == 5)
		oss << "...";
	oss << '"';
	std::string bytes(oss.str());

	//if(target_module.find("copytransmanager") == std::string::npos)
	LOG("[before_virtuaprotect][" + decstr(tid) + "] VirtualProtect(" + target_module + " - " + bytes + ", " + decstr((unsigned int)*size) + ", " + virtualprotect_flags_to_str(*new_protect) + ", " + hexstr(*p_old_protect) + ")\n");
	
	RELEASE_PIN_LOCK();
}

VOID PIN_FAST_ANALYSIS_CALL after_virtualprotect(THREADID tid, ADDRINT *ret)
{
	ACQUIRE_PIN_LOCK();

	LOG("[after_virtualprotect][" + decstr(tid) + "] Returning FALSE (real return value: " + hexstr(*ret) + ")\n");
	*ret = FALSE;

	RELEASE_PIN_LOCK();
}


WINDOWS::DWORD i = 0;
VOID PIN_FAST_ANALYSIS_CALL before_getcommandlinew(THREADID tid)
{
	ACQUIRE_PIN_LOCK();

	LOG("[before_getcommandlinew][" + decstr(tid) + "] All right, time to detach..\n");
	//if(i == 3)
		//PIN_Detach();
	i++;

	RELEASE_PIN_LOCK();
}


VOID PIN_FAST_ANALYSIS_CALL before_CreateToolhelp32Snapshot(THREADID tid, WINDOWS::DWORD *dwFlags, WINDOWS::DWORD *th32ProcessID)
{
	ACQUIRE_PIN_LOCK();

	LOG("[before_CreateToolhelp32Snapshot][" + decstr(tid) + "] CreateToolHelp32Snapshot(" + hexstr((UINT32)*dwFlags) + ", " + hexstr((UINT32)*th32ProcessID) + ")\n");

	RELEASE_PIN_LOCK();
}

VOID PIN_FAST_ANALYSIS_CALL after_CreateToolhelp32Snapshot(THREADID tid, WINDOWS::HANDLE *ret)
{
	ACQUIRE_PIN_LOCK();

	LOG("[after_CreateToolhelp32Snapshot][" + decstr(tid) + "] Returning INVALID_HANDLE_VALUE..\n");
	if(*ret != INVALID_HANDLE_VALUE_)
	{
		WINDOWS::CloseHandle(*ret);
		*ret = INVALID_HANDLE_VALUE_;
	}

	RELEASE_PIN_LOCK();
}


VOID ThreadFini(THREADID tid, const CONTEXT *ctxt, INT32 code, VOID *v)
{
	ACQUIRE_PIN_LOCK();

	LOG("[ThreadFini] thread " + decstr(tid) + " ends\n");

	RELEASE_PIN_LOCK();
}

VOID ThreadStart(THREADID tid, CONTEXT *ctxt, INT32 flags, VOID *v)
{
	ACQUIRE_PIN_LOCK();

	PIN_REGISTER eip;
	PIN_GetContextRegval(ctxt, REG_EIP, (UINT8*)&eip);

    LOG("[ThreadStart] thread begin " + decstr(tid) + " @ " + hexstr(eip.dword) + "\n");

	RELEASE_PIN_LOCK();
}

/* ===================================================================== */
// Instrumentation routines
/* ===================================================================== */
VOID Image(IMG img, VOID *v)
{
	// First part is to keep track of the begin/end addresses of the loaded modules
    ADDRINT module_low_limit = IMG_LowAddress(img),
        module_high_limit = IMG_HighAddress(img); 

	std::string image_path = StripPath(IMG_Name(img).c_str());
	std::transform(image_path.begin(), image_path.end(), image_path.begin(), tolower);

	std::pair<std::string, std::pair<ADDRINT, ADDRINT> > module_info = std::make_pair(
		image_path,
		std::make_pair(
			module_low_limit,
			module_high_limit
		)
	);

	module_list.insert(module_info);
	LOG("[Image] New module: " + image_path + " - [" + hexstr(module_low_limit) + ", " + hexstr(module_high_limit) + "]\n");

	if(image_path == "kernelbase.dll" || image_path == "kernel32.dll" || image_path == "gdi32.dll")
	{
		if(registerclassexw_hook_set == false)
		{
			RTN rtn = RTN_FindByName(img, "SelectClipRgn");
			if (RTN_Valid(rtn))
			{
				RTN_Open(rtn);
				RTN_InsertCall(rtn, IPOINT_BEFORE, AFUNPTR(before_registerclassexw), IARG_FAST_ANALYSIS_CALL, IARG_THREAD_ID, IARG_END);
            	RTN_Close(rtn);

				LOG("[Image] RegisterClassExW hook set!\n");
				registerclassexw_hook_set = true;
			}
		}

		if(createthread_hook_set == false)
		{
			RTN rtn = RTN_FindByName(img, "CreateThread");
			if (RTN_Valid(rtn))
			{
				RTN_Open(rtn);
				//RTN_ReplaceSignature(rtn, AFUNPTR(MyCreateThread), IARG_ORIG_FUNCPTR, IARG_END);
				RTN_Replace(rtn, AFUNPTR(MyCreateThread));
            	RTN_Close(rtn);

				LOG("[Image] CreateThread hook set!\n");
				createthread_hook_set = true;
			}
		}

		if(get_command_line_hook_set == false)
		{
			RTN rtn = RTN_FindByName(img, "GetCommandLineW");
			if (RTN_Valid(rtn))
			{
				RTN_Open(rtn);
				RTN_InsertCall(rtn, IPOINT_BEFORE, AFUNPTR(before_getcommandlinew), IARG_FAST_ANALYSIS_CALL, IARG_THREAD_ID, IARG_END);
            	RTN_Close(rtn);

				LOG("[Image] GetCommandLineW hook set!\n");
				get_command_line_hook_set = true;
			}
		}

		if(createtoolhel32snapshot_hook_set == false)
		{
			RTN rtn = RTN_FindByName(img, "CreateToolhelp32Snapshot");
			if (RTN_Valid(rtn))
			{
				RTN_Open(rtn);
				RTN_InsertCall(
					rtn, IPOINT_BEFORE, AFUNPTR(before_CreateToolhelp32Snapshot),
					IARG_FAST_ANALYSIS_CALL,
					IARG_THREAD_ID,
					IARG_FUNCARG_ENTRYPOINT_REFERENCE, 0,
					IARG_FUNCARG_ENTRYPOINT_REFERENCE, 1,
					IARG_END
				);

				RTN_InsertCall(
					rtn, IPOINT_AFTER, AFUNPTR(after_CreateToolhelp32Snapshot),
					IARG_FAST_ANALYSIS_CALL,
					IARG_THREAD_ID,
					IARG_FUNCRET_EXITPOINT_REFERENCE,
					IARG_END
				);
				RTN_Close(rtn);

				LOG("[Image] CreateToolhelp32Snapshot hook set!\n");
				createtoolhel32snapshot_hook_set = true;
			}
		}

        if(virtual_protect_hook_set == false)
		{
			RTN rtn = RTN_FindByName(img, "VirtualProtect");
			if (RTN_Valid(rtn))
			{
				RTN_Open(rtn);
				RTN_InsertCall(
					rtn, IPOINT_BEFORE, AFUNPTR(before_virtuaprotect),
					IARG_FAST_ANALYSIS_CALL,
					IARG_THREAD_ID,
					IARG_FUNCARG_ENTRYPOINT_REFERENCE, 0,
					IARG_FUNCARG_ENTRYPOINT_REFERENCE, 1,
					IARG_FUNCARG_ENTRYPOINT_REFERENCE, 2,
					IARG_FUNCARG_ENTRYPOINT_REFERENCE, 3,
					IARG_END
				);

				RTN_InsertCall(
					rtn, IPOINT_AFTER, AFUNPTR(after_virtualprotect),
					IARG_FAST_ANALYSIS_CALL,
					IARG_THREAD_ID,
					IARG_FUNCRET_EXITPOINT_REFERENCE,
					IARG_END
				);
				RTN_Close(rtn);

				LOG("[Image] VirtualProtect hook set!\n");
				virtual_protect_hook_set = true;
			}
		}
	}
}

VOID Fini(INT32 code, VOID *v)
{
    LOG("EOF================================\n");
}

int main(int argc, char *argv[])
{
    // Initialize PIN library. Print help message if -h(elp) is specified
    // in the command line or the command line is invalid 
	PIN_InitSymbols();
    if(PIN_Init(argc,argv))
        return Usage();

	// We knows for sure Themida is hooking ntdll in order to prevent debuggers to be able to attach themselves
	IMG_AddInstrumentFunction(Image, 0);
	PIN_AddFiniFunction(Fini, 0);

	// We also knows it's using quite some watchdogs
	// PIN_AddThreadStartFunction(ThreadStart, 0);
	// PIN_AddThreadFiniFunction(ThreadFini, 0);

    // Start the program, never returns
    PIN_StartProgram();
    
    return 0;
}

