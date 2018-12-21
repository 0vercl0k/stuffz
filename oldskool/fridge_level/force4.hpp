#ifndef FORCE4_HPP
#define FORCE4_HPP

#include "beer.hpp"

class Force4 : public Beer
{
    public:
        explicit Force4();
        explicit Force4(char* name);

        ~Force4();
        
        std::string get_type();

    private:
};

#endif
