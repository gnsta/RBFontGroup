from mojo.UI import *
from parseSyllable.configSyllable import *
import pathManager.pathSetting as extPath
import json
import os

"""
2020/03/25
create By Kim heesup
"""

def searchGroup(glyph,contourNumber,mode,jsonFileName):
	"""
	check that contour group is created
	if exist return file number else return None

	Args:
		glyph :: Rglyph

		contourNumber :: int
			contour that is being searched

		mode :: int
			0 - > matrix , 1-> topology
		
		jsonFileName :: Stirng
			file name that include data about contour group name

	Return :: List
		contain fileNumber and syllable
	"""
	print("searchGroup : ")
	print(os.getcwd())
	glyphConfigure = getConfigure(glyph)
	check = 0
	positionNumber = None
	#해당 컨투어가 초성인지 중성인지 종성인지 확인을 해 보아햐함
	#!!
	for i in range(0,len(glyphConfigure[str(glyph.unicode)])):
		for j in range(0,len(glyphConfigure[str(glyph.unicode)][i])):
			if contourNumber == glyphConfigure[str(glyph.unicode)][i][j]:
				check = 1
				positionNumber = i
				break

		if check == 1:
			break

	print("mode = ",mode)
	if mode == 0:
		setStat = getSmartSetStatMatrix()
		print("현재 스마트 셋의 상태 : ", setStat)
		searchFileName = "Matrix" + jsonFileName
	elif mode == 1:
		setStat = getSmartSetStatTopology()
		print("현재 스마트 셋의 상태 : ", setStat)
		searchFileName = "Topology" + jsonFileName


	print(extPath.baseDir + searchFileName)

	with open(extPath.baseDir + searchFileName, 'r') as f:
		json_data = json.load(f)

	glyphUniName =  "uni" + hex(glyph.unicode)[2:].upper()

	fileNumber = json_data[glyphUniName][positionNumber]
	print(positionNumber)
	if fileNumber != 0:
		#팝업창으로 띄워주면 좋을 부분
		print(Message("이미 그룹 연산이 진행이 되어 있으므로 그룹화 작업을 생략합니다."))
		return [fileNumber,positionNumber,0]
	else:
		if positionNumber == 0:
			appendNumber = setStat["first"] + 1
		elif positionNumber == 1:
			appendNumber = setStat["middle"] + 1
		elif positionNumber == 2:
			appendNumber = setStat["final"] + 1

		json_data[glyphUniName][positionNumber] = appendNumber

		with open(extPath.baseDir + searchFileName,'w',encoding = 'utf-8') as make_file:
			json.dump(json_data,make_file,indent = '\t')

		return [appendNumber,positionNumber]

def setGroup(glyph,positionNumber,mode,jsonFileName,appendNumber):
	"""
	store group information about glyph's contour to json File

	Args:
		glyph :: Rglyph

		positionNumber :: int
			syllable data

		mode :: int
			0 - > matrix , 1-> topology
		
		jsonFileName :: Stirng
			file name that include data about contour group name

		appendNumber :: int
			setNumber
	"""
	if mode == 0:
		searchFileName = "Matrix" + jsonFileName
	elif mode == 1:
		searchFileName = "Topology" + jsonFileName

	glyphUniName =  "uni" + hex(glyph.unicode)[2:].upper()

	with open(extPath.baseDir + searchFileName, 'r') as f:
		json_data = json.load(f)


	json_data[glyphUniName][positionNumber] = appendNumber

	# print(json_data)

	with open(extPath.baseDir + searchFileName,'w',encoding = 'utf-8') as make_file:
		json.dump(json_data,make_file,indent = '\t')



	
def getSmartSetStatMatrix():
	"""
	check how many set about matrix
	not count other

	set name format example
		:##(number)_##(syllable)_####(mode)
	"""

	matrixSetStat = {"first" : 0, "middle" : 0 , "final" : 0}

	setList = getSmartSets()

	for sl in setList:
		setName = sl.name
		setNameList = setName.split('_')
		modeName = setNameList[2]
		setNumber = int(setNameList[0])
		setSyllable = setNameList[1]

		if modeName ==  "Matrix":
			matrixSetStat[setSyllable] += 1

	return matrixSetStat



def getSmartSetStatTopology():
	"""
	check how many set about topology
	not count other

	set name format example
		:##(number)_##(syllable)_####(mode)
	"""

	topologySetStat  = {"first" : 0 , "middle" : 0 , "final" : 0}

	setList = getSmartSets()

	for sl in setList:
		setName = sl.name
		setNameList = setName.split('_')
		print(setNameList)
		modeName = setNameList[2]
		setNumber = int(setNameList[0])
		setSyllable = setNameList[1]

		if modeName == "Topology":
			topologySetStat[setSyllable] += 1

	return topologySetStat







