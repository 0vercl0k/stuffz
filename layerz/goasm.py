#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    goasm.py - bla
#    Copyright (C) 2012 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k
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

import sys

class GoAsmObject(object):
    """ All the "serializable" goasm objects inherit from this class """
    def __str__(self):
        pass

class CodeBlock(GoAsmObject):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return self.code

class RawContent(GoAsmObject):
    def __init__(self, raw, label_name = ''):
        self.raw = raw
        self.label_name = label_name

    def __str__(self):
        s = ''
        if self.label_name != '':
            s  = '%s:\n' % self.label_name
        s += 'db ' + ','.join(['0x%.2x' % ord(b) for b in self.raw])
        return s

class Section(object):
    """ A section of code/data can contain various stuff like string or bloc of code """
    def __init__(self, name, type_of_section):
        self.containing = []
        self.name = name
        assert(type_of_section in ['DATA', 'CODE'])
        self.type_of_section = type_of_section

    def add(self, x):
        assert(issubclass(x.__class__, GoAsmObject))
        self.containing.append(x)

    def is_code_section(self):
        return self.type_of_section == 'CODE'

    def is_data_section(self):
        return self.type_of_section == 'DATA'

    def __str__(self):
        s  = '%s SECTION %s\n' % (self.type_of_section, self.name)
        if self.is_code_section():
            s += 'start:\n'
        s += '\n'.join(map(str, self.containing))
        return s

class CodeSection(Section):
    """ A code section """
    def __init__(self, name):
        super(CodeSection, self).__init__(name, 'CODE')

class DataSection(Section):
    """ A data section """
    def __init__(self, name):
        super(DataSection, self).__init__(name, 'DATA')

class Executable(object):
    def __init__(self, name):
        self.name = name
        self.sections = []
        self.modules_to_link = 'kernel32.dll user32.dll gdi32.dll winspool.dll comdlg32.dll'.split(' ')

    def add(self, s):
        assert(issubclass(s.__class__, Section))
        self.sections.append(s)

    def __str__(self):
        s = ''
        for section in self.sections:
            s += str(section)
        return s

    def generate_link(self):
        """ Generate the link.txt """
        with open('link.txt', 'w') as f:
            f.write('%s.obj\n\n' % self.name)
            for module in self.modules_to_link:
                f.write(module + '\n')

    def generate_make(self):
        """ Generate the make.bat """
        with open('make.bat', 'w') as f:
            f.write('@echo off\n')
            f.write('set name=%s\n' % self.name)
            f.write('goasm  /fo %name%.obj %name%.asm\n')
            f.write('golink  @link.txt\n')
            f.write('del *.obj\n')
            f.write('pause')

    def generate_asm(self):
        with open('%s.asm' % self.name, 'w') as f:
            f.write(str(self))

    def generate(self):
        """ Generate the link.txt & the make.bat & the .asm """
        self.generate_link()
        self.generate_make()
        self.generate_asm()

def main(argc, argv):
    e = Executable('testin_project')

    c = CodeSection('koooode')
    c.add(RawContent('\xeb\xfe', 'label'))
    e.add(c)
    e.generate()
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))