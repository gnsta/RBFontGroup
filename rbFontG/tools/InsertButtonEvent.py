import os
from fwig.tools import attributetools as at

def BInsertPenPair(con,penNum):
    """insert atrribute penPair when user select two points (Button event)
    
    Args:
        con : Rcontour
        
        penNum : int
            penPair number
             
    Returns:
        Boolean
        if user selecte not exactly two point return flase
        if two point location exactly same return false
        other then that return true                        
    """
    
    check = 0
    
    s_points =[]
    
    for p in con.points:
        if((p.selected == True) and (p.type != 'offcurve')):
            check = check +1
            s_points.append(p)
            
    if check != 2:
        return False
    
    for p in con.points:
        temp_attr = at.Attribute(p)
        if(type(temp_attr.get_attr('penPair')) == str):            
            if(int(temp_attr.get_attr('penPair')[1]) == penNum):
                return False      
    
    point_attr1 = at.Attribute(s_points[0])
    point_attr2 = at.Attribute(s_points[1])
    
    s1 = 'z' + str(penNum) + 'l'
    s2 = 'z' + str(penNum) + 'r'
    
    if(s_points[0].x < s_points[1].x):       
        point_attr1.add_attr('penPair' , s1)
        point_attr2.add_attr('penPair' , s2)
    elif(s_points[0].x > s_points[1].x):
        point_attr1.add_attr('penPair',s2)
        point_attr2.add_attr('penPair',s1)
    else:
        return false        
    
    print(point_attr1.point.name)
    print(point_attr2.point.name)
                   
    return True    
    
 