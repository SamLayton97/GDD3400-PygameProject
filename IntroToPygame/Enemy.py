import Constants
from Vector import *
from Agent import *
import pygame
from pygame.locals import *
pygame.init()

# Basic enemy agent with seek-flee capabilities
class Enemy(Agent):

	# Draws vision-detection line on top of drawing itself and its vector line
	def draw(self, screen, target):
		# for debugging: draw line from enemy's center to target's center if following target
		if self.velocity.numerator != 0 or self.velocity.denominator != 0:
			pygame.draw.line(screen, pygame.Color(255, 0, 0), (self.objectCenter.numerator, self.objectCenter.denominator),
					(target.objectCenter.numerator, target.objectCenter.denominator), 3)

		# draw self and vector line
		super().draw(screen)

	# Updates enemy's position, following target object if within attack range
	def update(self, target):
		# calculate direction and distance to target
		directionToTarget = target.position - self.position
		distToTarget = directionToTarget.length()

		# if target is within attack range, follow it
		if distToTarget < Constants.ATTACK_RANGE:
			self.velocity = directionToTarget.normalize()
			super().update()