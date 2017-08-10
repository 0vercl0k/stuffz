#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    drcov_directory.py - Run drcov through a directory full of test cases
#    against a harness.
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
import subprocess
import multiprocessing
from functools import partial

drio_base = r'D:\Codes\DynamoRIO-Windows-6.2.0-2'
drio = os.path.join(drio_base, r'bin32\drrun.exe')

def GenerateCoverageTrace(harness, out_dir, testcase_path):
    cmd = [
        drio, '-t', 'drcov', '-dump_binary', '-logdir', out_dir,
        '--', harness, testcase_path
    ]
    with open(os.devnull, 'wb') as nul:
        subprocess.Popen(cmd, stdout = nul, stderr = nul).wait()
    return testcase_path

def main(argc, argv):
    if argc != 4:
        print './drcov_directory.py <harness.exe> <testcases> <output dir>'
        return 0

    harness, testcases, out_dir = argv[1:]
    if not os.path.isdir(testcases):
        print '[-]', testcases, 'needs to be a directory with test-cases.'
        return 0

    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
        print '[+] Created', out_dir

    print '[*] Generating coverage for ', harness, '..'
    gen_coverage = partial(GenerateCoverageTrace, harness, out_dir)
    files = [os.path.join(testcases, file_) for file_ in os.listdir(testcases)]
    p = multiprocessing.Pool(processes = multiprocessing.cpu_count() / 2)
    for filepath in p.imap_unordered(gen_coverage, files):
        print '[+] Generated trace for', filepath, '\r',

    print
    p.close()

    print '[+] Done.'
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
