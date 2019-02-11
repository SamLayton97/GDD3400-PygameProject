from Vector import *
import Constants
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
	collisionBox = pygame.Rect(position.numerator, position.denominator, size, size)
	isIt = True

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
		self.collisionBox = pygame.Rect(self.position.numerator, self.position.denominator, self.size, self.size)

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
		pygame.draw.rect(screen, self.color, self.collisionBox, 0)

		# for debugging: draw line pointing in direction of agent's velocity
		drawVector = self.velocity.scale(self.size)
		pygame.draw.line(screen, pygame.Color(0, 0, 255, 255), (self.objectCenter.numerator, self.objectCenter.denominator), 
				   (self.objectCenter.numerator + drawVector.numerator, self.objectCenter.denominator + drawVector.denominator), 4)

	# Updates agent's position and collision box
	def update(self, target, worldBounds):
		# calculate displacement of agent between frames
		displacementVector = self.velocity.scale(self.speed)

		# clamp displacement vector to within world bounds
		futureX = displacementVector.numerator + self.position.numerator
		futureY = displacementVector.denominator + self.position.denominator
		if (futureX < 0) or (futureX + self.size > worldBounds.numerator):
			displacementVector.numerator = 0
		if (futureY < 0) or (futureY + self.size > worldBounds.denominator):
			displacementVector.denominator = 0

		self.position += displacementVector
		self.objectCenter += displacementVector

		# calculate agent's collision box and detect collision
		self.collisionBox = pygame.Rect(self.position.numerator, self.position.denominator, self.size, self.size)
		self.collisionDetect(target)

	# Detects whether agent has collided with another,
	# and changes ai behaviors accordingly
	def collisionDetect(self, other):
		# if agent collides with another and agent can "tag back"
		if self.collisionBox.colliderect(other.collisionBox) == True:
			# swap seek-flee behaviors
			self.isIt = not self.isIt
			
			# start no-tag-backs timer
			pygame.time.set_timer(USEREVENT, Constants.NO_TAG_BACKS_DURATION)