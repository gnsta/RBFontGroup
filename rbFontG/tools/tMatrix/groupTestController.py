from rbFontG.tools.tMatrix.PhaseTool import *
import math
import numpy as np
class groupTestController:
    """
    create by Kim heesup
    """
    def __init__(self,matrix,k):
        """
        conduct inspectation about whether same group
        
        Args:
            matrix : standard group

            k : value of arrnage same group
        """
        self.k = k
        self.matrix = matrix

        self.standardMatrix = np.array(self.matrix.getMatrix())
    def conCheckGroup2(self,con):
        """inspect that glyph inlcude same contour
        
        Args:
            con : want to check contour
            
        return:
        if contour is included return contour else return None
        
        2020/03/12
        modify by Kim heesup
        change by numpy and modify np.all condition
        """
        sl = self.matrix.getDivideStatus() #standard position
        
        newMatrix = Matrix(con, self.matrix.getdivk())
        
        cl = newMatrix.getDivideStatus()

        #grouping by hor,val
        compareX = []
        compareY = []

        nsl = np.array(sl)
        ncl = np.array(cl)

        ncompare = np.abs(nsl - ncl)
        

        if np.all(ncompare <= self.k) == True:
            return con
        else:
            return None

    def conCheckGroup(self,con):
        """
        2020/03/17
        create by Kim heesup
        inspeect that glyph include same contour to Chineses contour

        Args:
            con :: want to check contour
        
        return:
        if contour is included return contour else return Non
        """

        compareMatrix = np.array(Matrix(con,self.matrix.getdivk()).getMatrix())

        diffMatrixCount = (self.matrix.getdivk() ** 2) * (self.k/100)

        compareStat = (self.standardMatrix == compareMatrix)

        countDiff = compareStat[np.where(compareStat == False)]

        if len(countDiff) <= diffMatrixCount:
            return con
        else:
            return None



    def glyphCheckGroup(self,glyph):
        """Check that glyph include same contour
        
        Args:
            glyphs : checked glyphs
            
        return:
        if glyph has included contour return glyph and contou else return None
        """ 

        rl = []
        
        for con in glyph.contours:
            re = self.conCheckGroup(con)
            if (re != None):
                rl.append([glyph,con])

        if(len(rl) == 0):
            return None
        else:
            return rl