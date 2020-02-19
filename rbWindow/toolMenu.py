from defconAppKit.windows.baseWindow import BaseWindowController
from vanilla import EditText, FloatingWindow, CheckBox, Button, HelpButton, RadioGroup, HorizontalLine
from mojo.UI import MultiLineView, SelectGlyph, Message
from mojo.events import addObserver,removeObserver
from mojo.drawingTools import fill, oval
from mojo.extensions import getExtensionDefault, setExtensionDefault
from rbWindow.contourPen import BroadNibPen
from rbWindow.sliderGroup import SliderGroup
from rbWindow.addGroupWindow import AddGroupWindow
import rbFontG.tools.tMatrix.PhaseTool
import rbFontG.tools.tMatrix.groupTestController
from rbFontG.tools.tTopology import topologyJudgement as tj
from rbFontG.tools.tTopology import topologyAssignment as ta
from rbFontG.tools import parseUnicodeControll as puc
import timeit#

def getMatchGroupByMatrix(inputGlyph, contourIndex, margin, width, height, file):

	investigateList = []
	glyphUni = file["uni" + hex(inputGlyph.unicode)[2:].upper()]

	s1 = puc.parseUnicodeController(glyphUni.unicode)

	for g in file:
		s2 = puc.parseUnicodeController(glyphUni.unicode)
		v = puc.judgeMentCandidate(s1,s2)
		if(v == True):
			investigateList.append(g)

	contour = inputGlyph.contours[contourIndex]

	standardMatrix = rbFontG.tools.tMatrix.PhaseTool.Matrix(contour,width,height)
	compareController = rbFontG.tools.tMatrix.groupTestController.groupTestController(standardMatrix,0)
	groupList = []

	for idx, compareGlyph in enumerate(investigateList):

		result = compareController.glyphCheckGroup(compareGlyph)
		if result is not None:
			groupList.append(result)

	return groupList

def text2Glyph(inputText, font):
	
	for glyph in font:
		if str(ord(inputText)) == str(glyph.unicode):
			return glyph

	return None

"""
	기준 컨투어 (standardContour)와 매칭되는 글리프, 컨투어 3차원 리스트를 groupList
"""
def getMatchGroupByTopology(standardGlyph,standardContour, k, font):
	start = timeit.default_timer()#
	investigateList = []

	res = []

	glyphUni = font["uni" + hex(standardGlyph.unicode)[2:].upper()]

	s1 = puc.parseUnicodeController(glyphUni.unicode)

	for g in font:
		s2 = puc.parseUnicodeController(g.unicode)
		v = puc.judgeMentCandidate(s1,s2)
		if(v == True):
			investigateList.append(g)
			g.selected = True

	sCheck = ta.checkCon(standardContour, k)
	sCheckControll = tj.topologyJudgementController(sCheck)

	for g in investigateList:
		temp = []
		for c in g:
			v = sCheckControll.topologyJudgement(c)
			if(v == True):
				temp.append([g,c])
		res.append(temp)
	
	stop = timeit.default_timer()#
	print(stop-start)#
	return res	


	
	
class toolsWindow:

	def __init__(self, mainWindow):

		self.defaultKey = "com.asaumierdemers.BroadNibBackground"
		self.mode = mainWindow.w.methodRadioGroup.get()		# mode 0: matrix, 1: topology
		self.groupList = mainWindow.groupList
		self.group = None
		self.file = mainWindow.file
		self.glyphs = []
		self.font = mainWindow.font
		self.mainWindow = mainWindow

	def createUI(self, sender):
		x = 10; y = 10; w = 150; h = 22; space = 5; size = (500,400); pos = (800,0);

		self.w = FloatingWindow((size[0],size[1]), "ToolsWindow")

		if(self.mode == 0):
			h = 50
			marginValue = getExtensionDefault("%s.%s" %(self.defaultKey, "margin"), 0)
			self.w.margin = SliderGroup((x,y,w,h), "Margin:", 0, 50, marginValue, callback=self.marginChanged)
			y += h + space
		
			widthValue = getExtensionDefault("%s.%s" %(self.defaultKey, "width"), 10)
			self.w.matrixWidth = SliderGroup((x,y,w,h), "Width:", 0, 100, widthValue, callback=self.widthChanged)
			y += h + space
		
			heightValue = getExtensionDefault("%s.%s" %(self.defaultKey, "height"), 10)
			self.w.matrixHeight = SliderGroup((x,y,w,h), "Height:", 0, 100, heightValue, callback=self.heightChanged)
			y += h + space
		
			self.w.divider1 = HorizontalLine((x,y,w,h))
			y += h + space

		h = 22
		self.w.editText = EditText((x,y,w,h), text="Input Glyph...")
		y += h + space

		h = 50
		indexValue = getExtensionDefault("%s.%s" %(self.defaultKey, "index"), 0)
		self.w.contourIndex = SliderGroup((x,y,w,h), "ContourIndex:", 0, 50, indexValue, callback=self.indexChanged)
		y += h + space

		h = 22
		self.w.searchGlyphListButton = Button((x,y,w,h), "Search", callback=self.searchGlyphListCallback)
		y += h + space

		self.w.open()

	def marginChanged(self, sender):
	    
	    setExtensionDefault("%s.%s" %(self.defaultKey, "margin"), int(sender.get()))
	    self.w.margin.updateView()
	    
	def widthChanged(self, sender):
	    
	    setExtensionDefault("%s.%s" %(self.defaultKey, "width"), int(sender.get()))
	    self.w.matrixWidth.updateView()
	    
	def heightChanged(self, sneder):
	    
	    setExtensionDefault("%s.%s" %(self.defaultKey, "height"), int(sender.get()))
	    self.w.matrixHeight.updateView()

	def indexChanged(self, sender):

		setExtensionDefault("%s.%s" %(self.defaultKey, "index"), int(sender.get()))
		self.w.contourIndex.updateView()

	def searchGlyphListCallback(self, sender):

		inputText = self.w.editText.get()
		targetGlyph = text2Glyph(inputText, self.font)
		contourIdx = int(self.w.contourIndex.slider.get())
		file = self.file
		# 한 글자 입력 시 모드에 따라 입력된 글리프와 컨투어 인덱스에 따른 그룹 리스트로 갱신한다.
		if len(inputText) == 1:
			if self.mode == 0:
				margin = int(self.w.margin.slider.get())
				width = int(self.w.matrixWidth.slider.get())
				height = int(self.w.matrixHeight.slider.get())

				#def getMatchGroupByMatrix(inputGlyph, contourIndex, margin, width, height, filePath)
				self.group = getMatchGroupByMatrix(targetGlyph, contourIdx, margin, width, height, file)


			elif self.mode == 1:

				self.group = getMatchGroupByTopology(targetGlyph, targetGlyph.contours[contourIdx], 2, self.font)

			if self.group is None:
				print(Message("찾으려는 그룹이 존재하지 않습니다."))
			else:
				self.mainWindow.groupList = self.group
				self.glyphs = []
				for groupElement in self.group:
					for idx, element in enumerate(groupElement):
						self.glyphs.append(element[0])

			self.mainWindow.w.lineView.set(self.glyphs)
			self.mainWindow.w.lineView.update()

		else:
			print(Message("한 글자만 입력해야 합니다."))
