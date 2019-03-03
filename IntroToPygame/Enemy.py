import Constants
from Vector import *
from Agent import *
import pygame
from pygame.locals import *
pygame.init()

# Basic enemy agent with seek-flee capabilities
class Enemy(Agent):

	# public variables
	interceptPoint = Vector(0, 0)

	# Draws vision-detection line on top of drawing itself and its vector line
	def draw(self, screen):
		# for debugging: draw line from enemy's center to target's center if following target
		if self.velocity.x != 0 or self.velocity.y != 0:
			pygame.draw.line(screen, pygame.Color(255, 0, 0), (self.objectCenter.x, self.objectCenter.y),
					(self.interceptPoint.x + self.objectCenter.x, self.interceptPoint.y + self.objectCenter.y), 3)

		# draw self and vector line
		super().draw(screen)

	# Updates enemy's position, following target object if within attack range
	def update(self, target, worldBounds):
		# calculate distance to target
		self.interceptPoint = target.position - self.position
		distToTarget = self.interceptPoint.length()

		# if target is within attack range, seek/flee from it
		if distToTarget < Constants.ATTACK_RANGE:
			self.velocity = self.interceptPoint.normalize()

			# if enemy is fleeing, reverse their velocity
			if not self.isIt:
				self.velocity = self.velocity.scale(-1)

			super().update(target, worldBounds)
		else:
			self.velocity = Vector(0, 0)