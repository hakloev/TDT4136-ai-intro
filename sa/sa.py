from datastructure import *
import sys, time

if len(sys.argv) == 6:
    m = n = int(sys.argv[1])
    k = int(sys.argv[2])
    Tmax = int(sys.argv[3])
    Ftarget = float(sys.argv[4])
    decT = float(sys.argv[5])
else:
    m = n = 8
    k = 1
    Tmax = 4096
    Ftarget = 1.0
    decT = 0.5

print('------------------------------------\n' + \
        'Initiated with the following values:\n' + \
        'm = n = %d\n' % (m) + \
        'k = %d\n' % (k) + \
        'Tmax = %d\n' % (Tmax) + \
        'Ftarget = %3.2f\n' % (Ftarget) + \
        'decT = %3.2f\n' % (decT) + \
        '------------------------------------')

class SA(object):

    def __init__(self):
        pass        
    
    def main_loop(self, P, Tmax, Ftarget, decT):
        '''
        This is the main loop, the algorithm itself. Based upon the pseudocode
        given in the exercise pdf
        '''
        T = Tmax
        while P.obj_func(P.board) < Ftarget and T > 0:
            neighbours = P.generate_neighbours()
            Pmax = P.get_best_neighbour(neighbours) # highest neighbour
            q = ((P.obj_func(Pmax) - P.obj_func(P.board)) / P.obj_func(P.board)) # sick function
            try:
                p = min(1, euler(-q / T)) # sicker function
            except OverflowError:
                print("I'm outa my loop")
                break
            x = randint(0, 1)
            if x > p:
                P.board = Pmax
            else:
                P.board = neighbours[randint(0, len(neighbours) - 1)] # random neighbour
            T -= decT # decreasing temperature 
        print('Completed with the following values:\n' + \
                'object_value: %3.2f\n' % (P.obj_func(P.board)) + \
                'T: %s\n' % (T) + \
                'Tmax: %s\n' % (Tmax) + \
                '------------------------------------\n' + \
                'Board:\n' + \
                '------------------------------------\n' + \
                '%s' % (P))

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
    nodes = Nodes(create_board(m, n, k), k)
    sa = SA()
    sa.main_loop(nodes, Tmax, Ftarget, decT) # P, Tmax, Ftarget, decT
