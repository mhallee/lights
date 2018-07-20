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
print "***************************"
print cdBaseText
print "***************************"
cdBrickText = cdBrickFile.read()

#Extract vertex points on base
pattern = re.compile("Vertices:(\r?\n)(.*?);",re.DOTALL)
baseMatches = re.findall(pattern,cdBaseText)
print "base match count" + str(len(baseMatches))
print "basematches [0] type" + str(type(baseMatches[0]))
brickMatches = re.findall(pattern, cdBrickText)
print "brickMatches [0] type" + str(type(brickMatches[0]))

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

