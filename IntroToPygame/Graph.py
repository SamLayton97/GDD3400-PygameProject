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

		# create queue of nodes
		breadthQueue = []

		# add/'visit' starting node
		breadthQueue.append(start)
		start.isVisited = True

		# while there are nodes in queue to explore (i.e., while path could still exist)
		while breadthQueue:
			# remove first node from queue
			curr = breadthQueue.pop(0)
			curr.isExplored = True

			# if current node is goal, return path from it
			if curr is end:
				return self.buildPath(curr)

			# iterate over node's neighbors
			for currNeighbor in curr.neighbors:
				# if search hasn't visited current neighbor
				if not currNeighbor.isVisited:
					# add neightbor to queue (i.e., visit neighbor) and set back pointer to current node
					breadthQueue.append(currNeighbor)
					currNeighbor.isVisited = True
					currNeighbor.backNode = curr

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

		# while there are nodes in queue to explore (i.e., while path could still exist)
		while djikstraQueue:
			# remove first node from queue
			curr = djikstraQueue.pop(0)
			curr.isExplored = True

			# if current node is goal, return path from it
			if curr is end:
				return self.buildPath(curr)

			# iterate over neighboring nodes
			for currNeighbor in curr.neighbors:
				# calculate distance from curr to its neighbor
				toNeighbor = currNeighbor.center - curr.center
				distToNeighbor = toNeighbor.length()

				# if current neighbor wasn't visited yet
				if not currNeighbor.isVisited:
					# 'visit' node / push it onto queue and set back node
					djikstraQueue.append(currNeighbor)
					currNeighbor.isVisited = True
					currNeighbor.backNode = curr

					# calculate and set cost to this node
					currNeighbor.cost = curr.cost + distToNeighbor

				# if current neighbor has been visited
				else:
					# update cost if cost from current node is less than existing cost
					newCost = distToNeighbor + curr.cost
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
		start.costToEnd = (end.center - start.center).length()
		start.cost = start.costFromStart + start.costToEnd

		# while there are nodes in queue to explore (i.e., while path could still exist)
		while aStarQueue:
			# remove first node from queue
			curr = aStarQueue.pop(0)
			curr.isExplored = True

			# if current node is goal, build and return path from it
			if curr is end:
				return self.buildPath(curr)

			# iterate over neighboring nodes
			for currNeighbor in curr.neighbors:
				# if current neighbor hasn't been visited yet
				if not currNeighbor.isVisited:
					# 'visit' node/push it onto queue and set its back node
					aStarQueue.append(currNeighbor)
					currNeighbor.isVisited = True
					currNeighbor.backNode = curr

					# calculate neighbor's travel cost
					currNeighbor.costFromStart = curr.costFromStart + (currNeighbor.center - curr.center).length()
					currNeighbor.costToEnd = (end.center - currNeighbor.center).length()
					currNeighbor.cost = currNeighbor.costFromStart + currNeighbor.costToEnd

				# if current neighbor has been visited
				else:
					# reevaluate actual cost to travel to this node, and update cost if necessary
					newActualCost = curr.costFromStart + (currNeighbor.center - curr.center).length()
					if newActualCost < currNeighbor.costFromStart:
						currNeighbor.costFromStart = newActualCost
						currNeighbor.cost = newActualCost + currNeighbor.costToEnd

			# re-sort priority queue from lowest to highest cost
			aStarQueue.sort(key=lambda x: x.cost)

		# if no path was found, return empty list
		return []

	def findPath_BestFirst(self, start, end):
		""" Best First Search """
		print("BEST_FIRST")
		self.reset()

		# create priority queue of nodes to visit and explore
		bestQueue = []

		# add/'visit' start node and assign its starting cost
		bestQueue.append(start)
		start.isVisited = True
		start.cost = (end.center - start.center).length()

		# while there are nodes in queue to explore (i.e., while path could still exist)
		while bestQueue:
			# remove first node from queue
			curr = bestQueue.pop(0)
			curr.isExplored = True

			# if current node is goal, build and return path from it
			if curr is end:
				return self.buildPath(curr)

			# iterate over neighboring nodes
			for currNeighbor in curr.neighbors:
				# if current neighbor wasn't visited yet
				if not currNeighbor.isVisited:
					# 'visit' node/push it onto queue and set back node
					bestQueue.append(currNeighbor)
					currNeighbor.isVisited = True
					currNeighbor.backNode = curr

					# calculate and set cost from this node to end
					currNeighbor.cost = (end.center - currNeighbor.center).length()
					
			# re-sort priority queue from lowest to highest cost
			bestQueue.sort(key=lambda x: x.cost)

		# if no path was found, return empty list
		return []

	def draw(self, screen):
		""" Draw the graph """
		for i in range(self.gridHeight):
			for j in range(self.gridWidth):
				self.nodes[i][j].draw(screen)