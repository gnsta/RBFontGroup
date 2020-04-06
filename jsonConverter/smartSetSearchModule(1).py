from mojo.UI import *
from parseSyllable.configSyllable import *
import json
import os
from rbFontG.tools.parseUnicodeControll import *

"""
2020/03/25
create By Kim heesup
"""

baseDir = "/Users/font/Desktop/GroupDict/"

def searchGroup(glyph,contourNumber,mode):
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
		contain fileNumber and syllable and last data is checkdata(if 0 -> grouped , 1 -> not grouped)

		수정부분 : json 파일로 찾지 말고 set 이용하여 해결
				 그룹핑 자체를 초, 중 ,종 으로 하지 않고 컨투어의 이름으로 바꿈 
	"""

	glyphConfigure = getConfigure(glyph)

	check = 0
	positionNumber = None
	searchSmartSet = None
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
	puc = parseUnicodeController(g.unicode)
	charsList = puc.getChars()

	if mode == 0:
		setStat = getSmartSetStatMatrix()
		print("현재 스마트 셋의 상태 : ", setStat)
		searchMode = "Matrix"
	elif mode == 1:
		setStat = getSmartSetStatTopology()
		print("현재 스마트 셋의 상태 : ", setStat)
		searchMode = "Topology"



	posiitonName = charsList[positionNumber]

	'''if positionNumber == 0:
		positionName = "first"
	elif positionNumber == 1:
		positionName = "middle"
	else:
		positionName = "final"'''



	sSets = getSmartSets()
	glyphNames = list()
	check = 0

	for sSet in sSets:
		checkSetName = str(sSet.name)
		checkSetNameList = checkSetName.split('_')
		print(checkSetNameList)
		if checkSetNameList[1] != positionName or checkSetNameList[2] != searchMode:
			continue
		print(sSet.glyphNames) 
		for item in sSet.glyphNames:
			if str(item) == glyph.name:
				searchSmartSet = sSet
				check = 1
				break

		if check == 1:
			break

	print(searchSmartSet)

	#glyphUniName =  "uni" + hex(glyph.unicode)[2:].upper()

	#fileNumber = json_data[glyphUniName][str(contourNumber)]

	if searchSmartSet is not None:
		#팝업창으로 띄워주면 좋을 부분
		print(Message("이미 그룹 연산이 진행이 되어 있으므로 그룹화 작업을 생략합니다."))
		return [checkSetNameList[0],positionNumber,0]
	else:
		if positionNumber == 0:
			appendNumber = setStat[posiitonName] + 1
		elif positionNumber == 1:
			appendNumber = setStat[posiitonName] + 1
		elif positionNumber == 2:
			appendNumber = setStat[posiitonName] + 1

		#json_data[glyphUniName][positionNumber] = appendNumber

		return [appendNumber,positionNumber,1]

def setGroup(glyph,contourNumber,mode,jsonFileName,appendNumber):
	"""
	store group information about glyph's contour to json File
	(Not Using)

	Args:
		glyph :: Rglyph

		contourNumber :: int
			glyph's contour number

		mode :: int
			0 - > matrix , 1-> topology
		
		jsonFileName :: Stirng
			file name that include data about contour group name

		appendNumber :: int
			setNumber
	"""

	if mode == 0:
		searchFileName = "Matrix"
	elif mode == 1:
		searchFileName = "Topology"


	glyphUniName =  "uni" + hex(glyph.unicode)[2:].upper()

	with open(baseDir + searchFileName, 'r') as f:
		json_data = json.load(f)


	json_data[glyphUniName][str(contourNumber)] = appendNumber

	with open(baseDir + searchFileName,'w',encoding = 'utf-8') as make_file:
		json.dump(json_data,make_file,indent = '\t')



	
def getSmartSetStatMatrix():
	"""
	check how many set about matrix
	not count other

	Args:
		character : hangle char
			investigated hangle character

	set name format example
		:##(number)_##(syllable)_####(mode)
	"""

	matrixSetStat = {'ㄱ':0, 'ㄲ':0, 'ㄴ':0, 'ㄷ':0, 'ㄸ':0, 'ㄹ':0, 'ㅁ':0, 'ㅂ':0, 'ㅃ':0, 'ㅅ':0, 'ㅆ':0,
        'ㅇ':0,'ㅈ':0, 'ㅉ':0, 'ㅊ':0, 'ㅋ':0, 'ㅌ':0, 'ㅍ':0, 'ㅎ':0, 'ㅏ':0,'ㅐ':0, 'ㅑ':0,'ㅒ':0,'ㅓ':0, 'ㅔ':0,
        'ㅕ':0,'ㅖ':0,'ㅗ':0, 'ㅘ':0, 'ㅙ':0, 'ㅚ':0,'ㅛ':0,'ㅜ':0,'ㅝ':0,'ㅞ':0,'ㅟ':0,'ㅠ':0, 'ㅡ':0,'ㅢ':0,'ㅣ':0,
        'ㄱㅅ' : 0,'ㄴㅈ': 0,'ㄴㅎ':0,'ㄹㄱ':0,'ㄹㅁ':0,'ㄹㅂ':0,'ㄹㅅ':0,'ㄹㅌ':0,'ㄹㅍ':0,'ㄹㅎ':0,'ㅂㅅ':0}

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



def getSmartSetStatTopology(character):
	"""
	check how many set about topology
	not count other

	set name format example
		:##(number)_##(syllable)_####(mode)
	"""

	matrixSetStat = {'ㄱ':0, 'ㄲ':0, 'ㄴ':0, 'ㄷ':0, 'ㄸ':0, 'ㄹ':0, 'ㅁ':0, 'ㅂ':0, 'ㅃ':0, 'ㅅ':0, 'ㅆ':0,
        'ㅇ':0,'ㅈ':0, 'ㅉ':0, 'ㅊ':0, 'ㅋ':0, 'ㅌ':0, 'ㅍ':0, 'ㅎ':0, 'ㅏ':0,'ㅐ':0, 'ㅑ':0,'ㅒ':0,'ㅓ':0, 'ㅔ':0,
        'ㅕ':0,'ㅖ':0,'ㅗ':0, 'ㅘ':0, 'ㅙ':0, 'ㅚ':0,'ㅛ':0,'ㅜ':0,'ㅝ':0,'ㅞ':0,'ㅟ':0,'ㅠ':0, 'ㅡ':0,'ㅢ':0,'ㅣ':0,
        'ㄱㅅ' : 0,'ㄴㅈ': 0,'ㄴㅎ':0,'ㄹㄱ':0,'ㄹㅁ':0,'ㄹㅂ':0,'ㄹㅅ':0,'ㄹㅌ':0,'ㄹㅍ':0,'ㄹㅎ':0,'ㅂㅅ':0}

	setList = getSmartSets()

	for sl in setList:
		setName = sl.name
		setNameList = setName.split('_')
		modeName = setNameList[2]
		setNumber = int(setNameList[0])
		setSyllable = setNameList[1]

		if modeName == "Topology":
			topologySetStat[setSyllable] += 1

	return topologySetStat







