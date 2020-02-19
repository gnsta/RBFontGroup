from defconAppKit.windows.baseWindow import BaseWindowController
from vanilla import EditText, FloatingWindow, CheckBox, Button, HelpButton
from mojo.UI import MultiLineView, SelectGlyph, Message
from mojo.events import addObserver,removeObserver
from mojo.drawingTools import fill, oval
from mojo.extensions import getExtensionDefault, setExtensionDefault
from rbWindow.contourPen import BroadNibPen
from rbWindow.sliderGroup import SliderGroup

class AddGroupWindow:

	def __init__(self, mainWindow):
		
		self.font = mainWindow.font
		self.addGlyph = None
		self.groupList = mainWindow.groupList
		self.mainWindow = mainWindow
		self.glyphs = None

	def createUI(self):
		x = 10; y = 10; w = 150; h = 22; space = 5; size = (500,400); pos = (800,0);
		self.w = FloatingWindow((pos[0], pos[1], size[0], size[1]), "Add Group Window")
		self.w.helpButton = HelpButton((x,y,20,20), callback=self.helpButtonCallback)
		y += h + space

		self.w.selectContourIndex = EditText((x,y,w,h), text="Input Contour Index...")
		y += h + space

		self.w.addGroupButton = Button((x,y,w,h), "Add Selected by Preview", callback=self.addGroupByUniCallback)
		y += h + space

		x = w + 30
		self.w.lineView = MultiLineView((x,0,-0,-0), selectionCallback=self.lineViewSelection, pointSize=20)
		self.w.lineView.setFont(self.font)

		self.glyphs = []
		if self.font is not None:
			for glyph in self.font:
				self.glyphs.append(glyph)

		self.w.lineView.set(self.glyphs)
		self.w.open()


	def addGroupByUniCallback(self, sender):
		
		if self.w.selectContourIndex.get().isdigit():
			idx = int(self.w.selectContourIndex.get())

		if self.addGlyph.contours[idx] is not None: 
			listIdx = len(self.groupList)
			self.groupList.append([[]])
			self.groupList[listIdx][0].insert(0, self.addGlyph)
			self.groupList[listIdx][0].insert(1, self.addGlyph.contours[idx])
			self.w.lineView.set(self)

		self.glyphs = []

		if self.groupList is None:
			print(Message("찾고자 하는 그룹이 존재하지 않습니다."))
			self.glyphs = RGlyph()
			self.glyphs.clear()
		else:
			for groupElement in self.groupList:
				for idx, element in enumerate(groupElement):
					self.glyphs.append(element[0])

		mainWindow.groupList = self.groupList
		self.w.lineView.set(self.glyphs)
		self.w.lineView.update()

	def lineViewSelection(self, sender):
		
		self.addGlyph = sender.getSelectedGlyph()

	def helpButtonCallback(self, sender):
		
		print(Message("1. Select Glyph from Preview\n2. Input Valid Contour Index Number\n3. Hit \"Add Group by Preview Button\""))
