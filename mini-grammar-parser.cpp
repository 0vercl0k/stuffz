/*
#
#    mini-grammar-parser.cpp - A simple class to parse/generate grammar-based output.
#    Copyright (C) 2014 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k
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
#include "mini-grammar-parser.hpp"
#include <fstream>
#include <list>
#include <iostream>
#include <sstream>

MiniGrammarParser::MiniGrammarParser(std::string &path_grammar)
    : m_path(path_grammar)
{
}

std::string MiniGrammarParser::generate_(std::shared_ptr<Rule> &rule)
{
    std::stringstream ss;

    if (rule->type == Rule::RuleChoice)
    {
        // If we have a RuleChoice, we pick one randomly according to
        // the different weights we got
        int idx = rand() % rule->total_weights;
        for (size_t i = 0; i < rule->children.size(); ++i)
        {
            idx -= rule->weights.at(i);
            if (idx < 0)
            {
                ss << generate_(rule->children.at(i));
                break;
            }
        }
    }
    else if (rule->type == Rule::RuleStar)
    {
        // RuleStar means we can execute the symbol child X times
        size_t max = (rand() % rule->max_occurences) + 1;
        for (size_t i = 0; i < max; ++i)
            ss << generate_(rule->children.at(0));
    }
    else if (rule->type == Rule::RuleConcatenation)
    {
        for (auto it = rule->children.begin(); it != rule->children.end(); ++it)
            ss << generate_(*it);
    }
    else if (rule->type == Rule::RuleSymbolName)
        // The children are usually RuleSymbolName ; we have to look into
        // the symbol store to find the rule
        ss << generate_(m_symbols.at(rule->name));
    else if (rule->type == Rule::RuleString)
    {
        // Here we can handle specific strings if we need so
        if (rule->name == "\\n")
            ss << std::endl;
        else if (rule->name == "\\t")
            ss << "\t";
        else
            ss << rule->name;
    }
    else
        throw std::runtime_error("Type unknown");

    return ss.str();
}

std::string MiniGrammarParser::generate(const std::string &rulename)
{
    return generate_(m_symbols.at(rulename));
}

size_t MiniGrammarParser::extract_integer(std::string &line, size_t &i)
{
    // Eat whitespaces
    for (; i < line.size() && (line.at(i) == ' ' || line.at(i) == '\t'); ++i);

    std::string integer_s;
    for (; i < line.size() && line.at(i) != ' '; i++)
        integer_s += line.at(i);

    size_t integer = atoi(integer_s.c_str());
    return integer;
}

bool MiniGrammarParser::extract_symbol_or_string(std::string &line, size_t &i, std::string &value_out)
{
    bool is_string = false;

    // Eat whitespaces
    for (; i < line.size() && (line.at(i) == ' ' || line.at(i) == '\t'); ++i);
    if (i >= line.size())
    {
        value_out = "line ending";
        goto end;
    }

    // Direct string
    if (line.at(i) == '\'' || line.at(i) == '"')
    {
        is_string = true;
        unsigned char delim = line.at(i);

        // Go over the delimiter obviously :))
        i++;

        // Retrieve the value
        for (; i < line.size() && line.at(i) != delim; ++i)
            value_out += line.at(i);

        // Go over the end delimiter now
        i++;
    }
    // Symbol name
    else
        for (; i < line.size() && line.at(i) != ' '; ++i)
            value_out += line.at(i);
end:
    return is_string;
}

void MiniGrammarParser::parse()
{
    std::ifstream input_file;
    input_file.open(m_path);

    std::string line;
    size_t line_n = 0;
    while (std::getline(input_file, line))
    {
        if (line == "" || line.at(0) == ' ' || line.at(0) == '#')
            continue;

        // First extract the name
        std::shared_ptr<Rule> rule = std::make_shared<Rule>();
        size_t i = 0;
        extract_symbol_or_string(line, i, rule->name);
        if (i == line.size())
            throw std::runtime_error("Corrupted line");

        std::cout << "[" << line_n << "] Symbol: " << rule->name << " ";

        // Eat whitespaces
        for (; i < line.size() && (line.at(i) == ' ' || line.at(i) == '\t'); ++i);
        if (i >= line.size())
            throw std::runtime_error("Corrupted line");

        // Parse the rule
        if (isdigit(line.at(i)))
        {
            rule->type = Rule::RuleChoice;
            rule->total_weights = 0;
            std::cout << "[Choice]";
            // Save the position, as we need to read several lines
            // for that type of rule
            std::streampos pos = input_file.tellg();

            do
            {
                if (line == "" || line.at(i) == '#')
                    continue;

                // If this is true, it means this is the starting of a new
                // rule definition
                if (isalpha(line.at(i)))
                    break;

                // Extract the weight value
                size_t weight = extract_integer(line, i);

                // Extract the symbol
                std::string out;
                bool is_string = extract_symbol_or_string(line, i, out);
                if (out == "line ending")
                    break;

                std::cout << ", ";
                std::shared_ptr<Rule> child = std::make_shared<Rule>();
                if (is_string)
                    child->type = Rule::RuleString;
                else
                    child->type = Rule::RuleSymbolName;

                // Add the rule into the symbol store
                child->name = out;
                rule->children.push_back(child);
                rule->weights.push_back(weight);
                rule->total_weights += weight;
                std::cout << "`" << child->name << "`(" << weight << ")";

                // As we are going to read a new line, set the current
                // offset to 0
                i = 0;
            } while (std::getline(input_file, line));

            // Don't forget to get back to the previous position
            // to continue the parsing
            input_file.seekg(pos);
        }
        else if (line.at(i) == '*')
        {
            rule->type = Rule::RuleStar;
            std::cout << "Star";
            i++;

            // Extract the maximum number of recursivity
            size_t max_occurences = extract_integer(line, i);

            std::string out;
            bool is_string = extract_symbol_or_string(line, i, out);
            std::cout << ", ";

            if (is_string)
                throw std::runtime_error("Found a string in a RuleStar definition");

            // Build the child rule
            std::shared_ptr<Rule> child = std::make_shared<Rule>();
            child->type = Rule::RuleSymbolName;
            child->name = out;

            // Build the rule
            rule->max_occurences = max_occurences;
            rule->children.push_back(child);
            std::cout << "`" << child->name << "`(max count: " << max_occurences << ")";
        }
        else if (isalnum(line.at(i)) || line.at(i) == '"' || line.at(i) == '\'')
        {
            rule->type = Rule::RuleConcatenation;
            std::cout << "Concat";

            while (i < line.size())
            {
                std::string out;
                bool is_string = extract_symbol_or_string(line, i, out);
                if (out == "line ending")
                    break;

                std::cout << ", ";
                std::shared_ptr<Rule> child = std::make_shared<Rule>();
                if (is_string)
                    child->type = Rule::RuleString;
                else
                    child->type = Rule::RuleSymbolName;

                child->name = out;
                rule->children.push_back(child);
                std::cout << "`" << child->name << "`";
            }
        }
        else
            throw std::runtime_error("A rule seems to be corrupted");

        line_n++;
        std::cout << std::endl;

        if (rule->type == Rule::RuleStar && rule->children.size() != 1)
            throw std::runtime_error("You have a Star rule with more than one child, hu?");

        if (rule->type != Rule::RuleString && rule->type != Rule::RuleSymbolName && rule->children.size() == 0)
            throw std::runtime_error("Seems you have a rule that does not have a children");

        m_symbols.insert(
            std::make_pair(
            rule->name,
            rule
            )
            );
    }

    input_file.close();
}