def getMaxXValue(con):
    """Get maximum x value about contours
    
    Args:
        con : Rcontour
    Return:
        maximum x value
    """
    max = -100000
    for p in con.points:
        if(max < p.x):
            max = p.x    
    return max

def getMinXValue(con):
    """Get minimum x value about contours
    
    Args:
        con : Rcontour
    Return:
        minimum x value
    """
    min = 100000
    for p in con.points:
        if(min > p.x):
            min = p.x
    return min

def getMaxYValue(con):
    """Get maximum y value about contours
    
    Args:
        con : Rcontour
    Return:
        maximum y value
    """
    max = -100000
    for p in con.points:
        if(max < p.y):
            max = p.y
    return max

def getMinYValue(con):
    """Get minimum y value about contours
    
    Args:
        con : Rcontour
    Return:
        minimum y value
    """
    min = 100000
    for p in con.points:
        if(min >  p.y):
            min = p.y
    return min


class Matrix:
    
    def __init__(self,con,kx,ky):
        """
        Divide Matrix by x & y. Calculate how many number of points are in the specific area of matrix.
        """
        
        self.matrix= []
        
        
        for i in range(0,kx):
            self.matrix.append([])
            
        for i in range(0,len((self.matrix))):
            for j in range(0,ky):
                self.matrix[i].append(0)    

        pl= []

        self.con = con
        self.kx = kx
        self.ky = ky

        self.maxx = 0
        self.minx = 0
        self.maxy = 0
        self.miny = 0

        for p in self.con.points:
            pl.append(self.getPointPart(p,kx,ky))

        for li in pl:
            self.matrix[li[0]][li[1]] = self.matrix[li[0]][li[1]] + 1

        
    def getKx(self):
        return self.kx

    def getKy(self):
        return self.ky

    def getCon(self):
        return self.con

    def getMinx(self):
        return self.minx
    def getMiny(self):
        return self.miny    

    def setKx(self, kx):
        self.kx = kx

    def setKy(self,ky):
        self.ky = ky

    def setCon(self,con):
        self.con = con              
        
            
    def getPointPart(self,p):
        """Get point's position if point's x is divided by kx and point's y is divided by ky.
    
        Args:
            p : Rpoint
        
            kx : dividing value of x
        
            ky : dividing value of y
        
        Return:
            point position
        """
    
        self.maxx = getMaxXValue(self.con) + 10
        self.minx = getMinXValue(self.con) - 10
        self.maxy = getMaxYValue(self.con) + 10
        self.miny = getMinYValue(self.con) - 10
    
        dis_x = maxx - minx
        dis_y = maxy - miny
    
        term_x = float(dis_x / self.kx)
        term_y = float(dis_y / self.ky)      
        
    
        compart_x = []
        compart_y = []
    
        compart_x.append(minx)
        compart_y.append(miny)
    
        num = 0
    
        while compart_x[num] + term_x < maxx:
            compart_x.append(compart_x[num] + term_x)
            num = num+1
        compart_x.append(maxx)

        num = 0
    
        while compart_y[num] + term_y < maxy:
            compart_y.append(compart_y[num] + term_y)
            num = num +1    
        compart_y.append(maxy)

    
        position_x = -1
        position_y = -1
    
        for i in range(0,len(compart_x)-1):
            if((compart_x[i] <= p.x)):
                position_x = i
            else:
                break
        
        for i in range(0,len(compart_y)-1):
            if((compart_y[i] <= p.y)):
                position_y = i
            else:
                break    
        
        rl = [position_x, position_y,p]
    
        return rl     
    
    
    def getPointCnt(self):
        res = 0
        for m in self.matrix:
            for j in m:
                res += j
        
        return res
        
    
    def getDivideStatus(self):
        """Get the number of point each case that points are arranged vertical or horizonal
    
        Args:       
            kx : dividing value of x
        
            ky : dividing value of y
        
        Return :
            list : [vertical arrange, horizonal arrange]     
        """
    
        point_stat = []
    
        rl = [[],[]]
    
        for i in range(0,self.kx):
            rl[0].append(0)
        
        for i in range(0,self.ky):
            rl[1].append(0)    
    
        for p in self.con.points:
            point_stat.append(self.getPointPart(p))
    
        for st in point_stat:
            cx = st[0]
            cy = st[1]
        
            rl[0][cx] = rl[0][cx] + 1
            rl[1][cy] = rl[1][cy] + 1
        
        return rl