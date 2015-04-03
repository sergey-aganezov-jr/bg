# -*- coding: utf-8 -*-
from unittest.mock import Mock
from collections import Counter
from bg.edge import BGEdge, BGEdge_JSON_SCHEMA_JSON_KEY
from bg.genome import BGGenome, BGGenome_JSON_SCHEMA_JSON_KEY
from bg.kbreak import KBreak
from bg.multicolor import Multicolor
from bg.vertex import BGVertex, BGVertex_JSON_SCHEMA_JSON_KEY

__author__ = "Sergey Aganezov"
__email__ = "aganezov(at)gwu.edu"
__status__ = "production"

import unittest
from bg.breakpoint_graph import BreakpointGraph


class BreakpointGraphTestCase(unittest.TestCase):
    def setUp(self):
        self.genome1 = BGGenome("red")
        self.genome2 = BGGenome("green")
        self.genome3 = BGGenome("blue")
        self.genome4 = BGGenome("black")
        self.genome5 = BGGenome("yellow")

    def test_empty_initialization(self):
        graph = BreakpointGraph()
        self.assertEqual(len(graph.bg), 0)
        self.assertEqual(len(graph.bg.edges()), 0)
        self.assertEqual(len(list(graph.edges())), 0)
        self.assertEqual(len(list(graph.nodes())), 0)

    def test_add_edge_without_multicolor(self):
        with self.assertRaises(TypeError):
            BreakpointGraph().add_edge(vertex1=BGVertex("v1"), vertex2=BGVertex("v2"))

    def test_get_vertex_by_name(self):
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor = Multicolor(self.genome4)
        graph.add_edge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        self.assertEqual(graph.get_vertex_by_name("v1"), v1)
        self.assertEqual(graph.get_vertex_by_name("v2"), v2)
        self.assertIsNone(graph.get_vertex_by_name("v3"))

    def test_add_edge(self):
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor = Multicolor(self.genome4)
        graph.add_edge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        self.assertEqual(len(graph.bg), 2)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(graph.bg.edges()), 1)
        self.assertEqual(len(graph.bg.edges(v1)), 1)
        self.assertEqual(graph.bg.edges(v1, data=True)[0][2]["multicolor"], multicolor)
        self.assertEqual(graph.bg.edges(v2, data=True)[0][2]["multicolor"], multicolor)

    def test_add_bgedge(self):
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor = Multicolor(self.genome4)
        bgedge = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        graph.add_bgedge(bgedge)
        self.assertEqual(len(graph.bg), 2)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(graph.bg.edges()), 1)
        self.assertEqual(len(graph.bg.edges(v1)), 1)
        self.assertEqual(graph.bg.edges(v1, data=True)[0][2]["multicolor"], multicolor)
        self.assertEqual(graph.bg.edges(v2, data=True)[0][2]["multicolor"], multicolor)

    def test_edges(self):
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        v3 = BGVertex("v3")
        multicolor1 = Multicolor(self.genome1)
        multicolor2 = Multicolor(self.genome4)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v3, multicolor=multicolor2)
        graph.add_edge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_edge(vertex1=v1, vertex2=v3, multicolor=multicolor2)
        edge_1_key = min(graph.bg[v2][v1].keys())
        edge_2_key = min(graph.bg[v3][v1].keys())
        for bgedge, key in graph.edges(keys=True):
            if bgedge == edge1:
                self.assertEqual(edge_1_key, key)
            elif bgedge == edge2:
                self.assertEqual(edge_2_key, key)

    def test_get_edge_by_two_vertices(self):
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        v3 = BGVertex("v3")
        multicolor1 = Multicolor(self.genome1)
        multicolor2 = Multicolor(self.genome4)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v3, multicolor=multicolor2)
        graph.add_edge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_edge(vertex1=v1, vertex2=v3, multicolor=multicolor2)
        self.assertEqual(graph.get_edge_by_two_vertices(vertex1=v1, vertex2=v2), edge1)
        self.assertEqual(graph.get_edge_by_two_vertices(vertex1=v2, vertex2=v1), edge1)
        self.assertEqual(graph.get_edge_by_two_vertices(vertex1=v1, vertex2=v3), edge2)
        self.assertEqual(graph.get_edge_by_two_vertices(vertex1=v3, vertex2=v1), edge2)

    def test_get_edges_by_vertex(self):
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        v3 = BGVertex("v3")
        multicolor1 = Multicolor(self.genome1)
        multicolor2 = Multicolor(self.genome4)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v3, multicolor=multicolor2)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge2)
        result = list(graph.get_edges_by_vertex(vertex=v1))
        self.assertTrue(edge1 in result)
        self.assertTrue(edge2 in result)
        edge_1_key = min(graph.bg[v1][v2].keys())
        edge_2_key = min(graph.bg[v1][v3].keys())
        result = list(graph.get_edges_by_vertex(vertex=v1, keys=True))
        for res_bgedge, res_key in result:
            if res_bgedge == edge1:
                self.assertEqual(edge_1_key, res_key)
            else:
                self.assertEqual(edge_2_key, res_key)

    def test_add_edge_with_already_existing_merge(self):
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor = Multicolor(self.genome4)
        graph.add_edge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        multicolor2 = Multicolor(self.genome2)
        graph.add_edge(vertex1=v1, vertex2=v2, multicolor=multicolor2)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(graph.get_edge_by_two_vertices(vertex1=v1, vertex2=v2).multicolor, multicolor + multicolor2)
        self.assertEqual(graph.get_edge_by_two_vertices(vertex1=v2, vertex2=v1).multicolor, multicolor + multicolor2)
        multicolor3 = Multicolor(self.genome4)
        graph.add_edge(vertex1=v1, vertex2=v2, multicolor=multicolor3)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(graph.get_edge_by_two_vertices(vertex1=v1, vertex2=v2).multicolor,
                         multicolor + multicolor2 + multicolor3)
        self.assertEqual(graph.get_edge_by_two_vertices(vertex1=v2, vertex2=v1).multicolor,
                         multicolor + multicolor2 + multicolor3)

    def test_add_bgedge_with_already_existing_merge(self):
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor = Multicolor(self.genome4)
        graph.add_bgedge(BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor))
        multicolor2 = Multicolor(self.genome2)
        graph.add_bgedge(BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor2))
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(graph.get_edge_by_two_vertices(vertex1=v1, vertex2=v2).multicolor, multicolor + multicolor2)
        self.assertEqual(graph.get_edge_by_two_vertices(vertex1=v2, vertex2=v1).multicolor, multicolor + multicolor2)
        multicolor3 = Multicolor(self.genome4)
        graph.add_bgedge(BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor3))
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(graph.get_edge_by_two_vertices(vertex1=v1, vertex2=v2).multicolor,
                         multicolor + multicolor2 + multicolor3)
        self.assertEqual(graph.get_edge_by_two_vertices(vertex1=v2, vertex2=v1).multicolor,
                         multicolor + multicolor2 + multicolor3)

    def test_add_edge_with_already_existing_no_merge(self):
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor = Multicolor(self.genome4)
        graph.add_edge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        multicolor2 = Multicolor(self.genome2)
        graph.add_edge(vertex1=v1, vertex2=v2, multicolor=multicolor2, merge=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 2)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in [Multicolor(self.genome4), Multicolor(self.genome2)])
        edges = list(graph.get_edges_by_vertex(vertex=v2))
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in [Multicolor(self.genome4), Multicolor(self.genome2)])
        multicolor3 = Multicolor(self.genome4)
        graph.add_edge(vertex1=v1, vertex2=v2, multicolor=multicolor3, merge=False)
        graph.add_edge(vertex1=v1, vertex2=v2, multicolor=multicolor3, merge=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 4)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in [Multicolor(self.genome4), Multicolor(self.genome2)])
        edges = list(graph.get_edges_by_vertex(vertex=v2))
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in [Multicolor(self.genome4), Multicolor(self.genome2)])

    def test_add_bgedge_with_already_existing_no_merge(self):
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor = Multicolor(self.genome4)
        graph.add_bgedge(BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor))
        multicolor2 = Multicolor(self.genome2)
        graph.add_bgedge(BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor2), merge=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 2)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in [Multicolor(self.genome4), Multicolor(self.genome2)])
        edges = list(graph.get_edges_by_vertex(vertex=v2))
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in [Multicolor(self.genome4), Multicolor(self.genome2)])
        multicolor3 = Multicolor(self.genome4)
        graph.add_bgedge(BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor3), merge=False)
        graph.add_bgedge(BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor3), merge=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 4)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in [Multicolor(self.genome4), Multicolor(self.genome2)])
        edges = list(graph.get_edges_by_vertex(vertex=v2))
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in [Multicolor(self.genome4), Multicolor(self.genome2)])

    def test_connected_components_iteration(self):
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        v3 = BGVertex("v3")
        v4 = BGVertex("v4")
        multicolor1 = Multicolor(self.genome1)
        multicolor2 = Multicolor(self.genome4)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v3, vertex2=v4, multicolor=multicolor2)
        edge3 = BGEdge(vertex1=v1, vertex2=v3, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge2)
        ccs = list(graph.connected_components_subgraphs())
        self.assertEqual(len(ccs), 2)
        for cc in ccs:
            self.assertEqual(len(list(cc.nodes())), 2)
            self.assertEqual(len(list(cc.edges())), 1)
        for cc in ccs:
            if v1 in cc.bg:
                self.assertEqual(cc.get_edge_by_two_vertices(vertex1=v1, vertex2=v2), edge1)
            else:
                self.assertEqual(cc.get_edge_by_two_vertices(vertex1=v3, vertex2=v4), edge2)
        graph.add_bgedge(edge3)
        ccs2 = list(graph.connected_components_subgraphs())
        self.assertEqual(len(ccs2), 1)
        self.assertEqual(len(list(ccs2[0].nodes())), 4)
        self.assertEqual(len(list(ccs2[0].edges())), 3)
        self.assertEqual(ccs2[0].get_edge_by_two_vertices(vertex1=v1, vertex2=v2), edge1)
        self.assertEqual(ccs2[0].get_edge_by_two_vertices(vertex1=v3, vertex2=v4), edge2)
        self.assertEqual(ccs2[0].get_edge_by_two_vertices(vertex1=v1, vertex2=v3), edge3)

    def test_delete_single_edge_existing(self):
        # regular case
        # added edge is deleted
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor = Multicolor(self.genome4)
        bgedge = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        graph.add_bgedge(bgedge)
        graph.delete_edge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        self.assertEqual(len(list(graph.edges())), 0)
        self.assertEqual(len(list(graph.nodes())), 2)
        graph.add_bgedge(bgedge)
        # added edge is deleted with swapping vertices (as we have non-directed edges, they shall be equal in case
        # of swapping vertices)
        graph.delete_edge(vertex1=v2, vertex2=v1, multicolor=multicolor)
        self.assertEqual(len(list(graph.edges())), 0)
        self.assertEqual(len(list(graph.nodes())), 2)
        # case with deleting a full existing portion of multi-edge with colors of multi-degree greater than 1
        multicolor2 = Multicolor(self.genome1, self.genome4, self.genome1)
        bgedge = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor2)
        graph.add_bgedge(bgedge)
        multicolor_to_delete = Multicolor(self.genome1, self.genome4)
        graph.delete_edge(vertex1=v1, vertex2=v2, multicolor=multicolor_to_delete)
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(list(graph.edges(nbunch=v1))[0].multicolor, Multicolor(self.genome1))
        # case with deleting an existing portion of multi-edge and non-existing portion of multi-edge
        # in this case existing portion must be deleted, while non-existing must be ignored
        graph = BreakpointGraph()
        v3 = BGVertex("v3")
        v4 = BGVertex("v4")
        multicolor3 = Multicolor(self.genome1, self.genome4)
        bgedge = BGEdge(vertex1=v3, vertex2=v4, multicolor=multicolor3)
        graph.add_bgedge(bgedge)
        multicolor_to_delete = Multicolor(self.genome1, self.genome1, self.genome1)
        graph.delete_edge(vertex1=v3, vertex2=v4, multicolor=multicolor_to_delete)
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(list(graph.edges(nbunch=v3))[0].multicolor, Multicolor(self.genome4))
        # case with deleting only a non-existing portion of existing single edge
        graph = BreakpointGraph()
        v5 = BGVertex("v5")
        v6 = BGVertex("v6")
        multicolor4 = Multicolor(self.genome1, self.genome4)
        bgedge = BGEdge(vertex1=v5, vertex2=v6, multicolor=multicolor4)
        graph.add_bgedge(bgedge)
        multicolor_to_delete = Multicolor(self.genome5, self.genome2, self.genome5)
        graph.delete_edge(vertex1=v5, vertex2=v6, multicolor=multicolor_to_delete)
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(list(graph.edges(nbunch=v5))[0].multicolor, Multicolor(self.genome4, self.genome1))
        graph.delete_edge(vertex1=v6, vertex2=v5, multicolor=multicolor_to_delete)
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(list(graph.edges(nbunch=v6))[0].multicolor, Multicolor(self.genome4, self.genome1))
        # checks that edge between two given vertices are deleted
        graph = BreakpointGraph()
        v5 = BGVertex("v5")
        v6 = BGVertex("v6")
        v7 = BGVertex("v7")
        multicolor4 = Multicolor(self.genome1, self.genome4)
        multicolor5 = Multicolor(self.genome1)
        bgedge = BGEdge(vertex1=v5, vertex2=v6, multicolor=multicolor5)
        bgedge1 = BGEdge(vertex1=v5, vertex2=v7, multicolor=multicolor4)
        graph.add_bgedge(bgedge)
        graph.add_bgedge(bgedge1)
        multicolor_to_delete = Multicolor(self.genome1, self.genome4)
        graph.delete_edge(vertex1=v5, vertex2=v6, multicolor=multicolor_to_delete)
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(list(graph.nodes())), 3)
        self.assertEqual(list(graph.edges(nbunch=v5))[0].multicolor, Multicolor(self.genome4, self.genome1))
        graph.add_bgedge(bgedge)
        graph.delete_edge(vertex1=v6, vertex2=v5, multicolor=multicolor_to_delete)
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(list(graph.nodes())), 3)
        self.assertEqual(list(graph.edges(nbunch=v5))[0].multicolor, Multicolor(self.genome4, self.genome1))

    def test_delete_single_bgedge_existing(self):
        # regular case
        # added bgedge is deleted
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor = Multicolor(self.genome4)
        bgedge = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        graph.add_bgedge(bgedge)
        graph.delete_bgedge(bgedge)
        self.assertEqual(len(list(graph.edges())), 0)
        self.assertEqual(len(list(graph.nodes())), 2)
        # added bgedge is deleted with swapping vertices (as we have non-directed edges, they shall be equal in case
        # of swapping vertices)
        graph.add_bgedge(bgedge)
        bgedge = BGEdge(vertex1=v2, vertex2=v1, multicolor=multicolor)
        graph.delete_bgedge(bgedge)
        self.assertEqual(len(list(graph.edges())), 0)
        self.assertEqual(len(list(graph.nodes())), 2)
        # case with deleting a full existing portion of multi-edge with colors of multi-degree greater than 1
        multicolor2 = Multicolor(self.genome1, self.genome4, self.genome1)
        bgedge = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor2)
        graph.add_bgedge(bgedge)
        multicolor_to_delete = Multicolor(self.genome1, self.genome4)
        graph.delete_bgedge(BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor_to_delete))
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(list(graph.edges(nbunch=v1))[0].multicolor, Multicolor(self.genome1))
        # case with deleting an existing portion of multi-edge and non-existing portion of multi-edge
        # in this case existing portion must be deleted, while non-existing must be ignored
        graph = BreakpointGraph()
        v3 = BGVertex("v3")
        v4 = BGVertex("v4")
        multicolor3 = Multicolor(self.genome1, self.genome4)
        bgedge = BGEdge(vertex1=v3, vertex2=v4, multicolor=multicolor3)
        graph.add_bgedge(bgedge)
        multicolor_to_delete = Multicolor(self.genome1, self.genome1, self.genome1)
        graph.delete_bgedge(BGEdge(vertex1=v3, vertex2=v4, multicolor=multicolor_to_delete))
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(list(graph.edges(nbunch=v3))[0].multicolor, Multicolor(self.genome4))
        # case with deleting only a non-existing portion of existing single edge
        graph = BreakpointGraph()
        v5 = BGVertex("v5")
        v6 = BGVertex("v6")
        multicolor4 = Multicolor(self.genome1, self.genome4)
        bgedge = BGEdge(vertex1=v5, vertex2=v6, multicolor=multicolor4)
        graph.add_bgedge(bgedge)
        multicolor_to_delete = Multicolor(self.genome5, self.genome2, self.genome5)
        graph.delete_bgedge(BGEdge(vertex1=v5, vertex2=v6, multicolor=multicolor_to_delete))
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(list(graph.edges(nbunch=v5))[0].multicolor, Multicolor(self.genome4, self.genome1))
        graph.delete_bgedge(BGEdge(vertex1=v6, vertex2=v5, multicolor=multicolor_to_delete))
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(list(graph.edges(nbunch=v6))[0].multicolor, Multicolor(self.genome4, self.genome1))
        # checks that edge between two given vertices are deleted
        graph = BreakpointGraph()
        v5 = BGVertex("v5")
        v6 = BGVertex("v6")
        v7 = BGVertex("v7")
        multicolor4 = Multicolor(self.genome1, self.genome4)
        multicolor5 = Multicolor(self.genome1)
        bgedge = BGEdge(vertex1=v5, vertex2=v6, multicolor=multicolor5)
        bgedge1 = BGEdge(vertex1=v5, vertex2=v7, multicolor=multicolor4)
        graph.add_bgedge(bgedge)
        graph.add_bgedge(bgedge1)
        multicolor_to_delete = Multicolor(self.genome1, self.genome4)
        graph.delete_bgedge(BGEdge(vertex1=v5, vertex2=v6, multicolor=multicolor_to_delete))
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(list(graph.nodes())), 3)
        self.assertEqual(list(graph.edges(nbunch=v5))[0].multicolor, Multicolor(self.genome4, self.genome1))
        graph.add_bgedge(bgedge)
        graph.delete_bgedge(BGEdge(vertex1=v6, vertex2=v5, multicolor=multicolor_to_delete))
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(list(graph.nodes())), 3)
        self.assertEqual(list(graph.edges(nbunch=v5))[0].multicolor, Multicolor(self.genome4, self.genome1))

    def test_delete_multiple_edges_existing(self):
        # test case with simple deleting any one out of two same edges
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor = Multicolor(self.genome4)
        bgedge = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        graph.add_bgedge(bgedge)
        graph.add_bgedge(bgedge, merge=False)
        graph.delete_edge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(list(graph.edges(nbunch=v1))[0].multicolor, Multicolor(self.genome4))
        self.assertEqual(list(graph.edges(nbunch=v2))[0].multicolor, Multicolor(self.genome4))
        # test case with simple deleting any one out of two same edges
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor = Multicolor(self.genome4)
        bgedge = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        graph.add_bgedge(bgedge)
        graph.add_bgedge(bgedge, merge=False)
        graph.delete_edge(vertex1=v2, vertex2=v1, multicolor=multicolor)
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(list(graph.edges(nbunch=v1))[0].multicolor, Multicolor(self.genome4))
        self.assertEqual(list(graph.edges(nbunch=v2))[0].multicolor, Multicolor(self.genome4))
        # test case with deleting one out of two edges with different multicolors
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor = Multicolor(self.genome4)
        multicolor1 = Multicolor(self.genome1)
        bgedge = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        bgedge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(bgedge)
        graph.add_bgedge(bgedge1, merge=False)
        graph.delete_edge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(list(graph.edges(nbunch=v1))[0].multicolor, Multicolor(self.genome4))
        self.assertEqual(list(graph.edges(nbunch=v2))[0].multicolor, Multicolor(self.genome4))
        # test case with deleting an edge with multi-color out of two edges with two multi-colors in each
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor = Multicolor(self.genome4, self.genome4)
        multicolor1 = Multicolor(self.genome4)
        bgedge = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        bgedge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(bgedge)
        graph.add_bgedge(bgedge1, merge=False)
        graph.delete_edge(vertex1=v2, vertex2=v1, multicolor=multicolor)
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(list(graph.edges(nbunch=v1))[0].multicolor, Multicolor(self.genome4))
        self.assertEqual(list(graph.edges(nbunch=v2))[0].multicolor, Multicolor(self.genome4))
        # test case with deleting one out of two edges with different multicolors
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor = Multicolor(self.genome4)
        multicolor1 = Multicolor(self.genome1)
        bgedge = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        bgedge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(bgedge)
        graph.add_bgedge(bgedge1, merge=False)
        graph.delete_edge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(list(graph.edges(nbunch=v1))[0].multicolor, Multicolor(self.genome4))
        self.assertEqual(list(graph.edges(nbunch=v2))[0].multicolor, Multicolor(self.genome4))
        # test case with deleting one out of two edges with different multicolors
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor = Multicolor(self.genome4)
        multicolor1 = Multicolor(self.genome1)
        bgedge = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        bgedge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(bgedge)
        graph.add_bgedge(bgedge1, merge=False)
        graph.delete_edge(vertex1=v2, vertex2=v1, multicolor=multicolor1)
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(list(graph.edges(nbunch=v1))[0].multicolor, Multicolor(self.genome4))
        self.assertEqual(list(graph.edges(nbunch=v2))[0].multicolor, Multicolor(self.genome4))
        # test case with deleting specific one out of two edges, with specific identification
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor = Multicolor(self.genome4)
        multicolor1 = Multicolor(self.genome4)
        bgedge = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        bgedge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(bgedge)
        graph.add_bgedge(bgedge1, merge=False)
        edge_to_delete_id = min(graph.bg[v1][v2].keys())
        edge_to_keep_id = max(graph.bg[v1][v2].keys())
        graph.delete_edge(vertex1=v2, vertex2=v1, multicolor=multicolor1, key=edge_to_delete_id)
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(list(graph.edges(nbunch=v1))[0].multicolor, Multicolor(self.genome4))
        self.assertEqual(list(graph.edges(nbunch=v2))[0].multicolor, Multicolor(self.genome4))
        key = min(graph.bg[v1][v2])
        self.assertEqual(key, edge_to_keep_id)
        key = min(graph.bg[v2][v1])
        self.assertEqual(key, edge_to_keep_id)

    def test_delete_multiple_bgedges_existing(self):
        # test case with simple deleting any one out of two same edges
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor = Multicolor(self.genome4)
        bgedge = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        graph.add_bgedge(bgedge)
        graph.add_bgedge(bgedge, merge=False)
        graph.delete_bgedge(BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor))
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(list(graph.edges(nbunch=v1))[0].multicolor, Multicolor(self.genome4))
        self.assertEqual(list(graph.edges(nbunch=v2))[0].multicolor, Multicolor(self.genome4))
        # test case with simple deleting any one out of two same edges
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor = Multicolor(self.genome4)
        bgedge = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        graph.add_bgedge(bgedge)
        graph.add_bgedge(bgedge, merge=False)
        graph.delete_bgedge(BGEdge(vertex1=v2, vertex2=v1, multicolor=multicolor))
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(list(graph.edges(nbunch=v1))[0].multicolor, Multicolor(self.genome4))
        self.assertEqual(list(graph.edges(nbunch=v2))[0].multicolor, Multicolor(self.genome4))
        # test case with deleting one out of two edges with different multicolors
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor = Multicolor(self.genome4)
        multicolor1 = Multicolor(self.genome1)
        bgedge = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        bgedge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(bgedge)
        graph.add_bgedge(bgedge1, merge=False)
        graph.delete_bgedge(BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1))
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(list(graph.edges(nbunch=v1))[0].multicolor, Multicolor(self.genome4))
        self.assertEqual(list(graph.edges(nbunch=v2))[0].multicolor, Multicolor(self.genome4))
        # test case with deleting an edge with multi-color out of two edges with two multi-colors in each
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor = Multicolor(self.genome4, self.genome4)
        multicolor1 = Multicolor(self.genome4)
        bgedge = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        bgedge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(bgedge)
        graph.add_bgedge(bgedge1, merge=False)
        graph.delete_bgedge(BGEdge(vertex1=v2, vertex2=v1, multicolor=multicolor))
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(list(graph.edges(nbunch=v1))[0].multicolor, Multicolor(self.genome4))
        self.assertEqual(list(graph.edges(nbunch=v2))[0].multicolor, Multicolor(self.genome4))
        # test case with deleting one out of two edges with different multicolors
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor = Multicolor(self.genome4)
        multicolor1 = Multicolor(self.genome1)
        bgedge = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        bgedge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(bgedge)
        graph.add_bgedge(bgedge1, merge=False)
        graph.delete_bgedge(BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1))
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(list(graph.edges(nbunch=v1))[0].multicolor, Multicolor(self.genome4))
        self.assertEqual(list(graph.edges(nbunch=v2))[0].multicolor, Multicolor(self.genome4))
        # test case with deleting one out of two edges with different multicolors
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor = Multicolor(self.genome4)
        multicolor1 = Multicolor(self.genome1)
        bgedge = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        bgedge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(bgedge)
        graph.add_bgedge(bgedge1, merge=False)
        graph.delete_bgedge(BGEdge(vertex1=v2, vertex2=v1, multicolor=multicolor1))
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(list(graph.edges(nbunch=v1))[0].multicolor, Multicolor(self.genome4))
        self.assertEqual(list(graph.edges(nbunch=v2))[0].multicolor, Multicolor(self.genome4))
        # test case with deleting specific one out of two edges, with specific identification
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor = Multicolor(self.genome4)
        multicolor1 = Multicolor(self.genome4)
        bgedge = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        bgedge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(bgedge)
        graph.add_bgedge(bgedge1, merge=False)
        edge_to_delete_id = min(graph.bg[v1][v2].keys())
        edge_to_keep_id = max(graph.bg[v1][v2].keys())
        graph.delete_bgedge(BGEdge(vertex1=v2, vertex2=v1, multicolor=multicolor1), key=edge_to_delete_id)
        self.assertEqual(len(list(graph.edges())), 1)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(list(graph.edges(nbunch=v1))[0].multicolor, Multicolor(self.genome4))
        self.assertEqual(list(graph.edges(nbunch=v2))[0].multicolor, Multicolor(self.genome4))
        key = min(graph.bg[v1][v2])
        self.assertEqual(key, edge_to_keep_id)
        key = min(graph.bg[v2][v1])
        self.assertEqual(key, edge_to_keep_id)

    def test_delete_single_edge_non_existing(self):
        # covers the case when there is attempt to delete an edge between two vertices that have no edges between them
        # nothing shall happen
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor = Multicolor(self.genome4)
        bgedge = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        graph.add_bgedge(bgedge)
        graph.delete_bgedge(bgedge)
        graph.delete_edge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        self.assertEqual(len(list(graph.edges())), 0)
        self.assertEqual(len(list(graph.nodes())), 2)
        with self.assertRaises(KeyError):
            graph.delete_edge(vertex1=v1, vertex2=v2, multicolor=multicolor, key=0)

    def test_delete_single_bgedge_non_existing(self):
        # covers the case when there is attempt to delete an edge between two vertices that have no edges between them
        # nothing shall happen
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor = Multicolor(self.genome4)
        bgedge = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        graph.add_bgedge(bgedge)
        graph.delete_bgedge(bgedge)
        graph.delete_bgedge(bgedge)
        self.assertEqual(len(list(graph.edges())), 0)
        self.assertEqual(len(list(graph.nodes())), 2)
        with self.assertRaises(KeyError):
            graph.delete_bgedge(bgedge, key=0)

    def test_single_edge_splitting_no_guidance_no_duplication_splitting(self):
        # test with a simple one-colored edge
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 1)
        graph.split_edge(vertex1=v1, vertex2=v2, multicolor=multicolor1, guidance=None, duplication_splitting=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 1)
        # test with a simple multi-colored edge, no duplications of same color
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1, self.genome4, self.genome2)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 1)
        graph.split_edge(vertex1=v1, vertex2=v2, multicolor=multicolor1, guidance=None, duplication_splitting=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 3)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        multicolors = [Multicolor(self.genome1), Multicolor(self.genome4), Multicolor(self.genome2)]
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in multicolors)
        # test case with a simple one-colored edge with duplications of the same color
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1, self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.split_edge(vertex1=v1, vertex2=v2, multicolor=multicolor1, guidance=None, duplication_splitting=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 1)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        self.assertEqual(edges[0].multicolor, multicolor1)
        # test case with a multi-colored edge with duplications of same color
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1, self.genome2, self.genome1, self.genome2, self.genome4)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.split_edge(vertex1=v1, vertex2=v2, multicolor=multicolor1, guidance=None, duplication_splitting=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 3)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        multicolors = [Multicolor(self.genome1, self.genome1), Multicolor(self.genome2, self.genome2), Multicolor(self.genome4)]
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in multicolors)

    def test_single_bgedge_splitting_no_guidance_no_duplication_splitting(self):
        # test with a simple one-colored edge
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 1)
        graph.split_bgedge(BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1), guidance=None,
                           duplication_splitting=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 1)
        # test with a simple multi-colored edge, no duplications of same color
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1, self.genome4, self.genome2)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 1)
        graph.split_bgedge(BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1), guidance=None,
                           duplication_splitting=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 3)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        multicolors = [Multicolor(self.genome1), Multicolor(self.genome4), Multicolor(self.genome2)]
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in multicolors)
        # test case with a simple one-colored edge with duplications of the same color
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1, self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.split_bgedge(BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1), guidance=None,
                           duplication_splitting=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 1)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        self.assertEqual(edges[0].multicolor, multicolor1)
        # test case with a multi-colored edge with duplications of same color
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1, self.genome2, self.genome1, self.genome2, self.genome4)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.split_bgedge(BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1), guidance=None,
                           duplication_splitting=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 3)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        multicolors = [Multicolor(self.genome1, self.genome1), Multicolor(self.genome2, self.genome2), Multicolor(self.genome4)]
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in multicolors)

    def test_multiple_bgedge_splitting_no_guidance_no_duplication_splitting(self):
        # test with a two one-colored edges (both will stay)
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge1, merge=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 2)
        graph.split_bgedge(BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1), guidance=None,
                           duplication_splitting=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 2)
        for bgedge in graph.edges():
            self.assertEqual(bgedge, edge1)
        # test with a multiple multi-colored edges, no duplications of same color (one splits, another stays)
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1, self.genome4, self.genome2)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge1, merge=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 2)
        graph.split_bgedge(BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1), guidance=None,
                           duplication_splitting=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 4)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        multicolors = [Multicolor(self.genome1), Multicolor(self.genome4), Multicolor(self.genome2), multicolor1]
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in multicolors)
        # test case with two one-colored edge with duplications of the same color
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1, self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge1, merge=False)
        graph.split_bgedge(BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1), guidance=None,
                           duplication_splitting=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 2)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        self.assertEqual(edges[0].multicolor, multicolor1)
        self.assertEqual(edges[1].multicolor, multicolor1)
        # test case with two a multi-colored edge with duplications of same color
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1, self.genome2, self.genome1, self.genome2, self.genome4)
        multicolor2 = Multicolor(self.genome1, self.genome2, self.genome1, self.genome2)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor2)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge2, merge=False)
        graph.split_bgedge(BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1), guidance=None,
                           duplication_splitting=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 4)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        multicolors = [Multicolor(self.genome1, self.genome1), Multicolor(self.genome2, self.genome2), Multicolor(self.genome4),
                       multicolor2]
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in multicolors)
        # when no edges between two given vertices (extracted form bgedge) have no similarities with a given one
        # no split shall be performed
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1, self.genome2, self.genome1, self.genome2, self.genome4)
        multicolor2 = Multicolor(self.genome1, self.genome2, self.genome1, self.genome2)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor2)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge2, merge=False)
        graph.split_bgedge(BGEdge(vertex1=v1, vertex2=v2, multicolor=Multicolor(self.genome5)), guidance=None,
                           duplication_splitting=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 2)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        multicolors = [multicolor1, multicolor2]
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in multicolors)

    def test_multiple_edge_splitting_no_guidance_no_duplication_splitting(self):
        # test with a two one-colored edges (both will stay)
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge1, merge=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 2)
        graph.split_edge(vertex1=v1, vertex2=v2, multicolor=multicolor1, guidance=None,
                         duplication_splitting=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 2)
        for bgedge in graph.edges():
            self.assertEqual(bgedge, edge1)
        # test with a multiple multi-colored edges, no duplications of same color (one splits, another stays)
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1, self.genome4, self.genome2)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge1, merge=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 2)
        graph.split_edge(vertex1=v1, vertex2=v2, multicolor=multicolor1, guidance=None,
                         duplication_splitting=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 4)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        multicolors = [Multicolor(self.genome1), Multicolor(self.genome4), Multicolor(self.genome2), multicolor1]
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in multicolors)
        # test case with two one-colored edge with duplications of the same color
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1, self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge1, merge=False)
        graph.split_edge(vertex1=v1, vertex2=v2, multicolor=multicolor1, guidance=None,
                         duplication_splitting=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 2)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        self.assertEqual(edges[0].multicolor, multicolor1)
        self.assertEqual(edges[1].multicolor, multicolor1)
        # test case with two a multi-colored edge with duplications of same color
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1, self.genome2, self.genome1, self.genome2, self.genome4)
        multicolor2 = Multicolor(self.genome1, self.genome2, self.genome1, self.genome2)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor2)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge2, merge=False)
        graph.split_edge(vertex1=v1, vertex2=v2, multicolor=multicolor1, guidance=None,
                         duplication_splitting=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 4)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        multicolors = [Multicolor(self.genome1, self.genome1), Multicolor(self.genome2, self.genome2), Multicolor(self.genome4),
                       multicolor2]
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in multicolors)
        # when no edges between two given vertices (extracted form bgedge) have no similarities with a given one
        # no split shall be performed
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1, self.genome2, self.genome1, self.genome2, self.genome4)
        multicolor2 = Multicolor(self.genome1, self.genome2, self.genome1, self.genome2)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor2)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge2, merge=False)
        graph.split_edge(vertex1=v1, vertex2=v2, multicolor=Multicolor(self.genome5), guidance=None,
                         duplication_splitting=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 2)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        multicolors = [multicolor1, multicolor2]
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in multicolors)

    def test_multiple_edge_splitting_with_guidance_no_duplication_splitting(self):
        # test with a two one-colored edges (both will stay)
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge1, merge=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 2)
        graph.split_edge(vertex1=v1, vertex2=v2, multicolor=multicolor1, guidance=[(self.genome1, )],
                         duplication_splitting=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 2)
        for bgedge in graph.edges():
            self.assertEqual(bgedge, edge1)
        # test with a multiple multi-colored edges, no duplications of same color (one splits, another stays)
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1, self.genome4, self.genome2)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge1, merge=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 2)
        graph.split_edge(vertex1=v1, vertex2=v2, multicolor=multicolor1, guidance=[(self.genome1, self.genome4)],
                         duplication_splitting=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 3)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        multicolors = [Multicolor(self.genome1, self.genome4), Multicolor(self.genome2), multicolor1]
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in multicolors)
        # test case with two one-colored edge with duplications of the same color
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1, self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge1, merge=False)
        graph.split_edge(vertex1=v1, vertex2=v2, multicolor=multicolor1, guidance=[(self.genome1, )],
                         duplication_splitting=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 2)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        self.assertEqual(edges[0].multicolor, multicolor1)
        self.assertEqual(edges[1].multicolor, multicolor1)
        # test case with two a multi-colored edge with duplications of same color
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1, self.genome2, self.genome1, self.genome2, self.genome4)
        multicolor2 = Multicolor(self.genome1, self.genome2, self.genome1, self.genome2)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor2)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge2, merge=False)
        graph.split_edge(vertex1=v1, vertex2=v2, multicolor=multicolor1, guidance=[(self.genome1, self.genome4)],
                         duplication_splitting=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 3)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        multicolors = [Multicolor(self.genome1, self.genome1, self.genome4), Multicolor(self.genome2, self.genome2),
                       multicolor2]
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in multicolors)
        # when no edges between two given vertices (extracted form bgedge) have no similarities with a given one
        # no split shall be performed
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1, self.genome2, self.genome1, self.genome2, self.genome4)
        multicolor2 = Multicolor(self.genome1, self.genome2, self.genome1, self.genome2)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor2)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge2, merge=False)
        graph.split_edge(vertex1=v1, vertex2=v2, multicolor=Multicolor(self.genome5), guidance=[(self.genome1, self.genome2)],
                         duplication_splitting=False)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 2)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        multicolors = [multicolor1, multicolor2]
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in multicolors)

    def test_multiple_edge_splitting_with_guidance_no_duplication_splitting_particular_id(self):
        # test with a two one-colored edges (both will stay)
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge1, merge=False)
        key = min(graph.bg[v1][v2].keys())
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 2)
        graph.split_edge(vertex1=v1, vertex2=v2, multicolor=multicolor1, guidance=[(self.genome1, )],
                         duplication_splitting=False, key=key)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 2)
        for bgedge in graph.edges():
            self.assertEqual(bgedge, edge1)
        # test with a multiple multi-colored edges, no duplications of same color (one splits, another stays)
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1, self.genome4, self.genome2, self.genome5)
        multicolor2 = Multicolor(self.genome1, self.genome4, self.genome2, self.genome3)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor2)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge2, merge=False)
        key = max(graph.bg[v1][v2].keys())  # consecutively added edges have consecutive ids, thus max correspond
        # to latest added edge
        edges = list(graph.edges())
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(edges), 2)
        graph.split_edge(vertex1=v1, vertex2=v2, multicolor=Multicolor(self.genome1, self.genome4, self.genome2),
                         guidance=[(self.genome1, self.genome4)],
                         duplication_splitting=False,
                         key=key)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 3)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        multicolors = [Multicolor(self.genome1, self.genome4), Multicolor(self.genome2, self.genome3), multicolor1]
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in multicolors)
        # test case with two one-colored edge with duplications of the same color
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1, self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge1, merge=False)
        key = max(graph.bg[v1][v2].keys())
        graph.split_edge(vertex1=v1, vertex2=v2, multicolor=multicolor1, guidance=[(self.genome1, )],
                         duplication_splitting=False, key=key)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 2)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        self.assertEqual(edges[0].multicolor, multicolor1)
        self.assertEqual(edges[1].multicolor, multicolor1)
        # test case with two a multi-colored edge with duplications of same color, key prevails over
        # similarity score of multicolor
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1, self.genome2, self.genome1, self.genome2, self.genome4)
        multicolor2 = Multicolor(self.genome1, self.genome2, self.genome1, self.genome2)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor2)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge2, merge=False)
        key = max(graph.bg[v1][v2].keys())
        graph.split_edge(vertex1=v1, vertex2=v2, multicolor=multicolor1, guidance=[(self.genome1, self.genome4)],
                         duplication_splitting=False, key=key)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 3)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        multicolors = [Multicolor(self.genome1, self.genome1), Multicolor(self.genome2, self.genome2),
                       multicolor1]
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in multicolors)
        # even when no edges between two given vertices (extracted form bgedge) that have zero similarities with
        # a given one, key argument dominates the choice of bgedge to be split
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1, self.genome2, self.genome1, self.genome2, self.genome4)
        multicolor2 = Multicolor(self.genome1, self.genome2, self.genome1, self.genome2)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor2)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge2, merge=False)
        key = min(graph.bg[v1][v2].keys())
        graph.split_edge(vertex1=v1, vertex2=v2, multicolor=Multicolor(self.genome5), guidance=[(self.genome1, self.genome2)],
                         duplication_splitting=False, key=key)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 3)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        multicolors = [multicolor2, Multicolor(self.genome1, self.genome1, self.genome2, self.genome2), Multicolor(self.genome4)]
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in multicolors)

    def test_splitting_all_edges_between_two_vertices(self):
        # test with a two one-colored edges (both will stay as is)
        # no guidance
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge1, merge=False)
        graph.split_all_edges_between_two_vertices(vertex1=v1, vertex2=v2)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 2)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        self.assertEqual(edges[0].multicolor, multicolor1)
        self.assertEqual(edges[1].multicolor, multicolor1)
        # test with a two one-colored edges (both will stay as is)
        # with guidance
        graph.split_all_edges_between_two_vertices(vertex1=v1, vertex2=v2, guidance=[(self.genome1, )])
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 2)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        self.assertEqual(edges[0].multicolor, multicolor1)
        self.assertEqual(edges[1].multicolor, multicolor1)
        # test with a two multi-colored edges no duplications
        # no guidance
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1, self.genome4, self.genome2)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge1, merge=False)
        graph.split_all_edges_between_two_vertices(vertex1=v1, vertex2=v2)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 6)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        multicolors = Multicolor.split_colors(multicolor=multicolor1)
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in multicolors)
        # test with a two multi-colored edges no duplications
        # with guidance
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1, self.genome4, self.genome2)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge1, merge=False)
        graph.split_all_edges_between_two_vertices(vertex1=v1, vertex2=v2, guidance=[(self.genome1, self.genome4)])
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 4)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        multicolors = Multicolor.split_colors(multicolor=multicolor1, guidance=[(self.genome1, self.genome4)])
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in multicolors)
        # test with a two multi-colored edges no duplications
        # no guidance
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1, self.genome4, self.genome2, self.genome1, self.genome2)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge1, merge=False)
        graph.split_all_edges_between_two_vertices(vertex1=v1, vertex2=v2, guidance=None)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 6)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        multicolors = Multicolor.split_colors(multicolor=multicolor1)
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in multicolors)
        # test with a two multi-colored edges with duplications
        # with guidance
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1, self.genome4, self.genome2, self.genome1, self.genome2)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge1, merge=False)
        graph.split_all_edges_between_two_vertices(vertex1=v1, vertex2=v2, guidance=[(self.genome1, self.genome4)])
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 4)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        multicolors = Multicolor.split_colors(multicolor=multicolor1, guidance=[(self.genome1, self.genome4)])
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in multicolors)

    def test_split_all_edges(self):
        # test with a four one-colored edges (all will stay as is)
        # two edges between vertices v1 and v2
        # one edge between vertices v1 and v3
        # one edge between vertices v4 and v5
        # no guidance
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        v3 = BGVertex("v3")
        v4 = BGVertex("v4")
        v5 = BGVertex("v5")
        multicolor1 = Multicolor(self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v3, multicolor=multicolor1)
        edge3 = BGEdge(vertex1=v4, vertex2=v5, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge1, merge=False)
        graph.add_bgedge(edge2)
        graph.add_bgedge(edge3)
        graph.split_all_edges()
        self.assertEqual(len(list(graph.nodes())), 5)
        self.assertEqual(len(list(graph.edges())), 4)
        self.assertEqual(len(list(graph.get_edges_by_vertex(vertex=v1))), 3)
        self.assertEqual(len(list(graph.get_edges_by_vertex(vertex=v2))), 2)
        self.assertEqual(len(list(graph.get_edges_by_vertex(vertex=v4))), 1)
        edges = list(graph.edges())
        for bgedge in edges:
            self.assertEqual(bgedge.multicolor, multicolor1)
        # test with a four multi-colored edges
        # two edges between vertices v1 and v2
        # one edge between vertices v1 and v3
        # one edge between vertices v4 and v5
        # no guidance
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        v3 = BGVertex("v3")
        v4 = BGVertex("v4")
        v5 = BGVertex("v5")
        multicolor1 = Multicolor(self.genome1, self.genome4, self.genome3)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v3, multicolor=multicolor1)
        edge3 = BGEdge(vertex1=v4, vertex2=v5, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge1, merge=False)
        graph.add_bgedge(edge2)
        graph.add_bgedge(edge3)
        graph.split_all_edges()
        self.assertEqual(len(list(graph.nodes())), 5)
        self.assertEqual(len(list(graph.edges())), 12)
        self.assertEqual(len(list(graph.get_edges_by_vertex(vertex=v1))), 9)
        self.assertEqual(len(list(graph.get_edges_by_vertex(vertex=v2))), 6)
        self.assertEqual(len(list(graph.get_edges_by_vertex(vertex=v4))), 3)
        edges = list(graph.edges())
        multicolors = Multicolor.split_colors(multicolor=multicolor1)
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in multicolors)
        # test with a four multi-colored edges
        # two edges between vertices v1 and v2
        # one edge between vertices v1 and v3
        # one edge between vertices v4 and v5
        # with guidance
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        v3 = BGVertex("v3")
        v4 = BGVertex("v4")
        v5 = BGVertex("v5")
        multicolor1 = Multicolor(self.genome1, self.genome4, self.genome3)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v3, multicolor=multicolor1)
        edge3 = BGEdge(vertex1=v4, vertex2=v5, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge1, merge=False)
        graph.add_bgedge(edge2)
        graph.add_bgedge(edge3)
        graph.split_all_edges(guidance=[(self.genome1, self.genome4)])
        self.assertEqual(len(list(graph.nodes())), 5)
        self.assertEqual(len(list(graph.edges())), 8)
        self.assertEqual(len(list(graph.get_edges_by_vertex(vertex=v1))), 6)
        self.assertEqual(len(list(graph.get_edges_by_vertex(vertex=v2))), 4)
        self.assertEqual(len(list(graph.get_edges_by_vertex(vertex=v4))), 2)
        edges = list(graph.edges())
        multicolors = Multicolor.split_colors(multicolor=multicolor1, guidance=[(self.genome1, self.genome4)])
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in multicolors)
        # test with a four multi-colored edges with duplications
        # two edges between vertices v1 and v2
        # one edge between vertices v1 and v3
        # one edge between vertices v4 and v5
        # no guidance
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        v3 = BGVertex("v3")
        v4 = BGVertex("v4")
        v5 = BGVertex("v5")
        multicolor1 = Multicolor(self.genome1, self.genome4, self.genome3, self.genome1, self.genome3)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v3, multicolor=multicolor1)
        edge3 = BGEdge(vertex1=v4, vertex2=v5, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge1, merge=False)
        graph.add_bgedge(edge2)
        graph.add_bgedge(edge3)
        graph.split_all_edges()
        self.assertEqual(len(list(graph.nodes())), 5)
        self.assertEqual(len(list(graph.edges())), 12)
        self.assertEqual(len(list(graph.get_edges_by_vertex(vertex=v1))), 9)
        self.assertEqual(len(list(graph.get_edges_by_vertex(vertex=v2))), 6)
        self.assertEqual(len(list(graph.get_edges_by_vertex(vertex=v4))), 3)
        edges = list(graph.edges())
        multicolors = Multicolor.split_colors(multicolor=multicolor1)
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in multicolors)
        # test with a four multi-colored edges with duplications
        # two edges between vertices v1 and v2
        # one edge between vertices v1 and v3
        # one edge between vertices v4 and v5
        # with guidance
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        v3 = BGVertex("v3")
        v4 = BGVertex("v4")
        v5 = BGVertex("v5")
        multicolor1 = Multicolor(self.genome1, self.genome4, self.genome3, self.genome1, self.genome3)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v3, multicolor=multicolor1)
        edge3 = BGEdge(vertex1=v4, vertex2=v5, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge1, merge=False)
        graph.add_bgedge(edge2)
        graph.add_bgedge(edge3)
        graph.split_all_edges(guidance=[(self.genome1, self.genome4)])
        self.assertEqual(len(list(graph.nodes())), 5)
        self.assertEqual(len(list(graph.edges())), 8)
        self.assertEqual(len(list(graph.get_edges_by_vertex(vertex=v1))), 6)
        self.assertEqual(len(list(graph.get_edges_by_vertex(vertex=v2))), 4)
        self.assertEqual(len(list(graph.get_edges_by_vertex(vertex=v4))), 2)
        edges = list(graph.edges())
        multicolors = Multicolor.split_colors(multicolor=multicolor1, guidance=[(self.genome1, self.genome4)])
        for bgedge in edges:
            self.assertTrue(bgedge.multicolor in multicolors)

    def test_delete_all_edges_between_two_vertices(self):
        # comprehensive test case with various possible edges between two given vertices
        # equipped with a random edge sticking out of vertex v1, but not towards vertex v2
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        v3 = BGVertex("v3")
        multicolor1 = Multicolor(self.genome1)
        multicolor2 = Multicolor(self.genome1, self.genome1)
        multicolor4 = Multicolor(self.genome1, self.genome4, self.genome2)
        multicolor5 = Multicolor(self.genome1, self.genome4, self.genome2, self.genome1, self.genome2)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor2)
        edge4 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor4)
        edge5 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor5)
        edge6 = BGEdge(vertex1=v1, vertex2=v3, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge2, merge=False)
        graph.add_bgedge(edge4, merge=False)
        graph.add_bgedge(edge5, merge=False)
        graph.add_bgedge(edge6, merge=False)
        graph.delete_all_edges_between_two_vertices(vertex1=v1, vertex2=v2)
        self.assertEqual(len(list(graph.nodes())), 3)
        self.assertEqual(len(list(graph.edges())), 1)
        edges = list(graph.get_edges_by_vertex(vertex=v1))
        self.assertEqual(edges[0].multicolor, multicolor1)

    def test_merge_graphs_with_another_graph_merge_added_edges(self):
        # merging an empty graph with existing one
        graph1 = BreakpointGraph()
        graph2 = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        v3 = BGVertex("v3")
        v4 = BGVertex("v4")
        v5 = BGVertex("v5")
        multicolor1 = Multicolor(self.genome1, self.genome4, self.genome2, self.genome1)
        multicolor2 = Multicolor(self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v3, multicolor=multicolor2)
        edge3 = BGEdge(vertex1=v4, vertex2=v5, multicolor=multicolor1)
        graph2.add_bgedge(edge1)
        graph2.add_bgedge(edge1, merge=False)
        graph2.add_bgedge(edge2, merge=False)
        graph2.add_bgedge(edge3, merge=False)
        result_graph = BreakpointGraph.merge(graph1, graph2, merge_edges=True)
        self.assertEqual(len(list(result_graph.nodes())), 5)
        self.assertEqual(len(list(result_graph.edges())), 3)
        self.assertEqual(len(list(result_graph.get_edges_by_vertex(vertex=v1))), 2)
        self.assertEqual(len(list(result_graph.get_edges_by_vertex(vertex=v2))), 1)
        self.assertEqual(len(list(result_graph.get_edges_by_vertex(vertex=v4))), 1)
        bgedges = list(result_graph.edges())
        multicolors = [multicolor1, multicolor2, multicolor1 + multicolor1]
        for bgedge in bgedges:
            self.assertTrue(bgedge.multicolor in multicolors)
        # merging a non empty graph with an empty one
        graph1 = BreakpointGraph()
        graph2 = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        v3 = BGVertex("v3")
        v4 = BGVertex("v4")
        v5 = BGVertex("v5")
        multicolor1 = Multicolor(self.genome1, self.genome4, self.genome2, self.genome1)
        multicolor2 = Multicolor(self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v3, multicolor=multicolor2)
        edge3 = BGEdge(vertex1=v4, vertex2=v5, multicolor=multicolor1)
        graph2.add_bgedge(edge1)
        graph2.add_bgedge(edge1, merge=False)
        graph2.add_bgedge(edge2, merge=False)
        graph2.add_bgedge(edge3, merge=False)
        result_graph = BreakpointGraph.merge(graph2, graph1, merge_edges=True)
        self.assertEqual(len(list(result_graph.nodes())), 5)
        self.assertEqual(len(list(result_graph.edges())), 3)
        self.assertEqual(len(list(result_graph.get_edges_by_vertex(vertex=v1))), 2)
        self.assertEqual(len(list(result_graph.get_edges_by_vertex(vertex=v2))), 1)
        self.assertEqual(len(list(result_graph.get_edges_by_vertex(vertex=v4))), 1)
        bgedges = list(result_graph.edges())
        multicolors = [multicolor1, multicolor2, multicolor1 + multicolor1]
        for bgedge in bgedges:
            self.assertTrue(bgedge.multicolor in multicolors)
        # merging two non empty graphs
        graph1 = BreakpointGraph()
        graph2 = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        v3 = BGVertex("v3")
        v4 = BGVertex("v4")
        v5 = BGVertex("v5")
        multicolor1 = Multicolor(self.genome1, self.genome4, self.genome2, self.genome1)
        multicolor2 = Multicolor(self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v3, multicolor=multicolor2)
        edge3 = BGEdge(vertex1=v4, vertex2=v5, multicolor=multicolor1)
        graph2.add_bgedge(edge1)
        graph2.add_bgedge(edge1, merge=False)
        graph2.add_bgedge(edge2, merge=False)
        graph2.add_bgedge(edge3, merge=False)
        graph1.add_bgedge(edge1)
        graph1.add_bgedge(edge1, merge=False)
        graph1.add_bgedge(edge2, merge=False)
        graph1.add_bgedge(edge3, merge=False)
        result_graph = BreakpointGraph.merge(graph2, graph1, merge_edges=True)
        self.assertEqual(len(list(result_graph.nodes())), 5)
        self.assertEqual(len(list(result_graph.edges())), 3)
        self.assertEqual(len(list(result_graph.get_edges_by_vertex(vertex=v1))), 2)
        self.assertEqual(len(list(result_graph.get_edges_by_vertex(vertex=v2))), 1)
        self.assertEqual(len(list(result_graph.get_edges_by_vertex(vertex=v4))), 1)
        bgedges = list(result_graph.edges())
        multicolors = [multicolor1 + multicolor1, multicolor2 + multicolor2,
                       multicolor1 + multicolor1 + multicolor1 + multicolor1]
        for bgedge in bgedges:
            self.assertTrue(bgedge.multicolor in multicolors)

    def test_merge_graphs_with_another_graph_no_merge_added_edges(self):
        # merging an empty graph with existing one
        graph1 = BreakpointGraph()
        graph2 = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        v3 = BGVertex("v3")
        v4 = BGVertex("v4")
        v5 = BGVertex("v5")
        multicolor1 = Multicolor(self.genome1, self.genome4, self.genome2, self.genome1)
        multicolor2 = Multicolor(self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v3, multicolor=multicolor2)
        edge3 = BGEdge(vertex1=v4, vertex2=v5, multicolor=multicolor1)
        graph2.add_bgedge(edge1)
        graph2.add_bgedge(edge1, merge=False)
        graph2.add_bgedge(edge2, merge=False)
        graph2.add_bgedge(edge3, merge=False)
        result_graph = BreakpointGraph.merge(graph1, graph2, merge_edges=False)
        self.assertEqual(len(list(result_graph.nodes())), 5)
        self.assertEqual(len(list(result_graph.edges())), 4)
        self.assertEqual(len(list(result_graph.get_edges_by_vertex(vertex=v1))), 3)
        self.assertEqual(len(list(result_graph.get_edges_by_vertex(vertex=v2))), 2)
        self.assertEqual(len(list(result_graph.get_edges_by_vertex(vertex=v4))), 1)
        bgedges = list(result_graph.edges())
        multicolors = [multicolor1, multicolor2]
        for bgedge in bgedges:
            self.assertTrue(bgedge.multicolor in multicolors)
        # merging a non empty graph with an empty one
        graph1 = BreakpointGraph()
        graph2 = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        v3 = BGVertex("v3")
        v4 = BGVertex("v4")
        v5 = BGVertex("v5")
        multicolor1 = Multicolor(self.genome1, self.genome4, self.genome2, self.genome1)
        multicolor2 = Multicolor(self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v3, multicolor=multicolor2)
        edge3 = BGEdge(vertex1=v4, vertex2=v5, multicolor=multicolor1)
        graph2.add_bgedge(edge1)
        graph2.add_bgedge(edge1, merge=False)
        graph2.add_bgedge(edge2, merge=False)
        graph2.add_bgedge(edge3, merge=False)
        result_graph = BreakpointGraph.merge(graph2, graph1, merge_edges=False)
        self.assertEqual(len(list(result_graph.nodes())), 5)
        self.assertEqual(len(list(result_graph.edges())), 4)
        self.assertEqual(len(list(result_graph.get_edges_by_vertex(vertex=v1))), 3)
        self.assertEqual(len(list(result_graph.get_edges_by_vertex(vertex=v2))), 2)
        self.assertEqual(len(list(result_graph.get_edges_by_vertex(vertex=v4))), 1)
        bgedges = list(result_graph.edges())
        multicolors = [multicolor1, multicolor2]
        for bgedge in bgedges:
            self.assertTrue(bgedge.multicolor in multicolors)
        # merging two non empty graphs
        graph1 = BreakpointGraph()
        graph2 = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        v3 = BGVertex("v3")
        v4 = BGVertex("v4")
        v5 = BGVertex("v5")
        multicolor1 = Multicolor(self.genome1, self.genome4, self.genome2, self.genome1)
        multicolor2 = Multicolor(self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v3, multicolor=multicolor2)
        edge3 = BGEdge(vertex1=v4, vertex2=v5, multicolor=multicolor1)
        graph2.add_bgedge(edge1)
        graph2.add_bgedge(edge1, merge=False)
        graph2.add_bgedge(edge2, merge=False)
        graph2.add_bgedge(edge3, merge=False)
        graph1.add_bgedge(edge1)
        graph1.add_bgedge(edge1, merge=False)
        graph1.add_bgedge(edge2, merge=False)
        graph1.add_bgedge(edge3, merge=False)
        result_graph = BreakpointGraph.merge(graph2, graph1, merge_edges=False)
        self.assertEqual(len(list(result_graph.nodes())), 5)
        self.assertEqual(len(list(result_graph.edges())), 8)
        self.assertEqual(len(list(result_graph.get_edges_by_vertex(vertex=v1))), 6)
        self.assertEqual(len(list(result_graph.get_edges_by_vertex(vertex=v2))), 4)
        self.assertEqual(len(list(result_graph.get_edges_by_vertex(vertex=v4))), 2)
        bgedges = list(result_graph.edges())
        multicolors = [multicolor1, multicolor2]
        for bgedge in bgedges:
            self.assertTrue(bgedge.multicolor in multicolors)

    def test_update_graph_with_another_graph_merge_added_edges(self):
        # updating an empty graph with non empty one
        graph1 = BreakpointGraph()
        graph2 = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        v3 = BGVertex("v3")
        v4 = BGVertex("v4")
        v5 = BGVertex("v5")
        multicolor1 = Multicolor(self.genome1, self.genome4, self.genome2, self.genome1)
        multicolor2 = Multicolor(self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v3, multicolor=multicolor2)
        edge3 = BGEdge(vertex1=v4, vertex2=v5, multicolor=multicolor1)
        graph2.add_bgedge(edge1)
        graph2.add_bgedge(edge1, merge=False)
        graph2.add_bgedge(edge2, merge=False)
        graph2.add_bgedge(edge3, merge=False)
        graph1.update(graph2, merge_edges=True)
        self.assertEqual(len(list(graph1.nodes())), 5)
        self.assertEqual(len(list(graph1.edges())), 3)
        self.assertEqual(len(list(graph1.get_edges_by_vertex(vertex=v1))), 2)
        self.assertEqual(len(list(graph1.get_edges_by_vertex(vertex=v2))), 1)
        self.assertEqual(len(list(graph1.get_edges_by_vertex(vertex=v4))), 1)
        bgedges = list(graph1.edges())
        multicolors = [multicolor1, multicolor2, multicolor1 + multicolor1]
        for bgedge in bgedges:
            self.assertTrue(bgedge.multicolor in multicolors)
        # updating a non empty graph with an empty one
        graph1 = BreakpointGraph()
        graph2 = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        v3 = BGVertex("v3")
        v4 = BGVertex("v4")
        v5 = BGVertex("v5")
        multicolor1 = Multicolor(self.genome1, self.genome4, self.genome2, self.genome1)
        multicolor2 = Multicolor(self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v3, multicolor=multicolor2)
        edge3 = BGEdge(vertex1=v4, vertex2=v5, multicolor=multicolor1)
        graph2.add_bgedge(edge1)
        graph2.add_bgedge(edge1, merge=False)
        graph2.add_bgedge(edge2, merge=False)
        graph2.add_bgedge(edge3, merge=False)
        graph2.update(graph1, merge_edges=True)
        self.assertEqual(len(list(graph2.nodes())), 5)
        self.assertEqual(len(list(graph2.edges())), 4)
        self.assertEqual(len(list(graph2.get_edges_by_vertex(vertex=v1))), 3)
        self.assertEqual(len(list(graph2.get_edges_by_vertex(vertex=v2))), 2)
        self.assertEqual(len(list(graph2.get_edges_by_vertex(vertex=v4))), 1)
        bgedges = list(graph2.edges())
        multicolors = [multicolor1, multicolor2]
        for bgedge in bgedges:
            self.assertTrue(bgedge.multicolor in multicolors)
        # updating a non empty graph with a non empty one
        graph1 = BreakpointGraph()
        graph2 = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        v3 = BGVertex("v3")
        v4 = BGVertex("v4")
        v5 = BGVertex("v5")
        multicolor1 = Multicolor(self.genome1, self.genome4, self.genome2, self.genome1)
        multicolor2 = Multicolor(self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v3, multicolor=multicolor2)
        edge3 = BGEdge(vertex1=v4, vertex2=v5, multicolor=multicolor1)
        graph2.add_bgedge(edge1)
        graph2.add_bgedge(edge1, merge=False)
        graph2.add_bgedge(edge2, merge=False)
        graph2.add_bgedge(edge3, merge=False)
        graph1.add_bgedge(edge1)
        graph1.add_bgedge(edge1, merge=False)
        graph1.add_bgedge(edge2, merge=False)
        graph1.add_bgedge(edge3, merge=False)
        graph2.update(graph1, merge_edges=True)
        self.assertEqual(len(list(graph2.nodes())), 5)
        self.assertEqual(len(list(graph2.edges())), 4)
        self.assertEqual(len(list(graph2.get_edges_by_vertex(vertex=v1))), 3)
        self.assertEqual(len(list(graph2.get_edges_by_vertex(vertex=v2))), 2)
        self.assertEqual(len(list(graph2.get_edges_by_vertex(vertex=v4))), 1)
        bgedges = list(graph2.edges())
        multicolors = [multicolor1 + multicolor1, multicolor2 + multicolor2, multicolor1 + multicolor1 + multicolor1,
                       multicolor1]
        for bgedge in bgedges:
            self.assertTrue(bgedge.multicolor in multicolors)

    def test_update_graph_with_another_graph_no_merge_added_edges(self):
        # updating an empty graph with existing one
        graph1 = BreakpointGraph()
        graph2 = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        v3 = BGVertex("v3")
        v4 = BGVertex("v4")
        v5 = BGVertex("v5")
        multicolor1 = Multicolor(self.genome1, self.genome4, self.genome2, self.genome1)
        multicolor2 = Multicolor(self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v3, multicolor=multicolor2)
        edge3 = BGEdge(vertex1=v4, vertex2=v5, multicolor=multicolor1)
        graph2.add_bgedge(edge1)
        graph2.add_bgedge(edge1, merge=False)
        graph2.add_bgedge(edge2, merge=False)
        graph2.add_bgedge(edge3, merge=False)
        graph1.update(graph2, merge_edges=False)
        self.assertEqual(len(list(graph1.nodes())), 5)
        self.assertEqual(len(list(graph1.edges())), 4)
        self.assertEqual(len(list(graph1.get_edges_by_vertex(vertex=v1))), 3)
        self.assertEqual(len(list(graph1.get_edges_by_vertex(vertex=v2))), 2)
        self.assertEqual(len(list(graph1.get_edges_by_vertex(vertex=v4))), 1)
        bgedges = list(graph1.edges())
        multicolors = [multicolor1, multicolor2]
        for bgedge in bgedges:
            self.assertTrue(bgedge.multicolor in multicolors)
        # updating a non empty graph with an empty one
        graph1 = BreakpointGraph()
        graph2 = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        v3 = BGVertex("v3")
        v4 = BGVertex("v4")
        v5 = BGVertex("v5")
        multicolor1 = Multicolor(self.genome1, self.genome4, self.genome2, self.genome1)
        multicolor2 = Multicolor(self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v3, multicolor=multicolor2)
        edge3 = BGEdge(vertex1=v4, vertex2=v5, multicolor=multicolor1)
        graph2.add_bgedge(edge1)
        graph2.add_bgedge(edge1, merge=False)
        graph2.add_bgedge(edge2, merge=False)
        graph2.add_bgedge(edge3, merge=False)
        graph2.update(graph1, merge_edges=False)
        self.assertEqual(len(list(graph2.nodes())), 5)
        self.assertEqual(len(list(graph2.edges())), 4)
        self.assertEqual(len(list(graph2.get_edges_by_vertex(vertex=v1))), 3)
        self.assertEqual(len(list(graph2.get_edges_by_vertex(vertex=v2))), 2)
        self.assertEqual(len(list(graph2.get_edges_by_vertex(vertex=v4))), 1)
        bgedges = list(graph2.edges())
        multicolors = [multicolor1, multicolor2]
        for bgedge in bgedges:
            self.assertTrue(bgedge.multicolor in multicolors)
        # updating a non empty graph with an empty one
        graph1 = BreakpointGraph()
        graph2 = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        v3 = BGVertex("v3")
        v4 = BGVertex("v4")
        v5 = BGVertex("v5")
        multicolor1 = Multicolor(self.genome1, self.genome4, self.genome2, self.genome1)
        multicolor2 = Multicolor(self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v3, multicolor=multicolor2)
        edge3 = BGEdge(vertex1=v4, vertex2=v5, multicolor=multicolor1)
        graph2.add_bgedge(edge1)
        graph2.add_bgedge(edge1, merge=False)
        graph2.add_bgedge(edge2, merge=False)
        graph2.add_bgedge(edge3, merge=False)
        graph1.add_bgedge(edge1)
        graph1.add_bgedge(edge1, merge=False)
        graph1.add_bgedge(edge2, merge=False)
        graph1.add_bgedge(edge3, merge=False)
        graph2.update(graph1, merge_edges=False)
        self.assertEqual(len(list(graph2.nodes())), 5)
        self.assertEqual(len(list(graph2.edges())), 8)
        self.assertEqual(len(list(graph2.get_edges_by_vertex(vertex=v1))), 6)
        self.assertEqual(len(list(graph2.get_edges_by_vertex(vertex=v2))), 4)
        self.assertEqual(len(list(graph2.get_edges_by_vertex(vertex=v4))), 2)
        bgedges = list(graph2.edges())
        multicolors = [multicolor1, multicolor2]
        for bgedge in bgedges:
            self.assertTrue(bgedge.multicolor in multicolors)

    def test_merge_all_edges_between_two_vertices(self):
        # if no edges exist between two vertices, no exception shall be risen
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor2 = Multicolor(self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor2)
        graph.add_bgedge(edge1)
        graph.delete_bgedge(bgedge=edge1)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 0)
        graph.merge_all_edges_between_two_vertices(vertex1=v1, vertex2=v2)
        self.assertEqual(len(list(graph.nodes())), 2)
        self.assertEqual(len(list(graph.edges())), 0)
        # if single edge exists between two vertices, nothing shall be done
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor2 = Multicolor(self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor2)
        graph.add_bgedge(edge1)
        graph.merge_all_edges_between_two_vertices(vertex1=v1, vertex2=v2)
        self.assertEqual(len(list(graph.nodes())), 2)
        edges = list(graph.edges())
        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0].multicolor, multicolor2)
        # multiple edges shall be glued together
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        multicolor1 = Multicolor(self.genome1)
        multicolor2 = Multicolor(self.genome1)
        multicolor3 = Multicolor(self.genome1, self.genome4)
        multicolor4 = Multicolor(self.genome3, self.genome4)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge2 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor2)
        edge3 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor3)
        edge4 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor4)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge2, merge=False)
        graph.add_bgedge(edge3, merge=False)
        graph.add_bgedge(edge4, merge=False)
        graph.merge_all_edges_between_two_vertices(vertex1=v1, vertex2=v2)
        self.assertEqual(len(list(graph.nodes())), 2)
        edges = list(graph.edges())
        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0].multicolor, multicolor1 + multicolor2 + multicolor3 + multicolor4)

    def test_merge_all_edges(self):
        # a single comprehensive case
        graph = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        v3 = BGVertex("v3")
        v4 = BGVertex("v4")
        v5 = BGVertex("v5")
        v6 = BGVertex("v6")
        v7 = BGVertex("v7")
        v8 = BGVertex("v8")
        multicolor1 = Multicolor(self.genome1, self.genome4, self.genome2, self.genome1)
        multicolor2 = Multicolor(self.genome1)
        edge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor1)
        edge12 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor2)
        edge2 = BGEdge(vertex1=v1, vertex2=v3, multicolor=multicolor2)
        edge3 = BGEdge(vertex1=v4, vertex2=v5, multicolor=multicolor1)
        edge32 = BGEdge(vertex1=v4, vertex2=v5, multicolor=multicolor2)
        edge4 = BGEdge(vertex1=v1, vertex2=v6, multicolor=multicolor1)
        edge5 = BGEdge(vertex1=v7, vertex2=v8, multicolor=multicolor1)
        graph.add_bgedge(edge1)
        graph.add_bgedge(edge1, merge=False)
        graph.add_bgedge(edge12, merge=False)
        graph.add_bgedge(edge2, merge=False)
        graph.add_bgedge(edge2, merge=False)
        graph.add_bgedge(edge3, merge=False)
        graph.add_bgedge(edge32, merge=False)
        graph.add_bgedge(edge4, merge=False)
        graph.add_bgedge(edge5, merge=False)
        graph.delete_bgedge(bgedge=edge5)
        self.assertEqual(len(list(graph.nodes())), 8)
        self.assertEqual(len(list(graph.edges())), 8)
        graph.merge_all_edges()
        self.assertEqual(len(list(graph.nodes())), 8)
        self.assertEqual(len(list(graph.get_edges_by_vertex(vertex=v1))), 3)
        self.assertEqual(len(list(graph.get_edges_by_vertex(vertex=v2))), 1)
        self.assertEqual(len(list(graph.get_edges_by_vertex(vertex=v6))), 1)
        self.assertEqual(len(list(graph.get_edges_by_vertex(vertex=v3))), 1)
        self.assertEqual(len(list(graph.get_edges_by_vertex(vertex=v4))), 1)
        self.assertEqual(len(list(graph.get_edges_by_vertex(vertex=v5))), 1)
        self.assertEqual(len(list(graph.get_edges_by_vertex(vertex=v7))), 0)
        self.assertEqual(len(list(graph.get_edges_by_vertex(vertex=v8))), 0)
        bgedges = list(graph.edges())
        multicolors = [multicolor1 + multicolor2 + multicolor1,
                       multicolor2 + multicolor2,
                       multicolor1,
                       multicolor1 + multicolor2]
        self.assertEqual(len(bgedges), 4)
        for bgedge in bgedges:
            self.assertTrue(bgedge.multicolor in multicolors)

    def test_edges_between_two_vertices(self):
        bg = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        v3 = BGVertex("v3")
        m = Multicolor(self.genome2)
        m2 = Multicolor(self.genome4)
        bgedge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=m)
        bgedge2 = BGEdge(vertex1=v1, vertex2=v2, multicolor=m2)
        bgedge3 = BGEdge(vertex1=v1, vertex2=v3, multicolor=m)
        bg.add_bgedge(bgedge=bgedge1)
        bg.add_bgedge(bgedge=bgedge1, merge=False)
        bg.add_bgedge(bgedge=bgedge2, merge=False)
        bg.add_bgedge(bgedge=bgedge3)
        ref_edges = [bgedge1, bgedge2]
        ref_keys = list(bg.bg[v1][v2].keys())
        for bgedge in bg.edges_between_two_vertices(vertex1=v1, vertex2=v2):
            self.assertTrue(bgedge in ref_edges)
        for bgedge, key in bg.edges_between_two_vertices(vertex1=v1, vertex2=v2, keys=True):
            self.assertTrue(bgedge in ref_edges)
            self.assertTrue(key in ref_keys)
        for bgedge in bg.edges_between_two_vertices(vertex1=v2, vertex2=v1):
            self.assertTrue(bgedge in ref_edges)
        for bgedge, key in bg.edges_between_two_vertices(vertex1=v2, vertex2=v1, keys=True):
            self.assertTrue(bgedge in ref_edges)
            self.assertTrue(key in ref_keys)

    def test_edges_between_two_vertices_incorrect(self):
        bg = BreakpointGraph()
        v1 = BGVertex("v1")
        v2 = BGVertex("v2")
        v3 = BGVertex("v3")
        m = Multicolor(self.genome2)
        bgedge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=m)
        bg.add_bgedge(bgedge=bgedge1)
        with self.assertRaises(ValueError):
            next(bg.edges_between_two_vertices(vertex1=v1, vertex2=v3))
        with self.assertRaises(ValueError):
            next(bg.edges_between_two_vertices(vertex1=v1, vertex2=v3, keys=True))
        with self.assertRaises(ValueError):
            next(bg.edges_between_two_vertices(vertex1=v3, vertex2=v1))
        with self.assertRaises(ValueError):
            next(bg.edges_between_two_vertices(vertex1=v3, vertex2=v1, keys=True))

    def test_apply_kbreak_incorrect_argument_type(self):
        # only KBreak instances and derivatives are allowed as ``kbreak`` argument to
        # BreakpointGraph.apply_kbreak method
        bg = BreakpointGraph()
        bad_arguments = [1, "a", (1,), [1]]
        for argument in bad_arguments:
            with self.assertRaises(TypeError):
                bg.apply_kbreak(kbreak=argument)

    def test_apply_kbreak_incorrect_invalid_kbreak(self):
        # a case when kbreak attributes were changed after its creation
        # the validity check has to be performed before a kbreak is applied
        bg = BreakpointGraph()
        v1, v2, v3, v4 = BGVertex("v1"), BGVertex("v2"), BGVertex("v3"), BGVertex("v4")
        mock_multicolor = Mock(spec=Multicolor)
        start_edges = [(v1, v2), (v3, v4)]
        end_edges = [(v1, v3), (v2, v4)]
        kbreak = KBreak(start_edges=start_edges,
                        result_edges=end_edges,
                        multicolor=mock_multicolor)
        kbreak.result_edges = [(v1, v3), (v2, v2)]
        with self.assertRaises(ValueError):
            bg.apply_kbreak(kbreak=kbreak)
        kbreak = KBreak(start_edges=start_edges,
                        result_edges=end_edges,
                        multicolor=mock_multicolor)
        kbreak.start_edges = [(v2, v2), (v1, v3)]
        with self.assertRaises(ValueError):
            bg.apply_kbreak(kbreak=kbreak)

    def test_apply_kbreak_incorrect_non_existing_vertices(self):
        # usual vertices that are specified in KBreak (both in starting and resulting edges)
        # must be present in BreakpointGraph instance
        bg = BreakpointGraph()
        v1, v2, v3, v4 = BGVertex("v1"), BGVertex("v2"), BGVertex("v3"), BGVertex("v4")
        v5 = BGVertex("v5")
        multicolor = Multicolor(self.genome2)
        bgedge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        bgedge2 = BGEdge(vertex1=v3, vertex2=v4, multicolor=multicolor)
        bg.add_bgedge(bgedge1)
        bg.add_bgedge(bgedge2)
        start_edges = [(v1, v5), (v3, v4)]
        end_edges = [(v1, v3), (v5, v4)]
        kbreak = KBreak(start_edges=start_edges,
                        result_edges=end_edges,
                        multicolor=multicolor)
        with self.assertRaises(ValueError):
            bg.apply_kbreak(kbreak=kbreak)

    def test_apply_kbreak_incorrect_non_existing_edge(self):
        # case when all targeted by kbreak vertices are present but not all pairs of starting edges with specified
        # multicolor actually correspond to existing edges (no subedge_allowed option is specified)
        bg = BreakpointGraph()
        v1, v2, v3, v4 = BGVertex("v1"), BGVertex("v2"), BGVertex("v3"), BGVertex("v4")
        multicolor = Multicolor(self.genome2)
        bgedge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        bgedge2 = BGEdge(vertex1=v3, vertex2=v4, multicolor=multicolor)
        bg.add_bgedge(bgedge1)
        bg.add_bgedge(bgedge2)
        start_edges = [(v1, v3), (v2, v4)]
        end_edges = [(v1, v3), (v2, v4)]
        kbreak = KBreak(start_edges=start_edges,
                        result_edges=end_edges,
                        multicolor=multicolor)
        with self.assertRaises(ValueError):
            bg.apply_kbreak(kbreak=kbreak)
        # case when all targeted edges exists (in terms of pairs of vertices), but not all of
        # them comply with kbreak multicolor
        bg = BreakpointGraph()
        v1, v2, v3, v4 = BGVertex("v1"), BGVertex("v2"), BGVertex("v3"), BGVertex("v4")
        multicolor = Multicolor(self.genome2)
        multicolor2 = Multicolor(self.genome4)
        bgedge1 = BGEdge(vertex1=v1, vertex2=v1, multicolor=multicolor)
        bgedge2 = BGEdge(vertex1=v3, vertex2=v4, multicolor=multicolor)
        bgedge3 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor2)
        bg.add_bgedge(bgedge1)
        bg.add_bgedge(bgedge2)
        bg.add_bgedge(bgedge3)
        start_edges = [(v1, v2), (v3, v4)]
        end_edges = [(v1, v3), (v2, v4)]
        kbreak = KBreak(start_edges=start_edges,
                        result_edges=end_edges,
                        multicolor=multicolor2)
        with self.assertRaises(ValueError):
            bg.apply_kbreak(kbreak=kbreak)

    def test_apply_kbreak_incorrect_non_existing_single_start_infinity_vertex(self):
        # infinity vertices can be created if needed, but must be present at start, if infinity edges are targeted
        # ======================================================================
        # the only exception if a pair of non-existing infinity vertices are targeted together
        # (a desire to create two new infinity edges, by breaking an imaginary edge between two infinity edges)
        # will be tested later
        bg = BreakpointGraph()
        v1, v2, v3 = BGVertex("v1"), BGVertex("v2"), BGVertex("v3")
        iv1 = BGVertex.construct_infinity_vertex_companion(v1)
        multicolor = Multicolor(self.genome2)
        bgedge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        bgedge2 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        bg.add_bgedge(bgedge1)
        bg.add_bgedge(bgedge2)
        start_edges = [(v1, iv1), (v1, v2)]
        end_edges = [(iv1, v2), (v1, v1)]
        kbreak = KBreak(start_edges=start_edges,
                        result_edges=end_edges,
                        multicolor=multicolor)
        with self.assertRaises(ValueError):
            bg.apply_kbreak(kbreak)

    def test_apply_kbreak_correct_no_infinity_vertices(self):
        # cases when no infinity vertices will be affected (from perspective of start edges)
        # by supplied k-break
        # ========================================================================
        # case 1, simple 2-break, single edges between all targeted pairs of vertices
        bg = BreakpointGraph()
        v1, v2, v3, v4 = BGVertex("v1"), BGVertex("v2"), BGVertex("v3"), BGVertex("v4")
        multicolor = Multicolor(self.genome2)
        bgedge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        bgedge2 = BGEdge(vertex1=v3, vertex2=v4, multicolor=multicolor)
        bg.add_bgedge(bgedge1)
        bg.add_bgedge(bgedge2)
        start_edges = [(v1, v2), (v3, v4)]
        end_edges = [(v1, v3), (v2, v4)]
        kbreak = KBreak(start_edges=start_edges,
                        result_edges=end_edges,
                        multicolor=multicolor)
        bg.apply_kbreak(kbreak=kbreak)
        self.assertEqual(len(list(bg.nodes())), 4)
        ref_edges = [BGEdge(vertex1=vertex1, vertex2=vertex2, multicolor=multicolor) for vertex1, vertex2 in end_edges]
        res_edges = []
        for vertex1, vertex2 in end_edges:
            for bgedge in bg.edges_between_two_vertices(vertex1=vertex1, vertex2=vertex2):
                res_edges.append(bgedge)
        self.assertEqual(len(res_edges), 2)
        self.assertListEqual(res_edges, ref_edges)
        self.assertEqual(len(list(bg.edges_between_two_vertices(vertex1=v1, vertex2=v2))), 0)
        self.assertEqual(len(list(bg.edges_between_two_vertices(vertex1=v3, vertex2=v4))), 0)
        # case 2, simple 3-break, single edges between all targeted pairs of vertices
        bg = BreakpointGraph()
        names = ["v1", "v2", "v3", "v4", "v5", "v6"]
        v1, v2, v3, v4, v5, v6 = (BGVertex(name) for name in names)
        multicolor = Multicolor(self.genome2)
        bgedge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        bgedge2 = BGEdge(vertex1=v3, vertex2=v4, multicolor=multicolor)
        bgedge3 = BGEdge(vertex1=v5, vertex2=v6, multicolor=multicolor)
        bg.add_bgedge(bgedge1)
        bg.add_bgedge(bgedge2)
        bg.add_bgedge(bgedge3)
        start_edges = [(v1, v2), (v3, v4), (v5, v6)]
        end_edges = [(v1, v3), (v2, v5), (v4, v6)]
        kbreak = KBreak(start_edges=start_edges,
                        result_edges=end_edges,
                        multicolor=multicolor)
        bg.apply_kbreak(kbreak=kbreak)
        self.assertEqual(len(list(bg.nodes())), 6)
        ref_edges = [BGEdge(vertex1=vertex1, vertex2=vertex2, multicolor=multicolor) for vertex1, vertex2 in end_edges]
        res_edges = []
        for vertex1, vertex2 in end_edges:
            for bgedge in bg.edges_between_two_vertices(vertex1=vertex1, vertex2=vertex2):
                res_edges.append(bgedge)
        self.assertEqual(len(res_edges), 3)
        self.assertListEqual(res_edges, ref_edges)
        self.assertEqual(len(list(bg.edges_between_two_vertices(vertex1=v1, vertex2=v2))), 0)
        self.assertEqual(len(list(bg.edges_between_two_vertices(vertex1=v3, vertex2=v4))), 0)
        self.assertEqual(len(list(bg.edges_between_two_vertices(vertex1=v5, vertex2=v6))), 0)
        # case 3, a 3-break, multiple edges exist between targeted pairs of vertices
        bg = BreakpointGraph()
        names = ["v1", "v2", "v3", "v4", "v5", "v6"]
        v1, v2, v3, v4, v5, v6 = (BGVertex(name) for name in names)
        multicolor = Multicolor(self.genome2)
        bgedge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        bgedge2 = BGEdge(vertex1=v3, vertex2=v4, multicolor=multicolor)
        bgedge3 = BGEdge(vertex1=v5, vertex2=v6, multicolor=multicolor)
        d_bgedge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        d_bgedge2 = BGEdge(vertex1=v3, vertex2=v4, multicolor=multicolor)
        d_bgedge3 = BGEdge(vertex1=v5, vertex2=v6, multicolor=multicolor)
        bg.add_bgedge(bgedge1)
        bg.add_bgedge(bgedge2)
        bg.add_bgedge(bgedge3)
        bg.add_bgedge(d_bgedge1, merge=False)
        bg.add_bgedge(d_bgedge2, merge=False)
        bg.add_bgedge(d_bgedge3, merge=False)
        start_edges = [(v1, v2), (v3, v4), (v5, v6)]
        end_edges = [(v1, v3), (v2, v5), (v4, v6)]
        kbreak = KBreak(start_edges=start_edges,
                        result_edges=end_edges,
                        multicolor=multicolor)
        bg.apply_kbreak(kbreak=kbreak)
        self.assertEqual(len(list(bg.nodes())), 6)
        edges = list(bg.edges())
        ref_edges = [BGEdge(vertex1=vertex1, vertex2=vertex2, multicolor=multicolor) for vertex1, vertex2 in end_edges]
        self.assertEqual(len(edges), 6)
        res_edges = []
        for vertex1, vertex2 in end_edges:
            for bgedge in bg.edges_between_two_vertices(vertex1=vertex1, vertex2=vertex2):
                res_edges.append(bgedge)
        self.assertListEqual(res_edges, ref_edges)
        self.assertEqual(len(list(bg.edges_between_two_vertices(vertex1=v1, vertex2=v2))), 1)
        self.assertEqual(len(list(bg.edges_between_two_vertices(vertex1=v3, vertex2=v4))), 1)
        self.assertEqual(len(list(bg.edges_between_two_vertices(vertex1=v5, vertex2=v6))), 1)

    def test_apply_kbreak_correct_paired_infinity_vertices(self):
        # cases when at least one of start or result edges in kbreak is specified by a pair of infinity vertices
        # if such double-infinity-edge is targeted for destruction, nothing shall happen,
        # while if such edge is targeted for creation, bo such edges shall be created
        # ========================================================================
        # case 1, simple 2-break, single edges between all targeted pairs of vertices
        # start edges contain a paired infinity vertices
        bg = BreakpointGraph()
        v1, v2, = BGVertex("v1"), BGVertex("v2")
        i_v1, i_v2 = BGVertex.construct_infinity_vertex_companion(v1), BGVertex.construct_infinity_vertex_companion(v2)
        multicolor = Multicolor(self.genome2)
        bgedge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor)
        bg.add_bgedge(bgedge1)
        start_edges = [(v1, v2), (i_v1, i_v2)]
        end_edges = [(v1, i_v1), (v2, i_v2)]
        kbreak = KBreak(start_edges=start_edges,
                        result_edges=end_edges,
                        multicolor=multicolor)
        bg.apply_kbreak(kbreak=kbreak)
        self.assertEqual(len(list(bg.nodes())), 4)
        ref_edges = [BGEdge(vertex1=vertex1, vertex2=vertex2, multicolor=multicolor) for vertex1, vertex2 in end_edges]
        res_edges = []
        for vertex1, vertex2 in end_edges:
            for bgedge in bg.edges_between_two_vertices(vertex1=vertex1, vertex2=vertex2):
                res_edges.append(bgedge)
        self.assertListEqual(res_edges, ref_edges)
        self.assertEqual(len(list(bg.edges_between_two_vertices(vertex1=v1, vertex2=v2))), 0)
        self.assertEqual(len(list(bg.edges_between_two_vertices(vertex1=i_v1, vertex2=i_v2))), 0)
        # case 2, simple 2-break, single edges between all targeted pairs of vertices
        # result edges contain a paired infinity vertices
        bg = BreakpointGraph()
        v1, v2, = BGVertex("v1"), BGVertex("v2")
        i_v1, i_v2 = BGVertex.construct_infinity_vertex_companion(v1), BGVertex.construct_infinity_vertex_companion(v2)
        multicolor = Multicolor(self.genome2)
        bgedge1 = BGEdge(vertex1=v1, vertex2=i_v1, multicolor=multicolor)
        bgedge2 = BGEdge(vertex1=v2, vertex2=i_v2, multicolor=multicolor)
        bg.add_bgedge(bgedge1)
        bg.add_bgedge(bgedge2)
        start_edges = [(v1, i_v1), (v2, i_v2)]
        end_edges = [(v1, v2), (i_v1, i_v2)]
        kbreak = KBreak(start_edges=start_edges,
                        result_edges=end_edges,
                        multicolor=multicolor)
        bg.apply_kbreak(kbreak=kbreak)
        ref_edges = [BGEdge(vertex1=vertex1, vertex2=vertex2, multicolor=multicolor) for vertex1, vertex2 in end_edges
                     if not (BGVertex.is_infinity_vertex(vertex1) and BGVertex(vertex2))]
        res_edges = []
        for vertex1, vertex2 in end_edges:
            if BGVertex.is_infinity_vertex(vertex1) and BGVertex.is_infinity_vertex(vertex2):
                continue
            for bgedge in bg.edges_between_two_vertices(vertex1=vertex1, vertex2=vertex2):
                res_edges.append(bgedge)
        self.assertListEqual(res_edges, ref_edges)
        self.assertEqual(len(list(bg.nodes())), 2)  # infinity vertices shall not be present if there are no in/out edges
        # case 3, simple 3-break, multiple edges between all targeted pairs of vertices
        # start edges contain a paired infinity vertices
        # result edges contain a paired infinity vertices
        bg = BreakpointGraph()
        v1, v2, v3 = BGVertex("v1"), BGVertex("v2"), BGVertex("v3")
        i_v1, i_v2, i_v3 = [BGVertex.construct_infinity_vertex_companion(vertex) for vertex in (v1, v2, v3)]
        multicolor = Multicolor(self.genome2)
        multicolor2 = Multicolor(self.genome4)
        bgedge1 = BGEdge(vertex1=v1, vertex2=i_v1, multicolor=multicolor)
        bgedge2 = BGEdge(vertex1=v2, vertex2=v3, multicolor=multicolor)
        d_bgedge1 = BGEdge(vertex1=v1, vertex2=i_v1, multicolor=multicolor2)
        d_bgedge2 = BGEdge(vertex1=v1, vertex2=v2, multicolor=multicolor2)
        d_bgedge3 = BGEdge(vertex1=v2, vertex2=v3, multicolor=multicolor2)
        bg.add_bgedge(bgedge1)
        bg.add_bgedge(bgedge2)
        bg.add_bgedge(d_bgedge1, merge=False)
        bg.add_bgedge(d_bgedge2, merge=False)
        bg.add_bgedge(d_bgedge3, merge=False)
        start_edges = [(v1, i_v1), (v2, v3), (i_v2, i_v3)]
        end_edges = [(v1, v2), (i_v1, i_v2), (v3, i_v3)]
        kbreak = KBreak(start_edges=start_edges,
                        result_edges=end_edges,
                        multicolor=multicolor)
        bg.apply_kbreak(kbreak=kbreak, merge=False)
        self.assertEqual(len(list(bg.nodes())), 5)
        ref_edges = [BGEdge(vertex1=vertex1, vertex2=vertex2, multicolor=multicolor) for vertex1, vertex2 in end_edges
                     if not (BGVertex.is_infinity_vertex(vertex1) and BGVertex.is_infinity_vertex(vertex2))]
        res_edges = []
        for vertex1, vertex2 in end_edges:
            if BGVertex.is_infinity_vertex(vertex1) and BGVertex.is_infinity_vertex(vertex2):
                continue
            for bgedge in bg.edges_between_two_vertices(vertex1=vertex1, vertex2=vertex2):
                if bgedge.multicolor == kbreak.multicolor:
                    res_edges.append(bgedge)
        self.assertListEqual(res_edges, ref_edges)
        self.assertEqual(bg.get_edge_by_two_vertices(vertex1=v1, vertex2=v2).multicolor, multicolor2)
        self.assertEqual(len(list(bg.edges_between_two_vertices(vertex1=v1, vertex2=v2))), 2)

    def test_json_serialization_no_subclassing(self):
        # breakpoint graph shall be serialized into json format, by utilizing to_json methods of its edges and vertices
        # BreakpointGraph does not utilize a simple json schema, but rather a more complex workflow
        # case with empty BreakpointGraph instance
        bg = BreakpointGraph()
        result = bg.to_json(schema_info=False)
        ref_result = {
            "edges": [],
            "vertices": [],
            "genomes": []
        }
        self.assertDictEqual(result, ref_result)
        # case with BreakpointGraph with a single edge and only two multicolors in it
        # multiplicity of colors is set to 1 and 2
        v1, v2, v3 = BGVertex("v1"), BGVertex("v2"), BGVertex("v3")
        color1, color2 = BGGenome("genome1"), BGGenome("genome2")
        bg = BreakpointGraph()
        bgedge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=Multicolor(color1, color2))
        bgedge1_reversed = BGEdge(vertex1=v2, vertex2=v1, multicolor=Multicolor(color1, color2))
        bgedge2 = BGEdge(vertex1=v1, vertex2=v3, multicolor=Multicolor(color1))
        bgedge2_reversed = BGEdge(vertex1=v3, vertex2=v1, multicolor=Multicolor(color1))
        bgedge3 = BGEdge(vertex1=v2, vertex2=v3, multicolor=Multicolor(color2))
        bgedge3_reversed = BGEdge(vertex1=v3, vertex2=v2, multicolor=Multicolor(color2))
        bg.add_bgedge(bgedge1)
        bg.add_bgedge(bgedge2)
        bg.add_bgedge(bgedge3)
        doubled_ref_result = {
            "edges": [
                # since BreakpointGraph stores undirected edges, both ways of representing an edges is acceptable
                bgedge1.to_json(),
                bgedge1_reversed.to_json(),
                bgedge2.to_json(),
                bgedge2_reversed.to_json(),
                bgedge3.to_json(),
                bgedge3_reversed.to_json()
            ],
            "vertices": [
                v1.to_json(),
                v2.to_json(),
                v3.to_json()
            ],
            "genomes": [
                color1.to_json(),
                color2.to_json()
            ]
        }
        result = bg.to_json()
        self.assertTrue("edges" in result)
        self.assertEqual(len(result["edges"]), 3)
        self.assertTrue("vertices" in result)
        self.assertEqual(len(result["vertices"]), 3)
        for edge_dict in result["edges"]:
            ref_edge_dict = None
            for ref_dict in doubled_ref_result["edges"]:
                if ref_dict["vertex1_id"] == edge_dict["vertex1_id"] and ref_dict["vertex2_id"] == edge_dict["vertex2_id"]:
                    ref_edge_dict = ref_dict
                    break
            self.assertDictEqual(Counter(edge_dict["multicolor"]), Counter(ref_edge_dict["multicolor"]))
        for vertex_dict in result["vertices"]:
            ref_vertex_dict = None
            for ref_dict in doubled_ref_result["vertices"]:
                if ref_dict["v_id"] == vertex_dict["v_id"]:
                    ref_vertex_dict = ref_dict
                    break
            self.assertDictEqual(vertex_dict, ref_vertex_dict)

    def test_json_deserialization(self):
        # simple case
        bg = BreakpointGraph()
        result = bg.to_json(schema_info=False)
        ref_result = {
            "edges": [],
            "vertices": [],
            "genomes": []
        }
        self.assertDictEqual(result, ref_result)
        # case with BreakpointGraph with a single edge and only two multicolors in it
        # multiplicity of colors is set to 1 and 2

        class BGVertexJSONShcemaWithSpecialAttribute(BGVertex.BGVertexJSONSchema):
            def make_object(self, data):
                new_vertex = super().make_object(data=data)
                new_vertex.special_attribute = "special_attribute"
                return new_vertex

        BreakpointGraph.vertices_json_schemas["BGVertexJSONShcemaWithSpecialAttribute"] = BGVertexJSONShcemaWithSpecialAttribute
        v1, v2, v3 = BGVertex("v1"), BGVertex("v2"), BGVertex("v3")
        v1.json_schema = BGVertexJSONShcemaWithSpecialAttribute()

        color1, color2 = BGGenome("genome1"), BGGenome("genome2")
        bg = BreakpointGraph()
        bgedge1 = BGEdge(vertex1=v1, vertex2=v2, multicolor=Multicolor(color1, color2))
        bgedge2 = BGEdge(vertex1=v1, vertex2=v3, multicolor=Multicolor(color1))
        bgedge3 = BGEdge(vertex1=v2, vertex2=v3, multicolor=Multicolor(color2))
        bg.add_bgedge(bgedge1)
        bg.add_bgedge(bgedge2)
        bg.add_bgedge(bgedge3)
        object = bg.to_json()
        new_bg = BreakpointGraph.from_json(object)
        self.assertEqual(len(list(new_bg.nodes())), 3)
        self.assertEqual(len(list(new_bg.edges())), 3)
        for vertex in new_bg.nodes():
            if vertex.name == "v1":
                self.assertTrue(vertex, "special_attribute")
                self.assertEqual(vertex.special_attribute, "special_attribute")
            self.assertTrue(vertex in [v1, v2, v3])
        for bgedge in new_bg.edges():
            self.assertTrue(bgedge in [bgedge1, bgedge2, bgedge3])

    def test_deserialization_incorrect_no_vertices(self):
        with self.assertRaises(ValueError):
            BreakpointGraph.from_json(data={"edges": []}, genomes_data={})


if __name__ == '__main__':  # pragma: no cover
    unittest.main()  # pragma: no cover