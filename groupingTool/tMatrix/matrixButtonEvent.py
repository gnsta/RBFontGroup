from groupingTool.tMatrix.PhaseTool import *
from groupingTool.tMatrix.groupPointMatch import *
from jsonConverter.converter import *
from rbWindow.ExtensionSetting import extensionValue
from rbWindow.ExtensionSetting.extensionValue import *
from mojo.extensions import *
from mojo.roboFont import CurrentGlyph
from attributeTool.strokeAttribute import *
"""
2020/02/24
Created by heesup Kim
"""
def mselectAttribute(groupDict,standardMatrix):
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
        mPoint = controllerList[i].matchPoint()
        if mPoint is not None:
            tmp = list()
            tmp.append(mPoint); tmp.append(mPoint.name);
            prevPointList.append(tmp)
            controllerList[i].mgiveSelected(mPoint)

    g = CurrentGlyph()
    for point in g.selectedPoints:
        tmp = list()
        tmp.append(point); tmp.append(point.name);
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
        mPoint = controllerList[i].matchPoint()
        if mPoint is not None:
            controllerList[i].mgiveAttrPenPair(mPoint)
            tmp = list()
            tmp.append(mPoint); tmp.append(mPoint.name);
            prevPointList.append(tmp)
            

    g = CurrentGlyph()
    for point in g.selectedPoints:
        tmp = list()
        tmp.append(point); tmp.append(point.name);
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
        mPoint = controllerList[i].matchPoint()
        if mPoint is not None:
            controllerList[i].mgiveDependX(mPoint)
            tmp = list()
            tmp.append(mPoint); tmp.append(mPoint.name);
            prevPointList.append(tmp)
            

    g = CurrentGlyph()
    for point in g.selectedPoints:
        tmp = list()
        tmp.append(point); tmp.append(point.name);
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
        mPoint = controllerList[i].matchPoint()
        if mPoint is not None:
            controllerList[i].mgiveDependY(mPoint)
            tmp = list()
            tmp.append(mPoint); tmp.append(mPoint.name);
            prevPointList.append(tmp)
            

    g = CurrentGlyph()
    for point in g.selectedPoints:
        tmp = list()
        tmp.append(point); tmp.append(point.name);
        prevPointList.append(tmp)


    restoreStack.push(prevPointList)
    setExtensionDefault(DefaultKey+".restoreStack", restoreStack)

def mgiveStrokeAttribute(groupDict,standardMatrix):
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
        mPoint = controllerList[i].matchPoint()
        if mPoint is not None:
            controllerList[i].mgiveStroke(mPoint)
            tmp = list()
            tmp.append(mPoint); tmp.append(mPoint.name);
            prevPointList.append(tmp)
            

    g = CurrentGlyph()
    for point in g.selectedPoints:
        tmp = list()
        tmp.append(point); tmp.append(point.name);
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
        mPoint = controllerList[i].matchPoint()
        if mPoint is not None:
            controllerList[i].mgiveInnerFill(mPoint)
            tmp = list()
            tmp.append(mPoint); tmp.append(mPoint.name);
            prevPointList.append(tmp)
            

    g = CurrentGlyph()
    for point in g.selectedPoints:
        tmp = list()
        tmp.append(point); tmp.append(point.name);
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
        if(standardMatrix.con != contoursList[i]):
            for sp in standardMatrix.con.points:
                if(sp.selected == True):
                    controllerList.append(groupPointMatchController(standardMatrix,sp,contoursList[i]))



    for i in range(0,len(controllerList)):
        mPoint = controllerList[i].matchPoint()
        if mPoint is not None:
            controllerList[i].mdeleteAttr(attribute,mPoint)
            tmp = list()
            tmp.append(mPoint); tmp.append(mPoint.name);
            prevPointList.append(tmp)
            

    g = CurrentGlyph()
    for point in g.selectedPoints:
        tmp = list()
        tmp.append(point); tmp.append(point.name);
        prevPointList.append(tmp)


    restoreStack.push(prevPointList)
    setExtensionDefault(DefaultKey+".restoreStack", restoreStack)