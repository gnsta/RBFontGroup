from defconAppKit.windows.baseWindow import BaseWindowController
from vanilla import EditText, FloatingWindow, CheckBox, Button, HelpButton
from mojo.UI import MultiLineView, SelectGlyph, Message
from mojo.events import addObserver,removeObserver
from mojo.drawingTools import fill, oval
from mojo.extensions import getExtensionDefault, setExtensionDefault
from rbWindow.contourPen import BroadNibPen
from rbWindow.sliderGroup import SliderGroup
import rbWindow.toolMenu as toolMenu
"""
	현재 설정된 groupDict에 글리프와 컨투어를 추가하는 윈도우
"""

""" deprecated

class AddGroupWindow:

	def __init__(self, mainWindow):
		
		self.font = mainWindow.font
		self.addGlyph = None
		self.groupDict = mainWindow.groupDict
		self.mainWindow = mainWindow
		self.glyphs = None

	def createUI(self):
		x = 10; y = 10; w = 150; h = 22; space = 5; size = (500,400); pos = (800,0);
		self.w = FloatingWindow((pos[0], pos[1], size[0], size[1]), "Add Group Window")
		self.w.helpButton = HelpButton((x,y,20,20), callback=self.helpButtonCallback)
		y += h + space

		self.w.selectGlyph = EditText((x,y,w,h), text="Input Glyph...")
		y += h + space

		self.w.selectContourIndex = EditText((x,y,w,h), text="Input Contour Index...")
		y += h + space

		self.w.addGroupButton = Button((x,y,w,h), "Add to Group", callback=self.addGroupByUniCallback)
		y += h + space

		x = w + 30
		self.w.open()


	def addGroupByUniCallback(self, sender):
		self.addGlyph = toolMenu.text2Glyph(self.w.selectGlyph.get(), self.mainWindow.font)


		if self.w.selectContourIndex.get().isdigit():
			idx = int(self.w.selectContourIndex.get())

		if self.addGlyph.contours[idx] is not None:
			try:
				self.groupDict[self.addGlyph].append(idx)
			except KeyError:
				self.groupDict[self.addGlyph] = [idx] 

		self.glyphs = []

		if self.groupDict is None:
			print(Message("찾고자 하는 그룹이 존재하지 않습니다."))
			self.glyphs = None
		else:
			for glyph in self.groupDict.keys():
				self.glyphs.append(glyph)

		self.mainWindow.groupDict = self.groupDict
		self.mainWindow.w.lineView.set(self.glyphs)
		self.mainWindow.w.lineView.update()

	def helpButtonCallback(self, sender):
		
		print(Message("1. Select Glyph from Preview\n2. Input Valid Contour Index Number\n3. Hit \"Add Group by Preview Button\""))
"""