import os
import sys
sys.path.append('/Applications/RoboFont.app/Contents/Resources/lib/python3.6/')
from fontParts.world import CurrentFont, OpenFont
import math
import rbFontG.tools.tMatrix.PhaseTool
import rbFontG.tools.tMatrix.groupTestController
import rbWindow.editWindow as ew
import pickle
from jsonConverter.makeJsonFile import *


#if __name__ == '__main__':

BroadNibBackgroundDefaultKey = "com.asaumierdemers.BroadNibBackground"

testPath = "/Users/sslab/Desktop/groupTest.ufo"
testFile = OpenFont(testPath,showInterface = False)



# c = g.contours[0]

# standardMatrix = rbFontG.tools.tMatrix.PhaseTool.Matrix(c,3,3)

# compareController = rbFontG.tools.tMatrix.groupTestController.groupTestController(standardMatrix,0)

# groupList = []


# for idx, comGlyph in enumerate(testFile):

#    resul = compareController.glyphCheckGroup(comGlyph)
#    if(resul != None):
#        groupList.append(resul)    

# print(groupList)

groupDict = None
#MakeJsonController(testPath,testFile)
#tempFileName = testPath.split('/')[-1]
#jsonFileName = tempFileName.split('.')[0] + '.json'
#print(jsonFileName)    
menuWindow = ew.EditGroupMenu(CurrentFont(), testFile)