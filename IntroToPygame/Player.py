from Vector import *
from Agent import *
import pygame
from pygame.locals import *
pygame.init()

# A player-controlled sheep-herding dog
class Player(Agent):

	# Moves player-object in response to player-input (WASD),
	# and updates velocity vector accordingly
	def update(self, worldBounds, graph, herd, gates):
		# determine un-normalized movement vector according to player-input
		xInput = 0
		yInput = 0
		pressed = pygame.key.get_pressed()
		if pressed[K_w]:
			yInput = -1
		elif pressed[K_s]:
			yInput = 1
		if pressed[K_a]:
			xInput = -1
		elif pressed[K_d]:
			xInput = 1

		# if player entered movement input, move player
		if xInput != 0 or yInput != 0:
			# accelerate player
			self.currSpeed = self.maxSpeed

			# update velocity and move player
			movementVector = Vector(xInput, yInput)
			self.velocity = movementVector.normalize()
			super().update(worldBounds)
		# otherwise, freeze movement by halting speed
		else:
			self.currSpeed = 0