from rbWindow.editWindow import *
from rbWindow.converter import *
<<<<<<< HEAD
import groupingTool.tMatrix.PhaseTool
import groupingTool.tMatrix.groupTestController
=======
import rbFontG.tools.tMatrix.PhaseTool
import rbFontG.tools.tMatrix.groupTestController
>>>>>>> parent of f58663d... merge completed
import rbWindow.editWindow as ew
import json
if __name__ == '__main__':
    
    g = CurrentGlyph()
    
    testPath = "/Users/font/Desktop/myungjo/groupTest.ufo"
    testFile = OpenFont(testPath,showInterface = False)
    
    jsonPath = "/Users/font/Desktop/myJSON.json"

    
    c = g.contours[0]
    
    standardMatrix = rbFontG.tools.tMatrix.PhaseTool.Matrix(c,3,3)
    
    compareController = rbFontG.tools.tMatrix.groupTestController.groupTestController(standardMatrix,0)
    
    groupList = []
    
    for idx, comGlyph in enumerate(testFile):

       resul = compareController.glyphCheckGroup(comGlyph)
       if(resul != None):
           groupList.append(resul)    

    groupDict = groupList2Dict(groupList)
    print(groupDict)
        
    groupDic2JSON(groupDict, jsonPath)
    recoverDic = json2groupDict(jsonPath)
    
    print(recoverDic)