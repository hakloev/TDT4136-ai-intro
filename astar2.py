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
                if adjNode not in self.closed and (adjNode.f, adjNode) not in self.opened:
                    self.updateNode(adjNode, node)
                    heapq.heappush(self.opened, (adjNode.f, adjNode))
                #elif node.g + adjNode.cost < adjNode.g:
                #    self.updateNode(adjNode, node)
                #    print("hit")
                #    if adjNode in self.closed:
                #        bullShitmetodeJegIkkeSKjonnerEnDrittAv(adjNode)
                             
           
    def updateNode(self, adjNode, node):
        adjNode.g = node.g + adjNode.cost
        adjNode.h = self.heuristicMD(adjNode)
        adjNode.parent = node
        adjNode.f = adjNode.h + adjNode.g
    
    def bullshitMetodeJegIkkeSKjonnerEnDrittAv(node):
        for kid in node.children:
            if (node.g + kid.cost) < kid.g:
                kid.parent = node
                kid.g = node.g + kid.cost
                kid.f = kid.h + kid.g

    def readBoard(self):
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
                if char == 'w':
                    listLine.append(Node(char, x, y, 100))
                if char == 'm':
                    listLine.append(Node(char, x, y, 50))
                if char == 'f':
                    listLine.append(Node(char, x, y, 10))
                if char == 'g':
                    listLine.append(Node(char, x, y, 5))
                if char == 'r':
                    listLine.append(Node(char, x, y, 1))
                if char == 'A':
                    startNode = Node(color(31, char), x, y, 0)
                    listLine.append(startNode)
                    self.startNode = startNode
                if char == 'B':
                    endNode = Node(color(31, char), x, y, 0)
                    listLine.append(endNode)
                    self.endNode = endNode
            self.nodes.append(listLine)
        
    def displayPath(self):
        node = self.endNode
        while node.parent is not self.startNode:
            node = node.parent
            node.char = color(32, 'O')
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

    def __init__(self, char, x, y, cost):
        self.char = char
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
        return self.f < other.f # Sorting on f(s) (A*-algorithm)

def color(color, string):
    return "\033[" + str(color) + "m" + string + "\033[0m"

if __name__ == "__main__":
    a = AStar()

