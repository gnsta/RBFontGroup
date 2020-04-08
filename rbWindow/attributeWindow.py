from vanilla import FloatingWindow, RadioGroup, Button, HUDFloatingWindow, ImageButton, TextBox, EditText
from rbFontG.tools.tTopology import topologyButtonEvent as tbt
from rbFontG.tools.tMatrix import matrixButtonEvent as mbt
from rbFontG.tools.tMatrix.PhaseTool import *
from mojo.UI import *
from jsonConverter.smartSetSearchModule import *
from rbWindow.Controller.toolMenuController import *


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
		self.w = HUDFloatingWindow((300,200), "Index Window")
		self.w.textBox = TextBox((10,10,100,22),"Contour Index")
		self.w.editText = EditText((140,10,50,22))
		self.w.btn = Button((10,50,80,22),"Submit", callback=self.submitCallback)
		self.w.open()
		self.contourNumber =None

		#예외가 발생하면 ui가 팝업되지 않도록
		
	def submitCallback(self,sender):

		print("start")
		print(self.w.editText.get())
		print(type(self.w.editText.get()))
		print("end")
		self.contourNumber = int(self.w.editText.get())

		try:
			newGlyph = self.mainWindow.file[CurrentGlyphWindow().getGlyph().name]
			print(newGlyph)
			checkSetData = searchGroup(newGlyph,self.contourNumber,self.mainWindow.mode,self.mainWindow)
			print(checkSetData)
			if checkSetData[2] == 1:
				raise NotSetExist

			self.mainWindow.standardContour = newGlyph.contours[self.contourNumber]
			self.mainWindow.groupDict = findContoursGroup(checkSetData,self.mainWindow)

		except Exception as e:
			Message("아직 그룹화가 진행되어지지 않았습니다.")
			print("예외가 발생했습니다",e)
			return

		self.createUI()
		


	def createUI(self):
		x = 10; y = 10; w = 150; h = 30; space = 5; size = (180,200); pos = (1200,300);

		self.w = HUDFloatingWindow((pos[0],pos[1],size[0],size[1]), "ToolsWindow")

		#h = 50
		#self.w.optionRadioGroup = RadioGroup((32,20,w,h), ["PenPair", "DependX", "DependY"], sizeStyle="small")
		#y += h + space + 15
		
		h = 22
		if(self.mode == matrixMode):
			self.w.innerFillButton = ImageButton((x,y,h,h), imagePath="/Users/sslab/Desktop/image/resized/innerFill.png", callback=self.mhandleInnerFill)
			y += h + space

			self.w.penPairButton = Button((x,y,w,h), "penPair", callback=self.mhandlePenPair)
			y += h + space

			self.w.dependXButton = Button((x,y,w,h), "dependX", callback=self.mhandleDependX)
			y += h + space

			self.w.dependYButton = Button((x,y,w,h), "dependY", callback=self.mhandleDependY)
			y += h + space

			self.w.deleteButton = Button((x,y,w,h), "delete Attribute", callback=None)
			y += h + space

			self.w.selectButton = Button((x,y,w,h), "select", callback=self.mhandleSelect)
			y += h + space

		else:
			self.w.innerFillButton = Button((x,y,w,h), "innerFill", callback=self.thandleInnerFill)
			y += h + space

			self.w.penPairButton = Button((x,y,w,h), "penPair", callback=self.thandlePenPair)
			y += h + space

			self.w.dependXButton = Button((x,y,w,h), "dependX", callback=self.thandleDependX)
			y += h + space

			self.w.dependYButton = Button((x,y,w,h), "dependY", callback=self.thandleDependY)
			y += h + space

			self.w.deleteButton = Button((x,y,w,h), "delete Attribute", callback=None)
			y += h + space

			self.w.selectButton = Button((x,y,w,h), "select", callback=self.thandleSelect)
			y += h + space

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
		tbt.innerFillAttribute(self.mainWindow.groupDict, self.mainWindow.standardContour,200)

	def thandlePenPair(self, sender):
		tbt.penPairAttribute(self.mainWindow.groupDict, self.mainWindow.standardContour,200)

	def thandleDependX(self, sender):
		tbt.dependXAttribute(self.mainWindow.groupDict, self.mainWindow.standardContour,200)

	def thandleDependY(self, sender):
		tbt.dependYAttribute(self.mainWindow.groupDict, self.mainWindow.standardContour,200)

	def thandleDelete(self, sender):
		pass

	def thandleSelect(self, sender):
		tbt.selectAttribute(self.mainWindow.groupDict, self.mainWindow.standardContour,200)