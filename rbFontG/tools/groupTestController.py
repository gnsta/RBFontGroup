from rbFontG.tools.PhaseTool import *
import math
class groupTestController:
    def __init__(self,matrix,k):
        """
        conduct inspectation about whether same group
        
        Args:
            matrix : standard group

            k : value of arrnage same group
        """
        self.k = k
        self.matrix = matrix
    def conCheckGroup(self,con):
        """inspect that glyph inlcude same contour
        
        Args:
            con : want to check contour
            
        return:
        if contour is included return contour else return None
        """
        sl = self.matrix.getDivideStatus() #standard position
        
        newMatrix = Matrix(con, self.matrix.getKx(), self.matrix.getKy())
        
        cl = newMatrix.getDivideStatus()
        
        print("*************************************")
        print("sl : " ,sl)
        print("cl : " , cl)
        print("*************************************")
        
        rx = 0
        ry = 0
        
        for i in range(0,len(sl)):
            for j in range(0,len(sl[i])):
                if(i == 0):
                    rx = rx + abs(sl[i][j] - cl[i][j])
                elif(i == 1):
                    ry = ry + abs(sl[i][j] - cl[i][j])

        rl = [rx,ry]
        
        print("rl : " , rl)

        distance = math.sqrt(math.pow(rx,2) + math.pow(ry,2))
        
        print("distance : " , distance)

        if(distance <= self.k):
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
        kx = self.matrix.getKx()
        ky = self.matrix.getKy()


        rl = []
        
        for con in glyph.contours:
            re = self.conCheckGroup(con)
            if (re != None):
                rl.append([glyph,con])

        if(len(rl) == 0):
            return None
        else:
            return rl