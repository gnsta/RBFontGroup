from fontTools.pens.basePen import BasePen
from mojo.drawingTools import oval, save, translate, rotate, restore

class BroadNibPen(BasePen):

    def __init__(self, glyphSet, step, width, height, angle, shape):
        BasePen.__init__(self, glyphSet)
        self.step = step
        self.width = width
        self.height = height
        self.angle = angle
        self.shape = shape
        self.firstPoint = None

    def _moveTo(self, pt):
        
        self.firstPoint = pt

    def _lineTo(self, pt):
        
        pt0 = self._getCurrentPoint()
        points = getPointsOnLine(self.step, pt0, pt)
        self._drawPoints(points)
    
    def _curveToOne(self, pt1, pt2, pt3):
        
        pt0 = self._getCurrentPoint()
        points = getPointsOnCurve(self.step, pt0, pt1, pt2, pt3)
        self._drawPoints(points)

    def _closePath(self):
        
        pt0 = self._getCurrentPoint()
        pt = self.firstPoint
        if pt0 != pt:
            points = getPointsOnLine(self.step, pt0, pt)
            self._drawPoints(points)

    def _drawPoints(self, points):
        
        for point in points:
            x, y = point
            save()
            translate(x, y)
            rotate(self.angle)
            translate(-self.width/2, -self.height/2)
            self.shape(0, 0, self.width, self.height)
            restore()

def getPointsOnCurve(n, p0, p1, p2, p3):
    x0, y0 = p0
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

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

    return points

def getPointsOnLine(n, p0, p1):
    x0, y0 = p0
    x1, y1 = p1

    points = [(x0, y0)]

    for t in range(1, n):
        t = t/n

        fx = x0 + t * (x1 - x0)
        fy = y0 + t * (y1 - y0)

        points.append((fx, fy))

    return points