from groupingTool.tMatrix.PhaseTool import *
from groupingTool.tMatrix.groupPointMatch import *
from jsonConverter.converter import *
from rbWindow.ExtensionSetting import extensionValue
from rbWindow.ExtensionSetting.extensionValue import *
from mojo.extensions import *
from mojo.roboFont import CurrentGlyph
"""
2020/02/24
Created by heesup Kim
"""
def mselectAttribute(groupDict,standardMatrix):
    controllerList = []
    contoursList = []
    prevPointList = list()
    restoreStack = getExtensionDefault(DefaultKey+".restoreStack")

    empty = restoreStack.isEmpty()

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
        if controllerList[i].matchPoint() is not None and empty is True:
            tmp = list()
            tmp.append(controllerList[i].matchPoint()); tmp.append(controllerList[i].matchPoint().name)
            prevPointList.append(tmp)

    if empty is True:
        g = CurrentGlyph()
        for point in g.selectedPoints:
            tmp = list()
            tmp.append(point); tmp.append(point.name)
            prevPointList.append(tmp)

        restoreStack.push(prevPointList)
        setExtensionDefault(DefaultKey+".restoreStack", restoreStack)
        

def mpenPairAttribute(groupDict,standardMatrix):
    controllerList = []
    contoursList = []
    prevPointList = list()
    restoreStack = getExtensionDefault(DefaultKey+".restoreStack")



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
        if controllerList[i].matchPoint() is not None:
            tmp = list()
            tmp.append(controllerList[i].matchPoint()); tmp.append(controllerList[i].matchPoint().name)
            prevPointList.append(tmp)

    g = CurrentGlyph()
    for point in g.selectedPoints:
        tmp = list()
        tmp.append(point); tmp.append(point.name)
        prevPointList.append(tmp)

    restoreStack.push(prevPointList)
    setExtensionDefault(DefaultKey+".restoreStack", restoreStack)

def mdependXAttribute(groupDict,standardMatrix):
    controllerList = []
    contoursList = []
    prevPointList = list()
    restoreStack = getExtensionDefault(DefaultKey+".restoreStack")

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
        if controllerList[i].matchPoint() is not None:
            tmp = list()
            tmp.append(controllerList[i].matchPoint()); tmp.append(controllerList[i].matchPoint().name)
            prevPointList.append(tmp)

    g = CurrentGlyph()
    for point in g.selectedPoints:
        tmp = list()
        tmp.append(point); tmp.append(point.name)
        prevPointList.append(tmp)

    restoreStack.push(prevPointList)
    setExtensionDefault(DefaultKey+".restoreStack", restoreStack)

def mdependYAttribute(groupDict,standardMatrix):
    controllerList = []
    contoursList = []
    prevPointList = list()
    restoreStack = getExtensionDefault(DefaultKey+".restoreStack")

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
        if controllerList[i].matchPoint() is not None:
            tmp = list()
            tmp.append(controllerList[i].matchPoint()); tmp.append(controllerList[i].matchPoint().name)
            prevPointList.append(tmp)

    g = CurrentGlyph()
    for point in g.selectedPoints:
        tmp = list()
        tmp.append(point); tmp.append(point.name)
        prevPointList.append(tmp)

    restoreStack.push(prevPointList)
    setExtensionDefault(DefaultKey+".restoreStack", restoreStack)

def minnerFillAttribute(groupDict,standardMatrix):
    controllerList = []
    contoursList = []
    prevPointList = list()
    restoreStack = getExtensionDefault(DefaultKey+".restoreStack")



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

        if controllerList[i].matchPoint() is not None:
            tmp = list()
            tmp.append(controllerList[i].matchPoint()); tmp.append(controllerList[i].matchPoint().name)
            prevPointList.append(tmp)

    g = CurrentGlyph()
    for point in g.selectedPoints:
        tmp = list()
        tmp.append(point); tmp.append(point.name)
        prevPointList.append(tmp)

    restoreStack.push(prevPointList)
    setExtensionDefault(DefaultKey+".restoreStack", restoreStack)
        
def mdeleteAttribute(groupDict,standardMatrix,attribute):
    controllerList = []
    contoursList = []
    prevPointList = list()
    restoreStack = getExtensionDefault(DefaultKey+".restoreStack")


    for k in groupDict.keys():
        for i in range(0,len(groupDict[k])):
            contoursList.append(k.contours[groupDict[k][i]])

    for i in range(0,len(contoursList)):
        for sp in standardMatrix.con.points:
            if(sp.selected == True):
                controllerList.append(groupPointMatchController(standardMatrix,sp,contoursList[i]))

    for i in range(0,len(controllerList)):
        controllerList[i].mdeleteAttr(attribute)
        if controllerList[i].matchPoint() is not None:
            tmp = list()
            tmp.append(controllerList[i].matchPoint()); tmp.append(controllerList[i].matchPoint().name)
            prevPointList.append(tmp)


    g = CurrentGlyph()
    for point in g.selectedPoints:
        tmp = list()
        tmp.append(point); tmp.append(point.name)
        prevPointList.append(tmp)

    restoreStack.push(prevPointList)
    setExtensionDefault(DefaultKey+".restoreStack", restoreStack)

