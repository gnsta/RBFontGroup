from vanilla import *
from mojo.UI import *
from random import *
from mojo.events import *
from AppKit import NSCircularSlider, NSColor, NSRegularControlSize
from defconAppKit.windows.baseWindow import BaseWindowController
from fontTools.pens.basePen import BasePen
from mojo.extensions import getExtensionDefault, setExtensionDefault, getExtensionDefaultColor, setExtensionDefaultColor
from mojo.drawingTools import *
import os
import math
import rbFontG.tools.PhaseTool
import rbFontG.tools.groupTestController



class EditGroupMenu:

	def __init__(self, font, groupList):
		self.font = font
		self.groupList = groupList
		self.createUI()

	def createUI(self):
		x = 10
		y = 10
		w = -10
		h = 22
		space = 5
		size = (300, 180)

		self.w = FloatingWindow((size[0], size[1]), "EditGroupMenu")
		
		self.w.editText = EditText((x,y,w,h), text="Input Glyph...", callback=self.editTextCallback)
		y += h + space
		
		self.w.searchGlyphListButton = Button((x,y,w,h), "Search", callback=self.searchGlyphListCallback)
		y += h + space
		
		self.w.searchGlyphListByUniButton = Button((x,y,w,h), "Search by Unicode", callback=self.searchGlyphListByUniCallback)
		y += h + space
            
		#self.w.checkCurrentGlyphListButton = Button((x,y,w,h), "Apply List Label", callback=self.actionCallback)
		#y += h + space

		#self.w.colorContourButton = Button((x,y,w,h), "Apply Contour Color", callback=self.colorCurrentContour)
		#y += h + space

		#self.w.excludeGlyphButton = Button((x,y,w,h), "Exclude Selected Glyph", callback=self.excludGlyph)
		#y += h + space
		
		#self.w.bind("close", self.closeCallback)
		self.w2 = FloatingWindow((600,400), minSize=(300,300))
		self.w2.lineView = MultiLineView((0,0,-0,-0), pointSize=30)
		self.w2.lineView.setFont(self.font)
		
		self.w2.open()
		self.w.open()

	def editTextCallback(self, sender):

		inputText = self.w.editText.get()
		if len(inputText > 1):
			self.w.editText.set(inputText[0])


	def searchGlyphListCallback(self, sender):
		
		inputText = self.w.editText.get()
		self.group = None

		if len(inputText) == 1:
		    for _groupList in self.groupList:
		        for group in _groupList:
		            for n, element in enumerate(group):
		                if n == 0:
		                    if str(ord(inputText)) == str(element.unicode):
		                        self.group = groupList
		        
		    self.glyphs = []
		    
		    if self.group is None:
		        print(Message("찾고자 하는 그룹이 존재하지 않습니다."))

		    for groupElement in self.group:
		        for idx, element in enumerate(groupElement):
		             self.glyphs.append(element[0])
		             
		    self.w2.lineView.set(self.glyphs)
		    self.w2.lineView.update()
		
		else:
			pass

	def searchGlyphListByUniCallback(self, sender):

		inputGlyph = SelectGlyph(self.font)
		self.group = None
		
		for _groupList in self.groupList:
		    for group in _groupList:
		        for n, element in enumerate(group):
		            if n == 0:
		                if str((inputGlyph.unicode)) == str(element.unicode):
		                    self.group = groupList
		        
		self.glyphs = []
		    
		if self.group is None:
			print(Message("찾고자 하는 그룹이 존재하지 않습니다."))

		for groupElement in self.group:
		    for idx, element in enumerate(groupElement):
		        self.glyphs.append(element[0])
		        
		self.w2.lineView.set(self.glyphs)
		self.w2.lineView.update()

"""
#Test Code
if __name__ == '__main__':
    g = CurrentGlyph()
  
    testPath = "/Users/lewis/Downloads/아카이브/groupTest.ufo"
    testFile = OpenFont(testPath,showInterface = False)
    
    c = g.contours[0]
    
    standardMatrix = rbFontG.tools.PhaseTool.Matrix(c,3,3)
    
    compareController = rbFontG.tools.groupTestController.groupTestController(standardMatrix,0)
    
    groupList = []
    
    for idx, comGlyph in enumerate(testFile):
        resul = compareController.glyphCheckGroup(comGlyph)
        if(resul != None):
            groupList.append(resul)
            
    menuWindow = EditGroupMenu(CurrentFont(), groupList)
"""
