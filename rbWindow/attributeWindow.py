from vanilla import FloatingWindow, RadioGroup, Button, HUDFloatingWindow, ImageButton
from rbFontG.tools.tTopology import topologyButtonEvent as tbt
from rbFontG.tools.tMatrix import matrixButtonEvent as mbt
from rbFontG.tools.tMatrix.PhaseTool import *


matrixMode = 0
topologyMode = 1

class attributeWindow:

	def __init__(self, mainWindow, mode):
		self.mainWindow = mainWindow
		self.mode = mode
		self.matrix = Matrix(self.mainWindow.standardContour,self.mainWindow.widthValue)

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
		mbt.minnerFillAttribute(self.mainWindow.groupDict, self.matrix)

	def mhandlePenPair(self, sender):
		mbt.mpenPairAttribute(self.mainWindow.groupDict, self.matrix)

	def mhandleDependX(self, sender):
		mbt.mdependXAttribute(self.mainWindow.groupDict, self.matrix)

	def mhandleDependY(self, sender):
		mbt.mdependYAttribute(self.mainWindow.groupDict, self.matrix)

	def mhandleDelete(self, sender):
		pass

	def mhandleSelect(self, sender):
		mbt.mselectAttribute(self.mainWindow.groupDict, self.matrix)





	"""
		콜백 메소드에 연결할 메소드(Topology)
	"""
	def thandleInnerFill(self, sender):
		tbt.minnerFillAttribute(self.mainWindow.groupDict, self.mainWindow.standardContour,500)

	def thandlePenPair(self, sender):
		tbt.minnerFillAttribute(self.mainWindow.groupDict, self.mainWindow.standardContour,500)

	def thandleDependX(self, sender):
		tbt.minnerFillAttribute(self.mainWindow.groupDict, self.mainWindow.standardContour,500)

	def thandleDependY(self, sender):
		tbt.minnerFillAttribute(self.mainWindow.groupDict, self.mainWindow.standardContour,500)

	def thandleDelete(self, sender):
		pass

	def thandleSelect(self, sender):
		tbt.minnerFillAttribute(self.mainWindow.groupDict, self.mainWindow.standardContour,500)