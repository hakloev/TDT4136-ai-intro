import numpy as np
from math import exp as euler
from random import randint, shuffle, randrange

class Nodes(object):
    '''
    Object
    '''
    def __init__(self, board, k):
        self.board = board
        self.k = k

    def __str__(self):
        '''
        to_string method, returns the current board
        '''
        return '\n'.join([repr(x) for x in self.board])

    def obj_func(self, board):
        '''
        Finds the relationship between the number of eggs on the board, 
        in every direction, and checks it agains the maximum allowed number of eggs, k
        Checks horizontal, vertical and all diagonals. 
        '''
        # Check horizontal and vertical
        number_of_wrong = vertical = horizontal = 0
        for i in range(len(board)):
            for j in range(len(board)):
                vertical += board[i][j]
                horizontal += board[j][i]
            number_of_wrong += max(0, vertical - self.k) + max(0, horizontal - self.k)
            vertical = horizontal = 0

        '''
        Due to the the complexity of searching through all the diagonals, we did not manage to create our own
        code for this. So we found the following code snippet on the StackOverflow-forum
        '''
        diagonal_matrix = np.array(board)
        diagonals = [diagonal_matrix[::-1,:].diagonal(i) for i in range(-3,4)]
        diagonals.extend(diagonal_matrix.diagonal(i) for i in range(3,-4,-1))
        count = 0
        diagonal_matrix = [n.tolist() for n in diagonals]
        for diagonal in range(len(diagonal_matrix)):
            for node in range(len(diagonal_matrix[diagonal])):
                count += diagonal_matrix[diagonal][node]
            number_of_wrong += max(0, count - self.k)
        count = 0

        # This needs to be changed? Temporary solution
        if number_of_wrong == 4:
            return 0.01
        return (1 / (number_of_wrong + 1))

    def generate_neighbours(self):
        '''
        Function that generates a set of neighbours (different boards) based on the current board state. 
        Returns a list of n neighbours. The neighbours are only generated if there are columns or rows with 
        egg > k. It randomly generates new rows by shuffeling them. We have not implemented support for diagonals
        in this function.
        '''
        to_check = []
        cols = []
        # Finds all columns 
        for i in range (len(self.board)):
            temp = []
            for j in range(len(self.board)):
                temp.append(self.board[j][i])
            cols.append(temp)
        # All columns with number_of_eggs > k, appended to a list
        to_check = [row for row in cols if sum(row) > self.k ]
        # Finding all rows that has an egg in a column > k eggs, and adds it to rows.
        rows = []
        for row in to_check:
            for x in range(len(row)):
                if row[x] == 1 and self.board[x] not in rows:
                    rows.append(self.board[x])
        
        neighbours = []
        for x in range(len(self.board)):
            if self.board[x] in rows:
                boardcopy = list(self.board) # Deep copy, making sure the copy doesn't point at the same memory address
                row = self.board[x]
                row = list(row)
                shuffle(row)
                self.board[x] = row
                neighbours.append(self.board)
                self.board = boardcopy
        ''' 
        If there is no neighbours, there is a conflict in the diagonals. We have no support for this, so shuffeling the first row
        Dangerous, and not legitimate hack. 
        '''
        if len(neighbours) == 0:
            neighbour = list(self.board)
            row = self.board[0]
            row = list(row)
            shuffle(row)
            neighbour[0] = row
            return [neighbour]
        return neighbours

    def get_best_neighbour(self, neighbours):
        '''
        Returns the best neighbour in the neighbours list using lambda (anonymous function)
        '''
        return max(neighbours, key=lambda x: [x for x in neighbours])

class SA(object):

    def __init__(self):
        pass

    def main_loop(self, P, Tmax, Ftarget, decT):
        T = Tmax
        while P.obj_func(P.board) < Ftarget and T > 0:
            neighbours = P.generate_neighbours()
            Pmax = P.get_best_neighbour(neighbours) # highest neighbour
            q = ((P.obj_func(Pmax) - P.obj_func(P.board)) / P.obj_func(P.board)) # sick function
            p = min(1, euler(-q / T)) # sicker function
            x = randint(0, 1)
            if x > p:
                P.board = Pmax
            else:
                P.board = neighbours[randint(0, len(neighbours) - 1)] # random neighbour
            T -= decT # decreasing temperature 
        return P

    def __str__(self):
        pass

def create_board(m, n, k):
    board = []
    row = [1 if x < k else 0 for x in range(m)]
    for y in range(m):
        temp = list(row)
        shuffle(temp)
        board.append(temp) 
    return board

if __name__ == '__main__':
    m = n = 6
    k = 2
    nodes = Nodes(create_board(m, n, k), k)
    sa = SA()
    print(sa.main_loop(nodes, 4096, 1.0, 0.5)) # P, Tmax, Ftarget, decT
