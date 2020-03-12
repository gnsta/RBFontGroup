from rbFontG.tools.tTopology.topologyAssignment import *
from fwig.tools import attributetools as at

class topologyJudgementController:
    """
    Create by Kim heesup
    """
    def __init__(self,sCon,cCon,k):
        """
        Args: 
            sCon :: RContour
                standard contour
            cCon :: RContour
                comparative contour
            k :: int
                value of divie(insert None topology at divided position)    

        2020/02/24
        modify by Kim heesup
        인자로 k추가 후 테스트 필요함        

        """
        self.sCon = sCon
        self.cCon = cCon
        self.k = k
        
        self.sCheckCon = checkCon(sCon,self.k)
        self.cCheckCon = checkCon(cCon,self.k)
        
    def topologyJudgement(self):
        """
        To Judgement whether or not the contour is same group
        
        Return: bool
            if same group return True else False
        """
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

    def giveSelected(self):
        """
        select to same point in same group
        """
        l1 = self.sCheckCon.tpPointList
        l2 = self.cCheckCon.tpPointList
        
        if self.cCheckCon == None:
            raise Exception('Please executed topologyJudgement method')

        for i in range(0,len(l1)):
            if(l1[i].point.selected == True):
                 l2[i].point.selected = True    
        

    def giveAttrPenPair(self):
        """
        Assign PenPair attribute to same point in same group
        """
        if self.cCheckCon == None:
            raise Exception('Please executed topologyJudgement method')

        l1 = self.sCheckCon.tpPointList
        l2 = self.cCheckCon.tpPointList    

        for i in range(0,len(l1)):
            if(l1[i].point.selected == True):
                temp = at.get_attr(l1[i].point,'penPair')
                at.add_attr(l2[i].point,'penPair',temp)
                
                                
    def giveDependX(self):
        """
        Assign dependX attribute to same point in same group
        """
        if self.cCheckCon == None:
            raise Exception('Please executed topologyJudgement method')

        l1 = self.sCheckCon.tpPointList
        l2 = self.cCheckCon.tpPointList    

        for i in range(0,len(l1)):
            if(l1[i].point.selected == True):
                temp = at.get_attr(l1[i].point,'dependX')
                at.add_attr(l2[i].point,'dependX',temp)

    def giveDependY(self):
        """
        Assign dependY attribute to same point in same group
        """
        if self.cCheckCon == None:
            raise Exception('Please executed topologyJudgement method')

        l1 = self.sCheckCon.tpPointList
        l2 = self.cCheckCon.tpPointList    

        for i in range(0,len(l1)):
            if(l1[i].point.selected == True):
                temp = at.get_attr(l1[i].point,'dependY')
                at.add_attr(l2[i].point,'dependY',temp)

    def giveInnerFill(self):
        """
        Assign innerfill attribute to same point in same group
        """
        if self.cCheckCon == None:
            raise Exception('Please executed topologyJudgement method')

        l1 = self.sCheckCon.tpPointList
        l2 = self.cCheckCon.tpPointList    

        for i in range(0,len(l1)):
            if(l1[i].point.selected == True):
                temp = at.get_attr(l1[i].point,'innerFill')
                at.add_attr(l2[i].point,'innerFill',temp)

    def deleteAttr(self,attribute):
        """
        delete attribute to same point in same group
        """
        if self.cCheckCon == None:
            raise Exception('Please executed topologyJudgement method')

        l1 = self.sCheckCon.tpPointList
        l2 = self.cCheckCon.tpPointList    

        for i in range(0,len(l1)):
            if(l1[i].point.selected == True):
                at.del_attr(l2[i].point,attribute)

