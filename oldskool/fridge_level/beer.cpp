#include "beer.hpp"

#include <iostream>
#include <cstring>
#include <cstdlib>
#include <cstdio>

Beer::Beer(char* name)
{
    unsigned int size = sizeof(char) * (strlen(name) + 1);
    m_name = (char*)malloc(size);
    memset(m_name, 0, size);
    strcpy(m_name, name);
    std::cout << "Creating a beer.." << std::endl;
}

Beer::~Beer()
{
    if(m_name != NULL)
        free(m_name);
    std::cout << "Killing a beer.." << std::endl;
}

char* Beer::get_name() const
{
    return m_name;
}

void Beer::set_empty_beer()
{
    m_is_empty_beer = true;
}

bool Beer::is_empty_beer()
{
    return m_is_empty_beer;
}
