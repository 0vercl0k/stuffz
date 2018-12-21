#include "force4.hpp"
#include <iostream>

Force4::Force4()
: Beer((char*)"Force4 - For the Gods by the Gods themselves.")
{
   std::cout << "Instanciate a force4.." << std::endl;
}

Force4::Force4(char* name)
: Beer(name)
{
    std::cout << "Instanciate a force4.." << std::endl;
}

Force4::~Force4()
{
    std::cout << "Killing a force4.." << std::endl;
}

std::string Force4::get_type()
{
    return std::string("f4");
}
