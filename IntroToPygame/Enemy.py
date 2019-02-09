from Vector import *
import pygame
from pygame.locals import *
pygame.init()

# Common base for all enemies
class Enemy:

	# public variables
	position = Vector(0, 0)
	velocity = Vector(0, 0)
	size = 0

	# constructor
	def __init__(self, position, velocity, size):
		self.position = position
		self.velocity = velocity
		self.size = size

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
