import os
import math
import rbFontG.tools.PhaseTool
import rbFontG.tools.groupTestController
import rbWindow.editWindow as ew
#Test Code
if __name__ == '__main__':
    
    BroadNibBackgroundDefaultKey = "com.asaumierdemers.BroadNibBackground"
    
    g = CurrentGlyph()
    
    testPath = "/Users/sslab/Desktop/myungjo/groupTest.ufo"
    testFile = OpenFont(testPath,showInterface = False)
    
    c = g.contours[0]
    
    standardMatrix = rbFontG.tools.PhaseTool.Matrix(c,3,3)
    
    compareController = rbFontG.tools.groupTestController.groupTestController(standardMatrix,0)
    
    groupList = []
    
    for idx, comGlyph in enumerate(testFile):

        resul = compareController.glyphCheckGroup(comGlyph)
        if(resul != None):
            groupList.append(resul)    
            
    menuWindow = ew.EditGroupMenu(CurrentFont(), groupList)
