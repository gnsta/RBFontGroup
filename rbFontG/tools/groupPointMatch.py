import copy
import math

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
		self.glyph = glyph

		self.standardCon = matrix.getCon()

	def matchPoint(self):
		"""
		match modify contour point and group contours point

		return:
			matched point

		example(if divided 3 by 3)
		-------------------------
		|		|		|2	3	|
		|		|	   4|1		|
		-------------------------
		|		|		|		|
		|		|		|		|
		-------------------------
		|		|		|		|
		|		|		|		|
		-------------------------

		if selected point is point 1

		point 2, point 3 and point 4 is group contour's points

		result is that point 1 and point 2 are match
		
		Because they are included same part and has shortest distance in the part
		"""	 
		pointPart = self.matrix.getPointPart(self.point)

		#find all point that contour's point that is located pointPart
		originpl = [] #original points

		checkMatrix = matrix(self.con,self.matrix.getKx,self.matrix.getKy)

		for p in con.points:
			checkPart = checkMatrix.getPointPart(p)
			if((pointPart[0] == checkPart[0]) and (pointPart[1] == checkPart[1])):
				originpl.append(p)


		#locate contour exactly matrix's contour
		standardMinx = self.matrix.getMinx()
		standardMiny = self.matrix.getMiny()

		checkMinx = checkMatrix.getMinx()
		checkMiny = checkMatrix.getMiny()

		termX = checkMinx - standardMinx
		termY = checkMiny - standardMiny

		copypl = copy.deepcopy(originpl)

		#apply pl
		for p in copypl:
			p.x = p.x - termX
			p.y = p.y - termY

		#get point that get minimum distance
		minDist = 10000000000
		indx = -1

		for	i,p in enumerate(coptpl):
			dist = math.sqrt(math.pow(self.point.x - p.x,2) + math.pow(self.point.y - p.y,2))
			if(min > dist):
				indx = i
				min = dist

		return pl[indx]		 









