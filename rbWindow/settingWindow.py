from vanilla import EditText, FloatingWindow, CheckBox, Button, HelpButton, RadioGroup, HorizontalLine, TextBox
from mojo.UI import MultiLineView, SelectGlyph, Message
import rbWindow.Controller.settingWindowController as sWC

COLOR_GREEN = (0,1,0,0.7)

class settingWindow:


	def __init__(self, mainWindow):
		self.mainWindow = mainWindow
		self.state = False

	def createUI(self, sender):

		x = 10; y = 10; w = 280; h = 22; space = 5; size = (180, 450); pos = (1300,400)

		self.w = FloatingWindow((pos[0], pos[1], size[0], size[1]), "Settings & Other")
		"""		
		self.w.addGroupListButton = Button((x,y,w,h), "Add Group", callback=self.addGroupListCallback)
		y += h + space
		"""

		self.w.markOptionTextBox = TextBox((x,y,w,h), "Marking Options")
		y += h + space
		"""
		self.w.checkGlyphListCheckBox = CheckBox((x,y,w,h), "Apply List Label", callback=self.checkGlyphListCallback)
		y += h + space"""

		h += 30
		self.w.colorContourCheckBox= CheckBox((x,y,w,h), "Apply Contour Color", callback=self.colorContourCallback)
		y += h + space

		self.w.divider1 = HorizontalLine((x,y,w,h))

		self.w.open()

	def checkGlyphListCallback(self, sender):
		pass
		"""
		print("before : ", self.mainWindow.selectedGlyphs)
		sWC.helpCheckGlyphList(self.w.checkGlyphListCheckBox, self.mainWindow)
		print("after : ", self.mainWindow.selectedGlyphs)"""
	def colorContourCallback(self, sender):

		self.mainWindow.state = self.w.colorContourCheckBox.get()

