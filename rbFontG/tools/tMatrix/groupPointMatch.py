import copy
import math
from rbFontG.tools.tMatrix.PhaseTool import *
from fwig.tools import attributetools as at
from groupingTool.clockWise.clockWiseGroup import *
"""
	2020/02/24
	create by kim heesup
"""

def calcDirection(con,point):
	"""
	make compare point data's direction
	[up,down,left,right]
	"""

	dr = [20,-20,0,0]
	dc = [0,0,-20,20]

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
	2020/02/24
	create by kim heesup
	"""
	def __init__(self,point,rx,ry,direction):
		"""
		contain RPoint, relocated x position, relocate y position
		"""
		self.point = point
		self.rx = rx
		self.ry = ry
		self.direction = direction

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

		#매트릭스 기준점을 가져옴
		standardCutLine = self.matrix.getMatrixCutLine()
		compareCutLine = checkMatrix.getMatrixCutLine()


		#additional mechanism
		dr = [20,-20,0,0]
		dc = [0,0,-20,20]

		#standard direction
		#사용하지 않는 로직
		checkSdirection = [0,0,0,0]
		r = self.point.y
		c = self.point.x
		for i in range(0,4):
			nr = r + dr[i]
			nc = c + dc[i]
			if self.matrix.con.pointInside((nc,nr)):
				checkSdirection[i] = 1



		#비교 컨투어 direction조사
		for p in self.con.points:
			if(p.type != 'offcurve'):
				checkPart = checkMatrix.getPointPart(p)
				if((pointPart[0] == checkPart[0]) and (pointPart[1] == checkPart[1])):
					originpl.append(p)


		#pointPart의 첫 원소는 x부분이고 두번째 원소는 y부분이다.
		#기준컨투어에서 점의 거리를 구함
		standard_dist = math.sqrt(math.pow(self.point.x - standardCutLine[0][pointPart[0]],2) + math.pow(self.point.y - standardCutLine[1][pointPart[1]],2))
		standard_term_x = self.matrix.getTermX()
		standard_term_y = self.matrix.getTermY()

		compare_term_x = checkMatrix.getTermX()
		compare_term_y = checkMatrix.getTermY()

		#get point that get minimum distance
		minDist = 10000000000
		indx = -1

		#시험 코드
		standardClockDegree = getPointClockDegree(self.matrix.con,self.point)
		print("standardClockDegree : ", standardClockDegree)
		print("compareCon:",self.con)

		for i in range(0,len(originpl)):
			print("compare point : ",originpl[i])
			#direction으로 1차 필터링
			diff_count = 0
			checkCdirection = calcDirection(self.con,originpl[i])
			print("checkSdirection : ", checkSdirection)
			print("checkCdirection : ",checkCdirection)
			for j in range(0,4):
				if(checkSdirection[j] != checkCdirection[j]):
					diff_count += 1

			if diff_count > 1:
				continue

			#회전율로 2차 필터링
			#compareClockDegree = getPointClockDegree(self.con,originpl[i])
			#print("compareClockDegree : ",compareClockDegree)
			#print("standardClockDegree - compareClockDegree: ", abs(standardClockDegree - compareClockDegree))

			#방향이 같은 것만 고려
			#if compareClockDegree > 0  and standardClockDegree < 0:
				#continue
			#elif compareClockDegree < 0  and standardClockDegree > 0:
				#continue

			#if abs(standardClockDegree - compareClockDegree) > 5000:
				#continue

			#거리로 3차 필터링
			compare_dist_origin_x = originpl[i].x - compareCutLine[0][pointPart[0]]
			compare_dist_origin_y = originpl[i].y - compareCutLine[1][pointPart[1]]

			#거리의 크기 조정
			compare_dist_x = (compare_dist_origin_x) * (standard_term_x / compare_term_x)
			compare_dist_y = (compare_dist_origin_y) * (standard_term_y / compare_term_y)

			#조정된 길이를 이용하여 거리를 구해줌
			compare_dist = math.sqrt(math.pow(compare_dist_x,2) + math.pow(compare_dist_y,2))

			dist = abs(standard_dist - compare_dist)
			print("dist : ",dist)

			if(minDist > dist):
				indx = i
				minDist = dist
		print("==========================================")

		#회전율 최종 필터링
		compareClockDegree = getPointClockDegree(self.con,originpl[indx])
		print("compareClockDegree : ",compareClockDegree)
		print("standardClockDegree - compareClockDegree: ", abs(standardClockDegree - compareClockDegree))

		#방향이 같은 것만 고려
		if compareClockDegree > 0  and standardClockDegree < 0:
			indx = -1
		elif compareClockDegree < 0  and standardClockDegree > 0:
			indx = -1

		if abs(standardClockDegree - compareClockDegree) > 5000:
			indx = -1

		if indx != -1:
			print(minDist)
			return originpl[indx]
		else:
			return None





		#locate contour exactly matrix's contour
		'''standardMinx = self.matrix.con.bounds[0]
		#standardMinx = getStandardMaxMin.getMinXValue()
		standardMinx = self.matrix.con.bounds[0]
		#standardMiny = getStandardMaxMin.getMaxYValue()
		standardMiny = self.matrix.con.bounds[1]

		#checkMinx = getCompareMaxMin.getMinXValue()
		checkMinx = self.con.bounds[0]
		#checkMiny = getCompareMaxMin.getMaxYValue()
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
			#direction오차를 줌
			diff_count = 0
			for j in range(0,4):
				if(o.direction[j] != checkSdirection[j]):
					diff_count += 1

			if diff_count > 1:
				continue

			dist = math.sqrt(math.pow(self.point.x - o.rx,2) + math.pow(self.point.y - o.ry,2))
			if(minDist > dist):
				indx = i
				minDist = dist

		if indx != -1:
			return relocatepl[indx].point
		else:
			return None'''


	"""
	각각의 속성을 넣어주는 함수들
	"""
	def mgiveSelected(self,matchPoint):
		if matchPoint is not None:
			matchPoint.selected = True

	def mgiveAttrPenPair(self,matchPoint):
		if matchPoint is not None:
			temp = at.get_attr(self.point,'penPair')
			at.add_attr(matchPoint,'penPair',temp)

	def mgiveDependX(self,matchPoint):
		if matchPoint is not None:
			temp = at.get_attr(self.point,'dependX')
			at.add_attr(matchPoint,'dependX',temp)

	def mgiveDependY(self,matchPoint):
		if matchPoint is not None:
			temp = at.get_attr(self.point,'dependY')
			at.add_attr(matchPoint,'dependY',temp)

	def mgiveInnerFill(self,matchPoint):
		if matchPoint is not None:
			temp = at.get_attr(self.point,'innerFill')
			at.add_attr(matchPoint,'innerFill',temp)

	def mdeleteAttr(self,attribute,matchPoint):
		if matchPoint is not None:
			at.del_attr(matchPoint,attribute)		













