import json
import os

baseDir = "/Users/font/Desktop/GroupDict/"

def MakeJsonController(testPath,testFile):
    """
    Make josn File mapping ufo
    for Example
    groupTest.ufo ->  MatrixgroupTest.json & topologygroupTest.json
    나중에 경로 변환 필요
    실제로 유아이에서 자원을 뽑아 올 때의 경로는
    /Applications/RoboFont.app/Contents/Resources 이다.
    """

    try:
        if not os.path.isdir(baseDir):
            os.makedirs(os.path.join(baseDir))
    except OSError:
        print("fail to create directory")

    tempFileName = testPath.split('/')[-1]
    jFileName = tempFileName.split('.')[0] + ".json"

    try:
        if not os.path.isfile(baseDir + "Matrix" + jFileName):
            print("파일 생성")
            unicodeDict = dict()
            size = 0
            for g in testFile:
                insert = dict()
                for i in range(0,len(g.contours)):
                    insert[i] = 0
                unicodeDict["uni"+hex(g.unicode)[2:].upper()] = insert
                size += 1
            with open(baseDir + "Matrix" + jFileName,'w',encoding = 'utf-8') as make_file:
                json.dump(unicodeDict,make_file,indent= '\t')
            with open(baseDir + "Topology" + jFileName,'w',encoding = 'utf-8') as make_file:
                json.dump(unicodeDict,make_file,indent= '\t')
    except OSError:
        print("fail to create directory")
        
