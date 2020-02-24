from rbFontG.tools.tMatrix.PhaseTool import *
from rbFontG.tools.tMatrix.groupPointMatch import *
from jsonConverter.converter import *

"""
2020/02/24
Created by heesup Kim
"""
def mselectAttribute(groupFilePath,originalFile,standardMatrix):
    controllerList = []
    contoursList = []
    groupDict = json2groupDict(groupFilePath,originalFile)

    for k in groupDict.keys():
        for i in range(0,len(groupDict[k])):
            contoursList.append(k.contours[groupDict[k][i]])

    for i in range(0,len(contoursList)):
        if(standardMatrix.con != contoursList[i]):
            for sp in standardMatrix.con.points:
                if(sp.selected == True):
                    controllerList.append(groupPointMatchController(standardMatrix,sp,contoursList[i]))

    for i in range(0,len(controllerList)):
        controllerList[i].mgiveSelected()

def mpenPairAttribute(groupFilePath,originalFile,standardMatrix):
    controllerList = []
    contoursList = []
    groupDict = json2groupDict(groupFilePath,originalFile)

    for k in groupDict.keys():
        for i in range(0,len(groupDict[k])):
            contoursList.append(k.contours[groupDict[k][i]])

    for i in range(0,len(contoursList)):
        if(standardMatrix.con != contoursList[i]):
            for sp in standardMatrix.con.points:
                if(sp.selected == True):
                    controllerList.append(groupPointMatchController(standardMatrix,sp,contoursList[i]))

    for i in range(0,len(controllerList)):
        controllerList[i].mgiveAttrPenPair()

def mdependXAttribute(groupFilePath,originalFile,standardMatrix):
    controllerList = []
    contoursList = []
    groupDict = json2groupDict(groupFilePath,originalFile)

    for k in groupDict.keys():
        for i in range(0,len(groupDict[k])):
            contoursList.append(k.contours[groupDict[k][i]])

    for i in range(0,len(contoursList)):
        if(standardMatrix.con != contoursList[i]):
            for sp in standardMatrix.con.points:
                if(sp.selected == True):
                    controllerList.append(groupPointMatchController(standardMatrix,sp,contoursList[i]))

    for i in range(0,len(controllerList)):
        controllerList[i].mgiveDependX()

def mdependYAttribute(groupFilePath,originalFile,standardMatrix):
    controllerList = []
    contoursList = []
    groupDict = json2groupDict(groupFilePath,originalFile)

    for k in groupDict.keys():
        for i in range(0,len(groupDict[k])):
            contoursList.append(k.contours[groupDict[k][i]])

    for i in range(0,len(contoursList)):
        if(standardMatrix.con != contoursList[i]):
            for sp in standardMatrix.con.points:
                if(sp.selected == True):
                    controllerList.append(groupPointMatchController(standardMatrix,sp,contoursList[i]))

    for i in range(0,len(controllerList)):
        controllerList[i].mgiveDependY()

def minnerFillAttribute(groupFilePath,originalFile,standardMatrix):
    controllerList = []
    contoursList = []
    groupDict = json2groupDict(groupFilePath,originalFile)

    for k in groupDict.keys():
        for i in range(0,len(groupDict[k])):
            contoursList.append(k.contours[groupDict[k][i]])

    for i in range(0,len(contoursList)):
        if(standardMatrix.con != contoursList[i]):
            for sp in standardMatrix.con.points:
                if(sp.selected == True):
                    controllerList.append(groupPointMatchController(standardMatrix,sp,contoursList[i]))

    for i in range(0,len(controllerList)):
        controllerList[i].mgiveInnerFill()

def mdeleteAttribute(groupFilePath,originalFile,standardMatrix):
    controllerList = []
    contoursList = []
    groupDict = json2groupDict(groupFilePath,originalFile)

    for k in groupDict.keys():
        for i in range(0,len(groupDict[k])):
            contoursList.append(k.contours[groupDict[k][i]])

    for i in range(0,len(contoursList)):
        for sp in standardMatrix.con.points:
            if(sp.selected == True):
                controllerList.append(groupPointMatchController(standardMatrix,sp,contoursList[i]))

    for i in range(0,len(controllerList)):
        controllerList[i].mdeleteAttr()

