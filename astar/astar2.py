#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Authors: Fredrik C. Berg and Håkon Ødegård Løvdal

We wanted to implement the algorithm based on the pseudocode given on it's learning. 
Due to some difficulties with implementing the agendaLoop we've also gotten some help from other students 
and the following webpage: http://www.laurentluce.com/posts/solving-mazes-using-python-simple-recursivity-and-a-search/

We're implementing the A*-algorithm with python3.
"""

from math import fabs as abs
import heapq, sys

class AStar(object):
        
    def __init__(self, debug=False):
        """
        Initializes the AStar object, which consists of all of the logic for performing a search using the 
        A*-algorithm. 
        """
        self.debug = debug
        self.opened = [] # Min-Heap consisting of opened nodes 
        heapq.heapify(self.opened)
        self.closed = set() # Set consisting of closest nodes (implemented as set to ensure no duplicate nodes)
        self.nodes = [] # The grid as a x*x-matrix of all the node-objects
        self.gridWidth = None
        self.gridHeight = None
        self.startNode = None
        self.endNode = None
        self.readBoard() 
        self.agendaLoop()

    def agendaLoop(self):
        """
        The main loop of the algorithm. 
        """
        heapq.heappush(self.opened, (self.startNode.f, self.startNode))
        while len(self.opened): # As long as opened heap consists of elements
            node = heapq.heappop(self.opened)[1] # Get the node-object with the lowest cost
            self.closed.add(node) # Add the current node to closed
            if node is self.endNode:
                """
                The node we're working on is the end node, so we can terminate and display the path
                """
                self.displayPath()
                break
            adjNodes = self.getAdjacentNodes(node) # Retrieves all the neighbouring nodes
            for adjNode in adjNodes:
                if adjNode not in self.closed and (adjNode.f, adjNode) not in self.opened:
                    """
                    If the neighbouring node isn't in the opened or closedlist, 
                    we want to update the node with new values.
                    """
                    self.updateNode(adjNode, node)
                    heapq.heappush(self.opened, (adjNode.f, adjNode))
                # The following code block is never used, so we comment it out, but we really can't understand why it's never accessed.
                #elif node.g + adjNode.cost < adjNode.g:
                #    self.updateNode(adjNode, node)
                #    if adjNode in self.closed:
                #        self.propegate(adjNode)
                             
           
    def updateNode(self, adjNode, node):
        """
        Method used by the main loop, to update a node with a new set of values for the f, g and h functions.
        @param node. The current node being worked on
        @param adjNode. The node being updated 
        """
        adjNode.g = node.g + adjNode.cost
        adjNode.h = self.heuristicMD(adjNode)
        adjNode.parent = node
        adjNode.f = adjNode.h + adjNode.g
    
    #def propegate(node):
    #    for child in node.children:
    #        if (node.g + child.cost) < child.g:
    #            child.parent = node
    #            child.g = node.g + child.cost
    #            child.f = child.h + child.g

    def readBoard(self):
        """
        Reads in a board from a text file, and stores each tile on the board as a node object. The nodes are 
        stored in a matrix, which is used to represent the board. 
        """
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
        """
        Starts from the end node, and traverses through the 
        linked list using the parent attribute. Used 
        to reconstruct the path from end to beginning.
        Also updates characters in node objects for nodes is closed and opened list.
        """
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
        """
        Gets the node at position x, y
        @returns Node. The node found
        @param x. The X coordinate
        @param y. The Y coordinate
        """
        return self.nodes[x][y]

    def getAdjacentNodes(self, node):
        """
        Finds and returns the nodes adjacent to a node as a list.
        The if checks ensure that we dont try to retrive a node outside the grid.
        @returns List. list of nodes
        @param node. Current node being searched
        """
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
        """
        Heuristic function being used. Calculates the manhattan distance between node and end.
        @param node. The current node being searched
        @returns Integer. The manhattan distance.
        """
        return abs(node.x - self.endNode.x) + abs(node.y - self.endNode.y)

class Node(object):

    def __init__(self, char, x, y, cost):
        """
        Initializes a node object. This is used to represent a tile on the game board, as well as 
        store information about the the g, h and f functions.
        @param char. Character used to represent the tile on the board
        @param x. The x coordinate
        @param y. The y coordinate
        @param walkable. Boolean value representing wether the tile is walkable
        """
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
        """
        toString method for node object. 
        @returns string A string representing the node
        """
        return "Node: %s, %s Cost: %s" % (self.x, self.y, self.cost)
    
    def __lt__(self, other):
        """
        Function for making the node objects comparable in the min-heap.
        @returns boolean Tells if self is less than other node.
        """
        return self.f < other.f # Sorting heap-queue on f(s) (A*-algorithm)


def color(color, string):
    """
    Simple function for adding color to the path
    @param color The color code
    @param string The string to be colorized
    @returns string A colorized string
    """
    return "\033[" + str(color) + "m" + string + "\033[0m"

"""
Main method for initializing the program
"""
if __name__ == "__main__":
    a = AStar()

