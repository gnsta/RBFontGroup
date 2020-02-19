
from vanilla import Slider, TextBox, EditText, Group

class SliderGroup(Group):

	def __init__(self, posSize, text, minValue, maxValue, value, callback):
		Group.__init__(self, posSize)
		self.text = TextBox((0,0,-0,20), text)
		self.slider = Slider((2,20,-60,17), minValue=minValue, maxValue=maxValue, value=value, sizeStyle="small", callback=self.sliderChanged)
		self.edit = EditText((-40,15,-0,22), text=str(value), placeholder=str(value), callback=self.editChanged)
		self.callback = callback

	def sliderChanged(self, sender):
		self.edit.set(str(int(self.slider.get())))
		self.callback(sender)

	def editChanged(self, sender):
		try:
			value = int(float(self.edit.get()))
		except ValueError:
			value = int(self.edit.getPlaceholder())
			self.edit.set(value)
		self.slider.set(value)
		#self.callback(sender)