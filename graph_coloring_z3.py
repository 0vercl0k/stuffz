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

    # We'll test if the graph is colorable with 1 then 2 then 3 ..colors until to find the correct number
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

    raise Exception('Could not find a solution.')

def build_peternson_3_coloring_graph():
    """Build http://en.wikipedia.org/wiki/File:Petersen_graph_3-coloring.svg"""
    G = pgv.AGraph()
    G.node_attr['style'] = 'filled'
    # Hum, the attribute 'directed' (in AGraph constructor) doesn't seem to work, so that's my workaround.
    G.edge_attr['dir'] = 'none'

    edges = [
        (0, 2), (0, 1), (0, 5), (0, 4), (1, 6), (1, 7),
        (2, 3), (2, 8), (3, 4), (3, 7), (4, 5), (4, 6),
        (5, 9), (6, 8), (7, 9), (8, 9), (9, 3)
    ]

    for i in range(10):
        G.add_node(i)

    for src, dst in edges:
        G.add_edge(src, dst)

    return (G, 'peternson_3_coloring_graph', 'circo')

def build_fat_graph():
    """Build http://www.graphviz.org/content/twopi2"""
    G = pgv.AGraph('graph_coloring_z3_example_fat_graph.gv')
    return (G, 'twopi2_fat_graph', 'twopi')

def main(argc, argv):
    print 'Building the graph..'

    Gs = [
        build_peternson_3_coloring_graph(),
        build_fat_graph()
    ]

    for G, name, layout in Gs:
        print 'Trying to color %s now (%d nodes, %d edges)..' % (repr(name), G.number_of_nodes(), G.number_of_edges())
        t1 = time.time()
        s = graph_coloring(G)
        t2 = time.time()

        print 'Here is the solution (in %ds):' % (t2 - t1)
        if len(s) < 20:
            print s
        else:
            print 'Too long, see the .png!'

        print 'Setting the colors on the nodes..'
        color_available = [
            'red',
            'blue',
            'green',
            'pink'
        ]

        for node in G.nodes_iter():
            n = G.get_node(node)
            n.attr['color'] = color_available[s[node]]

        print 'Saving it in the current directory with the layout %s..' % repr(layout)
        G.layout(layout)
        G.draw('./graph_coloring_z3_%s_colored.png' % name)
        print '---'
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))