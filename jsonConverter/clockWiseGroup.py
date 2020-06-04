import numpy as np
import json
from groupingTool.tMatrix import PhaseTool as pt
from groupingTool.tMatrix import groupTestController as gtc
from groupingTool.tMatrix import groupPointMatch as gpm

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
    현재 점의 진행방향이 시계방향인지 반시계 방향인지 확인

    Args:
        point1 :: RPoint
        point2 :: RPoint
        point3 :: RPoint
        조사하고자 하는 RPoint

    Returns :
        방향에 대한 정보 :: int
            시계방향이면 양수, 반시계 방향이면 음수
    """
    return (point1.x*point2.y) + (point2.x*point3.y) + (point3.x*point1.y) - ((point2.x*point1.y) + (point3.x*point2.y) + (point1.x*point3.y))

def sortByStartingPoint(pointList):
    """
    포인트 리스트에 대하여 y값을 기준으로 오름차순으로 정렬, 만약 y값이 값으면 x값을 기준으로 오름차순 정렬

    Args:
        pointList :: List
            정돈하고자 하는 리스트

    Returns: 
        정돈한 리스트 :: List
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
    """
    음수와 양수 값에 따라서 딕셔너리에 방향 횟수를 저장

     Args:
        value :: int
            방향값(getClockDirection 함수를 사용하여 반환된 값을 사용)
        dictionary :: Dict
            실질적인 데이터를 저장할 딕셔너리
    """
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
    """
    해당 컨투어의 점을 조사하여 시계방향과 반시계 방향을 판별하여 정보를 반환
    
     Args:
        con :: RContour
            조사하고자 하는 컨투어

    Returns: 
        방향횟수에 대한 정보를 가지고 있는 딕셔너리 :: Dict
    """
    
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
    
    
    if res['check'] == initCheck:
        if initCheck >=0:
            if res['reverse'] != 1:
                res['reverse'] -= 1
        else:
            if res['forword'] != 1: 
                res['forword'] -= 1
    
    return res            
    


                
            
