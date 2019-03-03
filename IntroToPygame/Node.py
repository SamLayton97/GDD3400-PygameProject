import pygame
import Vector
import Constants
import sys
import DrawableObject

from pygame import *
from Vector import *
from sys import *
from enum import Enum
from DrawableObject import *


class Node(DrawableObject):
	
	def __init__(self, x, y, position, size):
		""" Initialize the Node object """
		self.upperLeft = position					# upper left corner of the node rect
		self.center = position + size.scale(0.5)	# center of the node rect
		self.size = size							# size of the node
		self.neighbors = []							# list of neighbors of this node
		self.x = x									# index into the node list
		self.y = y									# index into the node list
		self.reset()
		self.isWalkable = True
		self.color = (14, 89, 2)
		self.boundingRect = pygame.Rect(self.upperLeft.x, self.upperLeft.y, size.x, size.y)

	def __str__(self):
		""" String version the Node object """
		value = "N(" + str(self.x) + ", " + str(self.y) + ", " + str(self.center) + ", " + str(self.isVisited) \
				+ ": " + str(self.costFromStart) + ", " + str(self.costToEnd) + ", " + str(self.cost) + ")"
		# If this node has a backnode, add it to the string representation
		if (self.backNode is not 0):
			value += " b: " + str(self.backNode.x) + ", " + str(self.backNode.y)
		return value

	def __lt__(self, other):
		""" Overloaded comparison operator to sort queue """
		return self.cost < other.cost

	def reset(self):
		""" Reset the node for the next search """
		self.isVisited = False		# Has been added to the queue
		self.isStart = False		# Is the starting node for this search
		self.isEnd = False			# Is the ending node for this search
		self.isExplored = False		# Has been popped off the queue!
		self.isPath = False			# Is in the final path
		self.costFromStart = sys.maxsize
		self.costToEnd = sys.maxsize
		self.cost = sys.maxsize		# total cost
		self.backNode = 0			# Node from which we explored this node

	def draw(self, screen):
		""" Draw the node """
		# Rect that represents the visual node
		rect = pygame.Rect(self.upperLeft.x, self.upperLeft.y, self.size.x, self.size.y)
		
		# Draw the solid colored rectangle if appropriate
		if self.isPath:
			pygame.draw.rect(screen, (0, 255, 255), rect)
		elif self.isStart:
			pygame.draw.rect(screen, (0, 255, 0), rect)
		elif self.isEnd:
			pygame.draw.rect(screen, (255, 0, 0), rect)
		elif self.isExplored:
			pygame.draw.rect(screen, (255, 0, 255), rect)
		elif self.isVisited:
			pygame.draw.rect(screen, (0, 0, 255), rect)
		else:
			pygame.draw.rect(screen, self.color, rect)

		# Draw the boundary of the node (the grid lines)
		if Constants.DEBUG_GRID_LINES:
			pygame.draw.rect(screen, (0, 0, 0), rect, Constants.DEBUG_LINE_WIDTH)

		# Draw the edges to each neighbor
		if Constants.DEBUG_NEIGHBOR_LINES:
			for node in self.neighbors:
				pygame.draw.line(screen, (0, 255, 0), (self.center.x, self.center.y), (node.center.x, node.center.y))

