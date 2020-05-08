from rbFontG.tools.tMatrix.PhaseTool import *
from rbFontG.tools.tMatrix.groupPointMatch import *
from jsonConverter.converter import *
from rbWindow.ExtensionSetting.extensionValue import *
from mojo.extensions import *

"""
2020/02/24
Created by heesup Kim
"""
def mselectAttribute(groupDict,standardMatrix):
    controllerList = []
    contoursList = []
    print("matrixButtonEvent standM:",standardMatrix)

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

def mpenPairAttribute(groupDict,standardMatrix):
    controllerList = []
    contoursList = []

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

def mdependXAttribute(groupDict,standardMatrix):
    controllerList = []
    contoursList = []

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

def mdependYAttribute(groupDict,standardMatrix):
    controllerList = []
    contoursList = []

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

def minnerFillAttribute(groupDict,standardMatrix):
    controllerList = []
    contoursList = []

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

def mdeleteAttribute(groupDict,standardMatrix,attribute):
    controllerList = []
    contoursList = []

    for k in groupDict.keys():
        for i in range(0,len(groupDict[k])):
            contoursList.append(k.contours[groupDict[k][i]])

    for i in range(0,len(contoursList)):
        for sp in standardMatrix.con.points:
            if(sp.selected == True):
                controllerList.append(groupPointMatchController(standardMatrix,sp,contoursList[i]))

    for i in range(0,len(controllerList)):
        controllerList[i].mdeleteAttr(attribute)

