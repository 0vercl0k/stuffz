#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    generate_dependency_graph.py - 
#    Copyright (C) 2015 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k
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
import pygraphviz as pgv
import re
import random

def generate_dependency_graph(filename = ''):
    '''Generates a dependency graph ; basically starting from the bottom
    of the AES implementation & going back til the beginning.
    It is not really helpful I know, but here is an example (that may help you
    understand what I have in mind):
        l0 a = T[out[1]]
        l1 z = T[a]
        l2 r = T[b]
        l3 z2 = T[a]

    The output graph for this code would be something like:
        Nodes : 0, 1, 2, 3
        Edges : (0 -> 1, 0 -> 3)

    It basically means the line 2 can be placed anywhere in the code, both the line 3 & 1 have to be
    placed *after* the line 0. You can shuffle 3 & 1 around, but they have to be placed after 1.
    '''
    G = pgv.AGraph()
    lines = []
    with open('aes_unrolled_code.raw.clean.unique_aabbccdd') as f:
        i = 0
        for line in f.readlines():
            line = line.strip()
            lines.append(line)
            color = 'black'
            if 'ShiftRows' in line:
                color = 'red'
            G.add_node(i, color = color)
            i += 1

    # From the end until the beginning of the file
    i = len(lines) - 1
    while i >= 0:
        line = lines[i]
        print i, line

        l, r = '', ''
        if 'ShiftRows' not in line:
            _, r = map(
                str.strip,
                line.split(' = ', 1)
            )

        result = re.findall('(out\[[0-9]{1,2}\])', r)

        # 3 cases
        if len(result) == 0:
            if 'ShiftRows' in line:
                # The normal case is something like:
                #   ShiftRows(out); <- We are here
                #   aa = Tyboxes[8][0][out[0]];
                #   bb = Tyboxes[8][1][out[1]];
                #   cc = Tyboxes[8][2][out[2]];
                #   dd = Tyboxes[8][3][out[3]];
                #   out[0] = (Txor[Txor[(aa >> 0)  [...]
                #   out[1] = (Txor[Txor[(aa >> 8)  [...]
                #   out[2] = (Txor[Txor[(aa >> 16) [...]
                #   out[3] = (Txor[Txor[(aa >> 24) [...]
                #   aa = Tyboxes[8][4][out[4]];
                #   bb = Tyboxes[8][5][out[5]];
                #   cc = Tyboxes[8][6][out[6]];
                #   dd = Tyboxes[8][7][out[7]];
                #   out[4] = (Txor[Txor[(aa >> 0)  [...]
                #   out[5] = (Txor[Txor[(aa >> 8)  [...]
                #   out[6] = (Txor[Txor[(aa >> 16) [...]
                #   out[7] = (Txor[Txor[(aa >> 24) [...]
                #   [...]
                # We want to constraint only the aa, bb, cc, dd lines
                x, pattern = 32, '[aa|bb|cc|dd]_[0-9]{1,2} ='
                # Here we handle only the last ShiftRows where you have something like:
                #   ShiftRows(out); <- We are here
                #   out[0] = Tboxes_[0][out[0]];
                #   out[1] = Tboxes_[1][out[1]];
                #   out[2] = Tboxes_[2][out[2]];
                #   out[3] = Tboxes_[3][out[3]];
                #   out[4] = Tboxes_[4][out[4]];
                #   out[5] = Tboxes_[5][out[5]];
                #   out[6] = Tboxes_[6][out[6]];
                #   out[7] = Tboxes_[7][out[7]];
                #   out[8] = Tboxes_[8][out[8]];
                #   out[9] = Tboxes_[9][out[9]];
                #   out[10] = Tboxes_[10][out[10]];
                #   out[11] = Tboxes_[11][out[11]];
                #   out[12] = Tboxes_[12][out[12]];
                #   out[13] = Tboxes_[13][out[13]];
                #   out[14] = Tboxes_[14][out[14]];
                #   out[15] = Tboxes_[15][out[15]];
                if 'Tboxes_' in lines[i + 1]:
                    x, pattern = 16, 'Tboxes_'

                print 'ShiftRows %d cases @l%d' % (x, i)
                for z in range(1, x + 1):
                    if re.search(pattern, lines[i + z]):
                        G.add_edge(i, i + z)

                # The first ShiftRows doesn't have any operations before
                if i != 0:
                    # The scenario is the following:
                    #   aa = Tyboxes[8][0][out[0]];
                    #   bb = Tyboxes[8][1][out[1]];
                    #   cc = Tyboxes[8][2][out[2]];
                    #   dd = Tyboxes[8][3][out[3]];
                    #   out[0] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
                    #   out[1] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
                    #   out[2] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
                    #   out[3] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);
                    #   aa = Tyboxes[8][4][out[4]];
                    #   bb = Tyboxes[8][5][out[5]];
                    #   cc = Tyboxes[8][6][out[6]];
                    #   dd = Tyboxes[8][7][out[7]];
                    #   out[4] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
                    #   out[5] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
                    #   out[6] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
                    #   out[7] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);
                    #   aa = Tyboxes[8][8][out[8]];
                    #   bb = Tyboxes[8][9][out[9]];
                    #   cc = Tyboxes[8][10][out[10]];
                    #   dd = Tyboxes[8][11][out[11]];
                    #   out[8] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
                    #   out[9] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
                    #   out[10] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
                    #   out[11] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);
                    #   aa = Tyboxes[8][12][out[12]];
                    #   bb = Tyboxes[8][13][out[13]];
                    #   cc = Tyboxes[8][14][out[14]];
                    #   dd = Tyboxes[8][15][out[15]];
                    #   out[12] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][Txor[(cc >> 0) & 0xf][(dd >> 0) & 0xf]]) | ((Txor[Txor[(aa >> 4) & 0xf][(bb >> 4) & 0xf]][Txor[(cc >> 4) & 0xf][(dd >> 4) & 0xf]]) << 4);
                    #   out[13] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][Txor[(cc >> 8) & 0xf][(dd >> 8) & 0xf]]) | ((Txor[Txor[(aa >> 12) & 0xf][(bb >> 12) & 0xf]][Txor[(cc >> 12) & 0xf][(dd >> 12) & 0xf]]) << 4);
                    #   out[14] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0xf]][Txor[(cc >> 16) & 0xf][(dd >> 16) & 0xf]]) | ((Txor[Txor[(aa >> 20) & 0xf][(bb >> 20) & 0xf]][Txor[(cc >> 20) & 0xf][(dd >> 20) & 0xf]]) << 4);
                    #   out[15] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0xf]][Txor[(cc >> 24) & 0xf][(dd >> 24) & 0xf]]) | ((Txor[Txor[(aa >> 28) & 0xf][(bb >> 28) & 0xf]][Txor[(cc >> 28) & 0xf][(dd >> 28) & 0xf]]) << 4);
                    #   ShiftRows(out); <- We are here
                    # We just want to constraint every out[X] lines so that they depend of the upcoming ShiftRows
                    # BUT we do not care about the aa/bb/cc/dd ; they will be constrained on every Txor lines
                    for z in range(32):
                        # As said, we don't care about the others (aa, bb, cc, dd)
                        if lines[i - z].startswith('out'):
                            G.add_edge(i - z, i)
                i -= 1
                continue
            else:
                what_to_look_for = 'aa_'
        elif len(result) == 1:
            what_to_look_for = result[0]
        else:
            pass

        print 'Scanning backward to find %r (from l%d to l0)' % (what_to_look_for, i)
        # Scan backwards to find where it comes from
        for j in range(i - 1, -1, -1):
            line_backward_scan = lines[j]

            if 'ShiftRows' in line_backward_scan:
                print 'Found a ShiftRows first @l%d' % j
                break

            l, _ = map(
                str.strip,
                line_backward_scan.split(' = ', 1)
            )

            # We just find a dependency, let's add an edge
            if what_to_look_for in l:
                print 'Found %r @%d, adding edge %d->%d' % (what_to_look_for, j, j, i)
                G.add_edge(j, i)

                if what_to_look_for == 'aa_':
                    print 'And adding all the rest..'
                    # In that case we have something like this:
                    #  aa = Tyboxes[6][8][out[8]];
                    #  bb = Tyboxes[6][9][out[9]];
                    #  cc = Tyboxes[6][10][out[10]];
                    #  dd = Tyboxes[6][11][out[11]];
                    #  out[8] = (Txor[Txor[(aa >> 0) & 0xf][(bb >> 0) & 0xf]][...]
                    #  out[9] = (Txor[Txor[(aa >> 8) & 0xf][(bb >> 8) & 0xf]][...]
                    #  out[10] = (Txor[Txor[(aa >> 16) & 0xf][(bb >> 16) & 0x[...]
                    #  out[11] = (Txor[Txor[(aa >> 24) & 0xf][(bb >> 24) & 0x[...]
                    G.add_edge(j + 1, i) # bb
                    G.add_edge(j + 2, i) # cc
                    G.add_edge(j + 3, i) # dd

                    G.add_edge(j + 0, i - 1)
                    G.add_edge(j + 1, i - 1)
                    G.add_edge(j + 2, i - 1)
                    G.add_edge(j + 3, i - 1)

                    G.add_edge(j + 0, i - 2)
                    G.add_edge(j + 1, i - 2)
                    G.add_edge(j + 2, i - 2)
                    G.add_edge(j + 3, i - 2)

                    G.add_edge(j + 0, i - 3)
                    G.add_edge(j + 1, i - 3)
                    G.add_edge(j + 2, i - 3)
                    G.add_edge(j + 3, i - 3)
                    i -= 3 # 3 because -1 at the end of the loop
                break

        i -= 1
        # raw_input('>> ')

    assert(G.number_of_nodes() == len(lines))
    if filename != '':
        print 'All right, it sounds like it is finished, checkout', filename
        G.write(filename)

    return G

def generate_shuffled_implementation_via_dependency_graph(dependency_graph, out_filename):
    '''This function is basically leveraging the graph we produced in the previous function
    to generate an actual shuffled implementation of the AES white-box without breaking any
    constraints, keeping the result of this new shuffled function the same as the clean version.'''
    lines = open('aes_unrolled_code.raw.clean.unique_aabbccdd', 'r').readlines()
    print ' > Finding the bottom of the graph..'
    last_nodes = set()
    for i in range(len(lines)):
        _, degree_o = dependency_graph.degree_iter(i, indeg = False, outdeg = True).next()
        if degree_o == 0:
            last_nodes.add(dependency_graph.get_node(i))

    assert(len(last_nodes) != 0)
    print ' > Good, check it out: %r' % last_nodes
    shuffled_lines = []
    step_n = 0
    print ' > Lets go'
    while len(last_nodes) != 0:
        print '  %.2d> Shuffle %d nodes / lines..' % (step_n, len(last_nodes))
        random.shuffle(list(last_nodes), random = random.random)
        shuffled_lines.extend(lines[int(i.get_name())] for i in last_nodes)
        step_n += 1

        print '  %.2d> Finding parents / stepping back ..' % step_n
        tmp = set()
        for node in last_nodes:
            tmp.update(dependency_graph.in_neighbors(node))
        last_nodes = tmp
        step_n += 1

    shuffled_lines = reversed(shuffled_lines)
    with open(out_filename, 'w') as f:
        f.write('''void aes128_enc_wb_final_unrolled_shuffled_%d(unsigned char in[16], unsigned char out[16])
{
memcpy(out, in, 16);
''' % random.randint(0, 0xffffffff))
        f.writelines(shuffled_lines)
        f.write('}')
    return shuffled_lines

def main(argc, argv):
    print 'Step 1: Generate the dependency graph..'
    G = generate_dependency_graph('aes.dot')
    print 'Step 2: Generate the shuffled implementation..'
    lines = generate_shuffled_implementation_via_dependency_graph(G, 'aes_unrolled_code.shuffled.clean')
    print 'E.O.F'
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
