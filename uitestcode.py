import os
import sys
sys.path.append('/Applications/RoboFont.app/Contents/Resources/lib/python3.6/')
from fontParts.world import CurrentFont, OpenFont
import math
import rbWindow.editWindow as ew
from jsonConverter.makeJsonFile import *
from testCode.initialization import *
from rbWindow.ExtensionSetting.extensionValue import *
from parseSyllable.configVersionFinal import *

print("uiTEST started")
configPreset = ConfigExtensionSetting(DefaultKey)
configPreset.checkLangauge()
configPreset.registerSettings()

#임시적으로 첨가해놓은 부분
testPath = GetFile()
testFile = OpenFont(testPath,showInterface = False)

groupDict = None
FileNameList = StartProgram(testPath,testFile,CurrentFont())
#setExtensionDefault(DefaultKey + ".file", CurrentFont())
setExtensionDefault(DefaultKey + ".font", CurrentFont())
setExtensionDefault(DefaultKey + ".jsonFileName1", FileNameList[0])
setExtensionDefault(DefaultKey + ".jsonFileName2", FileNameList[1])
syllableJudgementController = SyllableJudgement(testFile,testPath)
setExtensionDefault(DefaultKey + ".syllableJudgementController", syllableJudgementController)
menuWindow = ew.EditGroupMenu(groupDict,FileNameList[0],FileNameList[1])