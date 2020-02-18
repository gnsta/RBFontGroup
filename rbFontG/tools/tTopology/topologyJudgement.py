from rbFontG.tools.tTopology.topologyAssignment import *

class topologyJudgementController:
    def __init__(self,sCheckCon):
        """
        Make topologicalJudmentController that standaerd is sCheckCon's Rcontour

        Args:
        sCheckCon : checkCon object created by standard Rcontour
        """
        self.cCon = None
        self.k = sCheckCon.k
        
        self.sCheckCon = sCheckCon
        self.cCheckCon = None

        self.l1 = None
        self.l2 = None
        
    def topologyJudgement(self,cCon):
        """
        Judgement the Rcontour is same group with standartd contour

        Args:
        cCon : Rcontour that wnated to compare

        Return :
        if same group return True else false
        """
        self.cCon = cCon
        self.cCheckCon = checkCon(cCon,self.k)
        self.l1 = self.sCheckCon.tpPointList
        self.l2 = self.cCheckCon.tpPointList
        
        if(len(self.l1) != len(self.l2)):
            return False
            
            
        for i in range(0,len(self.l1)):
            if(self.l1[i].getX() != self.l2[i].getX()):
                return False
            if(self.l1[i].getY() != self.l2[i].getY()):
                return False
                
        return True


    def giveAttrPenPair(self):
        """
        Assign PenPair attribute to same point in same group
        """
        if self.cCheckCon == None:
            raise Exception('Please executed topologyJudgement method')

        for i in range(0,len(self.l1)):
            if(self.l1[i].point.selected == True):
                temp = get_attr(self.l1[i].point,'penPair')
                set_attr(self.l2[i].point,'penPair',temp)


    def giveDependX(self):
        """
        Assign DependX attribute to same point in same group
        """
        if self.cCheckCon == None:
            raise Exception('Please executed topologyJudgement method')
        for i in range(0,len(self.l1)):
            if(self.l1[i].point.selected == True):
                temp = get_attr(self.l1[i].point,'dependX')
                set_attr(self.l2[i].point,'dependX',temp)       

    def giveDependY(self):
        """
        Assign DependY attribute to same point in same group
        """
        if self.cCheckCon == None:
            raise Exception('Please executed topologyJudgement method')
        for i in range(0,len(self.l1)):
            if(self.l1[i].point.selected == True):
                temp = get_attr(self.l1[i].point,'dependY')
                set_attr(self.l2[i].point,'dependY',temp)

    def giveInnerType(self):
        """
        Assign innerType attribute to same point in same group
        """
        if self.cCheckCon == None:
            raise Exception('Please executed topologyJudgement method')
        for i in range(0,len(self.l1)):
            if(self.l1[i].point.selected == True):
                temp = get_attr(self.l1[i].point,'innerType')
                set_attr(self.l2[i].point,'innerType',temp)        