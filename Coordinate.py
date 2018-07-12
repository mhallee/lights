import math

class Coordinate:
	"""Holds x, y, z coordinates"""

	def __init__(self, xIn=0.0, yIn=0.0, zIn=0.0):
		self.x = xIn
		self.y = yIn
		self.z = zIn

	def seperation(self, other):
		"""Return true iff distance between self and other is within
		tolerance of the threshold"""
		return math.sqrt((self.x - other.x)**2 \
						+ (self.y - other.y)**2 \
						+ (self.z - other.z)**2)
		
	def __eq__(self, other):
		return (self.x == other.x 
			and self.y == other.y
			and self.z == other.z)

	def __str__(self):
		"""The string representation of a coordinate is x y z, ie
		1.0 2.0 3.0
		"""
		return '(' + str(self.x) + ', ' \
		+ str(self.y) + ', ' \
		+ str(self.z) + ')'

	def isZero(self):
		"""Returns true iff value in all directions is zero"""
		return self.x==0 and self.y==0 and self.z==0

	def vector(self):
		"""Returns a vector of the coordinate"""
		return [self.x,self.y,self.z]

	def length(self):
		"""Returns the length of the Coordinate treated as a vector"""
		return math.sqrt(self.x**2 + self.y**2 + self.z**2)