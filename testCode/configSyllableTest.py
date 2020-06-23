from rbFontG.tools.parseUnicodeControll import *
from rbWindow.contourPen import BroadNibPen
from defconAppKit.windows.baseWindow import BaseWindowController
from mojo.events import addObserver
from mojo.drawingTools import fill, oval
import parseContour.parseExample as parseExample
from parseSyllable.utility.syllableColor import *
if __name__ == '__main__':

	font = CurrentFont()
		
	gC = syllableColor(font)
	

"""
    	초중종 데이터를 활용하고 싶다면 data = getConfigre(RGlyph)
    	data : {'str(RGlyph.unicode'), [[초성 인덱스],[중성 인덱스], [종성 인덱스]}
	
    	초중종 데이터를 추가하고 싶다면, data.update(getConfigure(RGlyph))
	
    	주의점 : data의 크기가 너무나도 커질 수 있기 때문에 이 점에 유의한다.
"""