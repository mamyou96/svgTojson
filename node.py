# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 14:59:08 2022

@author: Mohammad Younesi
"""

class Node:
    '''
    Each point in the svg file is saved as a node. We keep track of the 
    adjacent nodes to each node (saving the edges). Moreover, each node has an
    unique index. Adjacent is a dictionary of all the adjacent nodes, keys of this 
    dictionary are the coordinates of the adjacent nodes, and the values are the type
    and the label of the corresponding edge.
    '''
    
    def __init__(self, indx, x, y):
        self.indx = indx
        self.x = x
        self.y = y
        self.adjacent = {}
        
    def add_neighbour(self,neighbour,label,tp):
        self.adjacent[neighbour] = (label,tp)
    
    def get_connections(self):
        return self.adjacent.keys()
    
    def get_indx(self):
        return self.indx
    
    
    def get_point(self):
        return [self.x,self.y]
    
    def get_label(self,neighbour):
        return self.adjacent[neighbour]

    def show(self):
        print("(%.1f, %.1f)" % (self.x, self.y))
