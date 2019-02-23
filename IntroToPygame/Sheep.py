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
	neighbors = []
	herd = []

	# Constructor:
	# Initialize all base Agent variables and then
	# set sheep to start with random velocity between -.5 and 5
	def __init__(self, position, size, maxSpeed, color, surface):
		# randomize sheep's starting velocity so that at least one component isn't 0
		velocityX = 0
		velocityY = 0
		while velocityX == 0 and velocityY == 0:
			velocityX = random.uniform(-.5, .5)
			velocityY = random.uniform(-.5, .5)
		randVector = Vector(velocityX, velocityY)
		self.velocity = randVector.normalize()
		
		# initialize base agent variables
		super().__init__(position, size, maxSpeed, color, surface)

		# rotate sheep to face randomized starting velocity and update collision box
		self.faceVelocity()

	# Draws vision-detection line on top of drawing itself and its vector line
	def draw(self, screen, dog):
		# for debugging: draw line from enemy's center to target's center if moving
		if self.currSpeed != 0:
			pygame.draw.line(screen, pygame.Color(255, 0, 0), (self.objectCenter.numerator, self.objectCenter.denominator),
					(dog.objectCenter.numerator, dog.objectCenter.denominator), 2)

		# for debugging: draw line to each sheep in list of neighbors
		for sheep in self.neighbors:
			pygame.draw.line(screen, pygame.Color(0, 0, 255), (self.objectCenter.numerator, self.objectCenter.denominator),
					(sheep.objectCenter.numerator, sheep.objectCenter.denominator), 2)

		# draw self and vector line
		super().draw(screen)

	# Updates sheep's position, running from player-dog if within run range
	def update(self, dog, worldBounds):
		# find neighbors within herd
		self.findNeighbors(self.herd)

		# calculate composite forces on sheep
		alignmentInfluence = self.calculateAlignment()
		cohesionInfluence = self.calculateCohesion()
		separationInfluence = self.calculateSeparation()
		dogInfluence = self.calculateDogInfluence(dog)
		forces = (alignmentInfluence.scale(Constants.SHEEP_ALIGNMENT_WEIGHT) + cohesionInfluence.scale(Constants.SHEEP_COHESION_WEIGHT) + 
			dogInfluence.scale(Constants.SHEEP_DOG_INFLUENCE_WEIGHT)) + separationInfluence.scale(Constants.SHEEP_SEPERATION_WEIGHT)

		# if external forces influence velocity of sheep
		if not (forces.numerator == 0 and forces.denominator == 0):
			# increase sheep's speed
			self.currSpeed = self.maxSpeed

			# update velocity to be normalized composite forces vector
			self.velocity = forces.normalize()
		# otherwise, freeze sheep's movement by locking speed
		else:
			self.currSpeed = 0

		super().update(dog, worldBounds)

	# Calculates influence force of dog's proximity on sheep's velocity
	def calculateDogInfluence(self, dog):
		dogInfluence = Vector(0, 0)

		# if the dog is within attack range
		if self.distanceToOther(dog) < Constants.ATTACK_RANGE:
			# calculate vector away from dog
			dogInfluence = self.objectCenter - dog.objectCenter
			dogInfluence.normalize()

		# return normalized dog-influence vector
		return dogInfluence

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
			cohesion += currSheep.position - self.position

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
			separation += currSheep.position - self.position

		# if number of neighbors wasn't 0, calculate and normalize vector away from neighborhood center of mass
		if neighborCount > 0:
			separation = separation.scale(-1 / neighborCount)
			separation = separation.normalize()

		# return separation influence vector
		return separation