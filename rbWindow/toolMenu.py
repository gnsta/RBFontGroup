from defconAppKit.windows.baseWindow import BaseWindowController
from vanilla import *
from mojo.UI import SelectGlyph, Message
from mojo.events import addObserver,removeObserver
from mojo.drawingTools import fill, oval
from mojo.extensions import getExtensionDefault, setExtensionDefault
from rbWindow.contourPen import BroadNibPen
from rbWindow.sliderGroup import SliderGroup
import groupingTool.tMatrix.PhaseTool
import groupingTool.tMatrix.groupTestController
from groupingTool.tTopology import topologyJudgement as tj
from groupingTool.tTopology import topologyAssignment as ta
from groupingTool import parseUnicodeControll as puc
import jsonConverter.searchModule as search
import timeit#
import jsonConverter.converter as convert
import rbWindow.Controller.toolMenuController as tMC
import rbWindow.Controller.toolMenuControllerChinese as ctMC
from rbWindow.ExtensionSetting.extensionValue import *

def text2Glyph(inputText, font):
	"""
	2020/03/23
	created by H.W. Cho
	return matching RGlyph object to inputText(str)

	Args :
		inputText : str
			target which want to convert into RGlyph object

	Return : glyph(RGlyph) or None
	"""	

	for glyph in font:
		if str(ord(inputText)) == str(glyph.unicode):
			return glyph

	return None


	
	
class toolsWindow:

	def __init__(self):

		self.createUI()

	def createUI(self):
		x = 10; y = 10; w = 150; h = 22; space = 10; size = (180,300); pos = (800,300);

		self.w = FloatingWindow((pos[0],pos[1], size[0],size[1]), "ToolsWindow")
		
		self.w.searchOptionText = TextBox((x,y,w,h), "Search Option", alignment="center")
		y += h + space

		h = 40
		self.w.divider1 = HorizontalLine((x,y,w,h))
		y += h + space

		"""
		# deprecated => preset margin, width, k

		h = 50
		self.marginValue = getExtensionDefault("%s.%s" %(self.defaultKey, "margin"), 0)
		self.w.margin = SliderGroup((x,y,w,h), "Margin:", 0, 50, self.marginValue, callback=self.marginChanged)
		y += h + space
	
		self.widthValue = getExtensionDefault("%s.%s" %(self.defaultKey, "width"), 10)
		self.mainWindow.widthValue = self.widthValue
		self.w.matrixWidth = SliderGroup((x,y,w,h), "Width & Height:", 0, 100, self.widthValue, callback=self.widthChanged)
		y += h + space

		self.kValue = getExtensionDefault("%s.%s" %(self.defaultKey, "k"), 10)
		self.mainWindow.kValue = self.kValue
		self.w.topologyK = SliderGroup((x,y,w,h), "K :", 0, 400, self.kValue, callback=self.kChanged)
		y += h + space
		"""

		"""
		# 2020/03/16 modified by cho : width & height should be same
		
		heightValue = getExtensionDefault("%s.%s" %(self.defaultKey, "height"), 10)
		self.w.matrixHeight = SliderGroup((x,y,w,h), "Height:", 0, 100, heightValue, callback=self.heightChanged)
		y += h + space
	
		self.w.divider2 = HorizontalLine((x,y,w,h))
		y += h + space
		"""

		h = 22
		self.w.editTextBox = TextBox((x,y,w-40, h), "Input Glyph : ", alignment="left")
		self.w.editText = EditText((x+w-40,y,40,h))
		y += h + space

		h = 50
		indexValue = getExtensionDefault("%s.%s" %(DefaultKey, "index"), 0)
		self.w.contourIndex = SliderGroup((x,y,w,h), "ContourIndex:", 0, 50, indexValue, callback=self.indexChanged)
		y += h + space

		h = 22
		self.w.searchGlyphListButton = Button((x,y,w,h), "Search", callback=self.searchGlyphListCallback)
		y += h + space

		self.w.open()

	
	"""
	# deprecated => preset values...
	
	def marginChanged(self, sender):
	    
	    setExtensionDefault("%s.%s" %(self.defaultKey, "margin"), int(sender.get()))
	    self.w.margin.updateView()
	    
	def widthChanged(self, sender):
	    
	    setExtensionDefault("%s.%s" %(self.defaultKey, "width"), int(sender.get()))
	    self.w.matrixWidth.updateView()

	def kChanged(self, sender):
	    
	    setExtensionDefault("%s.%s" %(self.defaultKey, "k"), int(sender.get()))
	    self.w.topologyK.updateView()
	"""
	    
	# def heightChanged(self, sneder):
	    
	#     setExtensionDefault("%s.%s" %(self.defaultKey, "height"), int(sender.get()))
	#     self.w.matrixHeight.updateView()

	def indexChanged(self, sender):

		setExtensionDefault("%s.%s" %(DefaultKey, "index"), int(sender.get()))
		self.w.contourIndex.updateView()

	def searchGlyphListCallback(self, sender):
		"""
		2020/02/25
		modified by Cho
		
		If there is saved file in directory, load groupDict,
		else go through matrix, topology process to get groupDict & save it.

		and then print it on the lineView.
		"""
		file = getExtensionDefault(DefaultKey+".file")
		jsonFilePath = getExtensionDefault(DefaultKey+".jsonFilePath")
		mode = getExtensionDefault(DefaultKey+".mode")
		jsonFileName1 = getExtensionDefault(DefaultKey+".jsonFileName1")
		jsonFileName2 = getExtensionDefault(DefaultKey+".jsonFileName2")
		font = getExtensionDefault(DefaultKey+".font")
		groupDict = getExtensionDefault(DefaultKey+".groupDict")
		KoreanCheck = getExtensionDefault(DefaultKey+".korean")

		inputText = self.w.editText.get()
		standardGlyph = text2Glyph(inputText, font); setExtensionDefault(DefaultKey + ".standardGlyph", standardGlyph)
		contourIndex = int(self.w.contourIndex.slider.get()); standardContour = standardGlyph.contours[contourIndex]; setExtensionDefault(DefaultKey + ".standardContour", standardContour)

		if KoreanCheck == True:
			print("korean")
			tMC.handleSearchGlyphList(standardGlyph, contourIndex, file, mode, jsonFileName1, jsonFileName2, font, groupDict)
		else:
			print("chinese")
			ctMC.cHandleSearchGlyphList(standardGlyph, contourIndex, file, mode, jsonFileName1, jsonFileName2, font, groupDict)
		return
