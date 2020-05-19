from mojo.UI import OpenGlyphWindow
from vanilla import EditText, FloatingWindow, CheckBox, Button, HelpButton, RadioGroup, HorizontalLine
from mojo.UI import MultiLineView, SelectGlyph, Message

    
def openGlyph(RGlyph, option):
    if option is True:
        OpenGlyphWindow(RGlyph, newWindow=True)
    else:
    	OpenGlyphWindow(RGlyph, newWindow=False)

class previewWindow:

	def __init__(self, mainWindow):
		self.mainWindow = mainWindow

	def createUI(self, sender):

		x = 10; y = 10; w = 280; h = 22; space = 5; size = (800,600)
		
		self.w = FloatingWindow((size[0],size[1]), "Preview Window")

		self.w.lineView = MultiLineView((w,0,520,600), pointSize=30, selectionCallback=self.lineViewSelectionCallback)
		self.w.lineView.setFont(self.mainWindow.file)
		self.w.lineView.set(self.mainWindow.glyphs)
		self.w.open()

	def lineViewSelectionCallback(self, sender):
		openGlyph(sender.getSelectedGlyph(), False)