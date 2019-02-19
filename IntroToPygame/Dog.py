from Vector import *
from Agent import *
import pygame
from pygame.locals import *
pygame.init()

# A player-controlled sheep-herding dog
class Dog(Agent):

    # Moves player-object in response to player-input (WASD),
    # and updates velocity vector accordingly
	def update(self, target, worldBounds):
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

        # move player in direction of normalized velocity, scaled up by their speed
		if xInput != 0 or yInput != 0:
			movementVector = Vector(xInput, yInput)
			self.velocity = movementVector.normalize()
			super().update(target, worldBounds)
		else:
			self.velocity = Vector(0, 0)