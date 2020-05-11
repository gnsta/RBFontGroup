from rbWindow.ExtensionSetting.extensionValue import *
from rbWindow.Controller.toolMenuController import *


def searchGroupProcess():
	
	selectedDict = dict()

	#try:
	standardGlyph = CurrentGlyph()
	for contour in standardGlyph.contours:
		for point in contour.bPoints:
			if point.selected is True:
				selectedDict[point.getParent().index] = True

	if len(selectedDict) != 1:
		print(Message("글자의 컨투어를 하나만 선택해주세요."))
		return

	contourIndex = list(selectedDict.keys())[0]
	file = getExtensionDefault(DefaultKey + ".file")
	jsonFilePath = getExtensionDefault(DefaultKey + ".jsonFilePath")

	handleSearchGlyphList(standardGlyph, contourIndex, file, jsonFilePath)

	for contour in standardGlyph.contours:
		contour.selected = False
	#except Exception as e:
	#	print(Message("예상치 못한 에러 발생...\n찾고자 하는 글리프를 선택한 뒤 해당 컨투어를 선택하여 주십시오."))

searchGroupProcess()