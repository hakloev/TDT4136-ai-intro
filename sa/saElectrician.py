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

	def createBoard(self):
		