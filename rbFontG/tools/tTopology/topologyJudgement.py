from rbFontG.tools.tTopology.topologyAssignment import *

class topologyJudgementController:
    def __init__(self,sCon,cCon):
        self.sCon = sCon
        self.cCon = cCon
        
        self.sCheckCon = checkCon(sCon,100000000)
        self.cCheckCon = checkCon(cCon,100000000)
        
    def topologyJudgement(self):
        l1 = self.sCheckCon.tpPointList
        l2 = self.cCheckCon.tpPointList
        
        if(len(l1) != len(l2)):
            return False
            
            
        for i in range(0,len(l1)):
            if(l1[i].getX() != l2[i].getX()):
                return False
            if(l1[i].getY() != l2[i].getY()):
                return False
                
        return True