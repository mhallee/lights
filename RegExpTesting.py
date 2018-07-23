"""RegExpTest.py

Converts Rhino-output 3D brick model into LIGGGHTS input form
Usable on rectangular prisms only

Length, Width, Height will correspond to x,y,z dimensions of the brick


Args:
cdBaseName:	  	Name of .cd file containing base bricks
cdBricksName: 	Name of the .cd file containing other bricks
LIGGGHTSName: 	The name of the file to be created with LIGGGHTS input
baseLength: 	Dimension of base units' longest edge
baseWidth:		Dimension of base units' second longest edge
baseHeight:		Dimension of base units' shortest edge
brickLength: 	Dimension of bricks' longest edge
brickWidth:		Dimension of bricks' second longest edge
brickHeight:	Dimension of bricks' shortest edge

A note about length/width/height and computing angles:

Raises:

"""

import sys
import re
import math
import numpy

from Brick import Brick

#Accept command line arguments
cdBaseName   = sys.argv[1]
cdBricksName = sys.argv[2]
LIGGGHTSName = sys.argv[3]
baseLength  = float(sys.argv[4])
baseWidth   = float(sys.argv[5])
baseHeight  = float(sys.argv[6])
brickLength = float(sys.argv[7])
brickWidth  = float(sys.argv[8])
brickHeight = float(sys.argv[9])

#Read data from files
cdBaseFile = open(cdBaseName, 'r')
cdBrickFile = open(cdBricksName, 'r')
cdBaseText = cdBaseFile.read()
cdBrickText = cdBrickFile.read()

#Extract vertex points on base
pattern = re.compile("Vertices:\r?\n(.*?);",re.DOTALL)
baseMatches = re.findall(pattern,cdBaseText)
brickMatches = re.findall(pattern, cdBrickText)

#Based on the .cd file type, every match is a set of vertices for a single
# mesh (brick).  Make these bricks
print "###############################################"
print "Importing Data"
print "###############################################"
print "Importing Base Unit Geometry"
baseBricks = []
counter = 0
for coordinateText in baseMatches:
	print "coordinate text type" + str(type(coordinateText))
	baseBricks.append(Brick(coordinateText,baseLength,baseWidth,baseHeight))
	counter += 1
	print "\t" +str(counter) + " base units imported."
print "\tComplete. Switching to bricks...\n"

print "Importing Brick Geometry"
bricks = []
counter = 0
for coordinateText in brickMatches:
	bricks.append(Brick(coordinateText,brickLength,brickWidth,brickHeight))
	counter += 1
	print "\t" + str(counter) + " bricks imported."
print "###############################################\n"

#Testing centroid units
print "#################TEST CASES####################"
print baseBricks[0]
print "All Coordinates"
print "Centroid:"
print baseBricks[0].centroid()

