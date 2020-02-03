from AppKit import *
from vanilla import FloatingWindow, Slider, RadioGroup, HorizontalLine, Button
import math
from defconAppKit.windows.baseWindow import BaseWindowController
from mojo.UI import Message


from mojo.glyphPreview import GlyphPreview
from mojo.events import addObserver, removeObserver
from mojo.roboFont import CurrentGlyph, CurrentFont, RGlyph, OpenWindow, version
from mojo.UI import AllSpaceCenters, CurrentGlyphWindow
import mojo.drawingTools as drawingTools

from lib.UI.stepper import SliderEditIntStepper
from lib.fontObjects.doodleComponent import DecomposePointPen

from fontTools.misc.transform import Transform
from math import radians

class EventExample(BaseWindowController):

	def __init__(self):
		windowWidth = 200
		windowHeight = 270

		self.w = FloatingWindow((windowWidth, windowHeight), "EventExample")
		self.w.eventRadioGroup = RadioGroup((32,60,-15,50), ["first", "second", "third"], sizeStyle="small")

		self.w.divider = HorizontalLine((15,121,-15,1))

		self.w.silderOne = Slider((10,140,-10,22), value=0, maxValue=200, minValue=-200, callback=None)
		self.w.silderTwo = Slider((10,170,-10,22), value=0, maxValue=200, minValue=-200, callback=None)
		self.w.commitBtn = Button((30,230,-30,30), "Commit", callback=self.commitBtnCallback)
		
	def commitBtnCallback(self, sender):
	    res=""
	    if self.w.eventRadioGroup.get() == 0:
	        res += "first"
	    elif self.w.eventRadioGroup.get() == 1:
	        res += "second"
	    elif self.w.eventRadioGroup.get() == 2:
	        res += "third"
	        
	    if self.w.silderOne.get() - self.w.silderTwo.get() < 0:
	        res += " Negative"
	    else :
	        res += " Positive"
	    print(Message(res))
         
OpenWindow(EventExample)
