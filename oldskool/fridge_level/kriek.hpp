#ifndef KRIEK_HPP
#define KRIEK_HPP

#include "beer.hpp"

class Kriek : public Beer
{
    public:
        explicit Kriek();
        explicit Kriek(char* name);

        ~Kriek();
        
        std::string get_type();

    private:

        unsigned int alcohol_percentage;
        unsigned int bla;
};

#endif
