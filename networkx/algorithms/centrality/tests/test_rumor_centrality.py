"""
    Unit tests for rumor centrality.
"""
import math

import pytest

import networkx as nx


class TestRumorCentrality:
    def setup_method(self):
        self.K2 = nx.complete_graph(2)
        self.P3 = nx.path_graph(3)
        self.P5 = nx.path_graph(5)
        self.S4 = nx.star_graph(4)
        self.S9 = nx.star_graph(9)

        G = nx.Graph()
        G.add_nodes_from(range(5))
        G.add_edge(0, 1)
        G.add_edge(1, 2)
        G.add_edge(2, 3)
        G.add_edge(1, 4)
        self.G = G
        # 0 -- 1 -- 2 -- 3
        #      |
        #      4

    def test_rumor_centrality_1(self):
        d = nx.rumor_centrality(self.K2)
        exact = dict(zip(range(2), [1] * 2))
        for n, rc in d.items():
            assert exact[n] == pytest.approx(rc, abs=1e-7)

    def test_rumor_centrality_2(self):
        d = nx.rumor_centrality(self.P3)
        exact = {0: 1, 1: 2, 2: 1}
        for n, rc in d.items():
            assert exact[n] == pytest.approx(rc, abs=1e-7)

    def test_rumor_centrality_3(self):
        d = nx.rumor_centrality(self.P5)
        exact = {0: 1, 1: 4, 2: 6, 3: 4, 4: 1}
        for n, rc in d.items():
            assert exact[n] == pytest.approx(rc, abs=1e-7)

    def test_rumor_centrality_4(self):
        d = nx.rumor_centrality(self.S4)
        exact = {0: 24, 1: 6, 2: 6, 3: 6, 4: 6}
        for n, rc in d.items():
            assert exact[n] == pytest.approx(rc, abs=1e-7)

    def test_rumor_centrality_5(self):
        d = nx.rumor_centrality(self.S9)
        exact = {
            0: math.factorial(9),
            1: math.factorial(8),
            2: math.factorial(8),
            3: math.factorial(8),
            4: math.factorial(8),
            5: math.factorial(8),
            6: math.factorial(8),
            7: math.factorial(8),
            8: math.factorial(8),
            9: math.factorial(8),
        }
        for n, rc in d.items():
            assert exact[n] == pytest.approx(rc, abs=1e-7)

    def test_rumor_centrality_6(self):
        d = nx.rumor_centrality(self.G)
        exact = {0: 3, 1: 12, 2: 8, 3: 2, 4: 3}
        for n, rc in d.items():
            assert exact[n] == pytest.approx(rc, abs=1e-7)

    def test_rumor_centrality_7(self):
        G = nx.cycle_graph(3)
        d = nx.rumor_centrality(G)
        exact = {0: 2, 1: 2, 2: 2}
        for n, rc in d.items():
            assert exact[n] == pytest.approx(rc, abs=1e-7)

    def test_rumor_centrality_8(self):
        G = self.G.copy()
        G.add_node(5)
        G.add_edge(4, 5)
        G.add_edge(2, 5)
        # 0 -- 1 -- 2 -- 3
        #      |    |
        #      4 -- 5
        d = nx.rumor_centrality(G)
        exact = {0: 9, 1: 45, 2: 45, 3: 9, 4: 18, 5: 18}
        for n, rc in d.items():
            assert exact[n] == pytest.approx(rc, abs=1e-7)

    def test_rumor_centrality_9(self):
        G = self.G.copy()
        G.add_edge(4, 5)
        G.add_edge(2, 5)
        G.add_edge(1, 6)
        G.add_edge(1, 7)
        G.add_edge(0, 8)
        #         6   7
        #          \ /
        # 8 -- 0 -- 1 -- 2 -- 3
        #           |    |
        #           4 -- 5
        d = nx.rumor_centrality(G)
        exact = {
            0: 2160,
            1: 7560,
            2: 3456,
            3: 432,
            4: 1512,
            5: 756,
            6: 945,
            7: 945,
            8: 270,
        }
        for n, rc in d.items():
            assert exact[n] == pytest.approx(rc, abs=1e-7)

    def test_rumor_centrality_10(self):
        G = nx.cycle_graph(5)
        G.add_edge(2, 4)
        with pytest.raises(NotImplementedError):
            nx.rumor_centrality(G)
