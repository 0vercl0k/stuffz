#ifndef BEER_HPP
#define BEER_HPP

#include <string>

class Beer
{
    public:
        explicit Beer(char* name);
        virtual ~Beer();

        virtual std::string get_type() = 0;
        char* get_name() const;
        void set_empty_beer();
        bool is_empty_beer();

    private:
        char* m_name;
        bool m_is_empty_beer;
};

#endif
