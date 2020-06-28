import copy
import math
from groupingTool.tMatrix.PhaseTool import *
from fwig.tools import attributetools as at
"""
	2020/02/24
	create by kim heesup
"""

def calcDirection(con,point):
	"""
	포인트 데이터가 해당 컨투어의 어느쪽에 위치하고 있는지 확인하는 함수

	Args:
		con :: RContour
			조사하고자 하는 컨투어
		point :: RPoint
			RContour안에 있는 조사하고자 하는 점
	
	Returs :
		위치 정보 :: list
			[up,down,left,right]
	"""

	dr = [10,-10,0,0]
	dc = [0,0,-10,10]

	#standard direction
	checkCdirection = [0,0,0,0]
	r = point.y
	c = point.x
	for i in range(0,4):
		nr = r + dr[i]
		nc = c + dc[i]
		if con.pointInside((nc,nr)):
			checkCdirection[i] = 1

	return checkCdirection


class matrixRelocatePoint:
	"""
	점과 위치와 방향정보를 새롭게 객체를 생성하여 연산을 진행하기 위한 class

	Args:
		point :: RPoint
			재배치 하고자 하는 점
		rx :: int
			x축의 재배치 위치
		ry :: int
			y축의 재배치 위치
		direction :: list
			calcDirection함수로 인한 결과
			
	"""
	def __init__(self,point,rx,ry,direction):
		self.point = point
		self.rx = rx
		self.ry = ry
		self.direction = direction

class groupPointMatchController:
	def __init__(self,matrix,point,con):
		"""
		같은 그룹 내에서의 컨투어의 점들에 대하여 최대한 비슷한 점을 골라냄

		Args:
			matrix :: Matrix Object 
				기준 Matrix 객체

			point :: RPoint  
				매칭을 시켜줄 점

			con :: RContour 
				그룹 내에 있는 컨투어
		"""
		self.matrix = matrix
		self.point = point
		self.con = con

		self.standardCon = matrix.getCon()

	def matchPoint(self):
		"""
		포인트를 매칭 시켜줌

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


		#additional mechanism
		dr = [10,-10,0,0]
		dc = [0,0,-10,10]

		#standard direction
		checkSdirection = [0,0,0,0]
		r = self.point.y
		c = self.point.x
		for i in range(0,4):
			nr = r + dr[i]
			nc = c + dc[i]
			if self.matrix.con.pointInside((nc,nr)):
				checkSdirection[i] = 1




		for p in self.con.points:
			if(p.type != 'offcurve'):
				checkPart = checkMatrix.getPointPart(p)
				if((pointPart[0] == checkPart[0]) and (pointPart[1] == checkPart[1])):
					originpl.append(p)



		#locate contour exactly matrix's contour
		standardMinx = self.matrix.con.bounds[0]
		standardMiny = self.matrix.con.bounds[1]

		checkMinx = self.con.bounds[0]
		checkMiny = self.con.bounds[1]


		termX = checkMinx - standardMinx
		termY = checkMiny - standardMiny

		#apply pl
		for p in originpl:
			rx = p.x - termX
			ry = p.y - termY
			checkCdirection = calcDirection(self.con,p)
			relocatepl.append(matrixRelocatePoint(p,rx,ry,checkCdirection))



		#get point that get minimum distance
		minDist = 10000000000
		indx = -1


		for	i,o in enumerate(relocatepl):
			if (o.direction[0] != checkSdirection[0]) or (o.direction[1] != checkSdirection[1]) or (o.direction[2] != checkSdirection[2]) or (o.direction[3] != checkSdirection[3]):
				continue
			dist = math.sqrt(math.pow(self.point.x - o.rx,2) + math.pow(self.point.y - o.ry,2))
			if(minDist > dist):
				indx = i
				minDist = dist

		if indx != -1:
			return relocatepl[indx].point
		else:
			return None

	"""
	각각의 속성을 넣어주는 함수들
	"""
	def mgiveSelected(self):
		insertPoint = self.matchPoint()
		if insertPoint is not None:
			insertPoint.selected = True

	def mgiveAttrPenPair(self):
		insertPoint = self.matchPoint()
		if insertPoint is not None:
			temp = at.get_attr(self.point,'penPair')
			at.add_attr(insertPoint,'penPair',temp)

	def mgiveDependX(self):
		insertPoint = self.matchPoint()
		if insertPoint is not None:
			temp = at.get_attr(self.point,'dependX')
			at.add_attr(insertPoint,'dependX',temp)

	def mgiveDependY(self):
		insertPoint = self.matchPoint()
		if insertPoint is not None:
			temp = at.get_attr(self.point,'dependY')
			at.add_attr(insertPoint,'dependY',temp)

	def mgiveInnerFill(self):
		insertPoint = self.matchPoint()
		if insertPoint is not None:
			temp = at.get_attr(self.point,'innerFill')
			at.add_attr(insertPoint,'innerFill',temp)

	def mdeleteAttr(self,attribute):
		insertPoint = self.matchPoint()
		if insertPoint is not None:
			at.del_attr(insertPoint,attribute)		













