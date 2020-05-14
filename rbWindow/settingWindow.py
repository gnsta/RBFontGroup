from mojo.UI import MultiLineView, SelectGlyph, Message
from AppKit import *
from vanilla import *
from mojo.extensions import getExtensionDefault, setExtensionDefault, getExtensionDefaultColor, setExtensionDefaultColor
import rbWindow.Controller.settingWindowController as sWC
from AppKit import NSCircularSlider, NSColor, NSRegularControlSize
from defconAppKit.windows.baseWindow import BaseWindowController
from fontTools.pens.basePen import BasePen
from mojo.extensions import getExtensionDefault, setExtensionDefault, getExtensionDefaultColor, setExtensionDefaultColor
from mojo.events import addObserver, removeObserver
from mojo.UI import UpdateCurrentGlyphView
from mojo.drawingTools import *
from vanilla import *
from rbWindow.sliderGroup import *
from rbWindow.ExtensionSetting.extensionValue import *

COLOR_GREEN = (0,1,0,0.7)
BroadNibBackgroundDefaultKey = "com.asaumierdemers.BroadNibBackground"

class settingWindow(BaseWindowController):

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.createUI(self)
        self.state = False

    def createUI(self, sender):

        x = 10; y = 10; w = -10; h = 40; space = 5; size = (150, 600); pos = (1300,400)
        self.w = FloatingWindow((400,950), "Background Setting")
        stepValue = getExtensionDefault(DefaultKey + ".step")
        print("stepValue : ",stepValue)
        self.w.step = SliderGroup((x, y, w, h), "Steps:", 0, 60, stepValue, callback=self.stepChanged)
        self.mainWindow.step = stepValue
        y+=h
        
        widthValue = getExtensionDefault("%s.%s" %(DefaultKey, ".width"), 50)
        self.w.width = SliderGroup((x, y, w, h), "Width:", 0, 300, widthValue, callback=self.widthChanged)
        self.mainWindow.width = widthValue
        y+=h
        
        heightValue = getExtensionDefault("%s.%s" %(DefaultKey, ".height"), 10)
        self.w.height = SliderGroup((x, y, w, h), "Height:", 0, 300, heightValue, callback=self.heightChanged)
        self.mainWindow.height = heightValue
        y+=h

        color = NSColor.colorWithCalibratedRed_green_blue_alpha_(1, 0, 0, .5)
        colorValue = getExtensionDefaultColor("%s.%s" %(DefaultKey, ".color"), color)
        self.w.colortext = TextBox((x, y, -0, 20), "Color:")
        self.w.color = ColorWell((70, y-5, w, 30), callback=self.colorChanged, color=colorValue)
        self.mainWindow.color = colorValue
        y+=h + 20

        self.w.markOptionTextBox = TextBox((x,y,w,h), "Marking Options")
        y += h + space
        """
        self.w.checkGlyphListCheckBox = CheckBox((x,y,w,h), "Apply List Label", callback=self.checkGlyphListCallback)
        y += h + space"""
        y += 30
        self.w.colorContourCheckBox= CheckBox((x,y,w,h), "Apply Contour Color", callback=self.colorContourCallback)
        y += h + 20

        self.w.methodRadioGroup = RadioGroup((x,y,w,h), ["Matrix", "Topology"], sizeStyle="small", callback=self.methodChangedCallback)
        y += h + space

        self.w.open()

    def colorChanged(self, sender):
        setExtensionDefaultColor("%s.%s" % (DefaultKey, ".color"), sender.get())
        self.mainWindow.color = self.getColor()
        self.updateView()

    def stepChanged(self, sender):
        setExtensionDefault("%s.%s" %(DefaultKey, ".step"), int(sender.get()))
        self.mainWindow.step = int(sender.get())
        print("self.mainWindow.window.step = ",self.mainWindow.step)
        self.updateView()

    def widthChanged(self, sender):
        setExtensionDefault("%s.%s" %(DefaultKey, ".width"), int(sender.get()))
        self.mainWindow.width = int(sender.get())
        self.updateView()

    def heightChanged(self, sender):
        setExtensionDefault("%s.%s" %(DefaultKey, ".height"), int(sender.get()))
        self.mainWindow.height = int(sender.get())
        self.updateView()


    def getColor(self):
        color = self.w.color.get()
        return color.getRed_green_blue_alpha_(None, None, None, None)

    def checkGlyphListCallback(self, sender):
        pass
        """
        print("before : ", self.mainWindow.selectedGlyphs)
        sWC.helpCheckGlyphList(self.w.checkGlyphListCheckBox, self.mainWindow)
        print("after : ", self.mainWindow.selectedGlyphs)"""
    def colorContourCallback(self, sender):
        self.mainWindow.state = self.w.colorContourCheckBox.get()

    def methodChangedCallback(self, sender):
        # select matrix or topology
        setExtensionDefault(DefaultKey+".mode", self.w.methodRadioGroup.get())

    def updateView(self, sender=None):
        UpdateCurrentGlyphView()

