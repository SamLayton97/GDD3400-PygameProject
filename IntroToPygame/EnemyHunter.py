import Constants
from Vector import *
from Agent import *
import pygame
from pygame.locals import *
pygame.init()

# Smarter enemy agent with pursue-evade capabilities
class EnemyHunter(Agent):

	# public variables
	interceptPoint = Vector(0, 0)

	# Draws vision-detection line on top of drawing itself and its vector line
	def draw(self, screen, target):
		# for debugging: draw line from enemy's center to where target is moving
		if self.velocity.numerator != 0 or self.velocity.denominator != 0:
			pygame.draw.line(screen, pygame.Color(255, 0, 0), (self.objectCenter.numerator, self.objectCenter.denominator),
					(self.interceptPoint.numerator, self.interceptPoint.denominator), 3)

		# draw self and vector line
		super().draw(screen)

	# Updates enemy's position, following target object if within attack range
	def update(self, target, worldBounds):
		print(str(self.isIt))
		# calculate distance to target
		directionVector = target.position - self.position
		distToTarget = directionVector.length()

		# if target is within attack range, pursue/evade it
		if distToTarget < Constants.ATTACK_RANGE:
			# estimate where target will be after t time
			timeToIntercept = distToTarget / self.speed
			targetTravelDist = timeToIntercept * target.speed
			self.interceptPoint = target.velocity.scale(targetTravelDist) + target.objectCenter

			# move agent in direction of / away from intercept point
			if self.isIt:
				interceptVector = self.interceptPoint - self.position
			else: 
				interceptVector = self.position - self.interceptPoint
			self.velocity = interceptVector.normalize()
			super().update(target, worldBounds)