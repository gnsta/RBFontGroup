from defconAppKit.windows.baseWindow import BaseWindowController
from vanilla import EditText, FloatingWindow, CheckBox, Button, HelpButton
from mojo.UI import MultiLineView, SelectGlyph, Message
from mojo.events import addObserver,removeObserver
from mojo.drawingTools import fill, oval
from rbWindow.contourPen import BroadNibPen

def getMatchGroup(inputText, groupList):

	for group in groupList:
		for elementPair in group:
			if str(ord(inputText)) == str(elementPair[0].unicode):
				return group

	return None

def getMatchGroupByGlyph(inputGlyph, groupList):

	for group in groupList:
		for elementPair in group:
			if str(inputGlyph.unicode) == str(elementPair[0].unicode):
				return group

	return None


class EditGroupMenu(BaseWindowController):

	def __init__(self, font, groupList):
		self.font = font
		self.groupList = groupList
		self.createUI()
		self.selectedGlyphs = []
		self.markColor = 0.3, 0.4, 0.7, 0.7
		self.rewindColor = None
		self.state = False
		self.group = None
		#####
		self.layerName = self.font.layerOrder[0]
		self.currentPen = None
		####

	def createUI(self):
		x = 10; y = 10; w = 280; h = 22; space = 5; size = (800, 600)

		self.w = FloatingWindow((size[0], size[1]), "EditGroupMenu")
		
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
		
	def addGroupListCallback(self, sender):

		x = 10; y = 10; w = 150; h = 22; space = 5; size = (500, 400); pos = (800, 0)

		self.addGlyph = None
		self.addContour = None
		self.w2 = FloatingWindow((pos[0], pos[1], size[0], size[1]), "AddGroupMenu")
		self.w2.helpButton = HelpButton((x,y,20,20), callback=self.helpButtonCallback)
		y += h + space

		self.w2.selectContourIndex = EditText((x,y,w,h), text="Input Contour Index...", callback=self.editContourIndex)
		y += h + space

		self.w2.addGroupButton = Button((x,y,w,h), "Add Group by Preview", callback=self.addGroupByUniCallback)
		y += h + space

		x = w + 30
		self.w2.lineView = MultiLineView((x,0,-0,-0), selectionCallback=self.lineViewSelection, pointSize = 20)
		self.w2.lineView.setFont(self.font)

		self.w2.glyphs = []
		for glyph in self.font:
			self.w2.glyphs.append(glyph)

		self.w2.lineView.set(self.w2.glyphs)
		self.w2.open()
	    
	def lineViewSelection(self, sender):

	    self.addGlyph = sender.getSelectedGlyph()
	    
	def editContourIndex(self, sender):
	    pass
	    
	def addGroupByUniCallback(self,sender):
	    
	    if self.w2.selectContourIndex.get().isdigit():
	        idx = int(self.w2.selectContourIndex.get())
	    
	    if self.addGlyph.contours[idx] is not None:
	        listIdx = len(self.groupList)
	        self.groupList.append([[]])
	        self.groupList[listIdx][0].insert(0, self.addGlyph)
	        self.groupList[listIdx][0].insert(1, self.addGlyph.contours[idx])
	        self.w2.lineView.set(self)
	          
	    self.glyphs = []
	    
	    if self.groupList is None:
	        print(Message("찾고자 하는 그룹이 존재하지 않습니다."))
	        self.glyphs = RGlyph()
	        self.glyphs.clear()
	    else:	
	        for groupElement in self.groupList:
	            for idx, element in enumerate(groupElement):
	                self.glyphs.append(element[0])

	    self.w2.lineView.set(self.glyphs)
	    self.w2.lineView.update()

	        # 그룹 리스트에 추가하기    
	def helpButtonCallback(self, sender):
	    
	    print(Message("1. Select Glyph from Preview\n2. Input Valid Contour Index Number\n3. Hit \"Add Group by Preview Button\""))
	    
	def editTextCallback(self, sender):

		inputText = self.w.editText.get()
		if len(str(inputText)) > 1:
			self.w.editText.set(str(inputText[0]))


	def searchGlyphListCallback(self, sender):
		
		inputText = self.w.editText.get()
		self.group = None

		if len(inputText) == 1:
		    for _groupList in self.groupList:
		        for group in _groupList:
		            for n, element in enumerate(group):
		                if n == 0:
		                    if str(ord(inputText)) == str(element.unicode):
		                        self.group = self.groupList
		        
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
		
		for _groupList in self.groupList:
		    for group in _groupList:
		        for n, element in enumerate(group):
		            if n == 0:
		                if str((inputGlyph.unicode)) == str(element.unicode):
		                    self.group = groupList
		
		for i in range(len(self.groupList)):
			if(str(inputGlyph.unicode) == str(self.groupList[i][0][0])):
				self.group = groupList
				print("asldjfklsdkajflsakdjflaskjdf")        
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
