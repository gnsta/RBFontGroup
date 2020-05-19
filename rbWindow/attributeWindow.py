
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
from fontParts.fontshell.contour import *

matrixMode = 0
topologyMode = 1



class attributeWindow:

	def __init__(self):
		
		self.createUI()
	
		

	def createUI(self):
		x = 10; y = 10; w = 100; h = 30; space = 5; self.size = (200,250); pos = (1200,300); self.minSize = (50,250);

		self.w = HUDFloatingWindow((pos[0],pos[1],self.minSize[0],self.minSize[1]), "ToolsWindow", minSize=(self.minSize[0], self.minSize[1]))
		
		h = 30

		self.w.innerFillButton = ImageButton((x,y,h,h), imagePath=extPath.ImagePath+extPath.attrImgList[0]+".png", callback=self.handleInnerFill)
		print("ImagePath = ", extPath.ImagePath+extPath.attrImgList[0]+".png")
		self.w.innerFillText = TextBox((x+40,y,w,h), "innerFill")
		y += h + space

		self.w.penPairButton = ImageButton((x,y,h,h), imagePath=extPath.ImagePath+extPath.attrImgList[1]+".png", callback=self.handlePenPair)
		self.w.PenPairText = TextBox((x+40,y,w,h), "penPair")
		y += h + space

		self.w.dependXButton = ImageButton((x,y,h,h), imagePath=extPath.ImagePath+extPath.attrImgList[2]+".png", callback=self.handleDependX)
		self.w.dependXText = TextBox((x+40,y,w,h), "dependX")
		y += h + space

		self.w.dependYButton = ImageButton((x,y,h,h), imagePath=extPath.ImagePath+extPath.attrImgList[3]+".png", callback=self.handleDependY)
		self.w.dependYText = TextBox((x+40,y,w,h), "depndY")
		y += h + space

		self.w.deleteButton = ImageButton((x,y,h,h), imagePath=extPath.ImagePath+extPath.attrImgList[4]+".png", callback=self.handleDelete)
		self.w.deleteText = TextBox((x+40,y,w,h), "delete")
		y += h + space

		self.w.selectButton = ImageButton((x,y,h,h), imagePath=extPath.ImagePath+extPath.attrImgList[5]+".png", callback=self.handleSelect)
		self.w.selectText = TextBox((x+40,y,w,h), "select")
		y += h + space

		self.w.minimizeBox = CheckBox((x,y,80,20), "", callback=self.minimizeCallback, value=True)
		y += h +space

		mode = getExtensionDefault(DefaultKey+".mode")

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
				print(prevContour, ", prevContour"); print(selectedContour, ", selectedContour"); print(prevGroupDict, ", prevGroupDict")
				try:
					contourList = prevGroupDict[currentGlyph] 
					
					for contourIdx in contourList:

						if selectedContour.index == contourIdx:
							res = True
							setExtensionDefault(DefaultKey+".standardContour", selectedContour)
							setExtensionDefault(DefaultKey+".standardGlyph", currentGlyph)
							if mode is matrixMode:
			
								matrix = Matrix(selectedContour, matrix_size); 
								setExtensionDefault(DefaultKey+".matrix", matrix)
							setExtensionDefault(DefaultKey+".contourNumber", selectedContour.index)
							return True

					# 같은 글리프라도 컨투어가 같은 그룹딕셔너리가 아니라면 익셉션을 raise한다.
					raise Exception

				except Exception as e:
					print("에러 발생")
					result = self.updateSmartSetChanged(selectedContour)
					
					if result is False:
						Message("해당되는 그룹 결과가 존재하지 않습니다. 탐색을 먼저 진행해주세요.")
					
					else:
						Message("해당되는 그룹이 존재합니다. 관련 정보를 갱신하였습니다.")
						
					return result

			else:
				return True

	def updateSmartSetChanged(self, selectedContour):
		"""
			이전 standardContour와 현재 선택된 standardContour의 smartSet이 다른 경우,
			이미 찾아놓은 smartSet이 존재하는 경우에 한하여 속성 부여에 필요한 인자들을 갱신합니다.
			(updateAttributeComponent의 보조함수)

			갱신되는 인자 : (contourNumber, standardContour, standardGlyph, groupDict)

			@param : 
				selectedContour(RContour) : 현재 속성을 부여하려는 point의 parent (RContour)
			
			@return :
				True : 갱신된 컨투어에 해당되는 스마트 셋이 존재하는 경우
				False : 갱신된 컨투어에 해당되는 스마트 셋이 존재하지 않는 경우 
		"""
		contourNumber = selectedContour.index;
		glyph = selectedContour.getParent();
		mode = getExtensionDefault(DefaultKey + ".mode")
		file = getExtensionDefault(DefaultKey + ".file")
		checkSetData = searchGroup(glyph, contourNumber, mode, file)

		if checkSetData[2] == 0:
			print("checkSetData[2] == 0 (이미 만들어진 그룹)")
			
			if mode is matrixMode:

				matrix = Matrix(selectedContour, matrix_size); 
				setExtensionDefault(DefaultKey+".matrix", matrix)
			
			groupDict = findContoursGroup(checkSetData, file, mode)
			setExtensionDefault(DefaultKey+".groupDict", groupDict)
			setExtensionDefault(DefaultKey+".contourNumber", contourNumber)
			setExtensionDefault(DefaultKey+".standardContour", selectedContour)
			setExtensionDefault(DefaultKey+".standardGlyph", glyph)
			return True
		
		else:
			print("checkSetData[2] != 0 or None")
			return False


	"""
		콜백 메소드에 연결할 메소드
	"""
	def handleDependX(self, sender):
		if self.updateAttributeComponent() is False:
			return
		
		mode = getExtensionDefault(DefaultKey+".mode")
		
		if mode is matrixMode:
			groupDict = getExtensionDefault(DefaultKey+".groupDict")
			matrix = getExtensionDefault(DefaultKey+".matrix")
			mbt.mdependXAttribute(groupDict, matrix)

		elif mode is topologyMode:
			groupDict = getExtensionDefault(DefaultKey+".groupDict")
			standardContour = getExtensionDefault(DefaultKey+".standardContour")
			k = getExtensionDefault(DefaultKey+".k")
			tbt.dependXAttribute(groupDict, standardContour, k)
				
		else:
			Message("모드 에러")

	def handleDependY(self, sender):
		if self.updateAttributeComponent() is False:
			return
		
		mode = getExtensionDefault(DefaultKey+".mode")
		
		if mode is matrixMode:
			groupDict = getExtensionDefault(DefaultKey+".groupDict")
			matrix = getExtensionDefault(DefaultKey+".matrix")
			mbt.mdependYAttribute(groupDict, matrix)

		elif mode is topologyMode:
			groupDict = getExtensionDefault(DefaultKey+".groupDict")
			standardContour = getExtensionDefault(DefaultKey+".standardContour")
			k = getExtensionDefault(DefaultKey+".k")
			tbt.mdependYAttribute(groupDict, standardContour, k)
				
		else:
			Message("모드 에러")

	def handlePenPair(self, sender):
		if self.updateAttributeComponent() is False:
			return
		
		mode = getExtensionDefault(DefaultKey+".mode")
		
		if mode is matrixMode:
			groupDict = getExtensionDefault(DefaultKey+".groupDict")
			matrix = getExtensionDefault(DefaultKey+".matrix")
			mbt.mpenPairAttribute(groupDict, matrix)

		elif mode is topologyMode:
			groupDict = getExtensionDefault(DefaultKey+".groupDict")
			standardContour = getExtensionDefault(DefaultKey+".standardContour")
			k = getExtensionDefault(DefaultKey+".k")
			tbt.penPairAttribute(groupDict, standardContour, k)
				
		else:
			Message("모드 에러")

	def handleInnerFill(self, sender):
		if self.updateAttributeComponent() is False:
			return
		
		mode = getExtensionDefault(DefaultKey+".mode")
		
		if mode is matrixMode:
			groupDict = getExtensionDefault(DefaultKey+".groupDict")
			matrix = getExtensionDefault(DefaultKey+".matrix")
			mbt.minnerFillAttribute(groupDict, matrix)

		elif mode is topologyMode:
			groupDict = getExtensionDefault(DefaultKey+".groupDict")
			standardContour = getExtensionDefault(DefaultKey+".standardContour")
			k = getExtensionDefault(DefaultKey+".k")
			tbt.innerFillAttribute(groupDict, standardContour, k)
				
		else:
			Message("모드 에러")

	def handleSelect(self, sender):
		if self.updateAttributeComponent() is False:
			return
		
		mode = getExtensionDefault(DefaultKey+".mode")
		
		if mode is matrixMode:
			groupDict = getExtensionDefault(DefaultKey+".groupDict")
			matrix = getExtensionDefault(DefaultKey+".matrix")
			mbt.mselectAttribute(groupDict, matrix)

		elif mode is topologyMode:
			groupDict = getExtensionDefault(DefaultKey+".groupDict")
			standardContour = getExtensionDefault(DefaultKey+".standardContour")
			k = getExtensionDefault(DefaultKey+".k")
			tbt.selectAttribute(groupDict, standardContour, k)
				
		else:
			Message("모드 에러")

	def handleDelete(self, sender):
		if self.updateAttributeComponent() is False:
			return
		
		mode = getExtensionDefault(DefaultKey+".mode")
		
		if mode is matrixMode:
			groupDict = getExtensionDefault(DefaultKey+".groupDict")
			matrix = getExtensionDefault(DefaultKey+".matrix")
			pass

		elif mode is topologyMode:
			groupDict = getExtensionDefault(DefaultKey+".groupDict")
			standardContour = getExtensionDefault(DefaultKey+".standardContour")
			k = getExtensionDefault(DefaultKey+".k")
			pass
				
		else:
			Message("모드 에러")
			
	def minimizeCallback(self, sender):
		if sender.get() == True:
			self.w.resize(self.minSize[0], self.minSize[1])
			self.w.minimizeBox.setTitle("")
		else:
			self.w.resize(self.size[0], self.size[1])
			self.w.minimizeBox.setTitle("최소화")