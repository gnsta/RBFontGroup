import os
import sys
sys.path.append('/Applications/RoboFont.app/Contents/Resources/lib/python3.6/')
from fontParts.world import CurrentFont, OpenFont
import math
import rbWindow.editWindow as ew
import pickle
from jsonConverter.makeJsonFile import *
from testCode.initialization import *

if __name__ == '__main__':

	BroadNibBackgroundDefaultKey = "com.asaumierdemers.BroadNibBackground"

	testPath = "/Users/sslab/Desktop/groupTest.ufo"
	testFile = OpenFont(testPath,showInterface = False)
    groupDict = None
    jsonFileName = StartProgram(testPath,testFile)       
    menuWindow = ew.EditGroupMenu(CurrentFont(), groupDict, testFile,jsonFileName)
