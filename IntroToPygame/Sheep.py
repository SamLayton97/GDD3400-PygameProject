import random
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

	# Constructor:
	# Initialize all base Agent variables and then
	# set sheep to start with random velocity between -.5 and 5
	def __init__(self, position, size, maxSpeed, color, surface):
		# initialize base agent variables
		super().__init__(position, size, maxSpeed, color, surface)

		# randomize sheep's starting velocity so that at least one component isn't 0
		velocityX = 0
		velocityY = 0
		while velocityX == 0 or velocityY == 0:
			velocityX = random.uniform(-.5, .5)
			velocityY = random.uniform(-.5, .5)
		randVector = Vector(velocityX, velocityY)
		self.velocity = randVector.normalize()

	# Draws vision-detection line on top of drawing itself and its vector line
	def draw(self, screen):
		# for debugging: draw line from enemy's center to target's center if moving
		if self.currSpeed != 0:
			pygame.draw.line(screen, pygame.Color(255, 0, 0), (self.objectCenter.numerator, self.objectCenter.denominator),
					(self.objectCenter.numerator - self.interceptPoint.numerator, self.objectCenter.denominator - self.interceptPoint.denominator), 2)

		# draw self and vector line
		super().draw(screen)

	# Updates sheep's position, running from player-dog if within run range
	def update(self, target, worldBounds):
		# calculate distance to target
		self.interceptPoint = self.position - target.position
		distToTarget = self.interceptPoint.length()

		# if target is within minimum range, flee
		if distToTarget < Constants.ATTACK_RANGE:
			self.currSpeed = self.maxSpeed
			self.velocity = self.interceptPoint.normalize()
			super().update(target, worldBounds)
		else:
			self.currSpeed = 0