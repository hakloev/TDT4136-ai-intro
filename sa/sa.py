
import numpy as np
from math import exp as euler
from random import randint, shuffle, randrange

class Nodes(object):

	def __init__(self, board, k):
		self.board = board
		self.k = k

	def __str__(self):
		# print board soulution 
		for x in range(len(self.board)):
			print(self.board[x])
		return ""

	def objFunc(self):
		#Finn forholdet mellom antall egg som allerede er på brettet, og sammenlign med det maksimale eggantallet...
		#sjekk horisontal
		numberOfWrong = 0
		vertical, horizontal = 0, 0
		for i in range(len(self.board)):
			for j in range(len(self.board)):
				vertical += self.board[i][j]
				horizontal += self.board[j][i]
			numberOfWrong += max(0, vertical - self.k) + max(0, horizontal - self.k)
			vertical = 0
			horizontal = 0

		#sjekk diagonal, both ways bitches!
		diagonalMatrix = np.array(self.board)
		diagonals = [diagonalMatrix[::-1,:].diagonal(i) for i in range(-3,4)]
		diagonals.extend(diagonalMatrix.diagonal(i) for i in range(3,-4,-1))
		count = 0
		diagonalMatrix = [n.tolist() for n in diagonals]
		for diagonal in range(len(diagonalMatrix)):
			for node in range(len(diagonalMatrix[diagonal])):
				count += diagonalMatrix[diagonal][node]
			numberOfWrong += max(0, count - self.k)
			count = 0
		print (1 - (1 / (numberOfWrong + 1)))
		self.genNeighbours()
		return (1 - (1 / (numberOfWrong + 1)))
	
	def genNeighbours(self):
		#TODO! DIS SHIT CAN LICK MAH BALLS... LIEK REEL HARD
		toCheck = []
		cols = []
		#Finner alle kolonner
		for i in range (len(self.board)):
			temp = []
			for j in range(len(self.board)):
				temp.append(self.board[j][i])
			cols.append(temp)
		#Alle kolonnner der numEggs > k, så legger vi de til en liste
		for row in cols:
			if (sum(row) > k):
				toCheck.append(row)
		ThaRows = []
		for row in toCheck:
			for x in range(len(row)):
				if row[x] == 1 and self.board[x] not in ThaRows:
					ThaRows.append(self.board[x])
		print(ThaRows)
		return 0

class SA(object):

	def __init__(self):
		pass

	def mainLoop(self, P, Tmax, Ftarget, decT):
		T = Tmax
		while P.objFunc() <= Ftarget and T > 0:
			neighbours = P.genNeighbours()
			Pmax = self.getBestNeighbour(neighbours) # highest neighbour
			q = ((Pmax.objFunc() - P.objFunc()) / P.objFunc()) # sick function
			p = min(1, euler(-q / T)) # sicker function
			x = random.randint(0, 1)
			if x > p:
				P = Pmax
			else:
				P = neighbours[randint(len(neighbours) - 1)] # random neighbour
			T -= decT # decreasing temperature 
		return P


	def __str__(self):
		pass


def createBoard(m, n, k):
	board = []
	row = [0] * m
	for x in range(k):
		row[x] = 1
	for y in range(m):
		temp = list(row)
		shuffle(temp)
		board.append(temp) 
	return board

if __name__ == '__main__':
	# create some boards
	m, n, k = 4, 4, 2
	nodes = Nodes(createBoard(m, n, k), k)
	print(nodes)
	nodes.objFunc()
	sa = SA()
	#sa.mainLoop(nodes, 1024, 1, 0.5) # P, Tmax, Ftarget, decT
