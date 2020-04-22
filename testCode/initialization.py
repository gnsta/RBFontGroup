from jsonConverter.makeJsonFile import *
from jsonConverter.clockWiseGroup import *
import rbWindow.editWindow as ew
from mojo.UI import *
import os
import math

class FileExist(Exception):
    def __init__(self,msg):
        self.msg = msg
        
    def __str__(self):
        return self.msg

def StartProgram(testPath,testFile):
    MakeJsonController(testPath,testFile)
    insert = dict()
    bar = ProgressBar('start',len(testFile),'initial setting...')
    barProcess = 0
    
    try:
        tempFileName = testPath.split('/')[-1]
        jsonFileName = os.getcwd() + '/jsonResource/' + tempFileName.split('.')[0] + '.json'
        if os.path.exists(jsonFileName):
            raise FileExist('해당 파일은 이미 존재합니다')
        for tg in testFile:
            barProcess += 1
            tempList = list()
            for tc in tg.contours:
                compare = getClockWiseList(tc)
                tempList.append(compare)
            insert[tg.name] = tempList
            if barProcess % 10 == 0:
                bar.tick(barProcess)     
        with open(jsonFileName,'w',encoding = 'utf-8') as make_file:
            json.dump(insert,make_file,indent = '\t')
    except FileExist as e:
        print(e)
    
    bar.close()

    return jsonFileName
