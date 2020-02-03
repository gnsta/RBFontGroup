import os
from fwig.tools import unicodetools as ut
from fwig.tools import attributetools as at

def get_maxX_value(con):
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

def get_minX_value(con):
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

def get_maxY_value(con):
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

def get_minY_value(con):
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

def get_pointPart(con,p,kx,ky):
    """Get point's position if point's x is divided by kx and point's y is divided by ky.
    
    Args:
        con : Rcontour
        
        p : Rpoint
        
        kx : dividing value of x
        
        ky : dividing value of y
        
    Return:
        point position
    """
    
    maxx = get_maxX_value(con) + 10
    minx = get_minX_value(con) - 10
    maxy = get_maxY_value(con) + 10
    miny = get_minY_value(con) - 10
    
    dis_x = maxx - minx
    dis_y = maxy - miny
    
    term_x = (dis_x / kx) + (dis_x % kx)
    term_y = (dis_y / ky) + (dis_y % ky)       
        
    
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
    