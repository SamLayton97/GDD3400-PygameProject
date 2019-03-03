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
	fleePoint = Vector(0, 0)
	dogPosition = Vector(0, 0)
	closestBoundPoint = Vector(0, 0)
	neighbors = []
	herd = []

	# Constructor:
	# Initialize all base Agent variables and then
	# set sheep to start with random velocity between -.5 and 5
	def __init__(self, surface, position, size, color, maxSpeed, angularSpeed):
		# randomize sheep's starting velocity so that at least one component isn't 0
		velocityX = 0
		velocityY = 0
		while velocityX == 0 and velocityY == 0:
			velocityX = random.uniform(-.5, .5)
			velocityY = random.uniform(-.5, .5)
		randVector = Vector(velocityX, velocityY)
		self.velocity = randVector.normalize()
		
		# initialize base agent variables
		super().__init__(surface, position, size, color, maxSpeed, angularSpeed)

		# rotate sheep to face randomized starting velocity and update collision box
		self.faceVelocity()

	# Draws vision-detection line on top of drawing itself and its vector line
	def draw(self, screen):
		# for debugging: draw line from sheep to dog's center if distance between them is less than attack range
		if Constants.DEBUG_DOG_INFLUENCE:
			distanceVector = self.objectCenter - self.dogPosition
			if distanceVector.length() < Constants.MIN_ATTACK_DIST:
				pygame.draw.line(screen, pygame.Color(255, 0, 0), (self.objectCenter.x, self.objectCenter.y),
						(self.dogPosition.x, self.dogPosition.y), Constants.DEBUG_LINE_WIDTH)

		# for debugging: draw line to each sheep in list of neighbors
		if Constants.DEBUG_NEIGHBORS:
			for sheep in self.neighbors:
				pygame.draw.line(screen, pygame.Color(0, 0, 255), (self.objectCenter.x, self.objectCenter.y),
						(sheep.objectCenter.x, sheep.objectCenter.y), Constants.DEBUG_LINE_WIDTH)

		# for debugging: draw line to closest boundary point (only if agent is close enough for bounds to influence agent's velocity)
		if Constants.DEBUG_BOUNDARIES and not (self.closestBoundPoint.x == self.objectCenter.x and self.closestBoundPoint.y == self.objectCenter.y):
			pygame.draw.line(screen, pygame.Color(255, 0, 255), (self.objectCenter.x, self.objectCenter.y),
					(self.closestBoundPoint.x, self.closestBoundPoint.y), Constants.DEBUG_LINE_WIDTH)

		# draw self and vector line
		super().draw(screen)

	# Updates sheep's position, running from player-dog if within run range
	def update(self, worldBounds, graph, dog, herd, gates):
		# find neighbors within herd
		self.findNeighbors(self.herd)

		# update position of dog
		self.dogPosition = dog.objectCenter

		# calculate each force affecting sheep
		alignmentInfluence = self.calculateAlignment()
		cohesionInfluence = self.calculateCohesion()
		separationInfluence = self.calculateSeparation()
		dogInfluence = self.calculateDogInfluence(dog)
		boundsInfluence = self.calculateBoundaryInfluence(worldBounds)

		# combine individual forces into composite force
		forces = (alignmentInfluence.scale(Constants.SHEEP_ALIGNMENT_WEIGHT) + cohesionInfluence.scale(Constants.SHEEP_COHESION_WEIGHT) + 
			dogInfluence.scale(Constants.SHEEP_DOG_INFLUENCE_WEIGHT)) + separationInfluence.scale(Constants.SHEEP_SEPARATION_WEIGHT) + boundsInfluence.scale(Constants.SHEEP_BOUNDARY_INFLUENCE_WEIGHT)

		# if external forces influence velocity of sheep
		if not (forces.x == 0 and forces.y == 0):
			# increase sheep's speed
			self.currSpeed = self.maxSpeed

			# update velocity to be normalized composite forces vector
			self.velocity = forces.normalize()
		# otherwise, freeze sheep's movement by locking speed
		else:
			self.currSpeed = 0

		super().update(worldBounds)

	# Calculates influence force of dog's proximity on sheep's velocity
	# and returns velocity moving away from the dog
	def calculateDogInfluence(self, dog):
		# define vector to hold velocity away from dog
		dogInfluence = Vector(0, 0)

		# if the dog is within attack range
		if self.distanceToOther(dog) < Constants.MIN_ATTACK_DIST:
			# calculate vector away from dog
			dogInfluence = self.objectCenter - dog.objectCenter
			dogInfluence.normalize()

		# return normalized dog-influence vector
		return dogInfluence

	# Calculates influence force of world bounds on sheep's velocity,
	# pushing the agent away from screen edges and corners
	def calculateBoundaryInfluence(self, worldBounds):
		# define vector to hold velocity away from screen bounds
		boundsInfluence = Vector(0, 0)

		# if sheep nears left/right boundaries, calculate vector directly away from those boundaries
		if self.objectCenter.x < Constants.SHEEP_BOUNDARY_RADIUS:
			boundsInfluence.x += self.objectCenter.x
		elif self.objectCenter.x > worldBounds.x - Constants.SHEEP_BOUNDARY_RADIUS:
			boundsInfluence.x += self.objectCenter.x - worldBounds.x

		# if sheep nears top/bottom boundardies, calculate vector directly away from those boundaries
		if (self.objectCenter.y < Constants.SHEEP_BOUNDARY_RADIUS):
			boundsInfluence.y += self.objectCenter.y
		elif self.objectCenter.y > worldBounds.y - Constants.SHEEP_BOUNDARY_RADIUS:
			boundsInfluence.y += self.objectCenter.y - worldBounds.y

		# update agent's closest bound point
		self.closestBoundPoint = self.objectCenter - boundsInfluence

		# if bounds influence is not zero vector, normalize it
		if not (boundsInfluence.x == 0 and boundsInfluence.x == 0):
			boundsInfluence = boundsInfluence.normalize()

		# return bounds influence
		return boundsInfluence

	# from a list of sheep, determine which ones are neighbors
	def findNeighbors(self, herd):
		# clear list of neighbors
		self.neighbors.clear()

		# iterate over every sheep in herd
		for sheep in herd:
			# if current sheep is not this sheep
			# and distance to current sheep is within neighbor radius
			if sheep != self and self.distanceToOther(sheep) < Constants.SHEEP_NEIGHBOR_RADIUS:
				# add current sheep to list of neighbors
				self.neighbors.append(sheep)

	# Calculates alignment influence where this sheep wants to move in same direction as its neighbors.
	# Note: First aspect of flocking behavior.
	def calculateAlignment(self):
		# define vector to keep track of neighbor velocities
		alignment = Vector(0, 0)
		neighborCount = len(self.neighbors)

		# iterate over each sheep and add its velocity to composite alignment velocity
		for currSheep in self.neighbors:
			alignment += currSheep.velocity

		# if the number of neighbors wasn't 0, normalize alignment vector
		if neighborCount > 0:
			alignment = alignment.scale(1 / neighborCount)
			alignment = alignment.normalize()

		# return alignment influence vector
		return alignment

	# Calculates cohesion influence where this sheep likes to cluster with other sheep.
	# Note: Second aspect of flocking behavior.
	def calculateCohesion(self):
		# define vector to keep track of neighbor positions
		cohesion = Vector(0, 0)
		neighborCount = len(self.neighbors)

		# iterate over each sheep and add distance from self to it to composite cohesion vector
		for currSheep in self.neighbors:
			cohesion += currSheep.objectCenter - self.objectCenter

		# if number of neighbors wasn't 0, calculate and normalize vector to neighborhood center of mass
		if neighborCount > 0:
			cohesion = cohesion.scale(1 / neighborCount)
			cohesion = cohesion.normalize()

		# return cohesion influence vector
		return cohesion

	# Calculates separation influence where this sheep likes to stay a sheep's length away from its neighbors.
	# Note: Third aspect of flocking behavior.
	def calculateSeparation(self):
		# define vector to track neighbors' positions
		separation = Vector(0, 0)
		neighborCount = len(self.neighbors)

		# iterate over each neighboring sheep and add distance from self to it to composite separation vector
		for currSheep in self.neighbors:
			separation += currSheep.objectCenter - self.objectCenter

		# if number of neighbors wasn't 0, calculate and normalize vector away from neighborhood center of mass
		if neighborCount > 0:
			separation = separation.scale(-1 / neighborCount)
			separation = separation.normalize()

		# return separation influence vector
		return separation