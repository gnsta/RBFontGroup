import numpy as np
import json
from rbFontG.tools.tMatrix import PhaseTool as pt
from rbFontG.tools.tMatrix import groupTestController as gtc
from rbFontG.tools.tMatrix import groupPointMatch as gpm

def consistClockWise(con):
    pointList = list(con.points)

    if(con.clockwise == False):
        pointList.reverse()
        rp = pointList[-1]
        pointList.insert(0,rp)
        del(pointList[-1])

    return pointList


def getClockDirection(point1 , point2, point3):
    """
    get value that indicate forword clockwise or reverse clockwise

    return : int
        if reverse clockwise return positive value else if forword clockwise return negative value 
    """
    return (point1.x*point2.y) + (point2.x*point3.y) + (point3.x*point1.y) - ((point2.x*point1.y) + (point3.x*point2.y) + (point1.x*point3.y))

def sortByStartingPoint(pointList):
    """
    sort by list's index 0 point has minimum y value. If  value same choose minimum x value

    Return: List
        sorted List
    """
    minY = 10000000000
    minX = 10000000000
        
    candidatePoints = []
    startPoint = None
    slist = []
        
    for i in range(0,len(pointList)):
        if(pointList[i].type != "offcurve"):
            if(minY > pointList[i].y):
                minY = pointList[i].y
                
    for i in range(0,len(pointList)):
        if(pointList[i].type != "offcurve"):
            if(minY == pointList[i].y):
                candidatePoints.append(pointList[i])
                
    for i in range(0,len(candidatePoints)):
        if(candidatePoints[i].type != "offcurve"):
            if(minX > candidatePoints[i].x):
                minX = candidatePoints[i].x
                
    for i in range(0,len(candidatePoints)):
        if(candidatePoints[i].type != "offcurve"):
            if(minX == candidatePoints[i].x):
                startPoint = candidatePoints[i]
                
                        
    num = -1
    for i in range(0,len(pointList)):
        if((startPoint.x == pointList[i].x) and (startPoint.y == pointList[i].y)):
            num = i
            break
                
    ll = pointList[i:len(pointList)]
    rl = pointList[0:i]
        
    offSlist = ll + rl
    #remove offCurvce
    for i in range(0,len(offSlist)):
        if(offSlist[i].type != "offcurve"):
            slist.append(offSlist[i])
    return slist

def renewDict(value,dictionary):
    if dictionary['check'] == 0:
        if value >= 0:
            dictionary['check'] = 1
            dictionary['reverse'] += 1
        else:
            dictionary['check'] = -1
            dictionary['forword'] += 1
    else:
        if value >= 0:
            if dictionary['check'] == -1:
                dictionary['reverse'] += 1
                dictionary['check'] = 1
        else:
            if dictionary['check'] == 1:
                dictionary['forword'] += 1
                dictionary['check'] = -1
                    
                        
def getClockWiseList(con):
    
    res = {'reverse' : 0 , 'forword' : 0, 'check' : 0}
    pointList = consistClockWise(con)
    sortPointList = sortByStartingPoint(pointList)
    initCheck = 0
    
    for i in range(0,len(sortPointList)-2):
        value = getClockDirection(sortPointList[i],sortPointList[i+1],sortPointList[i+2])
        if res['check'] == 0:
            if value >= 0:
                initCheck = 1
            else:
                initCheck = -1
        
        renewDict(value,res)
    
    value = getClockDirection(sortPointList[len(sortPointList) - 2], sortPointList[len(sortPointList) - 1], sortPointList[0])
    renewDict(value,res)
    value = getClockDirection(sortPointList[len(sortPointList) - 1], sortPointList[0], sortPointList[1])
    renewDict(value,res)
    
    #print(res)
    
    if res['check'] == initCheck:
        if initCheck >=0:
            if res['reverse'] != 1:
                res['reverse'] -= 1
        else:
            if res['forword'] != 1: 
                res['forword'] -= 1
    
    return res            
    


                
            
