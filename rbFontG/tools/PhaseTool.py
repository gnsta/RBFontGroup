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

def getPointPart(con,p,kx,ky):
    """Get point's position if point's x is divided by kx and point's y is divided by ky.
    
    Args:
        con : Rcontour
        
        p : Rpoint
        
        kx : dividing value of x
        
        ky : dividing value of y
        
    Return:
        point position
    """
    
    maxx = getMaxXValue(c) + 10
    minx = getMinXValue(c) - 10
    maxy = getMaxYValue(c) + 10
    miny = getMinYValue(c) - 10
    
    dis_x = maxx - minx
    dis_y = maxy - miny
    
    term_x = float(dis_x / kx)
    term_y = float(dis_y / ky)     
        
    
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
        
    rl = [position_x, position_y]
    
    return rl

def getDivideStatus(con,kx,ky):
    """Get the number of point each case that points are arranged vertical or horizonal
    
    Args:
        con : RContour
        
        kx : dividing value of x
        
        ky : dividing value of y
        
    Return :
        list : [vertical arrange, horizonal arrange]     
    """
    
    point_stat = []
    
    rl = [[],[]]
    
    for i in range(0,kx):
        rl[0].append(0)
        
    for i in range(0,ky):
        rl[1].append(0)    
    
    for p in con.points:
        point_stat.append(getPointPart(con,p,kx,ky))
    
    for st in point_stat:
        cx = st[0]
        cy = st[1]
        
        rl[0][cx] = rl[0][cx] + 1
        rl[1][cy] = rl[1][cy] + 1
        
    return rl      