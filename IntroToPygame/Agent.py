import math
from Vector import *
import Constants
import pygame
from pygame.locals import *
pygame.init()

# Base agent behaviors which all agents inherit from
class Agent:

	# public variables
	position = Vector(0, 0)
	objectCenter = Vector(0, 0)
	velocity = Vector(0, 0)
	size = Vector(0, 0)
	currSpeed = 0
	maxSpeed = 0
	color = (0, 0, 0)
	originalSurface = None
	surface = None
	collisionBox = None
	isIt = True
	canTagBack = True

	# Constructor:
	# Initializes agent's values to corresponding parameters and 
	# initializes their velocity and center from that.
	def __init__(self, position, size, maxSpeed, color, surface):
		# set variables to appropriate parameters
		self.position = position
		self.size = Vector(size.numerator, size.denominator)
		self.maxSpeed = maxSpeed
		self.color = color
		self.originalSurface = surface
		self.surface = surface

		# calculate agent's center and collision box
		self.objectCenter = Vector(position.numerator + (size.numerator / 2), position.denominator + (size.denominator / 2))
		self.updateCollisionBox()

	# Prints agent's size, position, velocity, and
	# center (in world coordinates) for debugging
	def __str__(self):
		stringSize = "Size: " + str(self.size) + "\n"
		stringPosition = "Position: (" + str(self.position.numerator) + ", " + str(self.position.denominator) + ")\n"
		stringVelocity = "Velocity: (" + str(self.velocity.numerator) + ", " + str(self.velocity.denominator) + ")\n"
		stringCenter = "Center: (" + str(self.objectCenter.numerator) + ", " + str(self.objectCenter.denominator) + ")\n"
		return stringSize + stringPosition + stringVelocity + stringCenter

	# Updates agent's position and collision box
	def update(self, target, worldBounds):
		# calculate displacement of agent between frames
		displacementVector = self.velocity.scale(self.currSpeed)

		# clamp displacement vector to within world bounds
		futureX = displacementVector.numerator + self.position.numerator
		futureY = displacementVector.denominator + self.position.denominator
		if (futureX < 0) or (futureX + self.size.numerator > worldBounds.numerator):
			displacementVector.numerator = 0
		if (futureY < 0) or (futureY + self.size.denominator > worldBounds.denominator):
			displacementVector.denominator = 0

		# update agent's position
		self.movePosition(displacementVector)

		# rotate agent's sprite to face direction of velocity
		rotationRadians = math.atan2(-self.velocity.denominator, self.velocity.numerator)
		rotationDegrees = math.degrees(rotationRadians)
		self.rotate(rotationDegrees - 90)

		# update agent's collision box and detect collision
		self.updateCollisionBox()
		self.collisionDetect(target)

	# Moves object by displacement vector
	def movePosition(self, displacementVector):
		self.position += displacementVector
		self.objectCenter += displacementVector

	# Rotates agent's sprite to face a given angle
	def rotate(self, angle):
		self.surface = pygame.transform.rotate(self.originalSurface, angle)

	# Updates collision box according to bounding box of agent's sprite
	def updateCollisionBox(self):
		self.collisionBox = self.surface.get_bounding_rect()
		self.collisionBox = self.collisionBox.move(self.position.numerator, self.position.denominator)

	# Detects whether agent has collided with another,
	# and changes ai behaviors accordingly
	def collisionDetect(self, other):
		# if agent collides with another and agent can "tag back"
		if self.collisionBox.colliderect(other.collisionBox) == True and self.canTagBack:
			# swap seek-flee behaviors
			self.isIt = not self.isIt
			
			# start no-tag-backs timer
			pygame.time.set_timer(USEREVENT, Constants.NO_TAG_BACKS_DURATION)
			self.canTagBack = False

	# Draws agents and its velocity at a given position on screen
	def draw(self, screen):
		# draw agent's sprite
		screen.blit(self.surface, (self.position.numerator, self.position.denominator))

		# for debugging: draw bounding rectangle of agent's sprite surface
		pygame.draw.rect(screen, self.color, self.collisionBox, 2)

		# for debugging: draw line pointing in direction of agent's velocity
		drawVector = self.velocity.scale(self.size.numerator)
		pygame.draw.line(screen, pygame.Color(0, 0, 255, 255), (self.objectCenter.numerator, self.objectCenter.denominator), 
				   (self.objectCenter.numerator + drawVector.numerator, self.objectCenter.denominator + drawVector.denominator), 4)