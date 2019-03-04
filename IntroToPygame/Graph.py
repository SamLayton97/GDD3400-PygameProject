import Constants
import Node
import pygame
import Vector

from pygame import *
from Vector import *
from Node import *
from enum import Enum

class SearchType(Enum):
	BREADTH_FIRST = 0
	DJIKSTRA = 1
	A_STAR = 2
	BEST_FIRST = 3

class Graph():
	def __init__(self):
		""" Initialize the Graph """
		self.nodes = []			# Set of nodes
		self.obstacles = []		# Set of obstacles - used for collision detection

		# Initialize the size of the graph based on the world size
		self.gridWidth = int(Constants.WORLD_WIDTH / Constants.GRID_SIZE)
		self.gridHeight = int(Constants.WORLD_HEIGHT / Constants.GRID_SIZE)

		# Create grid of nodes
		for i in range(self.gridHeight):
			row = []
			for j in range(self.gridWidth):
				node = Node(i, j, Vector(Constants.GRID_SIZE * j, Constants.GRID_SIZE * i), Vector(Constants.GRID_SIZE, Constants.GRID_SIZE))
				row.append(node)
			self.nodes.append(row)

		## Connect to Neighbors
		for i in range(self.gridHeight):
			for j in range(self.gridWidth):
				# Add the top row of neighbors
				if i - 1 >= 0:
					# Add the upper left
					if j - 1 >= 0:		
						self.nodes[i][j].neighbors += [self.nodes[i - 1][j - 1]]
					# Add the upper center
					self.nodes[i][j].neighbors += [self.nodes[i - 1][j]]
					# Add the upper right
					if j + 1 < self.gridWidth:
						self.nodes[i][j].neighbors += [self.nodes[i - 1][j + 1]]

				# Add the center row of neighbors
				# Add the left center
				if j - 1 >= 0:
					self.nodes[i][j].neighbors += [self.nodes[i][j - 1]]
				# Add the right center
				if j + 1 < self.gridWidth:
					self.nodes[i][j].neighbors += [self.nodes[i][j + 1]]
				
				# Add the bottom row of neighbors
				if i + 1 < self.gridHeight:
					# Add the lower left
					if j - 1 >= 0:
						self.nodes[i][j].neighbors += [self.nodes[i + 1][j - 1]]
					# Add the lower center
					self.nodes[i][j].neighbors += [self.nodes[i + 1][j]]
					# Add the lower right
					if j + 1 < self.gridWidth:
						self.nodes[i][j].neighbors += [self.nodes[i + 1][j + 1]]

	def getNodeFromPoint(self, point):
		""" Get the node in the graph that corresponds to a point in the world """
		return self.nodes[int(point.y/Constants.GRID_SIZE)][int(point.x/Constants.GRID_SIZE)]

	def placeObstacle(self, point, color):
		""" Place an obstacle on the graph """
		node = self.getNodeFromPoint(point)

		# If the node is not already an obstacle, make it one
		if node.isWalkable:
			# Indicate that this node cannot be traversed
			node.isWalkable = False		

			# Set a specific color for this obstacle
			node.color = color
			for neighbor in node.neighbors:
				neighbor.neighbors.remove(node)
			node.neighbors = []
			self.obstacles += [node]

	def reset(self):
		""" Reset all the nodes for another search """
		for i in range(self.gridHeight):
			for j in range(self.gridWidth):
				self.nodes[i][j].reset()

	def buildPath(self, endNode):
		""" Go backwards through the graph reconstructing the path """
		path = []
		node = endNode
		while node is not 0:
			node.isPath = True
			path = [node] + path
			node = node.backNode

		# If there are nodes in the path, reset the colors of start/end
		if len(path) > 0:
			path[0].isPath = False
			path[0].isStart = True
			path[-1].isPath = False
			path[-1].isEnd = True
		return path

	def findPath_Breadth(self, start, end):
		""" Breadth Search """
		print("BREADTH-FIRST")
		self.reset()

		# create queue of nodes and add/'visit' starting node
		searchQueue = []
		searchQueue.append(start)
		start.isVisited = True

		# while there are node in queue to explore (i.e., while path could still exist)
		while searchQueue:
			# remove first node from queue
			currNode = searchQueue.pop(0)
			currNode.isExplored = True

			# iterate over node's neighbors
			for currNeighbor in currNode.neighbors:
				# if search hasn't visited current neighbor
				if not currNeighbor.isVisited:
					# add neighbor to queue (i.e., visit neighbor) and set back pointer to current node
					searchQueue.append(currNeighbor)
					currNeighbor.isVisited = True
					currNeighbor.backNode = currNode

					# if current neighbor is the goal, build path from said node
					if currNeighbor == end:
						return self.buildPath(currNeighbor)

		# if no path was found, return empty list
		return []

	def findPath_Djikstra(self, start, end):
		""" Djikstra's Search """
		print("DJIKSTRA")
		self.reset()		

		# create priority queue of nodes
		djikstraQueue = []

		# add/'visit' starting node and assign its starting cost
		djikstraQueue.append(start)
		start.isVisited = True
		start.cost = 0

		# while there are node in queue to explore (i.e., while path could still exist)
		while djikstraQueue:
			# remove first node from queue
			currNode = djikstraQueue.pop(0)
			currNode.isExplored = True

			# if current node is goal, return path from it
			if currNode == end:
				return self.buildPath(currNode)

			# iterate over neighboring nodes
			for currNeighbor in currNode.neighbors:
				# if current neighbor wasn't visited yet
				if not currNeighbor.isVisited:
					# 'visit' node / push it onto queue and set back node
					djikstraQueue.append(currNeighbor)
					currNeighbor.isVisited = True
					currNeighbor.backNode = currNode

					# calculate and set cost to this node
					fromCurrToNeighbor = currNeighbor.center - currNode.center
					currNeighbor.cost = currNode.cost + (fromCurrToNeighbor.length() / Constants.GRID_SIZE)
				# if current neighbor has been visited
				else:
					# update cost if cost from curren node is less than existing cost
					fromCurrToNeighbor = currNeighbor.center - currNode.center
					newCost = fromCurrToNeighbor.length()
					if newCost < currNeighbor.cost:
						currNeighbor.cost = newCost

			# re-sort priority queue from lowest to highest cost
			djikstraQueue.sort(key=lambda x: x.cost)

		# if no path was found, return empty list
		return []


	def findPath_AStar(self, start, end):
		""" A Star Search """
		print("A_STAR")
		self.reset()

		# create priority queue of nodes
		aStarQueue = []

		# add/'visit' starting node and assign its initial cost(s)
		aStarQueue.append(start)
		start.isVisited = True
		start.costFromStart = 0
		fromStartToEnd = end.center - start.center
		start.costToEnd = fromStartToEnd.length() / Constants.GRID_SIZE
		start.cost = start.costFromStart + start.costToEnd


		return []

	def findPath_BestFirst(self, start, end):
		""" Best First Search """
		print("BEST_FIRST")
		self.reset()

		# create priority queue of nodes to visit and explore
		bestFirstQueue = []

		# add/'visit' start node and assign its starting cost
		bestFirstQueue.append(start)
		start.isVisited = True
		fromStartToEnd = end.center - start.center
		start.cost = fromStartToEnd.length() / Constants.GRID_SIZE

		# while there are node in queue to explore (i.e., while path could still exist)
		while bestFirstQueue:
			# remove first node from queue
			currNode = bestFirstQueue.pop(0)
			currNode.isExplored = True

			# if current node is goal, build and return path from it
			if currNode == end:
				return self.buildPath(currNode)

			# iterate over neighboring nodes
			for currNeighbor in currNode.neighbors:
				# if current node wasn't visited yet
				if not currNeighbor.isVisited:
					# 'visit' node/push it onto queue and set back node
					bestFirstQueue.append(currNeighbor)
					currNeighbor.isVisited = True
					currNeighbor.backNode = currNode

					# calculate and set cost from this node to end
					fromNeighborToEnd = end.center - currNeighbor.center
					currNeighbor.cost = fromNeighborToEnd.length() / Constants.GRID_SIZE
				
			# re-sort priority queue from lowest to highest cost
			bestFirstQueue.sort(key=lambda x: x.cost)

		# if no path was found, return empty list
		return []

	def draw(self, screen):
		""" Draw the graph """
		for i in range(self.gridHeight):
			for j in range(self.gridWidth):
				self.nodes[i][j].draw(screen)