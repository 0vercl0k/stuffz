/*
#
#    enumerate_com_objects_instanciable_from_browser.cpp -
#    Copyright (C) 2013 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
*/
#include <cstdio>
#include <windows.h>
#include <iostream>
#include <vector>
#include <map>
#include <cassert>
#include <string>

#define REGPATH_CLSID "Software\\Classes\\CLSID"
#define KEY_NAME_SIZE 1024
#define KEY_VALUE_SIZE KEY_NAME_SIZE

std::map<std::string, std::string> get_all_names_values(HKEY reghive, const std::string &regpath)
{
    CHAR name[KEY_NAME_SIZE] = {0}, value[KEY_VALUE_SIZE] = {0};
    HKEY hKey = 0;
    DWORD number_values = 0, i = 0, size_name = KEY_NAME_SIZE, size_value = KEY_NAME_SIZE;
    LONG ret = 0;
    std::map<std::string, std::string> store;

    ret = RegOpenKeyEx(
        reghive,
        regpath.c_str(),
        0,
        KEY_QUERY_VALUE,
        &hKey
    );

    assert(ret == ERROR_SUCCESS);

    ret = RegQueryInfoKey(
        hKey,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        &number_values,
        NULL,
        NULL,
        NULL,
        NULL
    );

    assert(ret == ERROR_SUCCESS);

    for(i = 0; i < number_values; ++i)
    {
        size_name = KEY_NAME_SIZE;
        size_value = KEY_NAME_SIZE;
        ret = RegEnumValue(
            hKey,
            i,
            name,
            &size_name,
            NULL,
            NULL,
            (LPBYTE)value,
            &size_value
        );

        assert(ret == ERROR_SUCCESS);

        std::string value_name(name);
        std::string value_value(value);
        if(size_value == 0)
            value_value = "(Value not set)";

        if(size_name == 0)
            value_name = "(Default)";

        store.insert(
            std::make_pair(
                value_name,
                value_value
            )
        );
        ZeroMemory(name, KEY_NAME_SIZE);
    }

    RegCloseKey(hKey);
    return store;
}

std::vector<std::string> get_all_subkeys(HKEY reghive, const std::string &regpath, bool fullpath = false)
{
    CHAR key_name[KEY_NAME_SIZE] = {0}, key_value[KEY_VALUE_SIZE] = {0};
    HKEY hKey = 0;
    DWORD number_subkeys = 0, i = 0, size_key_name = KEY_NAME_SIZE;
    LONG ret = 0;
    std::vector<std::string> store;

    ret = RegOpenKeyEx(
        reghive,
        regpath.c_str(),
        0,
        KEY_READ,
        &hKey
    );

    assert(ret == ERROR_SUCCESS);

    ret = RegQueryInfoKey(
        hKey,
        NULL,
        NULL,
        NULL,
        &number_subkeys,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL
    );

    assert(ret == ERROR_SUCCESS);

    for(i = 0; i < number_subkeys; ++i)
    {
        size_key_name = KEY_NAME_SIZE;
        ret = RegEnumKeyEx(
            hKey,
            i,
            key_name,
            &size_key_name,
            NULL,
            NULL,
            NULL,
            NULL
        );

        assert(ret == ERROR_SUCCESS);

        std::string key(key_name);
        if(fullpath)
        {
            key = regpath;
            key += '\\';
            key += key_name;
        }
        store.push_back(key);
        ZeroMemory(key_name, KEY_NAME_SIZE);
    }

    RegCloseKey(hKey);
    return store;
}

// https://www.opensource.apple.com/source/CyrusIMAP/CyrusIMAP-187.4/cyrus_imap/lib/stristr.c
char *stristr(const char *String, const char *Pattern)
{
      char *pptr, *sptr, *start;
      unsigned int  slen, plen;

      for (start = (char *)String,
           pptr  = (char *)Pattern,
           slen  = strlen(String),
           plen  = strlen(Pattern);

           /* while string length not shorter than pattern length */

           slen >= plen;

           start++, slen--)
      {
            /* find start of pattern in string */
            while (toupper(*start) != toupper(*Pattern))
            {
                  start++;
                  slen--;

                  /* if pattern longer than string */

                  if (slen < plen)
                        return(NULL);
            }

            sptr = start;
            pptr = (char *)Pattern;

            while (toupper(*sptr) == toupper(*pptr))
            {
                  sptr++;
                  pptr++;

                  /* if end of pattern then pattern was found */

                  if ('\0' == *pptr)
                        return (start);
            }
      }
      return(NULL);
}

// http://msdn.microsoft.com/en-us/library/windows/desktop/ms682390(v=vs.85).aspx
int main()
{
    std::vector<std::string> subkey_clsid = get_all_subkeys((HKEY)HKEY_LOCAL_MACHINE, std::string(REGPATH_CLSID), true);
    for(std::vector<std::string>::const_iterator it = subkey_clsid.begin(); it != subkey_clsid.end(); ++it)
    {
        std::vector<std::string> subkey_com = get_all_subkeys((HKEY)HKEY_LOCAL_MACHINE, *it, true);
        for(std::vector<std::string>::const_iterator it2 = subkey_com.begin(); it2 != subkey_com.end(); ++it2)
        {
            if(stristr(it2->c_str(), "inprocserver32") == NULL)
                continue;

            std::string full_regpath_com(*it);
            std::map<std::string, std::string> values = get_all_names_values((HKEY)HKEY_LOCAL_MACHINE, full_regpath_com);
            if(values.size() == 0 || values.count("(Default)") == 0)
                continue;

            // Treat interesting ones now
            unsigned int id_slash = full_regpath_com.find_last_of('\\');
            std::cout << full_regpath_com.substr(id_slash + 1, std::string::npos) << " - " << values.at("(Default)") << std::endl;

            std::string full_regpath_com_inproc(full_regpath_com);
            full_regpath_com_inproc += '\\';
            full_regpath_com_inproc += "inprocserver32";

            std::map<std::string, std::string> values_inproc = get_all_names_values((HKEY)HKEY_LOCAL_MACHINE, full_regpath_com_inproc);
            if(values_inproc.size() == 0 || values_inproc.count("(Default)") == 0)
                continue;

            std::cout << " Module: " << values_inproc.at("(Default)") << std::endl;
        }
    }
    return EXIT_SUCCESS;
}
