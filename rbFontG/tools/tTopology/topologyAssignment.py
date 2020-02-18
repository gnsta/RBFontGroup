from rbFontG.tools.tMatrix.PhaseTool import *
class topologicalRpoint:
    def __init__(self,point):
        self.point = point
        self.x = -1
        self.y = -1
        
    def setX(self,num):
        self.x = num
    def setY(self,num):
        self.y = num
    def getX(self):
        return self.x
    def getY(self):
        return self.y        
            


class checkCon:
    def __init__(self,con,k):
        """
        Args:

        con : Rcontour
        
        k : divid value that insert None value When designate topological
        example

        |-----------point-----------None-----------point----------|
        (insert None value where diviede)
        """
        self.con = con
        self.k = k
        self.pointList = list(con.points)
        
        self.consistClockWise()
        self.slist = self.sortByStartingPoint()

        self.maxx = getMaxXValue(self.con)
        self.minx = getMinXValue(self.con)
        self.maxy = getMaxYValue(self.con)
        self.miny = getMinYValue(self.con)

        self.dis_x = self.maxx - self.minx
        self.dis_y = self.maxy - self.miny

        self.term_x = float(self.dis_x / self.k)
        self.term_y = float(self.dis_y / self.k)

        self.tpPointList = self.assignmentTopological()
    
    def consistClockWise(self):
        """
        To be consisit contours clockwise if contour's clockwise False reverse the clockwise
        """
        
        if(self.con.clockwise == False):
            self.pointList.reverse()
            rp = self.pointList[-1]
            self.pointList.insert(0,rp)
            del(self.pointList[-1])
            
    def sortByStartingPoint(self):
        """
        Sort List By index 0 point has minimun Y value, if Y value same designate point has minimum x value

        Return :
        topologicalRpoint that not assign X Topological and Y Topological object List(just sorted by start point)
        """
        minY = 10000000000
        minX = 10000000000
        
        candidatePoints = []
        startPoint = None
        slist = []
        
        for i in range(0,len(self.pointList)):
            if(minY > self.pointList[i].y):
                minY = self.pointList[i].y
                
        for i in range(0,len(self.pointList)):
            if(minY == self.pointList[i].y):
                candidatePoints.append(self.pointList[i])
                
        for i in range(0,len(candidatePoints)):
            if(minX > candidatePoints[i].x):
                minX = candidatePoints[i].x
                
        for i in range(0,len(candidatePoints)):
            if(minX == candidatePoints[i].x):
                startPoint = candidatePoints[i]
                
                        
        num = -1
        for i in range(0,len(self.pointList)):
            if((startPoint.x == self.pointList[i].x) and (startPoint.y == self.pointList[i].y)):
                num = i;
                break;
                
        ll = self.pointList[i:len(self.pointList)]
        rl = self.pointList[0:i]
        
        offSlist = ll + rl
        #remove offCurvce
        for i in range(0,len(offSlist)):
            if(offSlist[i].type != "offcurve"):
                slist.append(offSlist[i])
        return slist
        
             
    def assignmentTopological(self):
        """
        Assign X Topological and Y Topological about  Sorted List that include topologicalRpoint

        Return :
        topologicalRpoint that assign X Topological and Y Topological object List
        """
        sortByX = sorted(self.pointList,key = lambda RPoint: RPoint.x)
        sortByY = sorted(self.pointList,key = lambda RPoint: RPoint.y)
        
        sortByXNone = []
        sortByYNone = []
        
        
        tx = self.term_x
        ty = self.term_y
        idx = 0
        
        tpRpl =[]
        
        while (idx < len(sortByX)):
            if(tx < sortByX[idx].x):
                sortByXNone.append(None)
                tx = tx + self.term_x
            else:
                sortByXNone.append(sortByX[idx])
                idx = idx + 1
        
        idx = 0
                
        while(idx < len(sortByY)):
            if(ty < sortByY[idx].y):
                sortByYNone.append(None)
                ty = ty + self.term_y
            else:
                sortByYNone.append(sortByY[idx])
                idx = idx +1
                           
                
        #assign topological
        for i in range(0,len(self.slist)):
            intpPoint = topologicalRpoint(self.slist[i])
            #assign x topological
            for j in range(0,len(sortByXNone)):
                if(sortByXNone[j] == None):
                    continue
                if((intpPoint.point.x == sortByXNone[j].x) and (intpPoint.point.y == sortByXNone[j].y)):
                    intpPoint.setX(j)
            #assign y topological
            for j in range(0,len(sortByYNone)):
                if(sortByYNone[j] == None):
                    continue
                if((intpPoint.point.x == sortByYNone[j].x) and (intpPoint.point.y == sortByYNone[j].y)):
                    intpPoint.setY(j)
            tpRpl.append(intpPoint)
            
        return tpRpl