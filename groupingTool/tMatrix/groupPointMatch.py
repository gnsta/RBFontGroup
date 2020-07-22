import copy
import math
from groupingTool.tMatrix.PhaseTool import *
from fwig.tools import attributetools as at
from groupingTool.clockWise.clockWiseGroup import *
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

	def matchPoint(self):
		"""
		포인트를 매칭 시켜줌
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
		minDiff_dir_zero = 10000000000
		dir_diff_zero_indx = -1

		minDiff_dir_one = 10000000000
		dir_diff_one_indx = -1

		diff_count_mode = 0

		#시험 코드
		standardClockDegree = getPointClockDegree(self.matrix.con,self.point)

		print("con : ", self.con)


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
				print("diff_count_out")
				continue
			elif diff_count == 0:
				diff_count_mode = 0
			elif diff_count == 1:
				diff_count_mode = 1


			#회전율로 2차 필터링
			compareClockDegree = getPointClockDegree(self.con,originpl[i])
			print("compareClockDegree : ",compareClockDegree)
			print("standardClockDegree - compareClockDegree: ", abs(standardClockDegree - compareClockDegree))

			#방향이 같은 것만 고려
			if compareClockDegree > 0  and standardClockDegree < 0:
				print("clock_out")
				continue
			elif compareClockDegree < 0  and standardClockDegree > 0:
				print("clock_out")
				continue

			diff = abs(standardClockDegree - compareClockDegree)

			if diff > 5000:
				continue

			#거리로 3차 필터링
			compare_dist_origin_x = originpl[i].x - compareCutLine[0][pointPart[0]]
			compare_dist_origin_y = originpl[i].y - compareCutLine[1][pointPart[1]]

			#거리의 크기 조정
			compare_dist_x = compare_dist_origin_x * standard_term_x / compare_term_x
			compare_dist_y = compare_dist_origin_y * standard_term_y / compare_term_y

			#조정된 길이를 이용하여 거리를 구해줌
			compare_dist = math.sqrt(math.pow(compare_dist_x,2) + math.pow(compare_dist_y,2))

			dist = abs(standard_dist - compare_dist)
			#print("커트된 기준점!!!")
			#print("x축 : ", compareCutLine[0][pointPart[0]])
			#print("y축 : ", compareCutLine[1][pointPart[1]])
			print("dist : ",dist)

			#if(minDist > dist):
				#indx = i
				#minDist = dist
			if dist > 25:
				print("dist : ", dist)
				continue

			if diff_count_mode == 0:
				if(minDiff_dir_zero > diff):
					minDiff_dir_zero = diff
					dir_diff_zero_indx = i
			elif diff_count_mode == 1:
				if(minDiff_dir_one > diff):
					minDiff_dir_one = diff
					dir_diff_one_indx = i


		if dir_diff_zero_indx != -1:
			print("매칭이 된 점: ", originpl[dir_diff_zero_indx])
			print("==========================================")
			return originpl[dir_diff_zero_indx]
		elif dir_diff_one_indx != -1:
			print("==========================================")
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













