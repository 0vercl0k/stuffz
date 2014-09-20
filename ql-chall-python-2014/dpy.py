#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    dpy.py - Displays Python objects in GDB as you would see them
#    in your Python shell
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

from __future__ import print_function
import gdb
import pprint

class PrettyPrintPyObject(gdb.Command):
    '''
    Pretty print Py*Object instances as you would see them
    in a Python shell

    Usage:
        dpy <address>
    '''
    def __init__(self):
        gdb.Command.__init__(self, 'dpy', gdb.COMMAND_NONE)
        infos = {
            'PyString' : self._display_string,
            'PyInt' : self._display_int,
            'PyNone' : self._display_none,

            'PyTuple' : self._display_tuple,
            'PyList' : self._display_list,
            'PyDict' : self._display_dict,
            
            'PyCode' : self._display_code,
            'PyFunction' : self._display_function
        }

        self.dispatcher = dict((int(gdb.parse_and_eval('&%s_Type' % k)), v) for k, v in infos.items())

    def _display_string(self, address):
        '''Displays PyStringObject'''
        PyStringObject_type = gdb.lookup_type('PyStringObject').pointer()
        s = address.cast(PyStringObject_type)
        size = int(s['ob_size'])
        return 'string', ''.join(chr(s['ob_sval'][i] & 0xff) for i in range(size))

    def _display_int(self, address):
        '''Displays PyIntObject'''
        PyIntObject_type = gdb.lookup_type('PyIntObject').pointer()
        i = address.cast(PyIntObject_type)
        return 'int', int(i['ob_ival'])

    def _display_none(self, address):
        '''Displays None'''
        return 'None', None

    def _display_tuple(self, address):
        '''Displays tuple'''
        PyTupleObject_type = gdb.lookup_type('PyTupleObject').pointer()
        t = address.cast(PyTupleObject_type)
        items = list()
        for i in range(int(t['ob_size'])):
            ty, v = self._dispatch(t['ob_item'][i])
            if ty == 'NotImplemented':
                v = 'UNKNOW'
            items.append(v)

        return 'tuple', tuple(items)

    def _display_list(self, address):
        '''Displays list'''
        PyListObject_type = gdb.lookup_type('PyListObject').pointer()
        l = address.cast(PyListObject_type)
        items = list()
        for i in range(int(l['ob_size'])):
            ty, v = self._dispatch(l['ob_item'][i])
            if ty == 'NotImplemented':
                v = 'UNKNOW'
            items.append(v)

        return 'list', items

    def _display_code(self, address):
        '''Displays PyCodeObject'''
        PyCodeObject_type = gdb.lookup_type('PyCodeObject').pointer()
        c = address.cast(PyCodeObject_type)
        code = {}

        for field in ('co_consts', 'co_code', 'co_names', 'co_varnames', 'co_name'):
            t, v = self._dispatch(c[field])
            if t == 'NotImplemented':
                v = 'UNKNOW'
            code[field] = v
        
        code['co_code'] = ''.join('\\x%.2x' % ord(i) for i in code['co_code'])
        return 'code', code

    def _display_function(self, address):
        '''Displays PyFunctionObject'''
        PyFunctionObject_type = gdb.lookup_type('PyFunctionObject').pointer()
        f = address.cast(PyFunctionObject_type)
        func = {}

        for field in ('func_code', 'func_doc', 'func_name', 'func_dict', 'func_module'):
            if f[field] != 0:
                t, v = self._dispatch(f[field])
                if t == 'NotImplemented':
                    v = 'UNKNOW'
            else:
                v = None
            func[field] = v

        return 'function', func

    def _display_dict(self, address):
        '''Displays PyDictObject ; http://www.laurentluce.com/posts/python-dictionary-implementation/'''
        PyDictObject_type = gdb.lookup_type('PyDictObject').pointer()
        d = address.cast(PyDictObject_type)
        di = {}
        for i in range(int(d['ma_mask']) - 1):
            entry = d['ma_table'][i]
            if entry['me_key'] != 0 and entry['me_value'] != 0:
                key, value = 'UNKNOW', 'UNKNOW'
                t, v = self._dispatch(entry['me_key'])
                if t != 'NotImplemented':
                    key = v

                t, v = self._dispatch(entry['me_value'])
                if t != 'NotImplemented':
                    value = v

                di[key] = value

        return 'dict', di

    def _dispatch(self, address):
        '''Dispatches a call to the function that will be able
        to display the type'''
        PyObject_type = gdb.lookup_type('PyObject').pointer()
        ob_type = int(address.cast(PyObject_type)['ob_type'])
        if ob_type in self.dispatcher:
            return self.dispatcher[ob_type](address)
        return 'NotImplemented', 0xb00b

    def invoke(self, arg, from_tty):
        '''Core of the command'''
        address_obj = gdb.parse_and_eval(arg)
        t, v = self._dispatch(address_obj)
        if t != 'NotImplemented':
            print('%s -> ' % t, end = '')
            pprint.pprint(v)
        else:
            print(':(')

PrettyPrintPyObject()
