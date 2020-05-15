
import pathManager.pathSetting as extPath
from vanilla import FloatingWindow, RadioGroup, Button, HUDFloatingWindow, ImageButton, TextBox, EditText, CheckBox
from rbFontG.tools.tTopology import topologyButtonEvent as tbt
from rbFontG.tools.tMatrix import matrixButtonEvent as mbt
from rbFontG.tools.tMatrix.PhaseTool import *
from mojo.UI import *
from jsonConverter.smartSetSearchModule import *
from rbWindow.Controller.toolMenuController import *
from rbWindow.ExtensionSetting.extensionValue import *
from fontParts.world import *


matrixMode = 0
topologyMode = 1



class attributeWindow:

	def __init__(self):
		#팝압창이 나오고 컴투어 인덱스 번호를 받음
		res = self.preprocess()
		if res is True:
			self.createUI()
		
	def preprocess(self):

		contourNumber = getExtensionDefault(DefaultKey + ".contourNumber")

		#try:
		file = getExtensionDefault(DefaultKey+".file")
		newGlyph = file[CurrentGlyphWindow().getGlyph().name]

		print(newGlyph)
		mode = getExtensionDefault(DefaultKey+".mode")
		print("mode : ", mode)
		print(newGlyph,",",contourNumber,",",file)
		checkSetData = searchGroup(newGlyph, contourNumber, mode, file)
		print("checkSetData in attributeW : ",checkSetData)
		if contourNumber is None:
			raise NotSetExist

		setExtensionDefault(DefaultKey+".standardContour", newGlyph.contours[contourNumber])
		setExtensionDefault(DefaultKey+".groupDict", findContoursGroup(checkSetData, file, mode))
		'''
		except Exception as e:
			print(contourNumber)
			Message("아직 그룹화가 진행되어지지 않았습니다.")
			print("예외가 발생했습니다",e)
			return False
		'''
		return True
		

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



	def updateAttributeComponent(self):
		"""
			2020/05/14 created by Cho H.W.

			사용자의 조작에 의해 찾아놓은 groupDict가 아닌 다른 요소에 대해 속성을 부여하는 과정에서
			필요한 인자들을(ex. matrix, groupDict, standardGlyph, ...) 갱신하기 위한 보조함수

			선택된 컨투어가 기존의 groupDict 내에 포함된 요소라면 갱신하지 않고 메소드가 종료됩니다.
		"""
		count = 0
		selectedContour = None
		currentGlyph = CurrentGlyph()
		prevGlyph = getExtensionDefault(DefaultKey+".standardGlyph")
		prevContour = getExtensionDefault(DefaultKey+".standardContour")
		prevGroupDict = getExtensionDefault(DefaultKey+".groupDict")
		mode = getExtensionDefault(DefaultKey+".mode")

		for contour in currentGlyph:
			if len(contour.selection) > 0:
				count += 1
				selectedContour = contour

		if count != 1:
			Message("하나의 컨투어를 선택해주십시오.")
			return False


		else: 
			# 현재 선택된 컨투어가 그룹딕셔너리에 있나 확인하기
			if selectedContour != prevContour:
				try:
					contourList = prevGroupDict[currentGlyph] 

					for contourIdx in contourList:

						if selectedContour.index == contourIdx:
		
							setExtensionDefault(DefaultKey+".standardContour", selectedContour)
							setExtensionDefault(DefaultKey+".standardGlyph", currentGlyph)
							if mode is matrixMode:
			
								matrix = Matrix(selectedContour, matrix_size); 
								setExtensionDefault(DefaultKey+".matrix", matrix)
							setExtensionDefault(DefaultKey+".contourNumber", selectedContour.index)
							return True

				except KeyError as e:
					Message("현재 찾은 그룹과 다른 그룹입니다. 탐색을 먼저 진행해주세요")
					return False

			else:
				return True

	"""
		콜백 메소드에 연결할 메소드(Matrix)
	"""
	def mhandleInnerFill(self, sender):
		self.updateAttributeComponent()
		groupDict = getExtensionDefault(DefaultKey+".groupDict")
		matrix = getExtensionDefault(DefaultKey+".matrix")
		mbt.minnerFillAttribute(groupDict, matrix)

	def mhandlePenPair(self, sender):
		self.updateAttributeComponent()
		groupDict = getExtensionDefault(DefaultKey+".groupDict")
		matrix = getExtensionDefault(DefaultKey+".matrix")
		mbt.mpenPairAttribute(groupDict, matrix)

	def mhandleDependX(self, sender):
		self.updateAttributeComponent()
		groupDict = getExtensionDefault(DefaultKey+".groupDict")
		matrix = getExtensionDefault(DefaultKey+".matrix")
		mbt.mdependXAttribute(groupDict, matrix)

	def mhandleDependY(self, sender):
		self.updateAttributeComponent()
		groupDict = getExtensionDefault(DefaultKey+".groupDict")
		matrix = getExtensionDefault(DefaultKey+".matrix")
		mbt.mdependYAttribute(groupDict, matrix)

	def mhandleDelete(self, sender):
		self.updateAttributeComponent()
		pass

	def mhandleSelect(self, sender):
		self.updateAttributeComponent()
		groupDict = getExtensionDefault(DefaultKey+".groupDict")
		matrix = getExtensionDefault(DefaultKey+".matrix")
		mbt.mselectAttribute(groupDict, matrix)





	"""
		콜백 메소드에 연결할 메소드(Topology)
	"""
	def thandleInnerFill(self, sender):
		self.updateAttributeComponent()
		groupDict = getExtensionDefault(DefaultKey+".groupDict")
		standardContour = getExtensionDefault(DefaultKey+".standardContour")
		k = getExtensionDefault(DefaultKey+".k")
		tbt.innerFillAttribute(groupDict, standardContour, k)

	def thandlePenPair(self, sender):
		self.updateAttributeComponent()
		groupDict = getExtensionDefault(DefaultKey+".groupDict")
		standardContour = getExtensionDefault(DefaultKey+".standardContour")
		k = getExtensionDefault(DefaultKey+".k")
		tbt.innerFillAttribute(groupDict, standardContour, k)

	def thandleDependX(self, sender):
		self.updateAttributeComponent()
		groupDict = getExtensionDefault(DefaultKey+".groupDict")
		standardContour = getExtensionDefault(DefaultKey+".standardContour")
		k = getExtensionDefault(DefaultKey+".k")
		tbt.innerFillAttribute(groupDict, standardContour, k)

	def thandleDependY(self, sender):
		self.updateAttributeComponent()
		groupDict = getExtensionDefault(DefaultKey+".groupDict")
		standardContour = getExtensionDefault(DefaultKey+".standardContour")
		k = getExtensionDefault(DefaultKey+".k")
		tbt.innerFillAttribute(groupDict, standardContour, k)

	def thandleDelete(self, sender):
		pass

	def thandleSelect(self, sender):
		self.updateAttributeComponent()
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