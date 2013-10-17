/*
    ___________.__               _________              __  .__              .__   
    \__    ___/|  |__   ____    /   _____/ ____   _____/  |_|__| ____   ____ |  |  
      |    |   |  |  \_/ __ \   \_____  \_/ __ \ /    \   __\  |/    \_/ __ \|  |  
      |    |   |   Y  \  ___/   /        \  ___/|   |  \  | |  |   |  \  ___/|  |__
      |____|   |___|  /\___  > /_______  /\___  >___|  /__| |__|___|  /\___  >____/
                    \/     \/          \/     \/     \/             \/     \/  
                    ProcessSpawner - This is the process spwaner which aims to
                    launch and inject the exception monitoring dll in the target process
                    address space thanks to MS Detours.

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

    DEBUGMSG("DetourCreateProcessWithDll time now..\n");

    /* love this function \o/ */
    return DetourCreateProcessWithDll(
        path_executable.c_str(),
        (char*)command_line.c_str(),
        NULL,
        NULL,
        FALSE,
        0,
        NULL,
        NULL,
        &si,
        &pi,
        dll_path.c_str(),
        0
    );
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