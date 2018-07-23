import sys
import re
import math
import numpy
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from Coordinate import Coordinate
from Quaternion import Quaternion

class Brick:
	"""Represents a single brick with 8 vertices"""
	def __init__(self,text,length,width,height):
		"""	Generates a new brick based on a text list of coordinates
		where each potential vertex is stored on a new line with
		numbers seperated by commas, i.e.
	
		0.0,1.0,2.0:
		3.0,4.0,5.0
		"""
		self.length = length
		self.width  = width
		self.height = height

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
		THRESHOLD = 0.001 #0.1% threshold for equality

		print "\t\tLength: " + str(self.length)
		print "\t\tHeight: " + str(self.height)
		#pick a random corner to compare to
		initial = self.coordinates[0]
		self.axis1 = Coordinate()
		self.axis2 = Coordinate() #using Coordinates to reflect vectors

		#find two normal vectors (ie edges) to brick
		for indexedPoint in self.coordinates:
			distanceTo = indexedPoint.seperation(initial)
			if (distanceTo < self.length*(1+THRESHOLD) and
				distanceTo > self.length*(1-THRESHOLD)):
				self.axis1.x = initial.x - indexedPoint.x
				self.axis1.y = initial.y - indexedPoint.y
				self.axis1.z = initial.z - indexedPoint.z
				print "\t\tFound axis1:  Initial Point " \
					+ str(initial) + ", Match Point " + str(indexedPoint)
			if (distanceTo < self.height*(1+THRESHOLD) and
				distanceTo > self.height*(1-THRESHOLD)):
				self.axis2.x = initial.x - indexedPoint.x
				self.axis2.y = initial.y - indexedPoint.y
				self.axis2.z = initial.z - indexedPoint.z
				print "\t\tFound axis2:  Initial Point " + str(initial) \
					+ ", Match Point " + str(indexedPoint)

		if self.axis1.isZero() or self.axis2.isZero():
			raise Exception("Error detecting a sides of length " 
				+ str(self.length) + " on brick \n" + str(self) + "\nAborting run.")

		print "\t\taxis1: " + str(self.axis1)
		print "\t\taxis2: " + str(self.axis2)

		#COMPUTE EULER ANGLES OF BRICK ROTATION FROM VECTOR AXES
		#check for dividing by zero, which is common bc tan(pi/2) = Inf
		if self.axis1.x==0:
			self.heading = math.pi/2
		else:
			self.heading = math.atan(self.axis1.y / self.axis1.x)

		axis1ProjectionXY = math.sqrt(self.axis1.x**2+self.axis1.y**2)
		if axis1ProjectionXY==0:
			self.attitude = 0
		else:
			self.attitude = math.atan(self.axis1.z / axis1ProjectionXY)
		
		#use relation b/w crossproduct and cosine to get angle between v2 and z axis
		cosRollAngle  = numpy.linalg.norm(numpy.dot(self.axis2.vector(),[0,0,1])) \
				/ self.axis2.length()
		self.bank = math.acos(cosRollAngle)

		#DISPLAY ANGLES IN DEGREES (this can be removed)
		print "\t\theading: " + str(self.heading) + " attitude: " + str(self.attitude) \
			+ " bank: " + str(self.bank)
		headingDeg = self.heading * 360 / (2 * math.pi)
		attitudeDeg = self.attitude * 360 / (2 * math.pi)
		bankDeg = self.bank * 360 / (2 * math.pi)
		print "\t\theading (Degrees): " + str(headingDeg) + " attitude (Degrees): " \
			+ str(attitudeDeg) + " bank (Degrees): " + str(bankDeg)

		#CONVERT FROM EULER TO QUATERNION
		#Using code from http://www.euclideanspace.com/maths/geometry/rotations/  .....
		#(continuing link from above)  ...  conversions/eulerToQuaternion/index.htm
		c1 = math.cos(self.heading / 2)
		s1 = math.sin(self.heading / 2)
		c2 = math.cos(self.attitude / 2)
		s2 = math.sin(self.attitude / 2)
		c3 = math.cos(self.bank / 2)
		s3 = math.sin(self.bank / 2)
		c1c2 = c1*c2
		s1s2 = s1*s2
		self.qw =c1c2*c3 - s1s2*s3
		self.qx =c1c2*s3 + s1s2*c3
		self.qy =s1*c2*c3 + c1*s2*s3
		self.qz =c1*s2*c3 - s1*c2*s3
		print "\t\tQUATERNION: w " + str(self.qw) + "; x " + str(self.qx) \
			+ "; y " + str(self.qy) + "; z " + str(self.qz)

		self.plot() #TAKE THIS OUT

	def __str__(self):
		"""The string representation of a brick is coordinate
		"""
		stringRep = ""
		for coordinate in self.coordinates:
			stringRep = stringRep + (str(coordinate.x) + ','
			+ str(coordinate.y) + ',' 
			+ str(coordinate.z) + '\n')	
		return stringRep

	def plot(self):
		fig = plt.figure()
		ax = fig.add_subplot(111,projection='3d')

		#plot points
		X = []
		Y = []
		Z = []
		for coordinate in self.coordinates:
			X.append(coordinate.x)
			Y.append(coordinate.y)
			Z.append(coordinate.z)
		ax.scatter(X, Y, Z, c='r',marker='o')

		#plot brick axes
		ax.plot([self.coordinates[0].x,self.coordinates[0].x - self.axis1.x],
				[self.coordinates[0].y,self.coordinates[0].y - self.axis1.y],
				[self.coordinates[0].z,self.coordinates[0].z - self.axis1.z],'b')
		ax.plot([self.coordinates[0].x,self.coordinates[0].x - self.axis2.x],
				[self.coordinates[0].y,self.coordinates[0].y - self.axis2.y],
				[self.coordinates[0].z,self.coordinates[0].z - self.axis2.z],'g')

		#add label
		ax.set_xlabel('x axis')
		ax.set_ylabel('y axis')
		ax.set_zlabel('z axis')

		
		plt.show()

