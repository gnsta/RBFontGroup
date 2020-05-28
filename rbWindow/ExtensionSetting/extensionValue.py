# 익스텐션 초기 기본 값 설정 (프로그램 초기 구동 시에 딱 한 번만 수행되고 이후론 수행하지 않음)
from AppKit import NSColor
from mojo.extensions import *
from rbWindow.Controller import linkedStack
from rbWindow.Controller.linkedStack import *

DefaultKey = "com.robofontTool.rbFontGroup"
rewindBufferSize = 50

class ConfigExtensionSetting:

	def __init__(self, registerKey):

		bufferStack = Stack(rewindBufferSize)

		self.registerKey = registerKey
		self.defaults = {
			self.registerKey + ".registered": True,
		    
		    self.registerKey + ".font": None,
		    self.registerKey + ".jsonFilePath": None,
		    self.registerKey + ".jsonFileName1": None,
		    self.registerKey + ".jsonFileName2": None,
		    self.registerKey + ".file": None,
		    
		    self.registerKey + ".mode": 0,

		    self.registerKey + ".margin": 20,
		    self.registerKey + ".width": 100,
		    self.registerKey + ".height": 100,
		    self.registerKey + ".k": 500,

		    self.registerKey + ".matrix_margin": 20,
		    self.registerKey + ".matrix_size": 3,
		    self.registerKey + ".topology_margin": 500,
		    
		    self.registerKey + ".groupDict": None,
		    self.registerKey + ".contourNumber": None,
		    self.registerKey + ".smartSet": None,
		    self.registerKey + ".standardContour": None,
		    self.registerKey + ".standardGlyph": None,
		    self.registerKey + ".matrix": None,
		    
		    self.registerKey + ".syllableJudgementController": None,
		    self.registerKey + ".smartSetIndex": None,
		    self.registerKey + ".restoreStack": bufferStack,
		    
		    self.registerKey + ".index": 0,
		    self.registerKey + ".step": 30,
		    self.registerKey + ".width": 30,
		    self.registerKey + ".height": 10,
		    self.registerKey + ".color": NSColor.colorWithCalibratedRed_green_blue_alpha_(1, 0, 0, .5)
		}


	def registerSettings(self):
		"""
			2020/05/06 created by Cho Hyun Woo
			Extension에 대한 기본적인 설정값을 등록한다.
		"""
		'''
		check = None
		try:
			check = getExtensionDefault(registerKey+".registered")
			if check is not True:
				raise NotRegisteredException
		
		except NotRegisteredException:
			'''

		registerExtensionDefaults(self.defaults)

	def removeSettings(self):

		"""
			익스텐션 세팅이 제대로 동작하지 않을 때 메인 코드에 한 번 넣고 돌린 후 지우고 다시 설치하여 사용한다.
		"""
		removeExtensionDefault(self.registerKey)

class NotRegisteredException(Exception):
    def __init__(self):
        super().__init__('First Started Program, Register Operated...')

