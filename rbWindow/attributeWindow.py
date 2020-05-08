
import pathManager.pathSetting as extPath
from vanilla import FloatingWindow, RadioGroup, Button, HUDFloatingWindow, ImageButton, TextBox, EditText, CheckBox
from rbFontG.tools.tTopology import topologyButtonEvent as tbt
from rbFontG.tools.tMatrix import matrixButtonEvent as mbt
from rbFontG.tools.tMatrix.PhaseTool import *
from mojo.UI import *
from jsonConverter.smartSetSearchModule import *
from rbWindow.Controller.toolMenuController import *
from mojo.extensions import *
from rbWindow.ExtensionSetting.extensionValue import *

matrixMode = 0
topologyMode = 1



class attributeWindow:

	def __init__(self, mainWindow):
		self.mainWindow = mainWindow

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
			file = getExtensionDefault(DefaultKey+".file")
			newGlyph = self.mainWindow.file[CurrentGlyphWindow().getGlyph().name]
			print(newGlyph)
			mode = getExtensionDefault(DefaultKey+".mode")
			print("mode : ", mode)

			checkSetData = searchGroup(newGlyph,self.contourNumber, mode,file)
			print(checkSetData)
			if checkSetData[2] == 1:
				raise NotSetExist

			setExtensionDefault(DefaultKey+".standardContour", newGlyph.contours[self.contourNumber])
			setExtensionDefault(DefaultKey+".groupDict", findContoursGroup(checkSetData, self.mainWindow.file))

		except Exception as e:
			Message("아직 그룹화가 진행되어지지 않았습니다.")
			print("예외가 발생했습니다",e)
			return

		self.createUI()
		

	def createUI(self):
		x = 10; y = 10; w = 100; h = 30; space = 5; self.size = (200,250); pos = (1200,300); self.minSize = (50,250);

		self.w = HUDFloatingWindow((pos[0],pos[1],self.minSize[0],self.minSize[1]), "ToolsWindow", minSize=(self.minSize[0], self.minSize[1]))

		#h = 50
		#self.w.optionRadioGroup = RadioGroup((32,20,w,h), ["PenPair", "DependX", "DependY"], sizeStyle="small")
		#y += h + space + 15
		
		h = 30

		self.w.innerFillButton = ImageButton((x,y,h,h), imagePath=extPath.ImagePath+extPath.attrImgList[0]+".png")
		print("ImagePath = ", extPath.ImagePath+extPath.attrImgList[0]+".png")
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

		self.w.minimizeBox = CheckBox((x,y,80,20), "", callback=self.minimizeCallback, value=True)
		y += h +space

		mode = getExtensionDefault(DefaultKey+".mode")

		if mode is matrixMode:
			matrix_size = getExtensionDefault(DefaultKey+".matrix_size")
			standardContour = getExtensionDefault(DefaultKey+".standardContour")
			setExtensionDefault(DefaultKey+".matrix", Matrix(standardContour, matrix_size))
			self.w.innerFillButton._setCallback(self.mhandleInnerFill)
			self.w.penPairButton._setCallback(self.mhandlePenPair)
			self.w.dependXButton._setCallback(self.mhandleDependX)
			self.w.dependYButton._setCallback(self.mhandleDependY)
			self.w.deleteButton._setCallback(None)
			self.w.selectButton._setCallback(self.mhandleSelect)

		elif mode is topologyMode:
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
		groupDict = getExtensionDefault(DefaultKey+".groupDict")
		matrix = getExtensionDefault(DefaultKey+".matrix")
		mbt.minnerFillAttribute(groupDict, matrix)

	def mhandlePenPair(self, sender):
		groupDict = getExtensionDefault(DefaultKey+".groupDict")
		matrix = getExtensionDefault(DefaultKey+".matrix")
		mbt.mpenPairAttribute(groupDict, matrix)

	def mhandleDependX(self, sender):
		groupDict = getExtensionDefault(DefaultKey+".groupDict")
		matrix = getExtensionDefault(DefaultKey+".matrix")
		mbt.mdependXAttribute(groupDict, matrix)

	def mhandleDependY(self, sender):
		groupDict = getExtensionDefault(DefaultKey+".groupDict")
		matrix = getExtensionDefault(DefaultKey+".matrix")
		mbt.mdependYAttribute(groupDict, matrix)

	def mhandleDelete(self, sender):
		pass

	def mhandleSelect(self, sender):
		groupDict = getExtensionDefault(DefaultKey+".groupDict")
		matrix = getExtensionDefault(DefaultKey+".matrix")
		mbt.mselectAttribute(groupDict, matrix)





	"""
		콜백 메소드에 연결할 메소드(Topology)
	"""
	def thandleInnerFill(self, sender):
		groupDict = getExtensionDefault(DefaultKey+".groupDict")
		standardContour = getExtensionDefault(DefaultKey+".standardContour")
		k = getExtensionDefault(DefaultKey+".k")
		tbt.innerFillAttribute(groupDict, standardContour, k)

	def thandlePenPair(self, sender):
		groupDict = getExtensionDefault(DefaultKey+".groupDict")
		standardContour = getExtensionDefault(DefaultKey+".standardContour")
		k = getExtensionDefault(DefaultKey+".k")
		tbt.innerFillAttribute(groupDict, standardContour, k)

	def thandleDependX(self, sender):
		groupDict = getExtensionDefault(DefaultKey+".groupDict")
		standardContour = getExtensionDefault(DefaultKey+".standardContour")
		k = getExtensionDefault(DefaultKey+".k")
		tbt.innerFillAttribute(groupDict, standardContour, k)

	def thandleDependY(self, sender):
		groupDict = getExtensionDefault(DefaultKey+".groupDict")
		standardContour = getExtensionDefault(DefaultKey+".standardContour")
		k = getExtensionDefault(DefaultKey+".k")
		tbt.innerFillAttribute(groupDict, standardContour, k)

	def thandleDelete(self, sender):
		pass

	def thandleSelect(self, sender):
		groupDict = getExtensionDefault(DefaultKey+".groupDict")
		standardContour = getExtensionDefault(DefaultKey+".standardContour")
		k = getExtensionDefault(DefaultKey+".k")
		tbt.innerFillAttribute(groupDict, standardContour, k)



	def minimizeCallback(self, sender):
		if sender.get() == True:
			self.w.resize(self.minSize[0], self.minSize[1])
			self.w.minimizeBox.setTitle("")
		else:
			self.w.resize(self.size[0], self.size[1])
			self.w.minimizeBox.setTitle("최소화")