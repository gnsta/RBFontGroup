from vanilla import FloatingWindow, RadioGroup, Button, HUDFloatingWindow, ImageButton, TextBox
from rbFontG.tools.tTopology import topologyButtonEvent as tbt
from rbFontG.tools.tMatrix import matrixButtonEvent as mbt
from rbFontG.tools.tMatrix.PhaseTool import *
import pathManager.pathSetting as extPath
import os
from mojo.UI import *
from jsonConverter.smartSetSearchModule import *


matrixMode = 0
topologyMode = 1


class NotSetExist(Exception):
	"""
	exception that Currnet glyph is not included any set
	"""
	def __init__(self):
		super().__init__('어느 그룹에도 속해있지 않은 글리프입니다.')


class attributeWindow:
	"""
	2020/04/06
	modify by Kim heesup
	change standardContour to user What the user is currently working on

	팝업창 하나 필요
	지금 띄워져 있는 글리프에 대하여 몇번 컨투어를 조작 할 것인지...
	"""

	def __init__(self, mainWindow, mode):
		self.mainWindow = mainWindow
		self.mode = mode
		#팝압창이 나오고 컴투어 인덱스 번호를 받음
		contourNumber =None
		try:
			newGlyph = mainWindow.file[CurrentGlyphWindow().getGlyph().name]
			checkSetData = searchGroup(newGLyph,contourNumber,mainWindow.mode,mainWindow)
			if checkSetData[2] == 0:
				raise NotSetExist

			mainWindow.standardContour = newGlyph.contours[contourNumber]
			mainWindow.groupDict = findContoursGroup(checkSetData,mainWindow)
		except Exception as e:
			print("예외가 발생했습니다",e)

		#예외가 발생하면 ui가 팝업되지 않도록
		


	def createUI(self):
		x = 10; y = 10; w = 100; h = 30; space = 5; size = (200,250); pos = (1200,300); minSize = (50,250);

		self.w = HUDFloatingWindow((pos[0],pos[1],size[0],size[1]), "ToolsWindow", minSize=(minSize[0], minSize[1]))

		#h = 50
		#self.w.optionRadioGroup = RadioGroup((32,20,w,h), ["PenPair", "DependX", "DependY"], sizeStyle="small")
		#y += h + space + 15
		
		h = 30

		self.w.innerFillButton = ImageButton((x,y,h,h), imagePath=extPath.ImagePath+extPath.attrImgList[0]+".png")
		self.w.innerFillText = TextBox((x+40,y,w,h), "innerFill")
		y += h + space

		self.w.penPairButton = ImageButton((x,y,h,h), imagePath=extPath.ImagePath+extPath.attrImgList[1]+".png")
		self.w.PenPairText = TextBox((x+40,y,w,h), "penPair")
		y += h + space

		self.w.dependXButton = ImageButton((x,y,h,h), imagePath=extPath.ImagePath+extPath.attrImgList[2]+".png")
		self.w.dependXText = TextBox((x+40,y,w,h), "dependX")
		y += h + space

		self.w.dependYButton = ImageButton((x,y,h,h), imagePath=extPath.ImagePath+extPath.attrImgList[3]+".png")
		self.w.dependYText = TextBox((x+40,y,w,h), "depndY")
		y += h + space

		self.w.deleteButton = ImageButton((x,y,h,h), imagePath=extPath.ImagePath+extPath.attrImgList[4]+".png")
		self.w.deleteText = TextBox((x+40,y,w,h), "delete")
		y += h + space

		self.w.selectButton = ImageButton((x,y,h,h), imagePath=extPath.ImagePath+extPath.attrImgList[5]+".png")
		self.w.selectText = TextBox((x+40,y,w,h), "select")
		y += h + space

		if self.mode is matrixMode:
			self.w.innerFillButton._setCallback(self.mhandleInnerFill)
			self.w.penPairButton._setCallback(self.mhandlePenPair)
			self.w.dependXButton._setCallback(self.mhandleDependX)
			self.w.dependYButton._setCallback(self.mhandleDependY)
			self.w.deleteButton._setCallback(None)
			self.w.selectButton._setCallback(self.mhandleSelect)

		elif self.mode is topologyMode:
			self.w.innerFillButton._setCallback(self.thandleInnerFill)
			self.w.penPairButton._setCallback(self.thandlePenPair)
			self.w.dependXButton._setCallback(self.thandleDependX)
			self.w.dependYButton._setCallback(self.thandleDependY)
			self.w.deleteButton._setCallback(None)
			self.w.selectButton._setCallback(self.thandleSelect)

		self.w.open()

	"""
		콜백 메소드에 연결할 메소드(Matrix)
	"""
	def mhandleInnerFill(self, sender):
		mbt.minnerFillAttribute(self.mainWindow.groupDict, Matrix(self.mainWindow.standardContour,self.mainWindow.widthValue),30)

	def mhandlePenPair(self, sender):
		mbt.mpenPairAttribute(self.mainWindow.groupDict, Matrix(self.mainWindow.standardContour,self.mainWindow.widthValue),30)

	def mhandleDependX(self, sender):
		mbt.mdependXAttribute(self.mainWindow.groupDict, Matrix(self.mainWindow.standardContour,self.mainWindow.widthValue),30)

	def mhandleDependY(self, sender):
		mbt.mdependYAttribute(self.mainWindow.groupDict, Matrix(self.mainWindow.standardContour,self.mainWindow.widthValue),30)

	def mhandleDelete(self, sender):
		pass

	def mhandleSelect(self, sender):
		mbt.mselectAttribute(self.mainWindow.groupDict, Matrix(self.mainWindow.standardContour,self.mainWindow.widthValue),30)





	"""
		콜백 메소드에 연결할 메소드(Topology)
	"""
	def thandleInnerFill(self, sender):
		tbt.innerFillAttribute(self.mainWindow.groupDict, self.mainWindow.standardContour,500)

	def thandlePenPair(self, sender):
		tbt.innerFillAttribute(self.mainWindow.groupDict, self.mainWindow.standardContour,500)

	def thandleDependX(self, sender):
		tbt.innerFillAttribute(self.mainWindow.groupDict, self.mainWindow.standardContour,500)

	def thandleDependY(self, sender):
		tbt.innerFillAttribute(self.mainWindow.groupDict, self.mainWindow.standardContour,500)


	def thandleDelete(self, sender):
		pass

	def thandleSelect(self, sender):
		tbt.selectAttribute(self.mainWindow.groupDict, self.mainWindow.standardContour,500)

