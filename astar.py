#!/usr/bin/env python
# -*- coding: utf-8 -*-

# We will implement the A*-algorithm with python3

from math import fabs as abs
import heapq

class AStar(object):
    
    def __init__(self): 
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.nodes = []
        self.end = None
        self.start = None
        self.readBoard()            

    def readBoard(self):
		board = open('boards/1.txt', 'r')
		x=0
		y=0
		for line in board:
			for char in line:
				if char == '.':
					self.nodes.append(Node(x, y, True))
				elif char == '#':
					self.nodes.append(Node(x, y, False))
				elif char == 'A':
					n = Node(x, y, True)
					self.nodes.append(n)
					self.start = n
				else:
					n = Node(x, y, True)
					self.nodes.append(n)
					self.end = n
				y+=1
			x+=1
			y=0	        
		board.close()
		for derp in self.nodes:
			derp.printNode()   

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
        print("Node: %s, %s, %s" % (self.x, self.y, self.walkable)) 

if __name__ == "__main__":
    a = AStar()
  
