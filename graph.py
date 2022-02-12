# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 14:59:07 2022

@author: Mohammad Younesi
"""

class Graph:
    '''
    I looked the problem as a graph. Each point in the svg file is a node, and the 
    nodes get connected through the edges. Each edge has a label and a type. Label, is the label 
    of its group, like "boundary-stair" and type is the edge chain id. 
    Nodes are saved in the graph as a dictionary by their coordinates. The reason behind this
    choice is because the coordinates of the nodes should be unique and our graph cannot
    contain duplidates nodes. 
    '''
    
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    
    def __iter__(self):
        return iter(self.vert_dict.values())
    
    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        self.vert_dict[(node.x,node.y)] = node
    
    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None
    
        
    def add_edge(self, frm, to, label,tp):

        self.vert_dict[frm].add_neighbour(self.vert_dict[to], label,tp)
        self.vert_dict[to].add_neighbour(self.vert_dict[frm], label,tp)

    def get_vertices(self):
        return self.vert_dict.keys()