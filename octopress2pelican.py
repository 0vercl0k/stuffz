#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    octopress2pelican.py - Converts the doar-e octopress markdown articles,
#    into ones that are compatible with Pelican.
#    Copyright (C) 2017 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k
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

def main(argc, argv):
    if argc != 3:
        print './octopress2pelican <octopress md post directory> <pelican post directory>'
        return 0

    octopress_dir, pelican_dir = argv[1 : ]
    if not os.path.isdir(octopress_dir):
        print octopress_dir, ' is not a directory, exiting'
        return 0

    if not os.path.isdir(pelican_dir):
        print pelican_dir, ' is not a directory, exiting'
        return 0

    for filename in os.listdir(octopress_dir):
        octopress_file = os.path.join(octopress_dir, filename)
        octopress_filename = os.path.basename(octopress_file)
        pelican_file = os.path.join(pelican_dir, octopress_filename)
        print 'Converting', octopress_filename, 'to', pelican_file, '...'
        with open(octopress_file, 'r') as infile:
            with open(pelican_file, 'w') as outfile:
                state = None
                prev_line_lf = False
                for line in infile.readlines():
                    if state is None and line.startswith('---'):
                        state = 'fix headers'
                    elif state == 'fix headers':
                        if line.startswith('title:'):
                            outfile.write(line.replace('title:', 'Title:').translate(None, '"'))
                        elif line.startswith('date: '):
                            outfile.write(line.replace('date:', 'Date:'))
                        elif line.startswith('categories:'):
                            outfile.write(line.replace('categories:', 'Tags:').translate(None, '[]'))
                        elif line.startswith('author: '):
                            outfile.write(line.replace('author:', 'Authors:'))
                        elif line.startswith('---'):
                            filename, _ = os.path.splitext(octopress_filename)
                            # strip the date
                            _, _, _, filename = filename.split('-', 3)
                            outfile.write('Slug: ' + filename + '\n\n')
                            state = 'fix body'
                    elif state == 'fix body':
                        if line.startswith('```') or line.startswith('{% codeblock %}'):
                            state = 'fix block'
                            block_start = '```'
                            if 'codeblock' in line:
                                block_start = '{% codeblock %}'
                            line = line.replace(block_start, '    :::')
                            if not prev_line_lf:
                                line = '\n' + line
                        elif line.startswith('{% img ') or line.startswith('{%img'):
                            # {% img center /images/ntdll.KiUserExceptionDispatcher/butterfly.png nt!KiExceptionDispatch graph from ReactOS %}
                            # {%img center /images/ntdll.KiUserExceptionDispatcher/butterfly.png nt!KiExceptionDispatch graph from ReactOS %}
                            # {% img center /images/debugger_data_model__javascript___x64_exception_handling/model.png %}
                            # {%img center /images/debugger_data_model__javascript___x64_exception_handling/model.png %}
                            line = line.translate(None, '{}%')
                            pieces = line.split()
                            style, link = pieces[1 : 3]
                            altattr = os.path.basename(link)
                            if len(pieces) > 3:
                                altattr = ' '.join(pieces[3 :])
                                print altattr
                            line = '<' + style + '>![' + altattr + '](' + link + ')</' + style + '>'
                        elif line.startswith("<div class='entry-content-toc'></div>"):
                            line = '[TOC]\n'
                        elif line.startswith('<!--more-->'):
                            line = '<!-- PELICAN_END_SUMMARY -->\n'
                        outfile.write(line)
                    elif state == 'fix block':
                        if line.startswith('```') or line.startswith('{% endcodeblock %}'):
                            state = 'fix body'
                        else:
                            outfile.write('    ' + line)

                    prev_line_lf = line == '\n'

        print 'Done'
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
