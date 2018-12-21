#include <windows.h>
#include <string>
#include <vector>
#include <detours.h>

#ifdef _DEBUG
#define DEBUGMSG(...) fprintf(stderr, __VA_ARGS__);
#else
#define DEBUGMSG(...) /* \o/ */
#endif

DWORD SpawnProcessAndInjectDll(std::string path_executable, std::vector<std::string> arguments, std::string dll_path)
{
    STARTUPINFO si = {0};
    PROCESS_INFORMATION pi = {0};
    HANDLE hRemoteThread;
    LPVOID remote_memory = NULL;
    DWORD tid = 0;
    bool ret = true;
    std::string command_line;

    for(std::vector<std::string>::const_iterator it = arguments.begin(); it != arguments.end(); ++it)
    {
        std::vector<std::string>::const_iterator it_end = arguments.end();
        --it_end;

        if(it->find(' ') != std::string::npos)
            command_line += '"' + *it + '"';
        else
            command_line += *it;

        if(it_end != it)
            command_line += ' ';
    }

    DEBUGMSG("Command line is ready:\n");
    DEBUGMSG("%s\n", command_line.c_str());

    DEBUGMSG("Creating process in suspended mode..\n");
    if(CreateProcess(
        NULL,
        (char*)command_line.c_str(),
        NULL,
        NULL,
        FALSE,
        CREATE_SUSPENDED | CREATE_NEW_CONSOLE,
        NULL,
        NULL,
        &si,
        &pi
    ) == FALSE)
        return 0;
    
    DEBUGMSG("Allocating memory in the remote process..\n");
    remote_memory = VirtualAllocEx(
        pi.hProcess,
        NULL,
        dll_path.size() + 1,
        MEM_COMMIT,
        PAGE_READWRITE
    );

    if(remote_memory == NULL)
        return 0;

    DEBUGMSG("Writing full path dll in the remote proces..\n");
    WriteProcessMemory(
        pi.hProcess,
        remote_memory,
        dll_path.c_str(),
        dll_path.size() + 1,
        0
    );

    DEBUGMSG("Creating the remote thread..\n");
    // That's not really clean, kernel32 is supposed to be loaded at a different base in the remote
    // process, but it doesn't seem to be the case on my tests, so whatever.
    LPTHREAD_START_ROUTINE loadlibrary_address = (LPTHREAD_START_ROUTINE)GetProcAddress(
        GetModuleHandle("kernel32"),
        "LoadLibraryA"
    );

    hRemoteThread = CreateRemoteThread(
        pi.hProcess,
        NULL,
        0,
        loadlibrary_address,
        remote_memory,
        0,
        &tid
    );

    if(hRemoteThread == NULL)
        return 0;

    DEBUGMSG("Waiting the remote thread ends..\n");
    WaitForSingleObject(hRemoteThread, INFINITE);

    DEBUGMSG("Freeing the remote memory..\n");
    VirtualFreeEx(
        pi.hProcess,
        remote_memory,
        0,
        MEM_DECOMMIT
    );
   
    DEBUGMSG("Resuming the main thread..\n");
    ResumeThread(pi.hThread);
    return 1;
}

int main(int argc, char* argv[])
{
    if(argc < 3)
    {
        printf("Usage: ./ProcessSpawner <full path dll> <path executable> [args..]");
        return EXIT_FAILURE;
    }

    /* Parse the command-line */
    std::string full_path_dll(argv[1]), path_exec(argv[2]);
    std::vector<std::string> arguments;

    // Don't forget the argv[0]!
    arguments.push_back(path_exec);
    if(argc > 2)
    {
        for(int i = 3; i < argc; ++i)
            arguments.push_back(std::string(argv[i]));
    }
    
    DEBUGMSG("Directory of the process to spawn: %s\n", path_exec.c_str());
    DEBUGMSG("Full-path of the DLL to inject: %s\n", full_path_dll.c_str());
    DEBUGMSG("The process must be run with %d arguments\n", arguments.size());

    if(arguments.size() > 0)
    {
        for(std::vector<std::string>::const_iterator it = arguments.begin(); it != arguments.end(); ++it)
            DEBUGMSG("   - %s\n", it->c_str());
    }

    DEBUGMSG("OK, spawning the process..\n");
    DWORD does_it_worked = SpawnProcessAndInjectDll(path_exec, arguments, full_path_dll);
    DEBUGMSG("Is the process creation + dll injection worker ? %d\n", does_it_worked);
    return EXIT_SUCCESS;
}