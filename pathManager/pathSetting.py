import mojo.extensions

toolName = "roboTool"

fontToolBundle = mojo.extensions.ExtensionBundle(toolName)
baseDir = fontToolBundle.resourcesPath() + "/GroupDict/"
saveFilePath = baseDir
ufoPath = "/Users/sslab/Desktop/groupTest2350.ufo"
ImagePath = fontToolBundle.resourcesPath()+"/"
resourcePath = ImagePath

attrImgList = ["innerFill", "penPair", "dependX", "dependY",  "rubbish", "select"]

