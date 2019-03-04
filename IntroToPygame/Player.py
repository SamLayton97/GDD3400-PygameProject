from Vector import *
from Agent import *
from Node import *
from Graph import *
import random
import pygame
from pygame.locals import *
pygame.init()

# A player-controlled sheep-herding dog
class Player(Agent):

	# public variables
	currPath = []
	searchType = SearchType.A_STAR

	# Moves dog agent along generated path and changes path-finding
	# algorithm according to user input.
	def update(self, worldBounds, graph, herd, gates):

		# change pathfinding search type if user presses corresponding button
		pressed = pygame.key.get_pressed()
		if pressed[K_a]:
			self.searchType = SearchType.A_STAR

			# DEBUGGING: find path from two random points on grid
			#debugStart = graph.nodes[random.randint(0, graph.gridHeight - 1)][random.randint(0, graph.gridWidth - 1)]
			#debugEnd = graph.nodes[random.randint(0, graph.gridHeight - 1)][random.randint(0, graph.gridWidth - 1)]
			#graph.findPath_AStar(debugStart, debugEnd)
		elif pressed[K_s]:
			self.searchType = SearchType.BEST_FIRST
		elif pressed[K_d]:
			self.searchType = SearchType.DJIKSTRA
		elif pressed[K_f]:
			self.searchType = SearchType.BREADTH_FIRST

		# if dog has no path to follow
		if not self.currPath:
			# find node closest agent's position [start node] and sheep's position [end node]
			dogNode = graph.getNodeFromPoint(self.objectCenter)
			sheepNode = graph.getNodeFromPoint(herd[0].objectCenter)

			# generate new path according to chosen pathfinding algorithm
			if self.searchType == SearchType.BREADTH_FIRST:
				self.currPath = graph.findPath_Breadth(dogNode, sheepNode)
			elif self.searchType == SearchType.DJIKSTRA:
				self.currPath = graph.findPath_Djikstra(dogNode, sheepNode)
			elif self.searchType == SearchType.A_STAR:
				self.currPath = graph.findPath_AStar(dogNode, sheepNode)
			else:
				self.currPath = graph.findPath_BestFirst(dogNode, sheepNode)
		# if agent does have path to follow
		else:
			# aim agent's velocity towards next node
			nextNodeVector = self.currPath[0].center - self.objectCenter
			self.velocity = nextNodeVector.normalize()
			self.currSpeed = self.maxSpeed

			# if agent is close to next node they're travelling to
			nodeProximityVector = self.currPath[0].center - self.objectCenter
			if nodeProximityVector.length() < Constants.GRID_SIZE:
				# pop node from list
				self.currPath.pop(0)

		# move dog agent
		super().update(worldBounds)