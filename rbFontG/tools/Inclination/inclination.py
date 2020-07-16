from mojo.roboFont import *
from mojo.drawingTools import fill, oval, rect

def getInclination(point1, point2):
	"""
	기울기를 반환해 주는 함수

	Args:
		point1 :: RPoint
		point2 :: RPoint

	Returns :: double
		직선의 기울기
	"""
	inclination = (point2.y - point1.y) / (point2.x - point1.x)

	return inclination


def getLine(point,inclination):
	"""
	직선을 반환하는 함수

	Args:
		point :: Rpoint
		inclination :: double
	
	Returns :: List
		[직선의 기울기, y절편]
	"""
	a = inclination

	b = point1.y / (a * point.x)

	return [a,b]

'''def checkPointPositionToLine(line, point):
	"""
	해당 점이 선의 위에 있나 아래에 있나 판별

	Args:
		line :: List
			[직선의 기울기, y절편]
		point :: RPoint

	Returns :: int 
		윗쪽에 있으면 1 아래에 있으면 -1 걸쳐 있으면 0을 반환
	"""

	res = line[0] * point.x + line[1]

	if res < point.y:
		return 1
	elif res > point.y:
		return -1
	else:
		return 0'''


'''def getInsertIndex(startPoint,conotur,line):
	"""
	새로운 점이 들어갈 위치를 찾는 함수

	Args:
		startPoint :: RPoint 
		contour :: RContour
		line :: list

	Returns :: int
		포인트가 들어갈 점
	"""

	res = -1

	#순회하는 다음점이 위에 있는지 아래에 있는지 체크를 해 줌
	standardCheck = checkPointPositionToLine(line,contour.points[startPoint.index+1])


	for i in range(startPoint.index+2, len(contour.points)):
		compareCheck = checkPointPositionToLine(line,contour.points[i])

		if compareCheck == standardCheck:
			continue
		else:
			res = i-1
			break

	return res'''


def getMatchPoint(line,contour):

	maxx = contour.bounds[2] + 10
	minx = contour.bounds[0] - 10
	#maxy = contour.bounds[3] + 10
	#miny = contour.bounds[1] - 10


	count = 0
	check = 0

	pointList = list()

	for i in range(minx,maxx):
		j = line[0] * i + line[1]
		if count == 0:
			count += 1
			if contour.pointInside((i,j)):
				count = 1
				continue
			else:
				count = -1
				continue

		if count == 1:
			if !contour.pointInside((i,j)):
				pointList.append((i,j))
				count = -1
		elif count == -1:
			if contour.pointInside((i,j)):
				pointList.append((i,j))
				count = 1

	return pointList




def getMatchLineAndContour(inclination,contour,point):
	"""
	직선과 컨투어가 만나는 페어점을 반환

	Args:
		inclination :: double
			기준이 되는 직선의 기울기
		contour :: RContour
		point :: RPoint
			해당 컨투어에서 PenPair를 잡아줄 점

	Returns :: List
		두 점에 대한 정보
	"""

	min1 = 1000000
	min2 = 1000000

	currentPen = BroadNibPen2(None,100,30,30,0,oval)

	contour.draw(currentPen)

	res = currentPen.getDrawPath()

	compareLine = getLine(point,inclination)


	pointList = getMatchPoint(compareLine,contour)

	if (len(pointList) % 2) != 0:
		compareLine[0] += 10
		pointList = getMatchPoint(compareLine,contour)
		if (len(pointList) % 2) != 0:
			compareLine[0] -= 20
			pointList = getMatchPoint(cimpareLine,contour)



	#리스트에서 해당 점의 인덱스를 찾아줌
	min_diff = 100000
	point_idx = -1

	for i in range(0,len(pointList)):
		_diff = abs(pointList.x - point.x) + abs(pointList.y - point.y)

		if min_diff < _diff:
			point_idx = i
			min_diff = _diff


	if point_idx % 2 == 0:
		return pointList[point_idx - 1]
	else:
		return pointList[point_idx + 1]










	#직선과 컨투어가 만나는 점을 구함
	'''for i in range(0,len(res)):
		#직선일때의 값
		line_amount = compareLine[0]*res[0] + compareLine[1]

		#곡선위의 값과의 차이
		_diff = abs(line_amount - res[1])

		#최소값이면 갱신 
		if min1 > _diff:
			min1 = _diff
			point1_location = res[i]
		elif min2 > _diff:
			min2 = _diff
			point2_location = res[i]
		else:
			continue

	location_diff1 = abs(point.x - point1_location[0]) + abs(point.y - point1_location[1])
	location_diff2 = abs(point.y - point2_loaction[0]) + abs(point.y - point2_location[1])

	if location_diff1 > location_diff2:
		insert_location = point1_location
	else:
		insert_location = point2_location

	return insert_location'''

'''def insertPointToContour(standardPoint1, standardPoint2, contour, comparePoint1):
	"""
	기준 컨투어에서 쌍을 만들었을 때 비교 컨투어에 해당 페어점을 추가

	Args:
		standardPoint1 :: RPoint
		standardPoint2 :: RPoint
		contour :: RContour
		comparePoint :: RPoint
	"""

	#직선의 정보를 가져옴
	lineInfo = getLine(standardPoint1,getInclination(standardPoint1,standardPoint2))

	#들어갈 인덱스 정보를 가져옴
	indexInfo = getInsertIndex(comparePoint1, contour, lineInfo)

	#들어갈 위치 정보를 가져옴
	pointLocation = getMatchLineAndContour(lineInfo,contour,comparePoint1)

	contours.insertPoint(indexInfo,pointLocation,type="curve",smooth=True)'''


