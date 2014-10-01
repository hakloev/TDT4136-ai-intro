#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code is commented in same way as astar1.py and astar2.py, but there are some differences
because this code implements BFS. We have commented the differences.  
"""

from math import fabs as abs
import sys

class AStar(object):
        
    def __init__(self, debug=False):
        self.debug = debug
        self.opened = [] # Queue for opened nodes
        self.closed = set()
        self.nodes = []
        self.gridWidth = None
        self.gridHeight = None
        self.startNode = None
        self.endNode = None
        self.readBoard() 
        self.agendaLoop()

    def agendaLoop(self):
        self.opened.append(self.startNode) # Append node to openened
        while len(self.opened):
            node = self.opened.pop(0) # Pop the first element (FIFO)
            self.closed.add(node)
            if node is self.endNode:
                self.displayPath()
                break
            adjNodes = self.getAdjacentNodes(node)
            for adjNode in adjNodes:
                if (adjNode.walkable) and (adjNode not in self.closed) and (adjNode not in self.opened):
                    self.updateNode(adjNode, node)
                    self.opened.append(adjNode)
                elif node.g + adjNode.cost < adjNode.g:
                    self.updateNode(adjNode, node)
                    if adjNode in self.closed:
                        self.propegate(adjNode)
                             
           
    def updateNode(self, adjNode, node):
        adjNode.g = node.g + adjNode.cost
        adjNode.h = self.heuristicMD(adjNode)
        adjNode.parent = node
        adjNode.f = adjNode.h + adjNode.g
    
    def propegate(self, node):
        for child in node.children:
            if (node.g + child.cost) < child.g:
                child.parent = node
                child.g = node.g + child.cost
                child.f = child.h + child.g

    def readBoard(self):
        chars = {"w": 100, "m":50, "f":10, "g":5, "r": 1, ".":0, "#":0}
        try:
            board = open('boards/board-%s.txt' % (sys.argv[1]) , 'r')
        except IndexError:
            board = open('boards/board-2-1.txt', 'r')
        lines = board.readlines()
        board.close()
        self.gridWidth = len(lines[0].strip()) 
        self.gridHeight = len(lines) 
        for x in range(len(lines)):
            line = lines[x].strip()
            listLine = []
            for y in range(len(line.strip())):
                char = line[y]
                if char in chars.keys():
                    if char == "#":
                        listLine.append(Node(char, x, y, chars[char], False))
                    else:
                        listLine.append(Node(char, x, y, chars[char]))
                if char == 'A':
                    startNode = Node(color(31, char), x, y, 0)
                    listLine.append(startNode)
                    self.startNode = startNode
                if char == 'B':
                    endNode = Node(color(31,char), x, y, 0)
                    listLine.append(endNode)
                    self.endNode = endNode
            self.nodes.append(listLine)
        
    def displayPath(self):
        if self.debug:
            for node in self.closed: 
                node.char = color(34, 'X')
            for node in self.opened:
                node[1].char = color(33, '*')
        node = self.endNode
        while node.parent is not self.startNode:
            node = node.parent
            node.char = color(32, 'O')
        self.startNode.char = color(31, 'A')
        self.endNode.char = color(31, 'B')
        for x in range(len(self.nodes)):
            for y in range(len(self.nodes[x])):
                print(self.nodes[x][y].char, end='')
            print()

    def getNode(self, x, y):    
        return self.nodes[x][y]

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
        node.children = nodes
        return nodes
    
    def heuristicMD(self, node):
        return abs(node.x - self.endNode.x) + abs(node.y - self.endNode.y)

class Node(object):

    def __init__(self, char, x, y, cost, walkable=True):
        self.char = char
        self.walkable = walkable
        self.cost = cost
        self.x = x
        self.y = y
        self.parent = None
        self.f = 0
        self.g = 0
        self.h = 0
        self.children = []

    def __str__(self):
        return "Node: %s, %s Cost: %s" % (self.x, self.y, self.cost)
    
    def __lt__(self, other):
        return self.f < other.f # Sorting on f(s) (A*-algorithm), but implemented with FIFO-queue)

def color(color, string):
    """
    Simple function for adding color to the path
    @param color The color code
    @param string The string to be colorized
    @returns string A colorized string
    """
    return "\033[" + str(color) + "m" + string + "\033[0m"

if __name__ == "__main__":
    a = AStar()

