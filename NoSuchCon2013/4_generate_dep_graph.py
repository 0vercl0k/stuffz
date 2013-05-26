#
#    4_generate_dep_graph.py - NoSuchCon 2013 Script to graph the algorithm with Graphviz.
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

import pygraphviz as pgv
import re

nodes = set()
edges = []

to_read = {}
table_counter = {}
tbox_idx = 10000

def get_tbox_id():
    global tbox_idx
    r = tbox_idx
    tbox_idx += 1
    return r

def clean_to_read(dest):
    if dest in to_read:
        del to_read[dest]

with open('ssa_algorithm_raw') as f:
    for line in f.readlines():
        line = line.strip()
        if line == '':
            continue

        nodes_to_add = []
        edges_to_add = []

        pattern    = '(.+) = T[H]*_([A-F0-9]+)\[(.+?)\];$'
        pattern_16 = '(.+) = T16_([A-F0-9]+)\[(.+)\]\[(.+)\];$'

        match = re.search(pattern, line)
        if match:
            fetch = match.group(3)
            tbox = 'T_%s' % match.group(2)
            dest = match.group(1)
            tbox_id = get_tbox_id()

            nodes_to_add.append(
                (tbox, 'box', 'yellow', tbox_id)
            )

            if fetch in to_read:
                edges_to_add.append(
                    (to_read[fetch], tbox_id)
                )
            else:
                # On ajoute le fetch vers la tbox
                edges_to_add.append(
                    (fetch, tbox_id)
                )
                # Et on ajoute le node
                nodes_to_add.append(
                    (fetch, 'circle', 'red' if fetch.startswith('out') else 'green', fetch)
                )

            clean_to_read(dest)

            if dest.startswith('output') == True:
                nodes_to_add.append(
                    (dest, 'circle', 'red', dest)
                )
                edges_to_add.append(
                    (tbox_id, dest)
                )
            else:
                to_read[dest] = tbox_id


        match = re.search(pattern_16, line)
        if match:
            fetchs = [
                match.group(3),
                match.group(4)
            ]
            tbox = 'T16_%s' % match.group(2)
            dest = match.group(1)
            tbox_id = get_tbox_id()

            nodes_to_add.append(
                (tbox, 'box', 'orange', tbox_id)
            )

            for fetch in fetchs:
                if fetch in to_read:
                    edges_to_add.append(
                        (to_read[fetch], tbox_id)
                    )
                else:
                    edges_to_add.append(
                        (fetch, tbox_id)
                    )
                    nodes_to_add.append(
                        (fetch, 'circle', 'red' if fetch.startswith('out') else 'green', fetch)
                    )

            clean_to_read(dest)

            if dest.startswith('output') == True:
                nodes_to_add.append(
                    (dest, 'circle', 'red', dest)
                )
                edges_to_add.append(
                    (tbox_id, dest)
                )
            else:
                to_read[dest] = tbox_id

        for e in nodes_to_add:
            nodes.add(e)
        for e in edges_to_add:
            edges.append(e)

print 'EOF, generating the graph'
G = pgv.AGraph(directed = False)
G.graph_attr.update({
    'splines' : 'true',
    'label' : 'tg'
})

G.node_attr.update({
    'style' : 'filled',
    'shape' : 'circle',
    'color' : 'grey',
    'fontname' : 'Consolas Bold', # monospace font ftw!
    'fontsize' : 9,
    'nojustify' : 'true'
})

G.edge_attr.update({
    'color' : 'blue',
    'dir' : 'forward',
    'arrowsize' : 1
})

for node, shape, color, idx in nodes:
    G.add_node(
        idx,
        shape = shape,
        color = color,
        label = node,
    )

for src, dst in edges:
    G.add_edge(
        src,
        dst
    )

print 'Nodes: %d, Edges: %d' % (G.number_of_nodes(), G.number_of_edges())
G.draw('dep_cfg.png', prog = 'dot')

