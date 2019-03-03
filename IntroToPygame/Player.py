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
	searchType = SearchType.BREADTH_FIRST

	# Moves dog agent along generated path and changes path-finding
	# algorithm according to user input.
	def update(self, worldBounds, graph, herd, gates):
		
		# change pathfinding search type if user presses corresponding button
		pressed = pygame.key.get_pressed()
		if pressed[K_a]:
			self.searchType = SearchType.A_STAR
		elif pressed[K_s]:
			self.searchType = SearchType.BEST_FIRST
		elif pressed[K_d]:
			self.searchType = SearchType.DJIKSTRA
		elif pressed[K_f]:
			self.searchType = SearchType.BREADTH_FIRST

		# if dog-agent has no current path to follow
		if not self.currPath:
			# generate new path according to chosen pathfinding algorithm
			if self.searchType == SearchType.BREADTH_FIRST:
				print("breadth")
			elif self.searchType == SearchType.DJIKSTRA:
				print("djikstra")
			elif self.searchType == SearchType.A_STAR:
				print("a*")
			else:
				print("best")

		# move dog agent
		#super().update(worldBounds)