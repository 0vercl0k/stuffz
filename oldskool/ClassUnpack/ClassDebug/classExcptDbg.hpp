/**
 * \file classExcptDbg.hpp
 * \author 0vercl0k
 */

#ifndef _CLASS_EXCPTDBG_
#define _CLASS_EXCPTDBG_

#include <exception>

class ExcptDbg : public std::exception
{
    private:
        std::string m_error;
        unsigned long m_num;

    public:
        ExcptDbg(const std::string& function, const unsigned int line, const unsigned long num = 0) throw()
        : m_num(num)
        {
            m_error = "Erreur dans la fonction " + function + " à la ligne " + DebugUrProcess::toString<int>(line);
        }

        virtual const char* what() const throw()
        {   return m_error.c_str(); }

        unsigned long getErrorNumber() const throw()
        { return m_num; }

        virtual ~ExcptDbg() throw()
        { }
};

#endif
