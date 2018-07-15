# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action
from sets import Set

class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		self.rowDimension = rowDimension
		self.colDimension = colDimension
		self.totalMines = totalMines
		self.startX = startX
		self.startY = startY
		self.currX = startX
		self.currY = startY
		self.grid = [[-2 for i in range(colDimension)] for j in range(rowDimension)]
		self.tempGrid = []
		self.states = [0 for i in range(3)]
		self.tempIndex = 0
		self.q = Set()
		self.makingMove = False
		self.flagging = False
		self.uncovering = False
		self.tempNum = 0
		pass
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		self.grid[self.currX][self.currY] = number
		if number != -1:
			self.q.add((self.currX, self.currY))

		if self.tempIndex >= len(self.tempGrid) and self.makingMove:
			self.tempIndex = 0
			self.makingMove = False
			if flagging: flagging = False
			elif uncovering: uncovering = False 
			
		if self.makingMove:
			self.currX = self.tempGrid[tempIndex][0]
			self.currY = self.tempGrid[tempIndex][1]
			tempIndex+=1
			if flagging:
				return Action(AI.Action.FLAG, self.currX, self.currY)
			elif uncovering:
				return Action(AI.Action.UNCOVER, self.currX, self.currY)

		tile = self.q.pop()
		if self.onlyMines(tile[0], tile[1]):
			self.flagMines(tile[0], tile[1])
			return Action(AI.Action.UNCOVER, self.tempGrid[0][0], self.tempGrid[0][1])
		elif self.onlyUncovered(tile[0], tile[1]):
			self.uncoverRest(tile[0], tile[1])
			return Action(AI.Action.UNCOVER, self.tempGrid[0][0], self.tempGrid[0][1])
		
		'''
		if self.tempIndex >= len(tempGrid):
			self.makingMove = False
			self.tempIndex = 0

		if self.grid[curX][curY]


		if self.makingMove:
			self.currX = self.tempGrid[tempIndex][0]
			self.currY = self.tempGrid[tempIndex][1]
			tempIndex+=1
			return Action(AI.Action.UNCOVER, self.currX, self.currY)

		if number >= 0:
			self.grid[curX][curY] = number
			if number == 0:
				self.tempGrid = getGrid(curX, curY)
				self.searching = True
		'''
		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

	def getGrid(x: int, y: int) -> list:
		grid = []
		if (curX == 0 and curY == 0) or (curX == (rowDimension - 1) and curY == 0) or (curX == 0 and curY == (colDimension - 1)) or (curX == (rowDimension - 1) and curY == (colDimension - 1)):
			if curX == 0 and curY == 0:
				grid.append((curX, curY + 1))
				grid.append((curX + 1, curY))
			elif curX == (rowDimension - 1) and curY == 0:
				grid.append((curX - 1, curY))
				grid.append((curX, curY + 1))
			elif curX == 0 and curY == (colDimension - 1):
				grid.append((curX, curY - 1))
				grid.append((curX + 1, curY))
			elif curX == (rowDimension - 1) and curY == (colDimension - 1):
				grid.append((curX - 1, curY))
				grid.append((curX, curY -  1))
		elif curX == 0 or curX == (rowDimension - 1):
			if curX == 0:
				grid.append((curX, curY - 1))
				grid.append((curX + 1, curY - 1))
				grid.append((curX + 1, curY))
				grid.append((curX + 1, curY + 1))
				grid.append((curX, curY + 1))
			elif curX == (rowDimension - 1):
				grid.append((curX, curY - 1))
				grid.append((curX - 1, curY - 1))
				grid.append((curX - 1, curY))
				grid.append((curX - 1, curY + 1))
				grid.append((curX, curY + 1))
		elif curY == 0 || curY == (colDimension - 1):
			if curY == 0:
				grid.append((curX - 1, curY))
				grid.append((curX - 1, curY + 1))
				grid.append((curX, curY + 1))
				grid.append((curX + 1, curY + 1))
				grid.append((curX + 1, curY))
			elif curY == (colDimension - 1):
				grid.append((curX - 1, curY))
				grid.append((curX - 1, curY - 1))
				grid.append((curX, curY - 1))
				grid.append((curX + 1, curY - 1))
				grid.append((curX + 1, curY))
		else:
			for i in range(curX-1, curY+2):
				for j in range(curY-1, curY+2):
					grid.append((i,j))

	def outOfBounds(self, x: int, y: int) -> bool:
		return x >= 0 and y >= 0 and x < self.rowDimension and y < colDimension

	def onlyMines(self, x: int, y: int) -> bool:
		grid = self.getGrid(x, y)
		mines = self.grid[x][y]
		uncovered = 0
		for coor in grid:
			if self.grid[coor[0]][coor[1]] == -2:
				uncovered+=1
		return mines == uncovered

	def onlyUncovered(self, x: int, y: int) -> bool:
		grid = self.getGrid(x, y)
		mines = self.grid[x][y]
		flagged = 0
		for coor in grid:
			if self.grid[coor[0]][coor[1]] == -1:
				flagged+=1
		return mines == flagged

	def flagMines(self, x: int, y: int):
		grid = self.getGrid(x, y)
		for i in range(len(grid)):
			if self.grid[grid[i][0]][grid[i][1]] != -2:
				del grid[i]
		self.tempGrid = grid
		self.makingMove = True
		self.flagging = True

	def uncoverRest(self, x: int, y: int):
		grid = self.getGrid(x, y)
		for i in range(len(grid)):
			if self.grid[grid[i][0]][grid[i][1]] != -2:
				del grid[i]
		self.tempGrid = grid
		self.makingMove = True
		self.uncovering = True

