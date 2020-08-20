import copy
import math
from groupingTool.tMatrix.PhaseTool import *
from groupingTool.clockWise.clockWiseGroup import *
from fwig.tools import attributetools as at
from groupingTool.clockWise.clockWiseGroup import *
from attributeTool.strokeAttribute import *
from mojo.extensions import getExtensionDefault, setExtensionDefault
from rbWindow.ExtensionSetting.extensionValue import *

"""
	2020/02/24
	create by kim heesup
"""

def getCurveDerivation(n, p0, pointType, clockWise):

	if p0.type == pointType:
		currentContour = p0.getParent()
		print("currentContour = ", currentContour)
		pointCount = len(currentContour.points)
		print("pointCount = ", pointCount)
		currentIndex = p0.index
		print("currentIndex = ", currentIndex)
		if currentContour.points[currentIndex-1].type == 'offcurve' and clockWise is True:
			return getPointOnCurveDerivation(n, currentContour.points[currentIndex-3], currentContour.points[currentIndex-2], currentContour.points[currentIndex-1], p0, False)
		elif currentContour.points[(currentIndex+1)%pointCount].type == 'offcurve' and clockWise is not True:
			return getPointOnCurveDerivation(n, currentContour.points[(currentIndex+3)%pointCount], currentContour.points[(currentIndex+2)%pointCount], currentContour.points[(currentIndex+1)%pointCount], p0, False)
		elif currentContour.points[(currentIndex+1)%pointCount].type == 'offcurve' and clockWise is True:
			return getPointOnCurveDerivation(n, p0, currentContour.points[(currentIndex+1)%pointCount], currentContour.points[(currentIndex+2)%pointCount], currentContour.points[(currentIndex+3)%pointCount], True)
		elif currentContour.points[currentIndex-1].type == 'offcurve' and clockWise is not True:
			return getPointOnCurveDerivation(n, p0, currentContour.points[currentIndex-1], currentContour.points[currentIndex-2], currentContour.points[currentIndex-3], True)
	else:
		return None

def getPointOnCurveDerivation(n, p0, p1, p2, p3, front):
    x0 = p0.x
    y0 = p0.y
    x1 = p1.x
    y1 = p1.y
    x2 = p2.x
    y2 = p2.y
    x3 = p3.x
    y3 = p3.y
    points = [(x0, y0)]
    for t in range(1, n):
        t = t/n
        ax = x0 + t * (x1 - x0)
        ay = y0 + t * (y1 - y0)
        bx = x1 + t * (x2 - x1)
        by = y1 + t * (y2 - y1)
        cx = x2 + t * (x3 - x2)
        cy = y2 + t * (y3 - y2)
        dx = ax + t * (bx - ax)
        dy = ay + t * (by - ay)
        ex = bx + t * (cx - bx)
        ey = by + t * (cy - by)
        fx = dx + t * (ex - dx)
        fy = dy + t * (ey - dy)
        points.append((fx, fy))

    if front is True:
    	first_point = points[0]
    	second_point = points[1]
    else:
    	first_point = points[-2]
    	second_point = points[-1]
    derivation = (second_point[1] - first_point[1])/(second_point[0] - first_point[0])

    return derivation


class ClockPointPair:
	def __init__(self,point,clockDegree,index):
	    self.point = point
	    self.clockDegree = clockDegree
	    self.index = index


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

	def firstFiltering(self,point,checkSdirection):
		"""
		matchPoint함수에서 적용
		1차 필터링 과정
		direction방법으로 필터링
		"""
		#direction으로 1차 필터링
		diff_count = 0
		checkCdirection = calcDirection(self.con,point)
		for j in range(0,4):
			if(checkSdirection[j] != checkCdirection[j]):
				diff_count += 1

		if diff_count > 1:
			return -1
		elif diff_count == 0:
			return 0
		elif diff_count == 1:
			return 1
	def secondFiltering(self,standardClockDegree,compareClockDegree):
		#방향이 같은 것만 고려
		# return None : 유망하지 않음
		if compareClockDegree > 0  and standardClockDegree < 0:
			return None
		elif compareClockDegree < 0  and standardClockDegree > 0:
			return None

		diff = abs(standardClockDegree - compareClockDegree)

		if diff > 10000:
			return None
		# 유망한 경우만 diff를 반환
		else:
			return diff



	def matchPoint(self):
		pointType = None
		if getExtensionDefault(DefaultKey + ".korean") is True:
			pointType = "curve"
		else:
			pointType = 'qcurve'
		"""
		포인트를 매칭 시켜줌
		"""	 
		print("self.con = ",self.con)
		#(매트릭스 좌표 x,y)
		pointPart = self.matrix.getPointPart(self.point)

		if self.point.type == pointType:
			standard_derivation = getCurveDerivation(100, self.point, pointType, self.point.getParent().clockwise)
		else:
			print("큐커브점이 아니라 계산 생략 및 종료")
			return
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
		#자신의 범위와 주변 범위들을 조사
		for p in self.con.points:

			if(p.type != 'offcurve'):
				checkPart = checkMatrix.getPointPart(p)
				# 조사하는 매트릭스의 x,y차가 1 이하면 조사 범위에 포함시킨다.
				check_part_one = abs(pointPart[0] - checkPart[0])		#x

				check_part_two = abs(pointPart[1] - checkPart[1])		#y

				
				if(check_part_one <= 1) and (check_part_two <= 1):
					originpl.append(p)




		#pointPart의 첫 원소는 x부분이고 두번째 원소는 y부분이다.
		#기준컨투어에서 점의 거리를 구함
		
		"""standard_dist = math.sqrt(math.pow(self.point.x - standardCutLine[0][pointPart[0]],2) + math.pow(self.point.y - standardCutLine[1][pointPart[1]],2))
								print("기준 좌표의 X 거리 = ", self.point.x - standardCutLine[0][pointPart[0]])
								print("기준 좌표의 Y 거리 = ", self.point.y - standardCutLine[1][pointPart[1]])
								print("기준 거리 = ", standard_dist)
								standard_term_x = self.matrix.getTermX()
								standard_term_y = self.matrix.getTermY()
								compare_term_x = checkMatrix.getTermX()
								compare_term_y = checkMatrix.getTermY()"""

		#get point that get minimum distance
		#minDiff_dir_zero = 10000000000
		dir_diff_zero_indx = -1

		#minDiff_dir_one = 10000000000
		dir_diff_one_indx = -1

		diff_count_mode = 0

		#시험 코드
		standardClockDegree = getPointClockDegree(self.matrix.con,self.point)
		
		secondResult_one = list() #두번째 필터링 까지의 결과
		secondResult_two = list()

		#originpl : 같은 그룹 내 컨투어 내 조사할 후보군 점
		for i in range(0,len(originpl)):			
			#direction으로 1차 필터링
			diff_count_mode = self.firstFiltering(originpl[i],checkSdirection)
			if diff_count_mode == -1:
				continue

			print("1차 필터링 통과")
			#회전율로 2차 필터링
			compareClockDegree = getPointClockDegree(self.con,originpl[i])
			#print("compareClockDegree = ",compareClockDegree)
			clock_diff = self.secondFiltering(standardClockDegree,compareClockDegree)
			#print("clock_diff = ",clock_diff)
			#if diff_count_mode == 0 and clock_diff is not None:
			if diff_count_mode == 0:
				temp_insert = ClockPointPair(originpl[i],clock_diff,i)
				secondResult_one.append(temp_insert)

			#elif diff_count_mode == 1 and clock_diff is not None:
			elif diff_count_mode == 1:
				temp_insert = ClockPointPair(originpl[i],clock_diff,i)
				secondResult_two.append(temp_insert)

		print("secondResult_one = ", secondResult_one)
		print("secondResult_two = ", secondResult_two)

		#두번째 결과까지 해서 정렬
		secondResultSorted_one = secondResult_one
		secondResultSorted_two = secondResult_two


		"""min_dist = 500
								minInclination = 999"""
		min_derivation = 0.3
		for i in range(0,len(secondResultSorted_one)):
			"""
			print("해당 점 조사 : ", secondResultSorted_one[i].point)
			#거리로 3차 필터링
			compare_dist_origin_x = secondResultSorted_one[i].point.x - compareCutLine[0][pointPart[0]]
			compare_dist_origin_y = secondResultSorted_one[i].point.y - compareCutLine[1][pointPart[1]]
			print("원래 거리 X= ", compare_dist_origin_x)
			print("비교 컨투어 기준점 X 포인트 = ", compareCutLine[0][pointPart[0]])
			print("원래 거리 Y = ", compare_dist_origin_y)
			print("비교 컨투어 기준점 Y 포인트 = ", compareCutLine[1][pointPart[1]])
                                      
			#거리의 크기 조정
			compare_dist_x = compare_dist_origin_x * standard_term_x / compare_term_x
			compare_dist_y = compare_dist_origin_y * standard_term_y / compare_term_y
			print("기준 매트릭스 단위 X 길이 = ", standard_term_x)
			print("기준 매트릭스 단위 Y 길이 = ", standard_term_y)
			print("비교 매트릭스 단위 X 길이 = ", compare_term_x)
			print("비교 매트릭스 단위 Y 길이 = ", compare_term_y)
			compare_inclination = compare_dist_x / compare_dist_y
			print("비교 좌표 기울기 = ",  compare_inclination)

			#조정된 길이를 이용하여 거리를 구해줌
			compare_dist = math.sqrt(math.pow(compare_dist_x,2) + math.pow(compare_dist_y,2))

			dist = abs(standard_dist - compare_dist)
			print("(x,y) = ", secondResult_one[i].point.x,",",secondResult_one[i].point.y)
			print("dist = ", dist)
			"""
			"""			
			if dist > 30:
				print("dist > 30 3차 필터링에서 걸러짐")
				continue
			else:"""
			if secondResult_one[i].point.type == pointType:
				compare_derivation = getCurveDerivation(100, secondResult_one[i].point, pointType, secondResult_one[i].point.getParent().clockwise)
				print("기준 미분값 = ", standard_derivation)
				print("비교 미분값 = ", compare_derivation)
				print("차이 = ", abs(standard_derivation - compare_derivation))
				print("비교 좌표 = ", secondResult_one[i].point)
				if abs(standard_derivation - compare_derivation) < min_derivation:
					min_derivation = abs(standard_derivation - compare_derivation)
					dir_diff_zero_indx = secondResultSorted_one[i].index

			else:
				continue
			"""
					if minInclination > abs(standard_inclination - compare_inclination):
					minInclination = abs(standard_inclination - compare_inclination)
					dir_diff_zero_indx = secondResultSorted_one[i].index"""

		if dir_diff_zero_indx != -1:
			return originpl[dir_diff_zero_indx]

		#추가적으로 점을 조사
		min_dist = 500
		minInclination = 999
		min_derivation = 0.3
		for i in range(0,len(secondResultSorted_two)):

			"""			
			#거리로 3차 필터링
			compare_dist_origin_x = secondResultSorted_two[i].point.x - compareCutLine[0][pointPart[0]]
			compare_dist_origin_y = secondResultSorted_two[i].point.y - compareCutLine[1][pointPart[1]]

			#거리의 크기 조정
			compare_dist_x = compare_dist_origin_x * standard_term_x / compare_term_x
			compare_dist_y = compare_dist_origin_y * standard_term_y / compare_term_y

			compare_inclination = compare_dist_x / compare_dist_y
			#조정된 길이를 이용하여 거리를 구해줌
			compare_dist = math.sqrt(math.pow(compare_dist_x,2) + math.pow(compare_dist_y,2))

			dist = abs(standard_dist - compare_dist)

			if dist > 30:
				continue
			else:"""
			if secondResult_two[i].point.type == pointType:
				print("현재 비교점 = ", secondResult_two[i].point)
				compare_derivation = getCurveDerivation(100, secondResult_two[i].point, pointType, secondResult_two[i].point.getParent().clockwise)
				if abs(standard_derivation - compare_derivation) < min_derivation:
					print("기준 미분값 = ", standard_derivation)
					print("비교 미분값 = ", compare_derivation)
					print("차이 = ", abs(standard_derivation - compare_derivation))
					print("비교 좌표 = ", secondResult_two[i].point)
					dir_diff_zero_indx = secondResultSorted_two[i].index
					min_derivation = abs(standard_derivation - compare_derivation)
			else:
				continue

		if dir_diff_one_indx != -1:
			return originpl[dir_diff_one_indx]
		else:
			return None

	"""
	각각의 속성을 넣어주는 함수들
	"""
	def mgiveSelected(self,matchPoint):
		if matchPoint is not None:
			matchPoint.selected = True

	def mgiveAttrPenPair(self,matchPoint):
		if matchPoint is not None:
			temp = at.get_attr(self.point,'penPair')
			if temp is not None:
				at.add_attr(matchPoint,'penPair',temp)

	def mgiveDependX(self,matchPoint):
		if matchPoint is not None:
			temp = at.get_attr(self.point,'dependX')
			if temp is not None:
				at.add_attr(matchPoint,'dependX',temp)

	def mgiveDependY(self,matchPoint):
		if matchPoint is not None:
			temp = at.get_attr(self.point,'dependY')
			if temp is not None:
				at.add_attr(matchPoint,'dependY',temp)

	def mgiveInnerFill(self,matchPoint):
		if matchPoint is not None:
			temp = at.get_attr(self.point,'innerFill')
			if temp is not None:
				at.add_attr(matchPoint,'innerFill',temp)

	def mgiveStroke(self,matchPoint):
		if matchPoint is not None:
			temp = at.get_attr(self.point,'stroke')
			if temp is not None:
				at.add_attr(matchPoint,'stroke',temp)

	def mdeleteAttr(self,attribute,matchPoint):
		if matchPoint is not None:
			at.del_attr(matchPoint,attribute)		