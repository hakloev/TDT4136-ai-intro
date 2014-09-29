#!/usr/bin/env python
# -*- coding: utf-8 -*-

# We will implement the A*-algorithm with python3

from math import fabs as abs
import heapq, sys

class AStar(object):
        
    def __init__(self, debug=False):
        self.debug = debug
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.nodes = []
        self.gridWidth = None
        self.gridHeight = None
        self.startNode = None
        self.endNode = None
        self.readBoard() 
        self.agendaLoop()

    def agendaLoop(self):
        heapq.heappush(self.opened, (self.startNode.f, self.startNode))
        while len(self.opened):
            node = heapq.heappop(self.opened)[1]
            self.closed.add(node)
            if node is self.endNode:
                self.displayPath()
                break
            adjNodes = self.getAdjacentNodes(node)
            for adjNode in adjNodes:
                if adjNode.walkable and adjNode not in self.closed:
                    if (adjNode.f, adjNode) in self.opened:
                        if adjNode.g > node.g:
                            self.updateNode(adjNode, node)
                    else:
                        self.updateNode(adjNode, node)
                        heapq.heappush(self.opened, (adjNode.f, adjNode))
           
    def updateNode(self, adjNode, node):
        adjNode.g = node.g
        adjNode.h = self.heuristicMD(adjNode)
        adjNode.parent = node
        adjNode.f = adjNode.h + adjNode.g

    def readBoard(self):
        try:
            board = open('boards/board-%s.txt' % (sys.argv[1]) , 'r')
        except IndexError:
            board = open('boards/board-1-1.txt', 'r')
        lines = board.readlines()
        board.close()
        self.gridWidth = len(lines[0].strip()) 
        self.gridHeight = len(lines) 
        for x in range(len(lines)):
            line = lines[x].strip()
            for y in range(len(line.strip())):
                char = line[y]
                if char == '.':
                    self.nodes.append(Node(x, y, True))
                elif char == '#':
                    self.nodes.append(Node(x, y, False))
                elif char == 'A':
                    startNode = Node(x, y, True)
                    self.nodes.append(startNode)
                    self.startNode = startNode
                elif char == 'B':
                    endNode = Node(x, y, True)
                    self.nodes.append(endNode)
                    self.endNode = endNode
                else:
                    print("DEBUG: There are whitespace characters here, why is this?")

    def displayPath(self):
        print("See mah path, path fastest in zhe world:\n*-----------*")
        node = self.endNode
        print("Cell: %d, %d" % (self.endNode.x, self.endNode.y))
        while node.parent is not self.startNode:
            node = node.parent
            print("Cell: %d, %d" % (node.x, node.y))
        print("Cell: %d, %d" % (self.startNode.x, self.startNode.y))
        print("*-----------*")

    def getNode(self, x, y):    
        return self.nodes[(x * self.gridWidth) + y]

    def getAdjacentNodes(self, node):
        nodes = []
        if node.x < self.gridHeight - 1:
            nodes.append(self.getNode(node.x + 1, node.y))
        if node.y > 0:
            nodes.append(self.getNode(node.x, node.y - 1))
        if node.x > 0:
            nodes.append(self.getNode(node.x - 1, node.y))
        if node.y < self.gridWidth - 1:
            nodes.append(self.getNode(node.x, node.y + 1))
        return nodes
    
    def heuristicMD(self, node):
        return abs(node.x - self.endNode.x) + abs(node.y - self.endNode.y)

class Node(object):

    def __init__(self, x, y, walkable):
        self.walkable = walkable
        self.x = x
        self.y = y
        self.parent = None
        self.f = 0
        self.g = 0
        self.h = 0

    def __str__(self):
        return "Node: %s, %s, %s" % (self.x, self.y, self.walkable)
    
    def __lt__(self, other):
        return self.g < other.g

if __name__ == "__main__":
    a = AStar()

