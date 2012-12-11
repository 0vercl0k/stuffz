#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    graph_coloring_z3.py - Constraint programming exercice: play with the graph coloring problem
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
import time
import pygraphviz as pgv
from z3 import *

def graph_coloring(graph):
    """Try to color graph with the least color possible"""
    s = Solver()
    nodes_colors = dict((node_name, Int('k%r' % node_name)) for node_name in graph.nodes())

    for i in range(1, graph.number_of_nodes()):
        for node in graph.nodes():
            s.add(nodes_colors[node] >= 0, nodes_colors[node] <= i)
            for neighbor in graph.neighbors(node):
                s.add(nodes_colors[node] != nodes_colors[neighbor])

        if s.check() == unsat:
            s.reset()
        else:
            print 'OK, found a solution with %d colors' % (i + 1)
            m = s.model()
            return dict((name, m[color].as_long()) for name, color in nodes_colors.iteritems())

    print 'Could not find a solution.'
    return None

def build_peternson_3_coloring_graph():
    """Build http://en.wikipedia.org/wiki/File:Petersen_graph_3-coloring.svg"""
    G = pgv.AGraph(directed = False)
    edges = [
        (0, 2), (0, 1), (0, 5), (0, 4), (1, 6), (1, 7),
        (2, 3), (2, 8), (3, 4), (3, 7), (4, 5), (4, 6),
        (5, 9), (6, 8), (7, 9), (8, 9), (9, 3)
    ]

    for i in range(10):
        G.add_node(i)

    for src, dst in edges:
        # Hum, the attribute 'directed' doesn't seem to work, so that's my workaround.
        G.add_edge(src, dst, dir = 'none')

    return G

def main(argc, argv):
    print 'Building the graph..'
    G = build_peternson_3_coloring_graph()

    print 'Graph successfully built, trying to color it now..'
    t1 = time.time()
    s = graph_coloring(G)
    t2 = time.time()

    print 'Here is the solution (in %ds):' % (t2 - t1)
    print s

    print 'Reconstructing the graph with colors..'
    color_available = [
        'red',
        'blue',
        'green',
        'pink'
    ]

    for node in G.nodes_iter():
        n = G.get_node(node)
        n.attr['color'] = color_available[s[node]]

    print 'Saving it in the current directory..'
    G.layout('circo')
    G.draw('./graph_colored.png')
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))