
import numpy as np
"""
2020/03/09
modify by Kim heesup

improve performance
"""
class GetMaxMinPointValue:
    """
    get contours maximum, minimun x,y value
    """
    def __init__(self,con):
        self.con = con
        self.p_list = []

        for p in self.con.points:
            if(p.type != "offcurve"):
                self.p_list.append(p)

        self.sortByX = sorted(self.p_list,key = lambda RPoint : RPoint.x)
        self.sortByY = sorted(self.p_list,key = lambda RPoint : RPoint.y)

    def getMaxXValue(self):
        return self.sortByX[-1].x
    def getMinXValue(self):
        return self.sortByX[0].x
    def getMaxYValue(self):
        return self.sortByY[-1].y
    def getMinYValue(self):
        return self.sortByY[0].y     

class Matrix:
    """
    create by Kim heesup
    """
    
    def __init__(self,con,divk):
        """
        Divide Matrix by x & y. Calculate how many number of points are in the specific area of matrix.
        """
        self.divk = divk
        self.con = con
        self.matrix = None
                            
    def getdivk(self):
        return self.divk 
    def getCon(self):
        return self.con            

    def getPointPart(self,p):
        """Get point's position if point's x is divided by kx and point's y is divided by ky.
    
        Args:
            p : Rpoint
        
            kx : dividing value of x
        
            ky : dividing value of y
        
        Return:
            point position
        """

        #getMinMax = GetMaxMinPointValue(self.con)
    
        #maxx = getMinMax.getMaxXValue() + 10
        #minx = getMinMax.getMinXValue() - 10
        #maxy = getMinMax.getMaxYValue() + 10
        #miny = getMinMax.getMinYValue() - 10

        maxx = self.con.bounds[2] + 10
        minx = self.con.bounds[0] - 10
        maxy = self.con.bounds[3] + 10
        miny = self.con.bounds[1] - 10
    
        term_x = float((maxx - minx) / self.divk)
        term_y = float((maxy - miny) / self.divk)      
        

        position_x = int((p.x - minx) // term_x);
        position_y = int((p.y - miny) // term_y);

        if(position_x >= self.divk):
            position_x = position_x - 1;
        if(position_y >= self.divk):
            position_y = position_y - 1;
        
        rl = [position_x, position_y]
    
        return rl     
    
    
    def getPointCnt(self):
        res = 0
        for m in self.matrix:
            for j in m:
                res += j
        
        return res
        
    
    def getDivideStatus(self):
        """Get the number of point each case that points are arranged vertical or horizontal
    
        Args:       
            kx : dividing value of x
        
            ky : dividing value of y
        
        Return :
            list : [vertical arrange, horizonal arrange]     
        """
    
        point_stat = []
    
        rl = []
        xrl = np.zeros(self.divk)
        yrl = np.zeros(self.divk)
    
    
        for p in self.con.points:
            if(p.type != "offcurve"):
                point_stat.append(self.getPointPart(p))
    
        for st in point_stat:
            cx = st[0]
            cy = st[1]

            xrl[cx] += 1
            yrl[cy] += 1

        rl.append(xrl.tolist())
        rl.append(yrl.tolist())
        
        return rl

    def getMatrix(self):
        """
        get matrix status that indicate how much points are located in specific area
        """

        if(self.matrix is None):

            self.matrix = []

            for i in range(0,self.divk):
                self.matrix.append([])
            
            for i in range(0,len((self.matrix))):
                for j in range(0,self.divk):
                    self.matrix[i].append(0)

            pl= []

            for p in self.con.points:
                if(p.type != "offcurve"):
                    pl.append(self.getPointPart(p))

            for li in pl:
                self.matrix[li[0]][li[1]] = self.matrix[li[0]][li[1]] + 1

            return self.matrix
        else:
            return self.matrix




