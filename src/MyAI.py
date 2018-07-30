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
from random import randrange
import math

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
		self.q = set()
		self.p = set()
		self.makingMove = False
		self.flagging = False
		self.uncovering = False
		self.madeHeuristic = False
		self.falseMoves = set()
		self.tempNum = 0
		self.unflagged = False
		pass
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		#print((self.currX, self.currY))
		if not self.unflagged:
			self.grid[self.currY][self.currX] = number
		if self.unflagged:
			self.unflagged = False
		if number != -1 and (self.currX, self.currY) not in self.p:
			self.q.add((self.currX, self.currY))

		if self.tempIndex >= len(self.tempGrid) and self.makingMove:
			self.tempIndex = 0
			self.makingMove = False
			del self.tempGrid[:]
			if self.flagging: 
				self.flagging = False
			if self.uncovering: 
				self.uncovering = False

		if self.makingMove:
			self.currX = self.tempGrid[self.tempIndex][0]
			self.currY = self.tempGrid[self.tempIndex][1]
			self.tempIndex+=1
			if self.flagging:
				return Action(AI.Action.FLAG, self.currX, self.currY)
			elif self.uncovering:
				return Action(AI.Action.UNCOVER, self.currX, self.currY)
		
		if self.madeHeuristic == True:
			'''
			if not self.validateHeuristic(self.currX, self.currY):
				print((self.currX, self.currY))
				self.falseMoves.add((self.currX, self.currY))
				if (self.currX, self.currY) in self.p:
					self.p.remove((self.currX, self.currY))
				self.unflagged = True
				self.grid[self.currY][self.currX] = -2
				self.madeHeuristic = False
				return Action(AI.Action.UNFLAG, self.currX, self.currY)
			print(self.grid)
			'''
			self.madeHeuristic = False
		
		if len(self.q) > 0:
			searchSpace = list(self.q)
			while len(searchSpace) > 0:
				tile = searchSpace.pop()
				if self.empty(tile[0], tile[1]):
					self.q.remove(tile)
					self.p.add(tile)
				elif self.onlyUncovered(tile[0], tile[1]):
					self.uncoverRest(tile[0], tile[1])
					self.q.remove(tile)
					self.p.add(tile)
					if(len(self.tempGrid) > 0):
						self.tempIndex += 1
						self.currX = self.tempGrid[0][0]
						self.currY = self.tempGrid[0][1] 
					return Action(AI.Action.UNCOVER, self.currX, self.currY)
				elif self.onlyMines(tile[0], tile[1]):
					self.flagMines(tile[0], tile[1])
					self.q.remove(tile)
					self.p.add(tile)
					self.tempIndex += 1
					self.currX = self.tempGrid[0][0]
					self.currY = self.tempGrid[0][1]
					return Action(AI.Action.FLAG, self.currX, self.currY)
			'''Do heuristic move
			   A flagging heuristic works better than an uncovering heuristic
			'''
			guessTile = self.flagHeuristic()
			self.currX = guessTile[0]
			self.currY = guessTile[1]
			self.madeHeuristic = True
			if guessTile in self.q:
				self.q.remove(guessTile)
			if guessTile not in self.p:
				self.p.add(guessTile)
			#print(self.grid)
			return Action(AI.Action.FLAG, self.currX, self.currY)
			
		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

	def getGrid(self, curX: int, curY: int) -> list:
		grid = []
		if (curX == 0 and curY == 0) or (curX == (self.colDimension - 1) and curY == 0) or (curX == 0 and curY == (self.rowDimension - 1)) or (curX == (self.colDimension - 1) and curY == (self.rowDimension - 1)):
			if curX == 0 and curY == 0:
				grid.append((curX, curY + 1))
				grid.append((curX + 1, curY))
				grid.append((curX + 1, curY + 1))
			elif curX == (self.colDimension - 1) and curY == 0:
				grid.append((curX - 1, curY))
				grid.append((curX, curY + 1))
				grid.append((curX - 1, curY + 1))
			elif curX == 0 and curY == (self.rowDimension - 1):
				grid.append((curX, curY - 1))
				grid.append((curX + 1, curY))
				grid.append((curX + 1, curY - 1))
			elif curX == (self.colDimension - 1) and curY == (self.rowDimension - 1):
				grid.append((curX - 1, curY))
				grid.append((curX, curY -  1))
				grid.append((curX - 1, curY - 1))
		elif curX == 0 or curX == (self.colDimension - 1):
			if curX == 0:
				grid.append((curX, curY - 1))
				grid.append((curX + 1, curY - 1))
				grid.append((curX + 1, curY))
				grid.append((curX + 1, curY + 1))
				grid.append((curX, curY + 1))
			elif curX == (self.colDimension - 1):
				grid.append((curX, curY - 1))
				grid.append((curX - 1, curY - 1))
				grid.append((curX - 1, curY))
				grid.append((curX - 1, curY + 1))
				grid.append((curX, curY + 1))
		elif curY == 0 or curY == (self.rowDimension - 1):
			if curY == 0:
				grid.append((curX - 1, curY))
				grid.append((curX - 1, curY + 1))
				grid.append((curX, curY + 1))
				grid.append((curX + 1, curY + 1))
				grid.append((curX + 1, curY))
			elif curY == (self.rowDimension - 1):
				grid.append((curX - 1, curY))
				grid.append((curX - 1, curY - 1))
				grid.append((curX, curY - 1))
				grid.append((curX + 1, curY - 1))
				grid.append((curX + 1, curY))
		else:
			for i in range(curY-1, curY+2):
				for j in range(curX-1, curX+2):
					if j == curX and i == curY:
						continue
					grid.append((j,i))
		return grid

	def outOfBounds(self, x: int, y: int) -> bool:
		return x >= 0 and y >= 0 and x < self.colDimension and y < self.rowDimension

	def onlyMines(self, x: int, y: int) -> bool:
		grid = self.getGrid(x, y)
		mines = self.grid[y][x]
		if mines == 0:
			return False
		for coor in grid:
			if self.grid[coor[1]][coor[0]] == -1:
				mines -= 1
		uncovered = 0
		for coor in grid:
			if self.grid[coor[1]][coor[0]] == -2:
				uncovered+=1
		return mines >= uncovered

	def onlyUncovered(self, x: int, y: int) -> bool:
		grid = self.getGrid(x, y)
		mines = self.grid[y][x]
		if mines == 0:
			return True
		flagged = 0
		for coor in grid:
			if self.grid[coor[1]][coor[0]] == -1:
				flagged+=1
		return mines == flagged

	def flagMines(self, x: int, y: int):
		grid = self.getGrid(x, y)
		temp = grid[:]
		for i in grid:
			if self.grid[i[1]][i[0]] != -2:
				temp.remove(i)
		self.tempGrid = temp
		self.currX = x
		self.currY = y
		self.makingMove = True
		self.flagging = True

	def empty(self, x: int, y: int):
		grid = self.getGrid(x, y)
		for i in grid:
			if not i in self.p:
				return False
		return True

	def uncoverRest(self, x: int, y: int):
		grid = self.getGrid(x, y)
		temp = grid[:]
		for i in grid:
			if self.grid[i[1]][i[0]] != -2:
				temp.remove(i)
		self.tempGrid = temp
		self.currX = x
		self.currY = y
		self.makingMove = True
		self.uncovering = True

	def flagHeuristic(self) -> tuple:
		searchSpace = list(self.q)
		grid = [0 for i in range(self.rowDimension * self.colDimension)]
		for tile in searchSpace:
			tileGrid = self.getGrid(tile[0], tile[1])
			number = self.grid[tile[1]][tile[0]]
			'''
			for square in tileGrid:
				if self.grid[square[1]][square[0]] == -1:
					number -= 1
			'''
			for square in tileGrid:
				if self.grid[square[1]][square[0]] == -2:
					#print("Tile: " + str(square[1]) + " " + str(square[0]))
					#print(square[1] * self.colDimension + square[0])
					grid[square[1] * self.colDimension + square[0]] += number
		
		for i in range(len(grid)):
			if grid[i] > 0:
				coorX = i % self.colDimension
				coorY = math.floor(i / self.colDimension)
				if (coorX, coorY) in self.falseMoves:
					#print("Zeroed: " + str((coorY, coorX)))
					grid[i] = 0
					#print("Val: " + str(grid[i]))
		'''
		maxGrid = []
		for i in range(len(grid)):
			if grid[i] == max(grid):
				coorX = i % self.colDimension
				coorY = math.floor(i / self.rowDimension)
				maxGrid.append((coorX, coorY))
		'''
		#print(len(grid))
		index = grid.index(max(grid))
		coorX = index % self.colDimension
		coorY = math.floor(index / self.colDimension)
		self.falseMoves.add((coorX, coorY))
		#print("In: " + str(index) + " Index: " + str((coorY, coorX)) + " Max: " + str(max(grid)) + " Act: " + str(grid[index]))
		#print(grid)
		#input()
		'''
		coor = grid.index(max(grid))
		coorX = coor % self.colDimension
		coorY = math.floor(coor / self.rowDimension)
		print("Coor: " + str((coorY, coorX)))
		'''
		'''
		tCoorX = 0
		tCoorY = 0
		if self.onEdge(coorX, coorY):
			tCoorX, tCoorY = self.trackToEdge(coorX, coorY, grid)
		else:
			tCoorX, tCoorY = self.trackToEdge(coorX, coorY, grid)
		if self.onEdge(tCoorX, tCoorY) or self.isCorner(tCoorX, tCoorY):
			coorX = tCoorX
			coorY = tCoorY
		'''

		#coorX, coorY = maxGrid[0]
		'''
		index = 1
		while index < len(maxGrid):
			coorX, coorY = maxGrid[index]
			index += 1
		
		if not (coorX, coorY) in self.falseMoves:
			return coorX, coorY

		randNum = randrange(0, len(grid) - 1)
		coorX = randNum % self.colDimension
		coorY = math.floor(randNum / self.rowDimension)
		while (coorX, coorY) in self.falseMoves:
			randNum = randrange(0, len(grid))
			coorX = randNum % self.colDimension
			coorY = math.floor(randNum / self.rowDimension)
		'''

		return coorX, coorY
		
	def validateHeuristic(self, x: int, y: int) -> bool:
		grid = self.getGrid(x, y)
		guess = (self.currX, self.currY)
		for i in grid:
			if self.grid[i[1]][i[0]] < 0:
				continue
			if self.onlyMines(i[0], i[1]) or self.onlyUncovered(i[0], i[1]):
				return True
		return False
		
	def onEdge(self, x: int, y: int) -> bool:
		return x == 0 or x == self.colDimension - 1 or y == 0 or y == self.rowDimension

	def isCorner(self, x: int, y: int) -> bool:
		return (x == 0 and y == 0) or (x == self.colDimension and y == 0) or (x == 0 and y == self.rowDimension) or (x == self.colDimension and y == self.rowDimension)

	def inBounds(self, x: int, y: int) -> bool:
		return x >= 0 and x < self.colDimension and y >= 0 and y < self.rowDimension

	def trackToEdge(self, x: int, y: int, grid: list) -> tuple:
		paths = [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]
		coor = (0, 0)
		for i in range(len(paths)):
			blocked = False
			currCoor = paths[i]
			while not blocked:
				if self.onEdge(currCoor[0], currCoor[1]):
					coor = currCoor
					break
				newCoor = (0, 0)
				if i == 0:
					newCoor = (currCoor[0] - 1, currCoor[1])

				elif i == 1:
					newCoor = (currCoor[0], currCoor[1] - 1)

				elif i == 2:
					newCoor = (currCoor[0], currCoor[1] + 1)

				elif i == 3:
					newCoor = (currCoor[0] + 1, currCoor[1])
				
				if grid[newCoor[1] * self.rowDimension + newCoor[0]] == 0:
					coor = currCoor
					blocked = True

				elif grid[newCoor[1] * self.rowDimension + newCoor[0]] != 0:
					currCoor = newCoor
		return coor
			
	def trackToCorner(self, x: int, y: int, grid: list) -> tuple:
		if self.isCorner(x, y):
			return x, y
		paths = []
		hor = False
		ver = False
		if x == 0 or x == self.colDimension:
			paths = [(x, y - 1), (x, y + 1)]
			ver = True
		elif y == 0 or y == self.rowDimension:
			paths = [(x - 1, y), (x + 1, y)]
			hor = True

		coor = (0, 0)
		for i in range(len(paths)):
			blocked = False
			currCoor = paths[i]
			while not blocked:
				if self.isCorner(currCoor[0], currCoor[1]):
					coor = currCoor
					break
				newCoor = (0, 0)
				if i == 0 and hor:
					newCoor = (currCoor[0] - 1, currCoor[1])

				elif i == 1 and hor:
					newCoor = (currCoor[0] + 1, currCoor[1])

				elif i == 0 and ver:
					newCoor = (currCoor[0], currCoor[1] - 1)

				elif i == 1 and ver:
					newCoor = (currCoor[0], currCoor[1] + 1)

				if grid[newCoor[1] * self.rowDimension + newCoor[0]] == 0:
					coor = currCoor
					blocked = True

				elif grid[newCoor[1] * self.rowDimension + newCoor[0]] != 0:
					currCoor = newCoor
		return coor


			
			
			
			
			
			
			
			 
