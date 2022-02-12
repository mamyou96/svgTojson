# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 14:59:09 2022

@author: Mohammad Younesi
"""

from xml.dom import minidom
from svg.path import parse_path
from svg.path.path import Line
import json
from node import Node
from graph import Graph
import argparse
import os
import sys

def parser(in_path:str,out_path:str):
    '''
    This is the main method of our program. It parses the svg file and creates the 
    corresponding graph. Then uses the graph to acquire the points, edges, edge_chain_ids,
    and label list. 
    '''
    doc = minidom.parse(in_path)  
    groups = doc.getElementsByTagName('g')
    graph = Graph()
    idx = 0 #this is the variable for keeping track of the nodes' indices
    i = -1  #represents the edge type
    for group in groups:
        label = group.getAttribute('id')
        if label!='annotation':
            children = group.childNodes
            for child in children:
                #print(label)
                if child.nodeName == 'path':
                    path = parse_path(child.getAttribute('d'))
                    prevs = set() #helps us to find when have entered a new shape. 
                    for e in path:
                        if isinstance(e, Line):
                            x0, y0 = e.start.real, e.start.imag 
                            x1, y1 = e.end.real, e.end.imag
                            if (x0,y0) not in prevs:
                            
                                if (x0,y0) not in graph.vert_dict.keys(): #checks when we enter a new shape
                                    i = i+1
                                    graph.add_vertex(Node(idx,x0,y0))
                                    idx = idx + 1
                                    prevs.add((x0,y0))
                            if (x1,y1) not in graph.vert_dict.keys():
                                graph.add_vertex(Node(idx,x1,y1))
                                idx = idx + 1
                                prevs.add((x1,y1))
                            #print(graph.vert_dict.keys())
                            graph.add_edge((x0,y0),(x1,y1),label,i)
    
                elif child.nodeName == 'rect':
                
                    x, y = float(child.getAttribute('x')),float(child.getAttribute('y'))
                    w, h = float(child.getAttribute('width')),float(child.getAttribute('height'))
                    i = i+1
                    p1,p2,p3,p4 = (x,y),(x+w,y),(x+w,y-h),(x,y-h) #four coordinates of the rectangle
                    if p1 not in graph.vert_dict.keys():
                        graph.add_vertex(Node(idx,p1[0],p1[1]))
                        idx = idx+1
                    if p2 not in graph.vert_dict.keys():
                        graph.add_vertex(Node(idx,p2[0],p2[1]))
                        idx = idx+1
                    if p3 not in graph.vert_dict.keys():
                        graph.add_vertex(Node(idx,p3[0],p3[1]))
                        idx = idx+1
                    if p4 not in graph.vert_dict.keys():
                        graph.add_vertex(Node(idx,p4[0],p4[1]))
                        idx = idx+1
                    graph.add_edge(p1,p2,label,i)
                    graph.add_edge(p2,p3,label,i)
                    graph.add_edge(p3,p4,label,i)
                    graph.add_edge(p4,p1,label,i)
    
    doc.unlink()    #unlink the doc as we don't need it anymore
    label_list = []
    edges = []
    edge_chain_ids = set()
    for ver in graph.vert_dict.values():
        for key,val in ver.adjacent.items():
            if ver.indx < key.indx: #printing the edges only once
                label_list.append(val[0])
                edge_chain_ids.add(val[1])
                edges.append([ver.indx,key.indx,val[1]])
    edge_chain_ids = list(edge_chain_ids)
    points = list(graph.vert_dict.keys())
    points = [list(x) for x in points]
    
    data = {'annotations' : {
    'points': points,
    'edges': edges,
    'edge_chain_ids':edge_chain_ids,
    'label_list':label_list
        }
    }
    
    #saving into json
    json_object = json.dumps(data, indent = 4)

    with open(out_path, 'w') as json_file:
        json_file.write(json_object)
        

def convert(file_in,file_out): #this method is not needed :D, but let's keep it!
    parser(file_in,file_out)
    
if __name__ == '__main__':
    
    #adding parser for easier access and usage
    my_parser = argparse.ArgumentParser(description='Parse a svg file to json',
                                    epilog='by @Mohammad Younesi')
    
    my_parser.add_argument('--file_in', action='store', type=str, required=True,
                           help='--file_in "<path/to/svg/file>"')
    my_parser.add_argument('--file_out', action='store', type=str, required=True,
                           help = '--file_out "<path/to/json/file>"')
    
    args = my_parser.parse_args()
    
    if not os.path.exists(args.file_in):
        print('The input path specified does not exist')
        sys.exit()

    if args.file_out[-5:]!='.json':
        print('The output file format should be json')
        sys.exit()
    if args.file_in[-4:]!='.svg':
        print('The input file format should be svg')
        sys.exit()
    parser(args.file_in,args.file_out) #running the main method
    