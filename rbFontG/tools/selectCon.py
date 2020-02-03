def get_initialContour(glyph):
	return 1

def get_midContour(glyph):
	return 1

def get_finalContour(glyph):

	y = [0,0,0]

	if(len(glyph.contours) != 3):
		return 2
	else:
		for i in range(0,3):
			min = 10000
			for p in glyph.contours[i].points:
				if(p.y < min):
					min = p.y
					y[i] = p.y

	aim = 0					
	for i in range(1,3):
		if(y[aim] > y[i]):
			aim = i

	return glyph.contours[aim]		
					



