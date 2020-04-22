import os
import sys
sys.path.append('/Applications/RoboFont.app/Contents/Resources/lib/python3.6/')
from fontParts.world import CurrentFont, OpenFont
import math
import rbWindow.editWindow as ew
from jsonConverter.makeJsonFile import *
from testCode.initialization import *



BroadNibBackgroundDefaultKey = "com.asaumierdemers.BroadNibBackground"

testPath = "/Users/sslab/Desktop/groupTest.ufo"
testFile = OpenFont(testPath,showInterface = False)





# c = g.contours[0]

# standardMatrix = rbFontG.tools.tMatrix.PhaseTool.Matrix(c,3,3)

# compareController = rbFontG.tools.tMatrix.groupTestController.groupTestController(standardMatrix,0)

# groupList = []


# for idx, comGlyph in enumerate(testFile):
BroadNibBackgroundDefaultKey = "com.asaumierdemers.BroadNibBackground"
testPath = "/Users/sslab/Desktop/groupTest.ufo"
testFile = OpenFont(testPath,showInterface = False)
groupDict = None
jsonFileName = StartProgram(testPath,testFile)
menuWindow = ew.EditGroupMenu(CurrentFont(), groupDict, testFile,jsonFileName)