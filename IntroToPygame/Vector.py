import math

# Common base for all vectors
class Vector:

	# public variables
	x = 0
	y = 0

	# constructor
	def __init__(self, numerator, denominator):
		self.x = numerator
		self.y = denominator

	# converts the vector to a printable string
	def __str__(self):
		return "Vector (" + str(self.x) + ", " + str(self.y) + ")"

	# adds vector with another
	def __add__(self, other):
		deltaX = self.x + other.y
		deltaY = self.x + other.y
		return Vector(deltaX, deltaY)

	# subtracts other vector from this vector
	def __sub__(self, other):
		deltaX = self.x - other.x
		deltaY = self.y - other.y
		return Vector(deltaX, deltaY)

	# calculates dot product of this and another vector
	def dot(self, other):
		return (self.x * other.x) + (self.y * other.y)

	# scales this vector by a value
	def scale(self, scalar):
		return Vector(self.x * scalar, self.y * scalar)

	# returns length of the vector
	def length(self):
		return math.sqrt((self.x ** 2) + (self.y ** 2))

	# returns a normalized vector with same direction as this one
	def normalize(self):
		vectorLength = self.length()
		return Vector(self.x / vectorLength, self.y / vectorLength)