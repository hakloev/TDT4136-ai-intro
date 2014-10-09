
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

	def objFunc(self, board):
		#Finn forholdet mellom antall egg som allerede er på brettet, og sammenlign med det maksimale eggantallet...
		#sjekk horisontal
		numberOfWrong = 0
		vertical, horizontal = 0, 0
		for i in range(len(board)):
			for j in range(len(board)):
				vertical += board[i][j]
				horizontal += board[j][i]
			numberOfWrong += max(0, vertical - self.k) + max(0, horizontal - self.k)
			vertical = 0
			horizontal = 0

		#Due to the the complexity of searching through all the diagonals, this sis 
		diagonalMatrix = np.array(board)
		diagonals = [diagonalMatrix[::-1,:].diagonal(i) for i in range(-3,4)]
		diagonals.extend(diagonalMatrix.diagonal(i) for i in range(3,-4,-1))
		count = 0
		diagonalMatrix = [n.tolist() for n in diagonals]
		for diagonal in range(len(diagonalMatrix)):
			for node in range(len(diagonalMatrix[diagonal])):
				count += diagonalMatrix[diagonal][node]
			numberOfWrong += max(0, count - self.k)
			count = 0
		if numberOfWrong == 4:
			return 0.01
		return (1 / (numberOfWrong + 1))
	
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
		#Finner rader som har et egg i en kolonne som har > k eggs, det er ThaRows
		ThaRows = []
		for row in toCheck:
			for x in range(len(row)):
				if row[x] == 1 and self.board[x] not in ThaRows:
					ThaRows.append(self.board[x])
		#print(ThaRows)

		neighbours = []
		for x in range(len(self.board)):
			if self.board[x] in ThaRows:
				#Vi har kommet til der de kopierer current board i koken. gogo hakloev, u can do dis.
				boardcopy = list(self.board) #Dyp kopi
				row = self.board[x]
				row = list(row)
				shuffle(row)
				self.board[x] = row
				neighbours.append(self.board)
				self.board = boardcopy
		for x in range(len(neighbours)):
			for y in range(len(neighbours[x])):
				print(neighbours[x][y])
			print()
		self.__str__()
		#Dersom det ikke finnes noen nabo, er det en konflikt på en diagonal. istedenfor å shuffle diagonalen, 
		if len(neighbours) == 0:
			neighbour = list(self.board)
			row = self.board[0]
			row = list(row)
			shuffle(row)
			neighbour[0] = row
			return [neighbour]
		return neighbours

	def getBestNeighbour(self, neighbours):
		best, number = 0, 0

		for x in range(len(neighbours)):
			objVal = self.objFunc(neighbours[x])
			if objVal > best:
				best = objVal
				number = x
		print("pmax", neighbours[number])
		print("maxobjval", self.objFunc(neighbours[number]))
		return neighbours[number]

class SA(object):

	def __init__(self):
		pass

	def mainLoop(self, P, Tmax, Ftarget, decT):
		T = Tmax
		while P.objFunc(P.board) < Ftarget and T > 0:
			print("objWhile", P.objFunc(P.board))
			print(Ftarget, T)
			neighbours = P.genNeighbours()
			Pmax = P.getBestNeighbour(neighbours) # highest neighbour
			q = ((P.objFunc(Pmax) - P.objFunc(P.board)) / P.objFunc(P.board)) # sick function
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
	m = n = 6
	k = 2
	nodes = Nodes(createBoard(m, n, k), k)
	print(nodes)
	sa = SA()
	sa.mainLoop(nodes, 4096, 1.0, 0.5) # P, Tmax, Ftarget, decT
