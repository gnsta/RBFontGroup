import os
import math
import rbFontG.tools.PhaseTool
import rbFontG.tools.groupTestController

if __name__ == '__main__':
    g = CurrentGlyph()
    
    testPath = "/Users/font/Desktop/groupTest.ufo"
    testFile = OpenFont(testPath,showInterface = False)
    
    c = g.contours[0]

    c.selected = True
    
    standardMatrix = rbFontG.tools.PhaseTool.Matrix(c,3,3)
    
    compareController = rbFontG.tools.groupTestController.groupTestController(standardMatrix,0)

    groupList = []
    
    for comGlyph in testFile:
            resul = compareController.glyphCheckGroup(comGlyph)

            if(resul != None):
            	groupList.append(resul)
            	for i in range(0,len(resul)):
            		resul[i][1] = True

    
    print(groupList)