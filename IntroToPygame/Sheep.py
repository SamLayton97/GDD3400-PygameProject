import Constants
from Vector import *
from Agent import *
import pygame
from pygame.locals import *
pygame.init()

# Basic sheep agent with flocking behavior
class Sheep(Agent):

	# public variables
	interceptPoint = Vector(0, 0)

	# Draws vision-detection line on top of drawing itself and its vector line
	def draw(self, screen):
		# for debugging: draw line from enemy's center to target's center if following target
		if self.velocity.numerator != 0 or self.velocity.denominator != 0:
			pygame.draw.line(screen, pygame.Color(255, 0, 0), (self.objectCenter.numerator, self.objectCenter.denominator),
					(self.interceptPoint.numerator + self.objectCenter.numerator, self.interceptPoint.denominator + self.objectCenter.denominator), 3)

		# draw self and vector line
		super().draw(screen)

	# Updates sheep's position, running from player-dog if within run range
	def update(self, target, worldBounds):
		# calculate distance to target
		self.interceptPoint = self.position - target.position
		distToTarget = self.interceptPoint.length()

		# if target is within minimum range, flee
		if distToTarget < Constants.ATTACK_RANGE:
			self.velocity = self.interceptPoint.normalize()
			super().update(target, worldBounds)
		else:
			self.velocity = Vector(0, 0)