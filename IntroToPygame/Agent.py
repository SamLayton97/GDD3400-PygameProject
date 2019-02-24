import math
from Vector import *
import Constants
import pygame
from pygame.locals import *
pygame.init()

# Base agent behaviors which all agents inherit from
class Agent:

	# public variables
	position = Vector(0, 0)			# top left corner of object
	objectCenter = Vector(0, 0)		# center of object
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
		self.objectCenter = self.position + self.size.scale(0.5)
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

		# clamp and update agent's position
		displacementVector = self.clampPosition(worldBounds, displacementVector)
		self.movePosition(displacementVector)

		# rotate agent to face velocity vector
		self.faceVelocity()

		# update agent's collision box and detect collision
		#self.updateCollisionBox()
		self.collisionDetect(target)

	# Moves object by displacement vector
	def movePosition(self, displacementVector):
		# update positions of both top-left corner and center of object
		self.position += displacementVector

	# Clamps future position to within world's bounds
	def clampPosition(self, worldBounds, displacementVector):
		# ignoring world bounds, calculate future position of agent after displacement
		futureX = displacementVector.numerator + self.objectCenter.numerator
		futureY = displacementVector.denominator + self.objectCenter.denominator

		# if future position exceeds world bounds, clamp displacement
		if (futureX < self.surface.get_width() / 2) or (futureX > worldBounds.numerator - self.surface.get_width() / 2):
			displacementVector.numerator = 0
		if (futureY < self.surface.get_height() / 2) or (futureY > worldBounds.denominator - self.surface.get_height() / 2):
			displacementVector.denominator = 0

		# return clamped displacement vector
		return displacementVector

	# Rotates agent's surface to face a given angle
	def rotate(self, angle):
		# rotate surface
		self.surface = pygame.transform.rotate(self.originalSurface, angle)

		# update collision box and object's center to match new rotated surface
		self.updateCollisionBox()
		self.objectCenter = self.position + Vector(self.surface.get_width() / 2, self.surface.get_height() / 2)

	# Rotates agent's sprite to face direction of velocity vector
	def faceVelocity(self):
		rotationRadians = math.atan2(-self.velocity.denominator, self.velocity.numerator)
		rotationDegrees = math.degrees(rotationRadians)
		self.rotate(rotationDegrees - 90)

	# Calculates distance to other agent
	def distanceToOther(self, other):
		distanceVector = other.objectCenter - self.objectCenter
		return distanceVector.length()

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
		if Constants.DEBUG_BOUNDING_RECTS:
			pygame.draw.rect(screen, self.color, self.collisionBox, Constants.DEBUG_LINE_WIDTH)

		# for debugging: draw line pointing in direction of agent's velocity
		if Constants.DEBUG_VELOCITY:
			drawVector = self.velocity.scale(30)
			pygame.draw.line(screen, pygame.Color(0, 255, 0, 255), (self.objectCenter.numerator, self.objectCenter.denominator), 
					   (self.objectCenter.numerator + drawVector.numerator, self.objectCenter.denominator + drawVector.denominator), Constants.DEBUG_LINE_WIDTH)