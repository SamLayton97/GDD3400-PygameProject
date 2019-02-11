import Constants
from Vector import *
from Agent import *
import pygame
from pygame.locals import *
pygame.init()

# Smarter enemy agent with pursue-evade capabilities
class EnemyHunter(Agent):

	# Draws vision-detection line on top of drawing itself and its vector line
	def draw(self, screen, target):
		# for debugging: draw line from enemy's center to where target is moving
		if self.velocity.numerator != 0 or self.velocity.denominator != 0:
			pygame.draw.line(screen, pygame.Color(255, 0, 0), (self.objectCenter.numerator, self.objectCenter.denominator),
					(target.objectCenter.numerator, target.objectCenter.denominator), 3)

		# draw self and vector line
		super().draw(screen)

	# Updates enemy's position, following target object if within attack range
	def update(self, target, worldBounds):
		print(str(self.isIt))
		# if enemy is "it", calculate direction vector towards target
		if self.isIt:
			directionVector = target.position - self.position
		# otherwise, calculate direction vector away from target
		else:
			directionVector = self.position - target.position

		# if target is within attack range, pursue/evade it
		distToTarget = directionVector.length()
		if distToTarget < Constants.ATTACK_RANGE:
			# estimate where target will be after t time
			timeToIntercept = distToTarget / self.speed
			targetTravelDist = timeToIntercept * target.speed
			interceptPoint = target.velocity.scale(targetTravelDist) + target.position

			# move agent in direction of intercept point
			interceptVector = interceptPoint - self.position
			self.velocity = interceptVector.normalize()
			super().update(target, worldBounds)