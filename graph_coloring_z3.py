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
from z3 import *

class Graph:
    def __init__(self, name):
        self.list_neighbor = {}
        self.list_node = {}
        self.name = name

    def add_node(self, node):
        self.list_node[node] = True

    def add_edge(self, node, nodebis):
        if node not in self.list_neighbor:
            self.list_neighbor[node] = []

        if nodebis not in self.list_neighbor[node]:
            self.list_neighbor[node].append(nodebis)

        if nodebis not in self.list_neighbor:
            self.list_neighbor[nodebis] = []

        if node not in self.list_neighbor[nodebis]:
            self.list_neighbor[nodebis].append(node)

    def neighbors(self, node):
        return self.list_neighbor[node] if node in self.list_neighbor else []

    def nodes(self):
        return self.list_node.keys()

def graph_coloring(graph):
    """Try to color graph with the least color possible"""
    s = Solver()
    nodes_colors = [Int('k%d' % n) for n in graph.nodes()]

    for i in range(len(graph.nodes())):
        for node_color in nodes_colors:
            s.add(node_color >= 0, node_color < i)

        for node in graph.nodes():
            color = Int('k%s' % node)
            for neighbor in graph.neighbors(node):
                s.add(color != nodes_colors[neighbor])

        if s.check() == unsat:
            s.reset()
        else:
            print 'OK, found a solution with %d colors' % (i + 1)
            m = s.model()
            return [('node_%d' % x, m[color].as_long()) for x, color in enumerate(nodes_colors)]

def build_peternson_3_coloring_graph():
    """Build http://en.wikipedia.org/wiki/File:Petersen_graph_3-coloring.svg"""
    G = Graph('peternson 3-coloring graph')
    edges = [
        (0, 2), (0, 1), (0, 5), (0, 4), (1, 6), (1, 7),
        (2, 3), (2, 8), (3, 4), (3, 7), (4, 5), (4, 6),
        (5, 9), (6, 8), (7, 9), (8, 9), (9, 3)
    ]

    for i in range(10):
        G.add_node(i)

    for src, dst in edges:
        G.add_edge(src, dst)

    return G

def main(argc, argv):
    print 'Building the graph..'
    G = build_peternson_3_coloring_graph()

    print '%s successfully built, trying to color it now..' % repr(G.name)
    t1 = time.time()
    s = graph_coloring(G)
    t2 = time.time()

    print 'Here is the solution (in %ds):' % (t2 - t1)
    print s
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))