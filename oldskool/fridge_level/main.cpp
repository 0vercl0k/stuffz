/*
**    main.cpp - Fridge binary by @0vercl0k & NiklosKoda for w3challs guys!
**    Copyright (C) 2011 0vercl0k
**
**    This program is free software: you can redistribute it and/or modify
**    it under the terms of the GNU General Public License as published by
**    the Free Software Foundation, either version 3 of the License, or
**    (at your option) any later version.
**
**    This program is distributed in the hope that it will be useful,
**    but WITHOUT ANY WARRANTY; without even the implied warranty of
**    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
**    GNU General Public License for more details.
**
**    You should have received a copy of the GNU General Public License
**    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <iostream>
#include <sstream>
#include <vector>
#include <string>
#include <cstdlib>
#include <list>

#include "beer.hpp"
#include "force4.hpp"
#include "kriek.hpp"

//Exploiting this binary drunk is not a good idea, trust me.
#define MAX_BEERS_IN_FRIDGE 5
#define MAX_EMPTY_BEERS 6

std::vector<Beer*> my_fridge;
static unsigned int empty_beer_nb = 0;

std::string get_command_args(std::string &input, std::vector<std::string> &args)
{
    size_t id_space = input.find(' ');
    std::string command(input);

    if(id_space != std::string::npos)
    {
        command = input.substr(0, id_space);

        size_t id_start = id_space + 1;
        while((id_space = input.find(' ', id_start)) != std::string::npos)
        {
            std::string arg(input.substr(id_start, (id_space - id_start)));
            if(arg.size() == 0)
                break;

            args.push_back(arg);
            id_start = id_space + 1;
        }

        std::string arg(input.substr(id_start, (input.size() - id_start)));
        if(arg != " ")
            args.push_back(arg);
    }

    return command;
}

bool add_beer(char* name, std::string &typebeer)
{
    if(typebeer != "f4" && typebeer != "krk")
    {
        std::cout << "You can choose only two types of beer: 'f4' or 'krk'. RTFM luke." << std::endl;
        return false;
    }

    Beer* b = NULL;
    if(typebeer == "f4")
        b = static_cast<Beer*>(new Force4(name));
    else
        b = static_cast<Beer*>(new Kriek(name));

    my_fridge.push_back(b);
    return true;
}

short string_to_short(std::string &n)
{
    return (short)atoi(n.c_str());
}

void dispatch_command(std::string &command, std::vector<std::string> &args)
{
    if(command == "help")
    {
        std::cout << "* add_beer <type of beer (f4 or krk)> <name_beer>: Add a beer to your fridge" << std::endl;
        std::cout << "* add_beers <type of beers (f4 or krk)> <name_beers> <number>: Add *number* beers to your fridge" << std::endl;
        std::cout << "* delete_beer <id>: Delete a beer" << std::endl;
        std::cout << "* list: List the beers" << std::endl;
    }

    if(command == "delete_beer")
    {
        if(args.size() != 1)
        {
            std::cout << "This option requires one argument, please read the source LUKE." << std::endl;
            return;
        }

        unsigned int id = 0;
        std::istringstream iss(args.at(0));
        iss >> id;

        if(my_fridge.size() == 0)
        {
            std::cout << "Ohai, the fridge is empty bitch." << std::endl;
            return;
        }

        if(id > (my_fridge.size() - 1))
        {
            std::cout << "You're trying to delete the beer id " << id << ", but you have a total of " << my_fridge.size() << " beers in the fridge." << std::endl;
            return;
        }

        /*
        if(empty_beer_nb < MAX_EMPTY_BEERS)
        {
            delete my_fridge.at(id);
            my_fridge[id] = new EmptyBeer();
        }
        else
        {
            std::vector<unsigned int> id_empty;

            // TIME TO DEFRAGMENT THIS SHITTY FRIDGE
            for(std::vector<Beer*>::iterator it = my_fridge.begin(); it != my_fridge.end(); ++it)
            {
                if((*it)->is_empty_beer() == true)
                {
                    delete *it;
                    id_empty.push_back(*it);
                }
            }
        */

        delete my_fridge.at(id)
        if(id != (my_fridge.size() - 1))
        {
            for(unsigned int i = id + 1; i < my_fridge.size(); ++i)
                my_fridge[(i - 1)] = my_fridge[i];
        }
    }

    if(command == "list")
    {
        unsigned int i = 0;
        for(std::vector<Beer*>::const_iterator it = my_fridge.begin();
            it != my_fridge.end();
            ++it, ++i)
        {
            std::cout << "----" << std::endl;
            std::cout << "ID: " << i << std::endl;
            std::cout << "Name: " << (*it)->get_name() << std::endl;
            std::cout << "Type of beer: " << (*it)->get_type() << std::endl;
        }
    }

    if(command == "add_beer")
    {
        if(args.size() != 2)
        {
            std::cout << "This option requires two arguments, please RTFM mofo." << std::endl;
            return;
        }

        if(my_fridge.size() >= MAX_BEERS_IN_FRIDGE)
        {
            std::cout << "You have enough beers in your fridge, bitch." << std::endl;
            return;
        }

        if(add_beer((char*)args.at(1).c_str(), args.at(0)))
            std::cout << "Beer successfuly added to your fridge." << std::endl;
    }

    if(command == "add_beers")
    {
        if(args.size() != 3)
        {
            std::cout << "This option requires three arguments, please RTFM mofo." << std::endl;
            return;
        }

        short nb = string_to_short(args.at(2));
        if(nb == 0)
            return;

        std::cout << nb << std::endl;

        if((nb+(short)my_fridge.size()) > MAX_BEERS_IN_FRIDGE)
        {
            std::cout << "You will have too much beers in your frigde, next time i'll break ya neck." << std::endl;
            return;
        }

        for(unsigned short i = 0; i < (unsigned short)nb; ++i)
            add_beer((char*)args.at(1).c_str(), args.at(0));
    }
}

int main(int argc, char* argv[])
{
    std::string input, command;
    std::vector<std::string> arguments;

    while(input != "exit" && input != "quit")
    {
        std::cout << "fridge@localhost> ";
        std::getline(std::cin, input);

        if(input.size() == 0)
            continue;

        command = get_command_args(input, arguments);

        dispatch_command(command, arguments);

        arguments.clear();
    }
    return 0;
}
