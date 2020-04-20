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

COLOR_GREEN = (0,1,0,0.7)
BroadNibBackgroundDefaultKey = "com.asaumierdemers.BroadNibBackground"

class settingWindow(BaseWindowController):

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.createUI(self)
        self.state = False

    def createUI(self, sender):

        x = 10; y = 10; w = -10; h = 40; space = 5; size = (200, 800); pos = (1300,400)
        self.w = FloatingWindow((400,950), "Background Setting")
        stepValue = getExtensionDefault("%s.%s" %(BroadNibBackgroundDefaultKey, "step"), 20)
        self.w.step = SliderGroup((x, y, w, h), "Steps:", 0, 60, stepValue, callback=self.stepChanged)
        self.mainWindow.step = stepValue
        y+=h
        
        widthValue = getExtensionDefault("%s.%s" %(BroadNibBackgroundDefaultKey, "width"), 50)
        self.w.width = SliderGroup((x, y, w, h), "Width:", 0, 300, widthValue, callback=self.widthChanged)
        self.mainWindow.width = widthValue
        y+=h
        
        heightValue = getExtensionDefault("%s.%s" %(BroadNibBackgroundDefaultKey, "height"), 10)
        self.w.height = SliderGroup((x, y, w, h), "Height:", 0, 300, heightValue, callback=self.heightChanged)
        self.mainWindow.height = heightValue
        y+=h
        
        angleValue = getExtensionDefault("%s.%s" %(BroadNibBackgroundDefaultKey, "angle"), 30)
        self.w.angle = SliderGroup((x, y, w, h), "Angle:", 0, 360, angleValue, callback=self.angleChanged)
        self.w.angle.slider.getNSSlider().cell().setSliderType_(NSCircularSlider)
        self.w.angle.text.setPosSize((0, 15, -0, 20))
        self.w.angle.slider.setPosSize((60, 10, 30, 30))
        self.w.angle.slider._nsObject.cell().setControlSize_(NSRegularControlSize)
        self.mainWindow.angle = angleValue
        y+=h + 20
        
        shapeValue = getExtensionDefault("%s.%s" %(BroadNibBackgroundDefaultKey, "shape"), 0)
        self.w.shapetext = TextBox((x, y, -0, 20), "Shape:")
        self.w.shape = RadioGroup((74, y, -0, 20), ["oval", "rect"], isVertical=False, callback=self.shapeChanged)
        self.mainWindow.shape = shapeValue
        self.w.shape.set(shapeValue)
        y+=h + 5

        color = NSColor.colorWithCalibratedRed_green_blue_alpha_(1, 0, 0, .5)
        colorValue = getExtensionDefaultColor("%s.%s" %(BroadNibBackgroundDefaultKey, "color"), color)
        self.w.colortext = TextBox((x, y, -0, 20), "Color:")
        self.w.color = ColorWell((70, y-5, w, 30), callback=self.colorChanged, color=colorValue)
        self.mainWindow.color = colorValue
        y+=h + 20

        self.w.markOptionTextBox = TextBox((x,y,w,h), "Marking Options")
        y += h + space
        """
        self.w.checkGlyphListCheckBox = CheckBox((x,y,w,h), "Apply List Label", callback=self.checkGlyphListCallback)
        y += h + space"""
        y += 50
        self.w.colorContourCheckBox= CheckBox((x,y,w,h), "Apply Contour Color", callback=self.colorContourCallback)
        self.w.open()

    def colorChanged(self, sender):
        setExtensionDefaultColor("%s.%s" % (BroadNibBackgroundDefaultKey, "color"), sender.get())
        self.mainWindow.color = self.getColor()
        self.updateView()

    def stepChanged(self, sender):
        setExtensionDefault("%s.%s" %(BroadNibBackgroundDefaultKey, "step"), int(sender.get()))
        self.mainWindow.step = int(sender.get())
        print("self.mainWindow.window.step = ",self.mainWindow.step)
        self.updateView()

    def widthChanged(self, sender):
        setExtensionDefault("%s.%s" %(BroadNibBackgroundDefaultKey, "width"), int(sender.get()))
        self.mainWindow.width = int(sender.get())
        self.updateView()

    def heightChanged(self, sender):
        setExtensionDefault("%s.%s" %(BroadNibBackgroundDefaultKey, "height"), int(sender.get()))
        self.mainWindow.height = int(sender.get())
        self.updateView()

    def angleChanged(self, sender):
        setExtensionDefault("%s.%s" %(BroadNibBackgroundDefaultKey, "angle"), int(sender.get()))
        self.mainWindow.angle = int(sender.get())
        self.updateView()

    def shapeChanged(self, sender):
        setExtensionDefault("%s.%s" %(BroadNibBackgroundDefaultKey, "shape"), sender.get())
        if self.w.shape.get() == 0:
            self.mainWindow.shape = oval
        else:
            self.mainWindow.shape = rect
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

    def updateView(self, sender=None):
        UpdateCurrentGlyphView()
