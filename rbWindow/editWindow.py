from defconAppKit.windows.baseWindow import BaseWindowController
from vanilla import EditText, FloatingWindow, CheckBox, Button, HelpButton, RadioGroup, HorizontalLine
from mojo.UI import MultiLineView, SelectGlyph, Message
from mojo.events import addObserver,removeObserver
from mojo.drawingTools import fill, oval
from mojo.extensions import getExtensionDefault, setExtensionDefault
from rbWindow.contourPen import BroadNibPen
from rbWindow.sliderGroup import SliderGroup
from rbWindow.addGroupWindow import AddGroupWindow
from rbWindow.toolMenu import toolsWindow

def getMatchGroup(inputText, groupList):

	for group in groupList:
		#print("group : ", group)
		for elementList in group:
			for idx, element in enumerate(elementList):
				if idx == 0:
					#print("element : "+str(element))
					if str(ord(inputText)) == str(element.unicode):
						return groupList

	return None

def getMatchGroupByGlyph(inputGlyph, groupList):

	for group in groupList:
		for elementList in group:
			for idx, element in enumerate(elementList):
				if idx == 0:
					#print("element : "+str(element))
					if str(inputGlyph.unicode) == str(element.unicode):
						return groupList

	return None


class EditGroupMenu(BaseWindowController):

	def __init__(self, font, groupList, file):
		self.font = font
		self.groupList = groupList
		self.defaultKey = "com.asaumierdemers.BroadNibBackground"
		self.createUI()
		self.selectedGlyphs = []
		self.markColor = 0.3, 0.4, 0.7, 0.7
		self.rewindColor = None
		self.state = False
		self.group = None
		self.file = file

		self.layerName = self.font.layerOrder[0]
		self.currentPen = None
		
		
	def createUI(self):
		x = 10; y = 10; w = 280; h = 22; space = 5; size = (800, 600)

		self.w = FloatingWindow((size[0], size[1]), "EditGroupMenu")
		
		self.w.methodRadioGroup = RadioGroup((32,20,w,50), ["Matrix", "Topology"], sizeStyle="small")
		y += 100 + space

		self.w.popSearchWindowButton = Button((x,y,w,h), "Go to Search Window", callback=self.popSearchWindow)
		y += h + space

		self.w.divider1 = HorizontalLine((x,y,w,h))
		y += h + space

		self.w.editText = EditText((x,y,w,h), text="Input Glyph...", callback=self.editTextCallback)
		y += h + space
			
		self.w.searchGlyphListButton = Button((x,y,w,h), "Search", callback=self.searchGlyphListCallback)
		y += h + space
		
		self.w.searchGlyphListByUniButton = Button((x,y,w,h), "Search by Unicode", callback=self.searchGlyphListByUniCallback)
		y += h + space
            
		self.w.checkGlyphListButton = Button((x,y,w,h), "Apply List Label", callback=self.checkGlyphListCallback)
		y += h + space
		
		self.w.addGroupListButton = Button((x,y,w,h), "Add Group", callback=self.addGroupListCallback)
		y += h + space
		
		h += 30
		self.w.colorContourCheckBox= CheckBox((10,y,w,h), "Apply Contour Color", callback=self.colorContourCallback)
		y += h + space

		#self.w.excludeGlyphButton = Button((x,y,w,h), "Exclude Selected Glyph", callback=self.excludGlyph)
		#y += h + space

		addObserver(self, "drawBroadNibBackground", "drawBackground")

		self.setUpBaseWindowBehavior()
		
		self.w.bind("close", self.windowCloseCallback)
		
		x = w + 30
		self.w.lineView = MultiLineView((x,0,-0,-0), pointSize=30)
		self.w.lineView.setFont(self.font)
		
		self.w.open()

	def popSearchWindow(self, sender):

		self.w3 = toolsWindow(self)
		self.w3.createUI(sender)
	
	def addGroupListCallback(self, sender):

		self.w2 = AddGroupWindow(self)
		self.w2.createUI()

	def editTextCallback(self, sender):

		inputText = self.w.editText.get()
		if len(str(inputText)) > 1:
			self.w.editText.set(str(inputText[0]))


	def searchGlyphListCallback(self, sender):
		
		inputText = self.w.editText.get()
		self.group = None

		if len(inputText) == 1:
		    self.group = getMatchGroup(inputText, self.groupList)
		    #print(self.group)    
		    self.glyphs = []
		    
		    if self.group is None:
		        print(Message("찾고자 하는 그룹이 존재하지 않습니다."))
		        self.glyphs = RGlyph()
		        self.glyphs.clear()
		    else:
        		    for groupElement in self.group:
        		        for idx, element in enumerate(groupElement):
        		             self.glyphs.append(element[0])
		             
		    self.w.lineView.set(self.glyphs)
		    self.w.lineView.update()

	def searchGlyphListByUniCallback(self, sender):

		inputGlyph = SelectGlyph(self.font)
		self.group = None
		
		self.group = getMatchGroupByGlyph(inputGlyph, self.groupList)
		#print(self.group)
		for i in range(len(self.groupList)):
			if(str(inputGlyph.unicode) == str(self.groupList[i][0][0])):
				self.group = groupList
			
		self.glyphs = []
		    
		if self.group is None:
			print(Message("찾고자 하는 그룹이 존재하지 않습니다."))
			self.glyphs = RGlyph()
			self.glyphs.clear()
		else:	
        		for groupElement in self.group:
        		    for idx, element in enumerate(groupElement):
        		        self.glyphs.append(element[0])
		        
		self.w.lineView.set(self.glyphs)
		self.w.lineView.update()

	def checkGlyphListCallback(self, sender):

		if self.glyphs is None:
			print(Message("칠할 수 있는 그룹이 존재하지 않습니다."))
			return
		
		if self.selectedGlyphs is not None:
        		for glyph in self.selectedGlyphs:
        		    glyph.markColor = self.rewindColor
        		    glyph.selected = False
		    
		self.selectedGlyphs = []
         
		for glyph in self.glyphs:
		    glyph.selected = True
		    glyph.markColor = self.markColor
		    self.selectedGlyphs.append(glyph)
		    
	def colorContourCallback(self, sender):
	    
	    self.state = self.w.colorContourCheckBox.get()
	    

	def windowCloseCallback(self, sender):
	    
	    if self.selectedGlyphs is not None:
	        for glyph in self.selectedGlyphs:
	            glyph.selected = False
	            glyph.markColor = self.rewindColor

	    removeObserver(self, "drawBackground")
	    super(BroadNibBackground, self).windowCloseCallback(sender)
	    
	def drawBroadNibBackground(self, info):

	    glyph = info["glyph"].getLayer(self.layerName)
	    
	    contour = None
	    if self.group is not None:
	    	for groupElement in self.group:
	        	for idx, element in enumerate(groupElement):
	        		if glyph == element[0]:
	        			contour = element[1]
	    
	    fill(0.7,0.3,1,0.6)
	    
	    if info["glyph"].layerName == self.layerName or not self.currentPen:
	        self.currentPen = BroadNibPen(None, 60, 80, 50, 30, oval)
	    
	    if contour is not None and self.state == True:    
	        contour.draw(self.currentPen)