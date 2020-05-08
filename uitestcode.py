import os
import sys
sys.path.append('/Applications/RoboFont.app/Contents/Resources/lib/python3.6/')
from fontParts.world import CurrentFont, OpenFont
import math
import rbWindow.editWindow as ew
from jsonConverter.makeJsonFile import *
from testCode.initialization import *
from rbWindow.ExtensionSetting.extensionValue import *


config = ConfigExtensionSettings(DefaultKey)
config.removeSettings()
config.registerSettings()

testPath = "/Users/sslab/Desktop/groupTest.ufo"
testFile = OpenFont(testPath,showInterface = False)
jsonFileName = StartProgram(testPath,testFile)
setExtensionDefault(DefaultKey + ".file", CurrentFont())
setExtensionDefault(DefaultKey + ".jsonFilePath", jsonFileName)
menuWindow = ew.EditGroupMenu(CurrentFont(), testFile,jsonFileName)

