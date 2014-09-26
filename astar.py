#!/usr/bin/env python
# -*- coding: utf-8 -*-

# We will implement the A*-algorithm with python3

from math import fabs as abs
import heapq

class AStar(object):
        
    def __init__(self, debug=False):
        self.debug = debug
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.nodes = []
        self.gridWidth = None
        self.gridHeight = None
        self.end = None
        self.start = None
        self.readBoard()            

    def readBoard(self):
        board = open('boards/1.txt', 'r')
        lines = board.readlines()
        board.close()
        self.gridWidth = len(lines[0]) - 1
        self.gridHeight = len(lines) - 1
        x, y = 0, 0
        for line in lines:
            for char in line.strip():
                if char == '.':
                    self.nodes.append(Node(x, y, True))
                elif char == '#':
                    self.nodes.append(Node(x, y, False))
                elif char == 'A':
                    start = Node(x, y, True)
                    self.nodes.append(start)
                    self.start = start
                elif char == 'B':
                    end = Node(x, y, True)
                    self.nodes.append(end)
                    self.end = end
                else:
                    print("DEBUG: There are whitespace characters here, why is this?")
                y += 1
            x += 1
            y = 0	     

    def getNode(self, x, y):
        return self.nodes[(x * self.gridWidth) + y]

    def getAdjacentNodes(self, node):
        nodes = []
        if node.x < self.gridWidth:
            nodes.append(self.getNode(node.x + 1, node.y))
        if node.y > 0:
            nodes.append(self.getNode(node.x, node.y - 1))
        if node.x > 0:
            nodes.append(self.getNode(node.x - 1, node.y))
        if node.y < self.gridWidth:
            nodes.append(self.getNode(node.x, node.y + 1))
        return nodes

    @staticmethod
    def heuristicMD(self, node):
        return abs(node.x - self.end.x) + abs(node.y - self.end.y)

class Node(object):

    def __init__(self, x, y, walkable):
        self.walkable = walkable
        self.x = x
        self.y = y
        self.parent = None
        self.f = 0
        self.g = 0
        #self.h = 0

    def __str__(self):
        return "Node: %s, %s, %s" % (self.x, self.y, self.walkable)

if __name__ == "__main__":
    a = AStar()

