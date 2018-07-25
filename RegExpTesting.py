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

#Check if output file already exists
try:
	f = open(LIGGGHTSName, 'r')
except IOError:
	print LIGGGHTSName + " does not yet exist, so it will be created"
else:
    t = raw_input(LIGGGHTSName + " already exists.  It will be written over.  Press ENTER to continue...")

#Read data from  infiles
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

print "\n###############################################"
print "Exporting Data"
print "###############################################"
outputFile = open(LIGGGHTSName, 'w')

atomID = 1
brickDensity = 2400 #g/cm
baseDensity = 2400 #g/cm

outputFile.write("#Brick/Wall Atoms\n")
for brick in bricks:
	#first line creats the atom at location, "creat_atoms" command
	outputFile.write("create_atoms 1 single " + str(brick.getCentroid().x) + " " 
		+ str(brick.getCentroid().y) + " " + str(brick.getCentroid().z) + "\n")
	#second line defines properties, "set atom" command
	outputFile.write("set atom " + str(atomID) + " type 1 shape " + str(brickLength/2) 
		+ " " + str(brickWidth/2) + " " + str(brickHeight/2) + " blockiness 4.0 4.0 density " 
		+ str(brickDensity) + " quat 1 0 0 0\n")
	#!!!!!!NOTE: ZERO ROTATION HARDCODED IN LINE ABOVE!!!!!!
	print "\texported particle " + str(atomID) + " (brick)"
	atomID += 1

outputFile.write("\n#Base Atoms\n")
for base in baseBricks:
	#first line creats the atom at location, "creat_atoms" command
	outputFile.write("create_atoms 1 single " + str(base.getCentroid().x) + " " 
		+ str(base.getCentroid().y) + " " + str(base.getCentroid().z) + "\n")
	#second line defines properties, "set atom" command
	outputFile.write("set atom " + str(atomID) + " type 1 shape " + str(baseLength/2) 
		+ " " + str(baseWidth/2) + " " + str(baseHeight/2) + " blockiness 4.0 4.0 density " 
		+ str(baseDensity)  + " quat 1 0 0 0\n")
	#!!!!!!NOTE: ZERO ROTATION HARDCODED IN LINE ABOVE!!!!!!
	print "\texported particle " + str(atomID) + " (base)"
	atomID += 1
print "Exporting complete."
