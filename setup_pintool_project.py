#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    setup_pintool_project.py - Just a little script to setup a VC10
#    project file for a Pin tool.
#    Copyright (C) 2013 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k
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
import os
import shutil

def main(argc, argv):
    pin_root = r'D:\Codes\Pin\pin-2.13-65163-msvc11-windows'
    project_root = r'D:\Codes'

    if argc != 2:
        print 'Usage: setup_pintool_project.py <project name>'
        return 0

    src = os.path.join(pin_root, 'source', 'tools', 'MyPinTool')
    dst = os.path.join(project_root, argv[1])
    os.mkdir(dst)
    print 'Copying the MyPinTool project in %r..'
    shutil.copy(
        os.path.join(src, 'MyPinTool.vcxproj'),
        os.path.join(dst, '%s.vcxproj' % argv[1])
    )
    shutil.copy(
        os.path.join(src, 'MyPinTool.cpp'),
        os.path.join(dst, '%s.cpp' % argv[1])
    )

    print 'Reading the VC project..'
    content = open(os.path.join(dst, '%s.vcxproj' % argv[1])).read()

    print 'Patching the relative references in the VC project, & renaming the solution/project..'
    patch_dic = [
        ('<None Include="..\README" />', ''),
        ('..\\..\\..', pin_root),
        ('..\\..', os.path.join(pin_root, 'source')),
        ('..', os.path.join(pin_root, 'source', 'tools')),
        ('MyPinTool', argv[1])
    ]

    for p, r in patch_dic:
        content = content.replace(p, r)

    print 'Writing the changes..'
    open(os.path.join(dst, '%s.vcxproj' % argv[1]), 'w').write(content)

    print 'Generating the .bat launcher..'
    with open(os.path.join(dst, 'run_debug.bat'), 'w') as f:
        f.write('%s -t %s -- whateveryouwant' % (
            os.path.join(pin_root, 'pin.exe'),
            os.path.join(dst, 'Debug', '%s.dll' % argv[1])
        ))

    print 'Done.'
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))