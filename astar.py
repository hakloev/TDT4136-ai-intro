#!/usr/bin/env python
# -*- coding: utf-8 -*-

# We will implement the A*-algorithm with python3

class Astar():
    
    def __init__(self): 
        print("init astar")

class Node():

    nodeName = None   

    def __init__(self):
        print("init node")
        self.nodeName = "node1"

    def name(self):
        print(self.nodeName)
        

if __name__ == "__main__":
    a = Astar()
    n = Node()
    n.name()
