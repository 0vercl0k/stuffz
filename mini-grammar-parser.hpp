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
#	PS D:\Codes\MiniGrammarParser\Debug> .\MiniGrammarParser.exe
#		[0] Symbol: QuotedSentences Star, `QuotedSentenceWithEOL`(max count: 20)
#		[1] Symbol: QuotedSentenceWithEOL Concat, `QuotedSentence`, `\n`
#		[2] Symbol: QuotedSentence Concat, `"`, `StartingWord`, `CommasOrNot`, ` `, `MiddleWord`, `"`
#		[3] Symbol: StartingWord [Choice], `Hello`(10), `Good morning`(5), `Yo`(1)
#		[4] Symbol: MiddleWord Concat, ```, `Name`, ```
#		[5] Symbol: CommasOrNot [Choice], `Commas`(1), ``(1)
#		[6] Symbol: Commas Star, `Comma`(max count: 10)
#		[7] Symbol: Comma Concat, `,`
#		[8] Symbol: Name [Choice], `Dad`(4), `Mama`(1), `man`(1)
#		=============
#		"Hello, `Dad`"
#		"Hello,,,,,,,,, `Dad`"
#		"Good morning, `Dad`"
#		"Hello `Dad`"
#		"Good morning `Dad`"
#		"Hello `Dad`"
#		"Good morning `Dad`"
#		"Hello `Dad`"
#		"Hello `Dad`"
#		"Yo `Dad`"
#		"Hello `Dad`"
#		"Hello `man`"
#		"Hello `Dad`"
#		"Good morning `Dad`"
#		"Hello `Dad`"
#		"Hello `Mama`"
#		"Hello `Dad`"
#		"Good morning `Dad`"
#		"Good morning,,,,,, `Dad`"
#
#	PS D:\Codes\MiniGrammarParser\Debug> type ..\demo.txt
#		QuotedSentences *20 QuotedSentenceWithEOL
#		QuotedSentenceWithEOL QuotedSentence "\n"
#		QuotedSentence '"' StartingWord CommasOrNot ' ' MiddleWord '"'
#		StartingWord 10 "Hello"
#		5 "Good morning"
#		1 "Yo"
#		MiddleWord '`' Name "`"
#		CommasOrNot 1 Commas
#		1 ""
#
#		Commas *10 Comma
#		Comma ','
#
#		# Comment, blabla
#
#		Name 4 "Dad"
#		1 "Mama"
#		1 "man"
*/
#pragma once
#include <string>
#include <vector>
#include <memory>
#include <map>

class MiniGrammarParser
{
public:
    struct Rule
    {
        enum type
        {
            RuleChoice,
            RuleConcatenation,
            RuleStar,
            RuleString,
            RuleSymbolName,
        } type;
        std::string name;
        std::vector<std::shared_ptr<Rule>> children; // Used if RuleChoice or RuleConcatenation
        std::vector<size_t> weights; // Used if RuleChoice
        size_t total_weights; // Used if RuleChoice
        size_t max_occurences; // Used if RuleStar
    };

    explicit MiniGrammarParser(std::string &path_grammar);

    void parse();
    std::string generate(const std::string &rulename);

private:
    std::string MiniGrammarParser::generate_(std::shared_ptr<Rule> &rule);
    size_t MiniGrammarParser::extract_integer(std::string &line, size_t &i);
    bool extract_symbol_or_string(std::string &line, size_t &i, std::string &value_out);

    std::map<std::string, std::shared_ptr<Rule>> m_symbols;
    std::string m_path;
};