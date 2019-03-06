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
	center = Vector(0, 0)		# center of object
	velocity = Vector(0, 0)
	targetVelocity = Vector(0, 0)	# 'ideal' velocity agent moves towards
	angularSpeed = 0
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
	def __init__(self, surface, position, size, color, maxSpeed, angularSpeed):
		# set variables to appropriate parameters
		self.position = position
		self.size = Vector(size.x, size.y)
		self.maxSpeed = maxSpeed
		self.color = color
		self.originalSurface = surface
		self.surface = surface
		self.angularSpeed = angularSpeed

		# calculate agent's center and collision box
		self.center = self.position + self.size.scale(0.5)
		self.updateCollisionBox()

	# Prints agent's size, position, velocity, and
	# center (in world coordinates) for debugging
	def __str__(self):
		stringSize = "Size: " + str(self.size) + "\n"
		stringPosition = "Position: (" + str(self.position.x) + ", " + str(self.position.y) + ")\n"
		stringVelocity = "Velocity: (" + str(self.velocity.x) + ", " + str(self.velocity.y) + ")\n"
		stringCenter = "Center: (" + str(self.center.x) + ", " + str(self.center.y) + ")\n"
		return stringSize + stringPosition + stringVelocity + stringCenter

	# Updates agent's position and collision box
	def update(self, worldBounds):
		# find inverse of current velocity
		inverseVelocity = self.targetVelocity - self.velocity

		# add scaled inverse velocity to current velocity (basic implementation of angular velocity)
		self.velocity += inverseVelocity.scale(self.angularSpeed)

		# calculate displacement of agent between frames
		displacementVector = self.velocity.scale(self.currSpeed)

		# clamp and update agent's position
		displacementVector = self.clampPosition(worldBounds, displacementVector)
		self.movePosition(displacementVector)

		# rotate agent to face velocity vector
		self.faceVelocity()

	# Moves object by displacement vector
	def movePosition(self, displacementVector):
		# update positions of both top-left corner and center of object
		self.position += displacementVector

	# Clamps future position to within world's bounds
	def clampPosition(self, worldBounds, displacementVector):
		# ignoring world bounds, calculate future position of agent after displacement
		futureX = displacementVector.x + self.center.x
		futureY = displacementVector.y + self.center.y

		# if future position exceeds world bounds, clamp displacement
		if (futureX < self.surface.get_width() / 2) or (futureX > worldBounds.x - self.surface.get_width() / 2):
			displacementVector.x = 0
		if (futureY < self.surface.get_height() / 2) or (futureY > worldBounds.y - self.surface.get_height() / 2):
			displacementVector.y = 0

		# return clamped displacement vector
		return displacementVector

	# Rotates agent's surface to face a given angle
	def rotate(self, angle):
		# rotate surface
		self.surface = pygame.transform.rotate(self.originalSurface, angle)

		# update collision box and object's center to match new rotated surface
		self.updateCollisionBox()
		self.center = self.position + Vector(self.surface.get_width() / 2, self.surface.get_height() / 2)

	# Rotates agent's sprite to face direction of velocity vector
	def faceVelocity(self):
		rotationRadians = math.atan2(-self.velocity.y, self.velocity.x)
		rotationDegrees = math.degrees(rotationRadians)
		self.rotate(rotationDegrees - 90)

	# Calculates distance to other object.
	# Note: Other object must have 'center' variable for this method to function.
	def distanceToOther(self, other):
		distanceVector = other.center - self.center
		return distanceVector.length()

	# Updates collision box according to bounding box of agent's sprite
	def updateCollisionBox(self):
		self.collisionBox = self.surface.get_bounding_rect()
		self.collisionBox = self.collisionBox.move(self.position.x, self.position.y)

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
		screen.blit(self.surface, (self.position.x, self.position.y))

		# for debugging: draw bounding rectangle of agent's sprite surface
		if Constants.DEBUG_BOUNDING_RECTS:
			pygame.draw.rect(screen, self.color, self.collisionBox, Constants.DEBUG_LINE_WIDTH)

		# for debugging: draw line pointing in direction of agent's velocity
		if Constants.DEBUG_VELOCITY:
			drawVector = self.velocity.scale(30)
			pygame.draw.line(screen, pygame.Color(0, 255, 0, 255), (self.center.x, self.center.y), 
					   (self.center.x + drawVector.x, self.center.y + drawVector.y), Constants.DEBUG_LINE_WIDTH)