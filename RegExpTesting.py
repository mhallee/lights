# RegExpTest.py
# Mitchell Hallee
# Takes 3 arguments: the name of the file containing base points
#




"""RegExpTest.py

Converts Rhino-output 3D brick model into LIGGGHTS input form
Usable on rectangular prisms only

Args:
cdBaseName:	  	Name of .cd file containing base bricks
cdBricksName: 	Name of the .cd file containing other bricks
LIGGGHTSName: 	The name of the file to be created with LIGGGHTS input
Length: 	  	Property of the bricks
Width:			Property of the bricks
Height:			Property of the bricks

Raises:

"""

import sys
import re
import math
import numpy

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
		return str(self.x) + ' ' \
		+ str(self.y) + ' ' \
		+ str(self.z)

	def isZero(self):
		"""Returns true iff value in all directions is zero"""
		return self.x==0 and self.y==0 and self.z==0

	def vector(self):
		"""Returns a vector of the coordinate"""
		return [self.x,self.y,self.z]

	def length(self):
		"""Returns the length of the Coordinate treated as a vector"""
		return math.sqrt(self.x**2 + self.y**2 + self.z**2)

class Quaternion:
	"""Represents the angle of a brick in quaternion format:
	where x,y,z define a vector of a brick axes and w is 
	the rotation around that axis"""	
	def __init__(self,w,x,y,z):
		self.w = w
		self.x = x
		self.y = y
		self.z = z

class Brick:
	"""Represents a single brick with 8 vertices"""
	def __init__(self,text,length,width):
		"""	Generates a new brick based on a text list of coordinates
		where each potential vertex is stored on a new line with
		numbers seperated by commas, i.e.
	
		0.0,1.0,2.0:
		3.0,4.0,5.0
		"""
		self.length = length
		self.width = width

		text = re.sub('\t','',text)
		text = re.sub(':', '', text)

		lines = str.splitlines(text)

		self.coordinates = []
		for line in lines:
			coordinates = line.split(',')
			try:
				indexedCoordinate = Coordinate(float(coordinates[0]),
										       float(coordinates[1]),
										       float(coordinates[2]))
			except ValueError:
				raise IOError("The line '" + line + "' appears within a vertex list"
					" but could not be parsed.  Use the form '#,#,#'.")
			if not (indexedCoordinate in self.coordinates):
				self.coordinates.append(indexedCoordinate)

		self.computeQuaternion()

	def __eq__(self, other):
		"""Defines how bricks should be compared. Specifically,
		2 bricks are 'equal' if they exist at the same coordinates
		"""

		# THIS IS NOT WORKING
		print "Call made to __eq__ on Brick class.  This function does not yet work."
		return(self.coordinates.x == other.coordinates.x 
				and self.coordinates.y == other.coordinates.y 
				and self.coordinates.z == other.coordinates.z 
			)

	def __str__(self):
		"""The string representation of a brick is coordinate
		"""
		stringRep = ""
		for coordinate in self.coordinates:
			stringRep = stringRep + (str(coordinate.x) + ','
			+ str(coordinate.y) + ',' 
			+ str(coordinate.z) + '\n')
		return stringRep

	def centroid(self):
		"""Returns a coordinate object describing the brick's centroid"""		
		sumX = 0.0
		sumY = 0.0
		sumZ = 0.0

		#the coordinates of the centroid are the average of the vertices
		for coordinate in self.coordinates:
			sumX += coordinate.x
			sumY += coordinate.y
			sumZ += coordinate.z

		return Coordinate(sumX / len(self.coordinates),
						  sumY / len(self.coordinates),
						  sumZ / len(self.coordinates))

	def computeQuaternion(self):
		THRESHOLD = 0.05 #5% threshold for equality

		print self.length
		print self.width
		#pick a random corner to compare to
		initial = self.coordinates[0]
		axis1 = Coordinate()
		axis2 = Coordinate() #using Coordinates to reflect vectors

		#find two normal vectors to brick
		for indexedPoint in self.coordinates:
			distanceTo = indexedPoint.seperation(initial)
			if (distanceTo < self.length*(1+THRESHOLD) and
				distanceTo > self.length*(1-THRESHOLD)):
				axis1.x = initial.x - indexedPoint.x
				axis1.y = initial.y - indexedPoint.y
				axis1.z = initial.z - indexedPoint.z
			if (distanceTo < self.width*(1+THRESHOLD) and
				distanceTo > self.width*(1-THRESHOLD)):
				axis2.x = initial.x - indexedPoint.x
				axis2.y = initial.y - indexedPoint.y
				axis2.z = initial.z - indexedPoint.z

		if axis1.isZero() or axis2.isZero():
			raise Exception("Error detecting a sides of length " 
				+ str(self.length) + " on brick \n" + str(self) + "\nAborting run.")

		print "axis1: " + str(axis1)
		print "axis2: " + str(axis2)

		#Compute euler angles for vectors
		#check for dividing by zero, which is common bc tan(pi/2) = Inf
		if axis1.x==0:
			yaw = math.pi/2
		else:
			yaw = math.atan(axis1.y / axis1.x)
		if axis1.y==0:
			pitch = math.pi/2
		else:
			pitch = math.atan(axis1.z / math.sqrt(axis1.x**2+axis1.y**2))
		#use relation b/w crossproduct and cosine to get angle between v2 and z axis


		roll  = numpy.linalg.norm(numpy.dot(axis2.vector(),[0,0,1])) \
				/ (axis2.length())

		print "\tyaw: " + str(yaw) + " pitch: " + str(pitch) + " roll: " + str(roll)


#Accept command line arguments
cdBaseName = sys.argv[1]
cdBricksName = sys.argv[2]
LIGGGHTSName = sys.argv[3]
brickLength = float(sys.argv[4])
brickWidth = float(sys.argv[5])
brickHeight = float(sys.argv[6])
baseLength = 0.2480 
baseHeight = 0.0900
baseWidth = 0.0900

#baseHeight = 0.1013
#baseLength = 0.5150
#baseWidth = 0.0900

#Read data from files
cdBaseFile = open(cdBaseName, 'r')
cdBrickFile = open(cdBricksName, 'r')
cdBaseText = cdBaseFile.read()
cdBrickText = cdBrickFile.read()

#Extract vertex points on base
pattern = re.compile("Vertices:\\n(.*?);",re.DOTALL)
baseMatches = re.findall(pattern,cdBaseText)
brickMatches = re.findall(pattern, cdBrickText)


#Based on the .cd file type, every match is a set of vertices for a single
# mesh (brick).  Make these bricks
print "###############################################"
print "Importing Base Unit Geometry"
baseBricks = []
counter = 0
for coordinateText in baseMatches:
	baseBricks.append(Brick(coordinateText,baseLength,baseWidth))
	counter += 1
	print "\t" +str(counter) + " base units imported."
print "\tComplete. Switching to bricks...\n"

print "Importing Brick Geometry"
bricks = []
counter = 0
for coordinateText in brickMatches:
	bricks.append(Brick(coordinateText,brickLength,brickWidth))
	counter += 1
	print "\t" + str(counter) + " bricks imported."
print "###############################################\n"

#Testing centroid units
print "#################TEST CASES####################"
print baseBricks[0]
print "All Coordinates"
print "Centroid:"
print baseBricks[0].centroid()	

