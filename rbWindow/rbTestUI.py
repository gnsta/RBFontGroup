import os
import math
import rbFontG.tools.tMatrix.PhaseTool
import rbFontG.tools.tMatrix.groupTestController
import rbWindow.editWindow as ew
import pickle
#Test Code
if __name__ == '__main__':
    
    BroadNibBackgroundDefaultKey = "com.asaumierdemers.BroadNibBackground"
    
    #g = CurrentGlyph()
    
    testPath = "/Users/sslab/Downloads/groupTest.ufo"
    testFile = OpenFont(testPath,showInterface = False)
    
    
    
    # c = g.contours[0]
    
    # standardMatrix = rbFontG.tools.tMatrix.PhaseTool.Matrix(c,3,3)
    
    # compareController = rbFontG.tools.tMatrix.groupTestController.groupTestController(standardMatrix,0)
    
    # groupList = []
    
    # for idx, comGlyph in enumerate(testFile):

    #    resul = compareController.glyphCheckGroup(comGlyph)
    #    if(resul != None):
    #        groupList.append(resul)    
    
   
   
   
   
    #for i in groupList:
    #    print(i)
    
    # destFile = "/Users/sslab/Desktop/list.txt"
    # with open(destFile, 'w') as f:
    #     f.write(groupList[0])
    # f.close()
    # res = None
    
    # with open(destFile, 'r') as f:
    #     print(str(f.read()))
    # with open()
    groupList = None
    menuWindow = ew.EditGroupMenu(CurrentFont(), groupList, testFile)
