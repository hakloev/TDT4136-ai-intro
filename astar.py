#!/usr/bin/env python
# -*- coding: utf-8 -*-

# We will implement the A*-algorithm with python3

from math import fabs as abs

class AStar(object):
    
    def __init__(self): 
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.nodes = []
        self.end = None
        self.start = None
        self.gridHeight, self.gridWidth = self.readBoard()            

    def readBoard(self):
        return 6, 6

    def heuristic(self, node):
        return abs(node.x - self.end.x) + abs(node.y - self.end.y)

class Node(object):

    def __init__(self, x, y, walkable):
        self.walkable = walkable
        self.x = x
        self.y = y
        self.parent = None
        self.f = 0
        self.g = 0
        self.h = 0

    def printNode(self):
        print("Node: %s, %s" % (self.x, self.y) 

if __name__ == "__main__":
    pass
