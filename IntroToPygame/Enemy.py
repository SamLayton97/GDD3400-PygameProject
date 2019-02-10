import Constants
from Vector import *
import pygame
from pygame.locals import *
pygame.init()

# Basic enemy agent with seek-flee capabilities
class Enemy:

	# public variables
	position = Vector(0, 0)
	velocity = Vector(0, 0)
	size = 0
	speed = 0
	objectCenter = Vector(0, 0)
	
	# Constructor:
	# Initializes agent's starting position,
    # size, and speed according to parameters, and 
    # initializes their velocity and center from that.
	def __init__(self, position, size, speed):
		# set position, size, and speed to parameters
		self.position = position
		self.size = size
		self.speed = speed

		# initialize velocity to 0 and calculate center of agent in world coordinates
		self.velocity = Vector(0, 0)
		self.objectCenter = Vector(position.numerator + (size / 2), position.denominator + (size / 2))

	# Prints agent's size, position, velocity, and
	# center (in world coordinates) for debugging
	def __str__(self):
		print("Size: " + str(self.size))
		print("Position: (" + str(self.position.numerator) + ", " + str(self.position.denominator) + ")\n")
		print("Velocity: (" + str(self.velocity.numerator) + ", " + str(self.velocity.denominator) + ")\n")
		print("Center: (" + str(self.objectCenter.numerator) + ", " + str(self.objectCenter.denominator) + ")\n")

	# Draws enemy and its velocity at a given position on the screen
	def draw(self, screen):
		# draw self
		pygame.draw.rect(screen, pygame.Color(255, 0, 0, 255), pygame.Rect(self.position.numerator, self.position.denominator, self.size, self.size), 0)

		# for debugging: draw line pointing in direction of enemy's velocity
		drawVector = self.velocity.scale(self.size)
		pygame.draw.line(screen, pygame.Color(0, 0, 255, 255), (self.objectCenter.numerator, self.objectCenter.denominator), 
				    (self.objectCenter.numerator + drawVector.numerator, self.objectCenter.denominator + drawVector.denominator), 4)

	# Updates enemy's position, following target object if within attack range
	def update(self, target):
		# calculate direction and distance to target
		directionToTarget = target.position - self.position
		distToTarget = directionToTarget.length()

		# if target is within attack range, follow it
		if distToTarget < Constants.ATTACK_RANGE:
			# apply normalized movement vector, scaled to  speed, to current position
			self.velocity = directionToTarget.normalize()
			self.position += self.velocity.scale(self.speed)
			self.objectCenter += self.velocity.scale(self.speed)