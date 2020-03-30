from rbFontG.tools.parseUnicodeControll import *
from parseSyllable.configVersion1 import *
from parseSyllable.configVersion2 import *

def getConfigure(RGlyph):
	"""
	Return :: Dictionary
		{"glyph.unicode" : [[first contour's index],[middle contour's index],[final contour's index]]}
	"""

	unicodeObj = parseUnicodeController(RGlyph.unicode)
	uniCodeIdx = unicodeObj.parseUnicode()

	configValue = None

	if uniCodeIdx[1] in parseUnicodeController.vowel_horizontal:
		configValue = getConfigureVersion1(RGlyph)
	else:
		configValue = getConfigureVersion2(RGlyph)

	return configValue