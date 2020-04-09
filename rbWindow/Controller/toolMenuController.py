import jsonConverter.searchModule as search
from mojo.UI import MultiLineView, SelectGlyph
import rbFontG.tools.tMatrix.PhaseTool
import rbFontG.tools.tMatrix.groupTestController
from rbFontG.tools.tTopology import topologyJudgement as tj
from rbFontG.tools.tTopology import topologyAssignment as ta
from rbFontG.tools import parseUnicodeControll as puc
import jsonConverter.converter as convert
from jsonConverter.smartSetSearchModule import *
from mojo.UI import SmartSet, addSmartSet

matrixMode = 0
topologyMode = 1

margin = 20
width = 100
k = 500

def getMatchGroupByMatrix(standardGlyph, contourIndex, margin, width, height, file,checkSetData,jsonFileName):
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
		mainWindow :: tool Menu object
			to get font File in searchGroup function
	Return : Dictionary
		key is glyph and value is list that same contours index
	2020/03/23
	add smart set that include smae glyph group
	set name format example
		: ##(number)_##(syllable)_####(mode)
	"""

	contour = standardGlyph.contours[contourIndex]

	standardMatrix = Matrix(contour,width)
	#k에 대한 마진값 적용하는 부분 넣어 주워야 함
	compareController = groupTestController(standardMatrix,0)
	smartSetGlyphs = []
	smartSet = SmartSet()

	if checkSetData[1] == 0:
		smartSet.name = str(checkSetData[0]) + "_first_Matrix_" + "(" + str(standardGlyph.unicode) + "-" + str(contourIndex) + ")"
	elif checkSetData[1] == 1:
		smartSet.name = str(checkSetData[0])  + "_middle_Matrix_" +"(" + str(standardGlyph.unicode) + "-" + str(contourIndex) + ")"
	elif checkSetData[1] == 2:
		smartSet.name = str(checkSetData[0]) + "_final_Matrix_"+"(" + str(standardGlyph.unicode) + "-" + str(contourIndex) + ")"

	smartGroupDict = {}
	smartContourList = [] 

	for compareGlyph in file:
		smartCheck = 0
		#print(checkSetData[1])
		#print(getConfigure(compareGlyph))
		searchContours = getConfigure(compareGlyph)[str(compareGlyph.unicode)][checkSetData[1]]
		for i in range(0,len(compareGlyph.contours)):
			if i in searchContours:	
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
	updateAllSmartSets()	



def getMatchGroupByTopology(standardGlyph,standardContour, k, file,checkSetData,jsonFileName):
	"""
	2020/03/25
	modify by Kim heesup
	To get group contours Based on standard Glyph's contour by topology
	Args :
		standardGlyph : RGlyph 
			glyph include standard contour
		contourIndex ::  int
			standard contour index that is included on standardGlyph
		k : int
			value of divide the x-axis and y-axis to consider None point
		file  : OpenFont
			File to investigate
		checkSetData :: List
			[setNumber, syllableNumber] (using to File naming)
		mainWindow :: tool Menu object
			to get font File in searchGroup function
	Return : Dictionary
		key is glyph and value is list that same contours index
	2020/03/23
	add smart set that include smae glyph group				
	"""

	smartSetGlyphs = []
	smartSet = SmartSet()
	if checkSetData[1] == 0:
		smartSet.name = str(checkSetData[0]) + "_first_Topology_" +"(" + str(standardGlyph.unicode) + "-" + str(contourIndex) + ")"
	elif checkSetData[1] == 1:
		smartSet.name = str(checkSetData[0])  + "_middle_Topology_"+"(" + str(standardGlyph.unicode) + "-" + str(contourIndex) + ")"
	elif checkSetData[1] == 2:
		smartSet.name = str(checkSetData[0]) + "_final_Topology_"+"(" + str(standardGlyph.unicode) + "-" + str(contourIndex) + ")"
	smartGroupDict = {}
	smartContourList = [] 


	for compareGlyph in file:
		smartCheck = 0
		searchContours = getConfigure(compareGlyph)[str(compareGlyph.unicode)][checkSetData[1]]
		for i in range(0,len(compareGlyph.contours)):
			if i in searchContours:
				resul = topologyJudgementController(standardGlyph.contours[contourIndex],compareGlyph.contours[i],k).topologyJudgement()
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
	updateAllSmartSets()


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
	checkSetData = searchGroup(standardGlyph,contourIndex,mainWindow.mode,mainWindow,True)
	if checkSetData[2] == 0:
		currentWindow.groupDict = findContoursGroup(checkSetData,mainWindow)
		print("이미 그룹화가 진행된 컨투어입니다.")

	else:
		if mainWindow.mode is matrixMode:
			#margin = int(currentWindow.w.margin.slider.get())
			#width = int(currentWindow.w.matrixWidth.slider.get())
			getMatchGroupByMatrix(standardGlyph, contourIndex, margin, width, width, file, checkSetData, mainWindow.jsonFileName)
			currentWindow.groupDict = findContoursGroup(checkSetData, mainWindow)

		elif mainWindow.mode is topologyMode:
			#k = int(currentWindow.w.topologyK.slider.get())
			getMatchGroupByTopology(standardGlyph, standardGlyph.contours[contourIndex], k, currentWindow.font,checkSetData,mainWindow.jsonFileName)
			currentWindow.groupDict = findContoursGroup(checkSetData, mainWindow)
		
		#if currentWindow.group is None:
			#print(Message("There is no matching group.")); return;

		#else:
			#currentWindow.mode = mainWindow.mode
			#saveGroupDict(currentWindow)

	#updateLineView(currentWindow)
	mainWindow.groupDict = currentWindow.groupDict

def findContoursGroup(checkSetData,mainWindow):
	"""
	find grouped contour reference by jsonFile and smartSet
	Args :
		checkSetData:: list
			[fileNumber,positionNumber,0]
		mainWindow :: object
			editWindow object
		mode :: int
		0 -> matrix , 1- > topology
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
		standardNameList = nameList[3].split('-')
		standardGlyphUnicode = int(standardNameList[0][1:])
		standardIdx = int(standardNameList[1][0:len(standardNameList[1])-1])
		if (nameList[0] == str(checkSetData[0])) and (nameList[1] == positionName) and (nameList[2] == modeName):
			groupSet = sset
			break

	for item in groupSet.glyphNames:
		glyphList.append(mainWindow.file[str(item)])


	for g in glyphList:
		searchContours = []
		for i,comc in enumerate(g.contours):
			if mainWindow.mode == 0:
				standardGlyph = mainWindow.file["uni" + str(hex(standardGlyphUnicode)[2:]).upper()]
				standardMatrix=Matrix(standardGlyph.contours[standardIdx],10)
				compareController = groupTestController(standardMatrix,0)
				result = compareController.conCheckGroup(comc)
				if result is not None:
					searchContours.append(i)
			elif mainWindow.mode == 1:
				standardGlyph = mainWindow.file["uni" + str(hex(standardGlyphUnicode)[2:]).upper()]
				result = topologyJudgementController(standardGlyph.contours[standardIdx],comc,200).topologyJudgement()
				if result is not False:
					searchContours.append(i)
		res[g] = searchContours

	return res