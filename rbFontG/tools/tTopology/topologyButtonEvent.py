from rbFontG.tools.tTopology.topologyJudgement import *
from rbFontG.tools.tTopology.topologyAssignment import *
from jsonConverter.converter import *

"""
2020/02/20
Created by heesup Kim
"""
def selectAttribute(groupFilePath,originalFile,standardContour,num):
	"""
	To select all same group's contours point that is same point with standard contour

	Args : 
		groupFile :: str
			file's path that has group contours
		originalFile :: File
			file that has total contours
		standardContour :: RContour
		num :: int
            value of divie(insert None topology at divided position) 
	"""
	controllerList = []
	contoursList = []
	groupDict = json2groupDict(groupFilePath,originalFile)

	#create topologyJudgementController object
	for k in groupDict.keys():
		for i in range(0,len(groupDict[k])):
			contoursList.append(k.contours[groupDict[k][i]])

	for i  in range(0,len(contoursList)):
		if(standardContour != contoursList[i]):
			controllerList.append(topologyJudgementController(standardContour,contoursList[i],num))

	for i in range(0, len(controllerList)):
		controllerList[i].giveSelected()

def penPairAttribute(groupFilePath,originalFile,standardContour,num):
	"""
	To give penPair attribute all same group's contours point that is same point with standard contour

	Args : 
		groupFile :: str
			file's path that has group contours
		originalFile :: File
			file that has total contours
		standardContour :: RContour
		num :: int
            value of divie(insert None topology at divided position) 
	"""
	controllerList = []
	contoursList = []
	groupDict = json2groupDict(groupFilePath,originalFile)

	#create topologyJudgementController object
	for k in groupDict.keys():
		for i in range(0,len(groupDict[k])):
			contoursList.append(k.contours[groupDict[k][i]])

	for i  in range(0,len(contoursList)):
		if(standardContour != contoursList[i]):
			controllerList.append(topologyJudgementController(standardContour,contoursList[i],num))

	for i in range(0, len(controllerList)):
		controllerList[i].giveAttrPenPair()

def dependXAttribute(groupFilePath,originalFile,standardContour,num):
	"""
	To give dependX attribute all same group's contours point that is same point with standard contour

	Args : 
		groupFile :: str
			file's path that has group contours
		originalFile :: File
			file that has total contours
		standardContour :: RContour
		num :: int
            value of divie(insert None topology at divided position) 
	"""
	controllerList = []
	contoursList = []
	groupDict = json2groupDict(groupFilePath,originalFile)

	#create topologyJudgementController object
	for k in groupDict.keys():
		for i in range(0,len(groupDict[k])):
			contoursList.append(k.contours[groupDict[k][i]])

	for i  in range(0,len(contoursList)):
		if(standardContour != contoursList[i]):
			controllerList.append(topologyJudgementController(standardContour,contoursList[i],num))

	for i in range(0, len(controllerList)):
		controllerList[i].giveDependX()

def dependYAttribute(groupFilePath,originalFile,standardContour,num):
	"""
	To give dependX attribute all same group's contours point that is same point with standard contour

	Args : 
		groupFile :: str
			file's path that has group contours
		originalFile :: File
			file that has total contours
		standardContour :: RContour
		num :: int
            value of divie(insert None topology at divided position) 
	"""
	controllerList = []
	contoursList = []
	groupDict = json2groupDict(groupFilePath,originalFile)

	#create topologyJudgementController object
	for k in groupDict.keys():
		for i in range(0,len(groupDict[k])):
			contoursList.append(k.contours[groupDict[k][i]])

	for i  in range(0,len(contoursList)):
		if(standardContour != contoursList[i]):
			controllerList.append(topologyJudgementController(standardContour,contoursList[i],num))

	for i in range(0, len(controllerList)):
		controllerList[i].giveDependY()

def innerFillAttribute(groupFilePath,originalFile,standardContour,num):
	"""
	To give innerFill attribute all same group's contours point that is same point with standard contour

	Args : 
		groupFile :: str
			file's path that has group contours
		originalFile :: File
			file that has total contours
		standardContour :: RContour
		num :: int
            value of divie(insert None topology at divided position) 
	"""
	controllerList = []
	contoursList = []
	groupDict = json2groupDict(groupFilePath,originalFile)

	#create topologyJudgementController object
	for k in groupDict.keys():
		for i in range(0,len(groupDict[k])):
			contoursList.append(k.contours[groupDict[k][i]])

	for i  in range(0,len(contoursList)):
		if(standardContour != contoursList[i]):
			controllerList.append(topologyJudgementController(standardContour,contoursList[i],num))

	for i in range(0, len(controllerList)):
		controllerList[i].giveInnerFill()

def deleteAttribute(groupFilePath,originalFile,standardContour,num):
	"""
	To delete attributet all same group's contours point that is same point with standard contour

	Args : 
		groupFile :: str
			file's path that has group contours
		originalFile :: File
			file that has total contours
		standardContour :: RContour
		num :: int
            value of divie(insert None topology at divided position) 
	"""
	controllerList = []
	contoursList = []
	groupDict = json2groupDict(groupFilePath,originalFile)

	#create topologyJudgementController object
	for k in groupDict.keys():
		for i in range(0,len(groupDict[k])):
			contoursList.append(k.contours[groupDict[k][i]])

	for i  in range(0,len(contoursList)):
		controllerList.append(topologyJudgementController(standardContour,contoursList[i],num))

	for i in range(0, len(controllerList)):
		controllerList[i].deleteAttr()				