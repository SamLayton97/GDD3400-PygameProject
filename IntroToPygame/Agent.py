from Vector import *
import pygame
from pygame.locals import *
pygame.init()

# Base agent behaviors which all agents inherit from
class Agent:

	# public variables
	position = Vector(0, 0)
	velocity = Vector(0, 0)
	size = 0
	speed = 0
	objectCenter = Vector(0, 0)
	color = (0, 0, 0)

	# Constructor:
	# Initializes agent's starting position,
	# size, speed, and color according to parameters, and 
	# initializes their velocity and center from that.
	def __init__(self, position, size, speed, color):
		# set position, size and speed to parameters
		self.position = position
		self.size = size
		self.speed = speed
		self.color = color

		# initialize speed and calculate agent's center in world coordinates
		self.velocity = Vector(0, 0)
		self.objectCenter = Vector(position.numerator + (size / 2), position.denominator + (size / 2))

	# Prints agent's size, position, velocity, and
	# center (in world coordinates) for debugging
	def __str__(self):
		stringSize = "Size: " + str(self.size) + "\n"
		stringPosition = "Position: (" + str(self.position.numerator) + ", " + str(self.position.denominator) + ")\n"
		stringVelocity = "Velocity: (" + str(self.velocity.numerator) + ", " + str(self.velocity.denominator) + ")\n"
		stringCenter = "Center: (" + str(self.objectCenter.numerator) + ", " + str(self.objectCenter.denominator) + ")\n"
		return stringSize + stringPosition + stringVelocity + stringCenter

	# Draws agents and its velocity at a given position on screen
	def draw(self, screen):
		# draw self
		pygame.draw.rect(screen, self.color, pygame.Rect(self.position.numerator, self.position.denominator, self.size, self.size), 0)

		# for debugging: draw line pointing in direction of agent's velocity
		drawVector = self.velocity.scale(self.size)
		pygame.draw.line(screen, pygame.Color(0, 0, 255, 255), (self.objectCenter.numerator, self.objectCenter.denominator), 
				   (self.objectCenter.numerator + drawVector.numerator, self.objectCenter.denominator + drawVector.denominator), 4)