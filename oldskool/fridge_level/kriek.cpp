#include "kriek.hpp"
#include <iostream>

Kriek::Kriek()
: Beer((char*)"Kriek - For the Gods by the Gods themselves.")
{
   std::cout << "Instanciate a kriek.." << std::endl; 
}

Kriek::Kriek(char* name)
: Beer(name)
{
    std::cout << "Instanciate a kriek.." << std::endl;
}

Kriek::~Kriek()
{
    std::cout << "Killing a kriek.." << std::endl;
}

std::string Kriek::get_type()
{
    return std::string("krk");
}