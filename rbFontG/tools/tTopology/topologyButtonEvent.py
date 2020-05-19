from rbFontG.tools.tTopology.topologyJudgement import *
from rbFontG.tools.tTopology.topologyAssignment import *
from jsonConverter.converter import *

"""
2020/02/20
Created by heesup Kim

2020/03/19
Modify by heesup Kim
파라미터 k와 변수 k가 중첩이 되어져서 잘못된 결과를 생성 -> 이를 수정
"""
def selectAttribute(groupDict,standardContour,num):
	"""
	To select all same group's contours point that is same point with standard contour

	Args : 
		groupFile :: str
			file's path that has group contours
		originalFile :: File
			file that has total contours
		standardContour :: RContour
		num :: int
            value of divide(insert None topology at divided position) 
	"""
	controllerList = []
	contoursList = []

	#create topologyJudgementController object
	for k in groupDict.keys():
		for i in range(0,len(groupDict[k])):
			contoursList.append(k.contours[groupDict[k][i]])

	for i  in range(0,len(contoursList)):
		if(standardContour != contoursList[i]):
			controllerList.append(topologyJudgementController(standardContour,contoursList[i],num))

	for i in range(0, len(controllerList)):
		controllerList[i].giveSelected()

def penPairAttribute(groupDict,standardContour,num):
	"""
	To give penPair attribute all same group's contours point that is same point with standard contour

	Args : 
		groupFile :: str
			file's path that has group contours
		originalFile :: File
			file that has total contours
		standardContour :: RContour
		num :: int
            value of divide(insert None topology at divided position) 
	"""
	controllerList = []
	contoursList = []

	#create topologyJudgementController object
	for k in groupDict.keys():
		for i in range(0,len(groupDict[k])):
			contoursList.append(k.contours[groupDict[k][i]])

	for i  in range(0,len(contoursList)):
		if(standardContour != contoursList[i]):
			controllerList.append(topologyJudgementController(standardContour,contoursList[i],num))

	for i in range(0, len(controllerList)):
		controllerList[i].giveAttrPenPair()

def dependXAttribute(groupDict,standardContour,num):
	"""
	To give dependX attribute all same group's contours point that is same point with standard contour

	Args : 
		groupFile :: str
			file's path that has group contours
		originalFile :: File
			file that has total contours
		standardContour :: RContour
		num :: int
            value of divide(insert None topology at divided position) 
	"""
	controllerList = []
	contoursList = []

	#create topologyJudgementController object
	for k in groupDict.keys():
		for i in range(0,len(groupDict[k])):
			contoursList.append(k.contours[groupDict[k][i]])

	for i  in range(0,len(contoursList)):
		if(standardContour != contoursList[i]):
			controllerList.append(topologyJudgementController(standardContour,contoursList[i],num))

	for i in range(0, len(controllerList)):
		controllerList[i].giveDependX()

def dependYAttribute(groupDict,standardContour,num):
	"""
	To give dependX attribute all same group's contours point that is same point with standard contour

	Args : 
		groupFile :: str
			file's path that has group contours
		originalFile :: File
			file that has total contours
		standardContour :: RContour
		num :: int
            value of divide(insert None topology at divided position) 
	"""
	controllerList = []
	contoursList = []

	#create topologyJudgementController object
	for k in groupDict.keys():
		for i in range(0,len(groupDict[k])):
			contoursList.append(k.contours[groupDict[k][i]])

	for i  in range(0,len(contoursList)):
		if(standardContour != contoursList[i]):
			controllerList.append(topologyJudgementController(standardContour,contoursList[i],num))

	for i in range(0, len(controllerList)):
		controllerList[i].giveDependY()

def innerFillAttribute(groupDict,standardContour,num):
	"""
	To give innerFill attribute all same group's contours point that is same point with standard contour

	Args : 
		groupFile :: str
			file's path that has group contours
		originalFile :: File
			file that has total contours
		standardContour :: RContour
		num :: int
            value of divide(insert None topology at divided position) 
	"""
	controllerList = []
	contoursList = []

	#create topologyJudgementController object
	for k in groupDict.keys():
		for i in range(0,len(groupDict[k])):
			contoursList.append(k.contours[groupDict[k][i]])

	for i  in range(0,len(contoursList)):
		if(standardContour != contoursList[i]):
			controllerList.append(topologyJudgementController(standardContour,contoursList[i],num))

	for i in range(0, len(controllerList)):
		controllerList[i].giveInnerFill()

def deleteAttribute(groupDict,standardContour,attribute,num):
	"""
	To delete attributet all same group's contours point that is same point with standard contour

	Args : 
		groupFile :: str
			file's path that has group contours
		originalFile :: File
			file that has total contours
		standardContour :: RContour
		attribute :: string
			attribute that want to delete
		num :: int
            value of divide(insert None topology at divided position) 
	"""
	controllerList = []
	contoursList = []

	#create topologyJudgementController object
	for k in groupDict.keys():
		for i in range(0,len(groupDict[k])):
			contoursList.append(k.contours[groupDict[k][i]])

	for i  in range(0,len(contoursList)):
		controllerList.append(topologyJudgementController(standardContour,contoursList[i],num))

	for i in range(0, len(controllerList)):
		controllerList[i].deleteAttr(attribute)				