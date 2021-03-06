# -*- coding: utf-8 -*-
"""Random Walk module."""
import numpy as np
from numpy import linalg as la
import networkx as nx
import matplotlib.pyplot as plt

class RandomWalk():
    """
    Random Walk class.
    >>> states = [0, 1, 2, 3, 4]
    >>> trans = np.array([[1,    0, 0,    0, 0],
                          [0.25, 0, 0.75, 0, 0],
                          [0, 0.25, 0, 0.75, 0],
                          [0, 0, 0.25, 0, 0.75],
                          [0, 0,    0, 1,    0]])
    >>> rw = RandomWalk(states, trans)
    """

    def __init__(self, states, transitions):
        """
        Init method.

        :param states: list of states of random walk
        :type states: list
        :param transitions: matrix of transitions
        :type transitions: np.array
        """
        self.S = states
        self.P = np.array(transitions)


    def get_edges(self):
        """
        Return none-zero weighted edges of random walk.

        :return: list of tuples consisting of from_node, to_node and weight
        """
        edges = []
        for i in self.S:
            for j in self.S:
                if self.P[i,j] > 0:
                    edges.append((i, j, self.P[i,j]))
        return edges


    def trans_power(self, n):
        """
        Return n'th power of transition matrix.

        :param n: power of desired matrix
        :type n: int
        :return: n'th power of transition matrix 
        """
        return la.matrix_power(self.P, n)


    def get_comun_graph(self):
        DG = nx.DiGraph()
        DG.add_weighted_edges_from(self.get_edges())
        return DG


    def color_map(self):
        DG = self.get_comun_graph()
        color_map = []
        for node in DG:
            if DG.has_edge(node , node):
                color_map.append('red')
            else: 
                color_map.append('blue')
        return color_map


    def plot_comm_graph(self):
        color_map = self.color_map()
        plt.style.use('seaborn')
        plt.subplot(111)
        nx.draw_circular(self.get_comun_graph(), node_color = color_map ,  with_labels=True, font_weight='bold')
        plt.show()


    def is_ireducible(self):
        return nx.is_strongly_connected(self.get_comun_graph())


    def get_commun_classes(self):
        cls_list = [x for x in nx.strongly_connected_components(self.get_comun_graph())]
        cls_dict= dict()
        for cls in cls_list:
            cls = list(cls)
            idx = [self.states.index(c) for c in cls]
            sub_trans = np.take(np.take(self.P, idx, axis=0), idx, axis =1)
            is_recurrent = np.all(sub_trans.sum(axis =1 )==1)
            if is_recurrent: 
                cls_dict['recurrent'] = [cls, sub_trans]
            else: 
                cls_dict['transient'] = [cls, sub_trans]
        return cls_dict