from mojo.UI import *
from parseSyllable.configSyllable import *
import json
import os
from groupingTool.tMatrix.PhaseTool import *
from groupingTool.tMatrix.groupTestController import *
from groupingTool.tTopology.topologyJudgement import *
from groupingTool.tTopology.topologyAssignment import *
from rbWindow.ExtensionSetting.extensionValue import *

"""
create By Heesup Kim
"""

baseDir = "/Users/font/Desktop/GroupDict/"

matrix_margin = 20
matrix_size = 3
topology_margin = 500

def cSearchGroup(glyph,contourNumber,mode,file,message = False):
	"""
	스마트셋에 그룹이 존재하는지 확인(한자버전)
	Args:
		glyph :: RGlyph
			검사를 진행하고자 하는 RGlyph
		contourNumber :: int
			RGlyph의 검사를 진행하고자 하는 컨투어의 번호
		mode :: int
			0 -> matrix, 1 -> topology
		file :: RFont
			작업하고 있는 RFont

	Return :: int
		현재 그룹의 번호
	"""

	check = 0
	positionNumber = None
	searchSmartSet = None

	if mode == 0:
		print("mode : Matrix")
		setStat = cGetSmartSetStatMatrix()
		print("현재 스마트 셋의 상태 : ", setStat)
		searchMode = "Matrix"
	elif mode == 1:
		print("mode : Topology")
		setStat = cGetSmartSetStatTopology()
		print("현재 스마트 셋의 상태 : ", setStat)
		searchMode = "Topology"

	sSets = getSmartSets()
	glyphNames = list()
	check = 0


	for sSet in sSets:
		checkSetName = str(sSet.name)
		checkSetNameList = checkSetName.split('_')
		if len(checkSetNameList) != 3:
			continue

		#검사를 진행을 해야함(기준 컨투어는 알고 있고 비교 글리프에 있는 컨투어는 순회를 하면서 조사하는 방식)
		#matrix 체크에서는 같은 그룹이 아니면 None이고 topology 에서는 같은 그룹이 아니면 flase반환
		standardNameList = checkSetNameList[2].split('-')
		print(standardNameList)
		standardGlyphUnicode = int(standardNameList[0][4:])
		standardIdx = int(standardNameList[1][:len(standardNameList[1]) -1]) 
		for item in sSet.glyphNames:
			if item != glyph.name:
				continue
			if mode == 0:
				#해당 그룹을 조사
				print("standardNameList[0]",standardNameList[0])
				print("standardNameList[0][4:]",standardNameList[0][4:])
				standardGlyph = file["cid" + str(standardNameList[0][4:]).upper()]
				standardMatrix=Matrix(standardGlyph.contours[standardIdx],matrix_size)
				compareController = groupTestController(standardMatrix,matrix_margin)
				result = compareController.conCheckGroup(glyph[contourNumber])

				if result is not None: 
					searchSmartSet = sSet
					check = 1
					message = True
					break

			elif mode == 1:
				standardGlyph = file["cid" + str(standardNameList[0][4:]).upper()]
				result = topologyJudgementController(standardGlyph.contours[standardIdx],glyph[contourNumber],topology_margin).topologyJudgement()
				if result is not False: 
					searchSmartSet = sSet
					check = 1
					message = True
					break

		if check == 1:
			break

	if searchSmartSet is not None:
		if message == True:
			appendNumber = str(searchSmartSet.name).split('_')[0]
			print("checkSetNameList : ", checkSetNameList)
			print(Message("이미 그룹 연산이 진행이 되어 있으므로 그룹화 작업을 생략합니다."))
		return [int(checkSetNameList[0]),positionNumber,0]
	else:
		return [int(setStat[0]),positionNumber,1]






def searchGroup(glyph,contourNumber,mode,file,message = False):
	"""
	스마트셋에 그룹이 존재하는지 확인
	Args:
		glyph :: RGlyph
			검사를 진행하고자 하는 RGlyph
		contourNumber :: int
			RGlyph의 검사를 진행하고자 하는 컨투어의 번호
		mode :: int
			0 - > matrix , 1-> topology
		file :: RFont
			작업하고 있는 RFont

	Return :: List
		[스마트 셋의 번호,음절 번호(0 - 초성, 1- 중성, 2- 종성),그룹화 진행 여부에 대한 번호(0 -> grouped , 1 -> not grouped)]
	"""

	syllableJudgementController = getExtensionDefault(DefaultKey + ".syllableJudgementController")
	glyphConfigure = syllableJudgementController.GetSyllable(glyph)
	print('glyphConfigure : ', glyphConfigure)


	check = 0
	positionNumber = None
	searchSmartSet = None

	#해당 컨투어가 초성인지 중성인지 종성인지 확인
	for i in range(0,len(glyphConfigure[str(glyph.unicode)])):
		for j in range(0,len(glyphConfigure[str(glyph.unicode)][i])):
			if contourNumber == glyphConfigure[str(glyph.unicode)][i][j]:
				check = 1
				positionNumber = i
				break

		if check == 1:
			break

	if mode == 0:
		setStat = getSmartSetStatMatrix()
		print("현재 스마트 셋의 상태 : ", setStat)
		searchMode = "Matrix"
	elif mode == 1:
		setStat = getSmartSetStatTopology()
		print("현재 스마트 셋의 상태 : ", setStat)
		searchMode = "Topology"

	if positionNumber == 0:
		positionName = "first"
	elif positionNumber == 1:
		positionName = "middle"
	else:
		positionName = "final"



	sSets = getSmartSets()
	glyphNames = list()
	check = 0

	for sSet in sSets:
		checkSetName = str(sSet.name)
		checkSetNameList = checkSetName.split('_')
		if checkSetNameList[1] != positionName or checkSetNameList[2] != searchMode:
			continue

		#검사를 진행을 해야함(기준 컨투어는 알고 있고 비교 글리프에 있는 컨투어는 순회를 하면서 조사하는 방식)
		#matrix 체크에서는 같은 그룹이 아니면 None이고 topology 에서는 같은 그룹이 아니면 flase반환
		standardNameList = checkSetNameList[3].split('-')
		standardGlyphUnicode = int(standardNameList[0][1:])
		standardIdx = int(standardNameList[1][0:len(standardNameList)-1]) 
		for item in sSet.glyphNames:
			if item != glyph.name:
				continue
			if mode == 0:
				standardGlyph = file["uni" + str(hex(standardGlyphUnicode)[2:]).upper()]
				standardMatrix=Matrix(standardGlyph.contours[standardIdx],matrix_size)
				compareController = groupTestController(standardMatrix,matrix_margin)
				result = compareController.conCheckGroup(glyph[contourNumber])

				if result is not None: 
					searchSmartSet = sSet
					check = 1
					message = True
					break
			elif mode == 1:
				standardGlyph = file["uni" + str(hex(standardGlyphUnicode)[2:]).upper()]
				result = topologyJudgementController(standardGlyph.contours[standardIdx],glyph[contourNumber],topology_margin).topologyJudgement()
				if result is not False: 
					searchSmartSet = sSet
					check = 1
					message = True
					break
					
		if check == 1:
			break

	if positionNumber == 0:
		appendNumber = setStat["first"]
	elif positionNumber == 1:
		appendNumber = setStat["middle"]
	elif positionNumber == 2:
		appendNumber = setStat["final"]

	if searchSmartSet is not None:
		if message == True:
			appendNumber = str(searchSmartSet.name).split('_')[0]
			print(Message("이미 그룹 연산이 진행이 되어 있으므로 그룹화 작업을 생략합니다."))
		return [int(appendNumber),positionNumber,0]
	else:
		return [appendNumber,positionNumber,1]

	print("return None")

def setGroup(glyph,contourNumber,mode,jsonFileName,appendNumber):
	"""
	글리프의 컨투어에 대한 그룹 정보를 json파일에 저장
	(Not Using)
	Args:
		glyph :: Rglyph
			조사를 진행하는 Rglyph
		contourNumber :: int
			RGlyph의 검사를 진행하고자 하는 컨투어의 번호
		mode :: int
			0 - > matrix , 1-> topology
		jsonFileName :: Stirng
			컨투어의 그룹 이름 데이터를 저장하고 있는 json파일 이름
			file name that include data about contour group name
		appendNumber :: int
			스마트셋에 대한 번호 정보
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
	현재 스마트 셋을 조사하여 다음 그룹화 진행시 어느 번호에 저장해야 하는지 반환(Matrix)
	set name format example
		:##(number)_##(syllable)_####(mode)

	Returns:
		번호에 대한 정보 :: list
			[초성번호, 중성번호, 종성번호]
	"""

	matrixSetStat = {"first" : 0, "middle" : 0 , "final" : 0}

	firstl = list()
	middlel = list()
	finall = list()

	setList = getSmartSets()

	for sl in setList:
		setName = sl.name
		setNameList = setName.split('_')
		modeName = setNameList[2]
		setNumber = int(setNameList[0])
		setSyllable = setNameList[1]

		#한자일 경우는 조사하지 않음
		if len(setNameList) == 2:
			continue

		if modeName ==  "Matrix":
			#matrixSetStat[setSyllable] += 1
			if setSyllable == "first":
				firstl.append(setNumber)
			elif setSyllable == "middle":
				middlel.append(setNumber)
			elif setSyllable == "final":
				finall.append(setNumber)

	firstl.sort()
	middlel.sort()
	finall.sort()


	check = 0 
	for i in range(0,len(firstl)):
		if (i +1) != firstl[i]:
			matrixSetStat["first"] = i
			check = 1
	if check == 0:
		matrixSetStat["first"] = len(firstl) + 1

	check = 0 
	for i in range(0,len(middlel)):
		if (i +1) != middlel[i]:
			matrixSetStat["middle"] = i
			check = 1
	if check == 0:
		matrixSetStat["middle"] = len(middlel) + 1

	check = 0 
	for i in range(0,len(finall)):
		if (i +1) != finall[i]:
			matrixSetStat["final"] = i
			check = 1
	if check == 0:
		matrixSetStat["final"] = len(finall) + 1

	return matrixSetStat



def getSmartSetStatTopology():
	"""
	현재 스마트 셋을 조사하여 다음 그룹화 진행시 어느 번호에 저장해야 하는지 반환(Topology)
	set name format example
		:##(number)_##(syllable)_####(mode)

	Returns:
		번호에 대한 정보 :: list
			[초성번호, 중성번호, 종성번호]
	"""

	topologySetStat  = {"first" : 0 , "middle" : 0 , "final" : 0}

	firstl = list()
	middlel = list()
	finall = list()

	setList = getSmartSets()

	for sl in setList:
		setName = sl.name
		setNameList = setName.split('_')
		modeName = setNameList[2]
		setNumber = int(setNameList[0])
		setSyllable = setNameList[1]

		#한자일 경우는 조사하지 않음
		if len(setNameList) == 2:
			continue

		if modeName == "Topology":
			if setSyllable == "first":
				firstl.append(setNumber)
			elif setSyllable == "middle":
				middlel.append(setNumber)
			elif setSyllable == "final":
				finall.append(setNumber)


	firstl.sort()
	middlel.sort()
	finall.sort()

	check = 0 
	for i in range(0,len(firstl)):
		if (i +1) != firstl[i]:
			topologySetStat["first"] = i
			check = 1
	if check == 0:
		topologySetStat["first"] = len(firstl) + 1

	check = 0 
	for i in range(0,len(middlel)):
		if (i +1) != middlel[i]:
			topologySetStat["middle"] = i
			check = 1
	if check == 0:
		topologySetStat["middle"] = len(middlel) + 1

	check = 0 
	for i in range(0,len(finall)):
		if (i +1) != finall[i]:
			topologySetStat["final"] = i
			check = 1
	if check == 0:
		topologySetStat["final"] = len(finall) + 1

	return topologySetStat

def cGetSmartSetStatMatrix():
	"""
	현재 스마트 셋을 조사하여 다음 그룹화 진행시 어느 번호에 저장해야 하는지 반환(Matrix)
	set name format example
		:##(number)_Matrix

	Returns:
		번호에 대한 정보 :: list
			[그룹 번호, mode 정보]
	"""
	setList = getSmartSets()

	numberl = list()

	for sl in setList:
		setName = sl.name
		setNameList = setName.split('_')
		modeName = setNameList[1]
		setNumber = int(setNameList[0])

		if len(setNameList) != 3:
			continue

		if modeName ==  "Matrix":
			numberl.append(setNumber)

	#print("######numberl : ", numberl)
	numberl.sort()


	#적절한 위치를 찾기
	if len(numberl) == 0:
		return [1,"Matrix"]
	elif len(numberl) == 1:
		if numberl[0] == 1:
			return [2,"Matrix"]
		elif numberl[0] != 1:
			return [1,"Matrix"]
	elif numberl[0] != 1:
		return [1,"Matrix"]

	check = 0
	res = 0
	resList = list()

	for i in range(0,len(numberl)-2):
		if numberl[i] != numberl[i+1] -1:
			res = numberl[i] + 1
			check = 1
			break

	#print("numberl len ", len(numberl) )

	if check == 0:
		res = numberl[len(numberl)-1] +1

	resList.append(res)
	resList.append("Matrix")

	return resList

def cGetSmartSetStatTopology():
	"""
	현재 스마트 셋을 조사하여 다음 그룹화 진행시 어느 번호에 저장해야 하는지 반환(Matrix)
	set name format example
		:##(number)_Matrix

	Returns:
		번호에 대한 정보 :: list
			[그룹 번호, mode 정보]
	"""
	setList = getSmartSets()

	numberl = list()

	for sl in setList:
		setName = sl.name
		setNameList = setName.split('_')
		modeName = setNameList[1]
		setNumber = int(setNameList[0])

		if len(setNameList) != 3:
			continue

		if modeName ==  "Topology":
			numberl.append(setNumber)


	numberl.sort()


	#적절한 위치를 찾기
	if len(numberl) == 0:
		return [1,"Topology"]
	elif len(numberl) == 1:
		if numberl[0] == 1:
			return [2,"Topology"]
		elif numberl[0] != 1:
			return [1,"Topology"]
	elif numberl[0] != 1:
		return [1,"Topology"]

	check = 0
	res = 0
	resList = list()

	for i in range(0,len(numberl)-2):
		if numberl[i] != numberl[i] -1:
			res = numberl[i] + 1
			check = 1
			break

	if check == 0:
		res = numberl[len(numberl)-1] +1

	resList.append(res)
	resList.append("Topology")

	return resList


