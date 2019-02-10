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

	# draws enemy at a given position on the screen
	def draw(self, screen):
		# draw self
		pygame.draw.rect(screen, pygame.Color(255, 0, 0, 255), pygame.Rect(self.position.numerator, self.position.denominator, self.size, self.size), 0)

		# for debugging: draw line pointing in direction of enemy's velocity
		drawVector = self.velocity.normalize()
		drawVector = drawVector.scale(30)
		pygame.draw.line(screen, pygame.Color(0, 255, 0, 255), (self.position.numerator + (self.size / 2), self.position.denominator + (self.size / 2)), 
				   (self.position.numerator + (self.size / 2) + drawVector.numerator, self.position.denominator + (self.size / 2) + drawVector.denominator), 4)

	# updates enemy's position based on its normalized velocity
	def update(self):
		normVel = self.velocity.normalize()
		self.position += normVel
