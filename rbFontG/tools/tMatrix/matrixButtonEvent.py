from rbFontG.tools.tMatrix.PhaseTool import *
from rbFontG.tools.tMatrix.groupPointMatch import *
from jsonConverter.converter import *

"""
2020/02/24
Created by heesup Kim
"""
def mselectAttribute(groupFilePath,originalFile,standardMatrix):
    """
    select points that are included same group
    Args:
        groupFilePath :: str
            json file that include same group in the form of dictionary

        originalFile :: RFont
            original ufo File

        standardMatrix :: Matrix
            Matrix that is created by standard Contour
    """
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
    """
    give penpair attribute to points that are included same group
    Args:
        groupFilePath :: str
            json file that include same group in the form of dictionary

        originalFile :: RFont
            original ufo File

        standardMatrix :: Matrix
            Matrix that is created by standard Contour
    """
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
    """
    give dependX attribute to points that are included same group
    Args:
        groupFilePath :: str
            json file that include same group in the form of dictionary

        originalFile :: RFont
            original ufo File

        standardMatrix :: Matrix
            Matrix that is created by standard Contour
    """
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
    """
    give dependY attribute to points that are included same group
    Args:
        groupFilePath :: str
            json file that include same group in the form of dictionary

        originalFile :: RFont
            original ufo File

        standardMatrix :: Matrix
            Matrix that is created by standard Contour
    """
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
    """
    give innerFill attribute to points that are included same group
    Args:
        groupFilePath :: str
            json file that include same group in the form of dictionary

        originalFile :: RFont
            original ufo File

        standardMatrix :: Matrix
            Matrix that is created by standard Contour
    """
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

def mdeleteAttribute(groupFilePath,originalFile,standardMatrix,attribute):
    """
    delete attribute to points that are included same group
    Args:
        groupFilePath :: str
            json file that include same group in the form of dictionary

        originalFile :: RFont
            original ufo File

        standardMatrix :: Matrix
            Matrix that is created by standard Contour

        attribute :: str
            delete Atrribute
    """
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
        controllerList[i].mdeleteAttr(attribute)

