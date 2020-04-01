from defconAppKit.windows.baseWindow import BaseWindowController
from vanilla import *
from mojo.UI import MultiLineView, SelectGlyph, Message
from mojo.events import addObserver,removeObserver
from mojo.drawingTools import fill, oval
from mojo.extensions import getExtensionDefault, setExtensionDefault
from rbWindow.contourPen import BroadNibPen
from rbWindow.sliderGroup import SliderGroup
import rbFontG.tools.tMatrix.PhaseTool
import rbFontG.tools.tMatrix.groupTestController
from rbFontG.tools.tTopology import topologyJudgement as tj
from rbFontG.tools.tTopology import topologyAssignment as ta
from rbFontG.tools import parseUnicodeControll as puc
import jsonConverter.searchModule as search
import timeit#
import jsonConverter.converter as convert
import rbWindow.Controller.toolMenuController as tMC

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

	def __init__(self, mainWindow):

		self.defaultKey = "com.asaumierdemers.BroadNibBackground"
		# self.mainWindow.mode = mainWindow.w.methodRadioGroup.get()		# mode 0: matrix, 1: topology

		self.file = mainWindow.file
		self.groupDict = None

		self.font = mainWindow.font
		self.mainWindow = mainWindow
		self.marginValue = 0
		self.widthValue = 0
		self.mainWindow.widthValue = 0
		self.selectedGlyphs = []


	def createUI(self, sender):
		x = 10; y = 10; w = 150; h = 22; space = 10; size = (180,300); pos = (800,300);

		self.w = FloatingWindow((pos[0],pos[1], size[0],size[1]), "ToolsWindow")
		
		self.w.searchOptionText = TextBox((x,y,w,h), "Search Option", alignment="center")
		y += h + space

		h = 40
		self.w.methodRadioGroup = RadioGroup((x,y,w,h), ["Matrix", "Topology"], sizeStyle="small", callback=self.methodChangedCallback)
		y += h + space

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
		indexValue = getExtensionDefault("%s.%s" %(self.defaultKey, "index"), 0)
		self.w.contourIndex = SliderGroup((x,y,w,h), "ContourIndex:", 0, 50, indexValue, callback=self.indexChanged)
		y += h + space

		h = 22
		self.w.searchGlyphListButton = Button((x,y,w,h), "Search", callback=self.searchGlyphListCallback)
		y += h + space

		self.w.open()


	def methodChangedCallback(self, sender):
		# select matrix or topology
		"""
		if self.w.methodRadioGroup.get() == 0:
			self.w.margin.enable()
			self.w.matrixWidth.enable()
			self.w.topologyK.disable()
			
		else:
			self.w.margin.disable()
			self.w.matrixWidth.disable()
			self.w.topologyK.enable()
		"""
		self.mainWindow.mode = self.w.methodRadioGroup.get()
	
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

		setExtensionDefault("%s.%s" %(self.defaultKey, "index"), int(sender.get()))
		self.w.contourIndex.updateView()

	def searchGlyphListCallback(self, sender):
		"""
		2020/02/25
		modified by Cho
		
		If there is saved file in directory, load groupDict,
		else go through matrix, topology process to get groupDict & save it.

		and then print it on the lineView.
		"""
		inputText = self.w.editText.get()
		standardGlyph = text2Glyph(inputText, self.font); self.mainWindow.standardGlyph = standardGlyph
		contourIndex = int(self.w.contourIndex.slider.get()); self.mainWindow.standardContour = standardGlyph.contours[contourIndex]	# standardGlyph로부터 standardContour 인덱스 설정
		file = self.file

		
		tMC.handleSearchGlyphList(self.mainWindow.standardGlyph, contourIndex, self.mainWindow.file, self, self.mainWindow)
		return
