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
		self.tempNum = 0
		pass
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		self.grid[self.currY][self.currX] = number
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
		
		if len(self.q) > 0:
			searchSpace = list(self.q)
			while len(searchSpace) > 0:
				tile = searchSpace.pop()
				if self.onlyUncovered(tile[0], tile[1]):
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
			if guessTile in self.q:
				self.q.remove(guessTile)
			self.currX = guessTile[0]
			self.currY = guessTile[1]
			self.p.add(guessTile)
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
		return mines == uncovered

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
			for square in tileGrid:
				if self.grid[square[1]][square[0]] == -2:
					grid[square[1] * self.rowDimension + square[0]] += number
		coor = searchSpace.index(max(searchSpace))
		coorX = coor % self.colDimension
		coorY = math.floor(coor / self.rowDimension)
		print("Heuristic Index: " + str(coorX) + " " + str(coorY))
		return coorX, coorY
				
			
			
			
			
			
			
			
			
			
			 
