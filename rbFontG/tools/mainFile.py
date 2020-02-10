import os
import math
import rbFontG.tools.PhaseTool
import rbFontG.tools.groupTestController

if __name__ == '__main__':
    g = CurrentGlyph()
    
    testPath = "/Users/font/Desktop/groupTest.ufo"
    testFile = OpenFont(testPath,showInterface = False)
    
    c = g.contours[0]
    
    standardMatrix = rbFontG.tools.PhaseTool.Matrix(c,3,3)
    
    compareController = rbFontG.tools.groupTestController.groupTestController(standardMatrix,0)
    
    for comGlyph in testFile:
            print(compareController.glyphCheckGroup(comGlyph))
    
    print(g)