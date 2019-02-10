import math

# Common base for all vectors
class Vector:

	# public variables
	numerator = 0
	denominator = 0

	# constructor
	def __init__(self, numerator, denominator):
		self.numerator = numerator
		self.denominator = denominator

	# converts the vector to a printable string
	def __str__(self):
		return "Vector (" + str(self.numerator) + ", " + str(self.denominator) + ")"

	# adds vector with another
	def __add__(self, other):
		deltaX = self.numerator + other.numerator
		deltaY = self.denominator + other.denominator
		return Vector(deltaX, deltaY)

	# subtracts other vector from this vector
	def __sub__(self, other):
		deltaX = self.numerator - other.numerator
		deltaY = self.denominator - other.numerator
		return Vector(deltaX, deltaY)

	# calculates dot product of this and another vector
	def dot(self, other):
		return (self.numerator * other.numerator) + (self.denominator * other.denominator)

	# scales this vector by a value
	def scale(self, scalar):
		return Vector(self.numerator * scalar, self.denominator * scalar)

	# returns length of the vector
	def length(self):
		return math.sqrt(self.numerator ** 2 + self.denominator ** 2)

	# returns a normalized vector with same direction as this one
	def normalize(self):
		vectorLength = self.length()
		return Vector(self.numerator / vectorLength, self.denominator / vectorLength)