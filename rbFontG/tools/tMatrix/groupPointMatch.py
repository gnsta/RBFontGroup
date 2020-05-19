import copy
import math
from rbFontG.tools.tMatrix.PhaseTool import *
from fwig.tools import attributetools as at


class matrixRelocatePoint:
	"""
	2020/02/24
	create by kim heesup
	"""
	def __init__(self,point,rx,ry):
		"""
		contain RPoint, relocated x position, relocate y position
		"""
		self.point = point
		self.rx = rx
		self.ry = ry

class groupPointMatchController:
	def __init__(self,matrix,point,con):
		"""
		controll match modify contour point and group contours point

		Args:
			matrix : standard contour

			point :  selected point

			con : contour that is included group 
		"""
		self.matrix = matrix
		self.point = point
		self.con = con

		self.standardCon = matrix.getCon()

	def matchPoint(self):
		"""
		match modify contour point and group contours point

		return:
			matched point

		example(if divided 3 by 3)
		-------------------------------------------------
		|		|		|2	3	|
		|		|	       4|1		|
		-------------------------------------------------
		|		|		|		|
		|		|		|		|
		-------------------------------------------------
		|		|		|		|
		|		|		|		|
		-------------------------------------------------

		if selected point is point 1

		point 2, point 3 and point 4 is group contour's points

		result is that point 1 and point 2 are match
		
		Because they are included same part and has shortest distance in the part
		"""	 
		pointPart = self.matrix.getPointPart(self.point)
		getStandardMaxMin = GetMaxMinPointValue(self.matrix.con)

		#find all point that contour's point that is located pointPart
		originpl = [] #original points

		relocatepl = []

		checkMatrix = Matrix(self.con,self.matrix.getdivk())
		getCompareMaxMin = GetMaxMinPointValue(checkMatrix.con)

		for p in self.con.points:
			if(p.type != 'offcurve'):
				checkPart = checkMatrix.getPointPart(p)
				if((pointPart[0] == checkPart[0]) and (pointPart[1] == checkPart[1])):
					originpl.append(p)


		#locate contour exactly matrix's contour
		standardMinx = getStandardMaxMin.getMinXValue()
		standardMiny = getStandardMaxMin.getMaxYValue()

		checkMinx = getCompareMaxMin.getMinXValue()
		checkMiny = getCompareMaxMin.getMaxYValue()

		termX = checkMinx - standardMinx
		termY = checkMiny - standardMiny

		#apply pl
		for p in originpl:
			rx = p.x - termX
			ry = p.y - termY
			relocatepl.append(matrixRelocatePoint(p,rx,ry))



		#get point that get minimum distance
		minDist = 10000000000
		indx = -1

		for	i,o in enumerate(relocatepl):
			dist = math.sqrt(math.pow(self.point.x - o.rx,2) + math.pow(self.point.y - o.ry,2))
			if(minDist > dist):
				indx = i
				minDist = dist

		return relocatepl[indx].point

	def mgiveSelected(self):
		insertPoint = self.matchPoint()
		insertPoint.selected = True

	def mgiveAttrPenPair(self):
		insertPoint = self.matchPoint()
		temp = at.get_attr(self.point,'penPair')
		at.add_attr(insertPoint,'penPair',temp)

	def mgiveDependX(self):
		insertPoint = self.matchPoint()
		temp = at.get_attr(self.point,'dependX')
		at.add_attr(insertPoint,'dependX',temp)

	def mgiveDependY(self):
		insertPoint = self.matchPoint()
		temp = at.get_attr(self.point,'dependY')
		at.add_attr(insertPoint,'dependY',temp)

	def mgiveInnerFill(self):
		insertPoint = self.matchPoint()
		temp = at.get_attr(self.point,'innerFill')
		at.add_attr(insertPoint,'innerFill',temp)

	def mdeleteAttr(self,attribute):
		insertPoint = self.matchPoint()
		at.del_attr(insertPoint,attribute)		












