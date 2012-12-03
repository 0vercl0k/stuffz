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
#include "toolbox.hpp"
#include "config.hpp"

#include <sstream>
#include <ctime>

std::string generate_unique_report_path(PCHAR exec_name, DWORD exception_address)
{
    std::string report_path(CRASHDUMP_BASE_DIR);
    std::stringstream st;

    report_path += exec_name;

    /* Create a directory to store the crash of the target */
    CreateDirectory(report_path.c_str(), NULL);
    st << "\\exceptionaddress_" << std::hex << exception_address;
    st << "pid_" << std::dec << GetCurrentProcessId();
    st << "tick_" << GetTickCount64();
    st << "timestamp_" << time(NULL);
    st << ".txt";

    report_path += st.str();
    return report_path;
}