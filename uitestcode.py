import os
import math
import rbFontG.tools.tMatrix.PhaseTool
import rbFontG.tools.tMatrix.groupTestController
import rbWindow.editWindow as ew
import pickle
from jsonConverter.makeJsonFile import *
from jsonConverter.clockWiseGroup import *

class FileExist(Exception):
    def __init__(self,msg):
        self.msg = msg
        
    def __str__(self):
        return self.msg


if __name__ == '__main__':
    
    BroadNibBackgroundDefaultKey = "com.asaumierdemers.BroadNibBackground"
    
    g = CurrentGlyph()
    testPath = "/Users/font/Desktop/groupTest.ufo"
    testFile = OpenFont(testPath,showInterface = False)

    
    
    
    
    # c = g.contours[0]
    
    # standardMatrix = rbFontG.tools.tMatrix.PhaseTool.Matrix(c,3,3)
    
    # compareController = rbFontG.tools.tMatrix.groupTestController.groupTestController(standardMatrix,0)
    
    # groupList = []
    
    
    # for idx, comGlyph in enumerate(testFile):

    #    resul = compareController.glyphCheckGroup(comGlyph)
    #    if(resul != None):
    #        groupList.append(resul)    
  
    # print(groupList)
   
    groupDict = None
    MakeJsonController(testPath,testFile)
    insert = dict()
    
    try:
        tempFileName = testPath.split('/')[-1]
        jsonFileName = './' + tempFileName.split('.')[0] + '.json'
        if os.path.exists(jsonFileName):
            raise FileExist('해당 파일은 이미 존재합니다')
        for tg in testFile:
            tempList = list()
            for tc in tg.contours:
                compare = getClockWiseList(tc)
                tempList.append(compare)
            insert[tg.name] = tempList
        
        with open(jsonFileName,'w',encoding = 'utf-8') as make_file:
            json.dump(insert,make_file,indent = '\t')
    except FileExist as e:
        print(e)
        
        
    
    #menuWindow = ew.EditGroupMenu(CurrentFont(), groupDict, testFile,jsonFileName)