from rbFontG.tools.tMatrix.PhaseTool import *
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

        '''resultMatrix = []

        for i in range(0,self.matrix.getKx()):
            resultMatrix.append([])

        for i in range(0,len(resultMatrix)):
            for j in range(0,self.matrix.getKy()):
                resultMatrix[i].append(0)

        slMatrix = self.matrix.matrix
        clMatrix = newMatrix.matrix

        for i in range(0,len(slMatrix)):
            for j in range(0,len(slMatrix[i])):
                resultMatrix[i][j] = abs(slMatrix[i][j] - clMatrix[i][j])

        print("resultMatrix : ", resultMatrix)        

        #searching
        for i in range(0,len(resultMatrix)):
            for j in range(0,len(resultMatrix[i])):
                if(resultMatrix[i][j] > self.k):
                    return None

        return con'''

        #grouping by hor,val
        compareX = []
        compareY = []

        for i in range(0,self.matrix.getKx()):
            compareX.append(0)

        for i in range(0,self.matrix.getKy()):
            compareY.append(0)

        for i in range(0,len(sl[0])):
            compareX[i] = abs(sl[0][i] - cl[0][i])

        for i in range(0,len(sl[1])):
            compareY[i] = abs(sl[1][i] - cl[1][i])

        print("compareX" , compareX)
        print("compareY ", compareY)


        for  i in range(0,len(compareX)):
            if(self.k < compareX[i]):
                return None
        for i in range(0,len(compareY)):
            if(self.k < compareY[i]):
                return None

        return con
        

        #grouping by 2 value
        '''rx = 0
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
            return None'''   




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