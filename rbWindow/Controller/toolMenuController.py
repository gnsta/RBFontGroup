import jsonConverter.searchModule as search
from mojo.UI import MultiLineView, SelectGlyph
import rbFontG.tools.tMatrix.PhaseTool
import rbFontG.tools.tMatrix.groupTestController
from rbFontG.tools.tTopology import topologyJudgement as tj
from rbFontG.tools.tTopology import topologyAssignment as ta
from rbFontG.tools import parseUnicodeControll as puc
import jsonConverter.converter as convert
from jsonConverter.smartSetSearchModule import *
from parseSyllable.configSyllable import *
from mojo.UI import *

matrixMode = 0
topologyMode = 1


def getMatchGroupByMatrix(standardGlyph, contourIndex, margin, width, height, file,checkSetData):
	"""
	2020/03/35 
	modify by Kim heesup

	To get group contours Based on standard Glyph's contour by Matrix

	Args :
		standardGlyph :: RGlyph 
			glyph include standard contour
		contourIndex ::  int
			standard contour index that is included on standardGlyph
		margin :: int
			error range whther or not the compare contour is same group with standard contour
		width :: int
			value of divide the x-axis
		height :: int
			value of divede the y-axis
		file  :: OpenFont
			File to investigate
		checkSetData :: List
			[setNumber, syllableNumber] (using to File naming)
	Return : Dictionary
		key is glyph and value is list that same contours index


	2020/03/23
	add smart set that include smae glyph group

	set name format example
		: ##(number)_##(syllable)_####(mode)
	"""

	contour = standardGlyph.contours[contourIndex]

	standardMatrix = rbFontG.tools.tMatrix.PhaseTool.Matrix(contour,width)
	compareController = rbFontG.tools.tMatrix.groupTestController.groupTestController(standardMatrix,0)
	smartSetGlyphs = []
	smartSet = SmartSet()

	if checkSetData[1] == 0:
		smartSet.name = str(checkSetData[0]) + "_first_Matrix"
	elif checkSetData[1] == 1:
		smartSet.name = str(checkSetData[0])  + "_middle_Matrix"
	elif checkSetData[1] == 2:
		smartSet.name = str(checkSetData[0]) + "_final_Matrix"

	smartGroupDict = {}
	smartContourList = [] 

	for compareGlyph in file:
		smartCheck = 0
		for i in range(0,len(compareGlyph.contours)):
				result = compareController.conCheckGroup(compareGlyph.contours[i])
				if result is not None:
					smartContourList.append(i)
					smartCheck = 1
					#setGroup(compareGlyph,i,matrixMode,jsonFileName,checkSetData[0])

		if(smartCheck == 1):
			glyphUniName = "uni"+hex(compareGlyph.unicode)[2:].upper()
			smartGroupDict[glyphUniName] = smartContourList
			smartSetGlyphs.append("uni"+hex(compareGlyph.unicode)[2:].upper())
			smartContourList = []
			#setGroup(compareGlyph,checkSetData[1],0,jsonFileName,checkSetData[0])

	smartSet.glyphNames = smartSetGlyphs
	addSmartSet(smartSet)	


def getMatchGroupByTopology(standardGlyph,standardContour, k, file,checkSetData):
	"""
	2020/03/25
	modify by Kim heesup

	To get group contours Based on standard Glyph's contour by topology

	Args :
		standardGlyph : RGlyph 
			glyph include standard contour
		standardContour :  RContour
			standard contour that is included on standardGlyph
		k : int
			value of divide the x-axis and y-axis to consider None point
		file  : OpenFont
			File to investigate
		checkSetData :: List
			[setNumber, syllableNumber] (using to File naming)
	Return : Dictionary
		key is glyph and value is list that same contours index

	2020/03/23
	add smart set that include smae glyph group				
	"""

	smartSetGlyphs = []
	smartSet = SmartSet()
	if checkSetData[1] == 0:
		smartSet.name = str(checkSetData[0]) + "_first_Topology"
	elif checkSetData[1] == 1:
		smartSet.name = str(checkSetData[0])  + "_middle_Topology"
	elif checkSetData[1] == 2:
		smartSet.name = str(checkSetData[0]) + "_final_Topology"
	smartGroupDict = {}
	smartContourList = [] 


	for compareGlyph in file:
		smartCheck = 0
		for i in range(0,len(compareGlyph.contours)):
			resul = tj.topologyJudgementController(standardContour,compareGlyph.contours[i],k).topologyJudgement()
			if(resul == True):
				smartCheck = 1
				smartContourList.append(i)

		if(smartCheck == 1):
			glyphUniName = "uni"+hex(compareGlyph.unicode)[2:].upper()
			smartGroupDict[glyphUniName] = smartContourList
			smartSetGlyphs.append("uni"+hex(compareGlyph.unicode)[2:].upper())
			smartContourList = []

	smartSet.glyphNames = smartSetGlyphs
	addSmartSet(smartSet)
			

def handleSearchGlyphList(standardGlyph, contourIndex, file, currentWindow, mainWindow):
	"""
		2020/03/23
		created by H.W. Cho

		Get matching file and update currentWindow's group. If there is no matching file,
		search process will find a new group. Update view is followed at the end of process.

		Args:
			standardGlyph(RGlyph), contourIndex(int) : target object which want to search.
			file(RFont) : search area
			currentWindow(toolMenu object)

		2020/03/25
		modifyed by Kim heesup
		add smart set information

	"""
	#currentWindow.group = search.getGroupDictFile(standardGlyph, contourIndex, currentWindow.font, mainWindow.mode, currentWindow.widthValue, currentWindow.marginValue)
	checkSetData = searchGroup(standardGlyph,contourIndex,mainWindow.mode)
	if checkSetData[2] == 0:
		currentWindow.groupDict = findContoursGroup(checkSetData,mainWindow)
		print("이미 그룹화가 진행된 컨투어입니다.")
	else:
		if mainWindow.mode is matrixMode:
			margin = int(currentWindow.w.margin.slider.get())
			width = int(currentWindow.w.matrixWidth.slider.get())
			getMatchGroupByMatrix(standardGlyph, contourIndex, margin, width, width, file, checkSetData)
			currentWindow.groupDict = findContoursGroup(checkSetData,mainWindow)

		elif mainWindow.mode is topologyMode:
			k = int(currentWindow.w.topologyK.slider.get())
			getMatchGroupByTopology(standardGlyph, standardGlyph.contours[contourIndex], k, currentWindow.font,checkSetData)
			currentWindow.groupDict = findContoursGroup(checkSetData,mainWindow)

	print(currentWindow.groupDict)
	mainWindow.groupDict = currentWindow.groupDict

	
def findContoursGroup(checkSetData,mainWindow):
	"""
	find grouped contour reference by jsonFile and smartSet

	Args :
		checkSetData:: list
			[fileNumber,positionNumber,0]

		mainWindow :: object
			editWindow object
	Return :: Dictionary
		key is glyph and value is list that same contours index
	"""


	ssets = getSmartSets()
	glyphList = list()
	res = dict()
	positionName  = None

	if mainWindow.mode == 0:
		modeName = "Matrix"
	else:
		modeName = "Topology"

	if checkSetData[1] == 0:
		positionName = "first"
	elif checkSetData[1] == 1:
		positionName = "middle"
	else:
		positionName = "final"

	print("checkSetData :", checkSetData)
	print("positionName :",positionName)


	for sset in ssets:
		nameList = str(sset.name).split('_')
		if (nameList[0] == str(checkSetData[0])) and (nameList[1] == positionName) and (nameList[2] == modeName):
			print('a')
			groupSet = sset
			break

	for item in groupSet.glyphNames:
		glyphList.append(mainWindow.file[str(item)])


	for g in glyphList:
		res[g] = getConfigure(g)[str(g.unicode)][checkSetData[1]]

	return res



	

