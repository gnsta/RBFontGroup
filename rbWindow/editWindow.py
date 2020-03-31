from defconAppKit.windows.baseWindow import BaseWindowController
from vanilla import EditText, FloatingWindow, CheckBox, Button, HelpButton, RadioGroup, HorizontalLine
from mojo.UI import MultiLineView, SelectGlyph, Message
from mojo.events import addObserver,removeObserver
from mojo.drawingTools import fill, oval
from mojo.extensions import getExtensionDefault, setExtensionDefault
from rbWindow.contourPen import BroadNibPen
from rbWindow.sliderGroup import SliderGroup
#from rbWindow.addGroupWindow import AddGroupWindow
from rbWindow.toolMenu import toolsWindow
from rbWindow.attributeWindow import attributeWindow
from rbWindow.previewWindow import previewWindow
from rbWindow.settingWindow import settingWindow
from mojo.UI import CurrentFontWindow
from AppKit import *


def getMatchGroupDic(inputText, groupDict):
	"""
		2020/03/12
		created by H.W. Cho
		
		Param:
			- inputText(str)
			- groupDict(dict)
		Return:
			groupDict if inputText is in groupDict else None
			Can be used as check whether groupDict contians inputText or not.
	"""
	for key in groupDict.keys():
		if str(ord(inputText)) == str(key.unicode):
			return groupDict

	return None


def getContourListByDic(groupDic):
	"""
		2020/03/12
		created by H.W. Cho
		
		Param:
			- groupDict(dict)
		Return:
			- contourList(list) which glyphs' contourList of groupDict.

	"""
	contourList = []

	for glyph in groupDic.keys():
		for idx in groupDic[glyph]:
			contourList.append(glyph.contours[idx])

	return contourList


def getGlyphListByDic(groupDic):
	"""
		2020/03/12
		created by H.W. Cho

		Param:
			- groupDict(dict)
		Return:
			- glyphList(list)
	"""
	glyphList = []

	for glyph in groupDic.keys():
		glpyhList.add[glyph]

	return glyphList


def getMatchGroupDicByGlyph(inputGlyph, groupDict):
	"""
		2020/03/12
		created by H.W. Cho
		
		Param:
			- inputGlyph(RGlyph)
			- groupDict(dict)
		Return:
			if exists, groupDict(dict)
			else, None
	"""
	if inputGlyph in groupDict.keys():
		return groupDict
	
	return None


class EditGroupMenu:

	def __init__(self, font, file):
		
		self.font = font
		self.groupDict = None
		
		self.defaultKey = "com.asaumierdemers.BroadNibBackground"
		self.selectedGlyphs = []                # Apply List Label을 통해 색칠된 글리프들을 다시 무채색으로 변환하기 위한 변수
		self.markColor = 0.3, 0.4, 0.7, 0.7
		self.state = False
		self.layerName = self.font.layerOrder[0]
		self.currentPen = None
		self.file = file
		self.widthValue = None
		self.window = None		# 현재 띄워져 있는 ufo 윈도우
		self.mode = None  		# 연산 방법(matrix, topology)
		self.w3 = None
		self.createUI()
		
		
	"""
		UI 컴포넌트 부착
	"""
	def createUI(self):
		self.window = CurrentFontWindow()
		if self.window is None:
			return

		toolbarItems = self.window.getToolbarItems()
		newItem = dict(itemIdentifier="Search", label="Search", imageNamed=NSImageNameRevealFreestandingTemplate, callback=self.popSearchWindow)
		newItem2 = dict(itemIdentifier="Rewind", label="Rewind", imageNamed=NSImageNameRefreshFreestandingTemplate, callback=None)
		newItem3 = dict(itemIdentifier="Save", label="Save", imageNamed=NSImageNameComputer, callback=None)
		self.newItem4 = dict(itemIdentifier="Exit", label="Exit", imageNamed=NSImageNameStopProgressFreestandingTemplate, callback=self.windowCloseCallback)
		newItem5 = dict(itemIdentifier="Settings", label="Settings", imageNamed=NSImageNameAdvanced, callback=None) 
		newItem6 = dict(itemIdentifier="Attribute", label="Attribute", imageNamed=NSImageNameFontPanel, callback=self.popAttributeWindow)
		#newItem7 = dict(itemIdentifier="Other", label="Other", imageNamed=NSImageNameIconViewTemplate, callback=self.popSettingWindow)       
		# add the new item to the existing toolbar
		toolbarItems.append(newItem)
		toolbarItems.append(newItem2)
		toolbarItems.append(newItem3)
		toolbarItems.append(self.newItem4)
		toolbarItems.append(newItem5)
		toolbarItems.append(newItem6)
		#toolbarItems.append(newItem7)
		# get the vanilla window object
		vanillaWindow = self.window.window()
		# set the new toolbaritems in the window
		self.window.toolbar = vanillaWindow.addToolbar(toolbarIdentifier="myCustomToolbar", toolbarItems=toolbarItems, addStandardItems=False)
		# done
		x = 10; y = 10; w = 280; h = 22; space = 5; size = (800, 600)

		"""		
		self.w.addGroupListButton = Button((x,y,w,h), "Add Group", callback=self.addGroupListCallback)
		y += h + space
		"""


		#self.w.excludeGlyphButton = Button((x,y,w,h), "Exclude Selected Glyph", callback=self.excludGlyph)
		#y += h + space

		addObserver(self, "drawBroadNibBackground", "drawBackground")


	def popSettingWindow(self,sender):
		if self.w3 is None:
			print(Message("탐색을 먼저 진행해야 합니다."))
			return
		self.w6 = settingWindow(self)
		self.w6.createUI(sender)

	def popPreviewWindow(self, sender):

		self.w5 = previewWindow(self)
		self.w5.createUI(sender)
		
	def popAttributeWindow(self, sender):

		# Window for Assign & Remove Attribute
		if self.mode is None:
			print(Message("먼저 속성을 부여할 그룹을 찾아야 합니다."))
			return
		self.w4 = attributeWindow(self,self.mode)
		self.w4.createUI()


	def popSearchWindow(self, sender):

		# Window for Matrix & Topology Process
		self.w3 = toolsWindow(self)
		self.w3.createUI(sender)

	def colorContourCallback(self, sender):
	   
	    # check option : paint glyphList's contours or not
	    self.state = self.w.colorContourCheckBox.get()
	    

	def windowCloseCallback(self, sender):
	    
	    if self.w3.selectedGlyphs is not None:
	        for glyph in self.w3.selectedGlyphs:
	            glyph.markColor = None

	    removeObserver(self, "drawBackground")
	    super(BroadNibBackground, self).windowCloseCallback(sender)
	

	def drawBroadNibBackground(self, info):
		print("drawBackground")
		# paint current group's contour
		targetGlyph = info["glyph"].getLayer(self.layerName)

		# picks current contours which should be painted from current group
		contourList = []

		if self.groupDict is not None:
			for glyph in self.groupDict.keys():
				if targetGlyph == glyph:
					for idx in self.groupDict[glyph]:
						contourList.append(glyph.contours[idx])

		fill(0.7,0.3,1,0.6)			#r,g,b setting
		if info["glyph"].layerName == self.layerName or not self.currentPen:
			self.currentPen = BroadNibPen(None, 60, 80, 50, 30, oval)
		print(self.state)
		for contour in contourList:
			if contour is not None and self.state == 1:
				contour.draw(self.currentPen)