from Vector import *
from Agent import *
from Graph import *
import pygame
from pygame.locals import *
pygame.init()

# A player-controlled sheep-herding dog
class Player(Agent):

	# public variables
	currPath = []

	# Moves dog agent along generated path and changes path-finding
	# algorithm according to user input.
	def update(self, worldBounds, graph, herd, gates):
		
		# if dog-agent has no current path to follow
		if not self.currPath:
			# generate new path according to chosen pathfinding algorithm
			print("generate path")

		# move dog agent
		#super().update(worldBounds)