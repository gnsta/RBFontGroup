import pandas as pd 
import numpy as np
import matplotlib.pylab as plt
from sklearn.cluster import KMeans
from rbFontG.tools.parseUnicodeControll import *
from parseSyllable.utility.contourDistributionChart import *
from rbFontG.tools.parseUnicodeControll import *
import os
import json
from mojo.UI import *

class PositionState:
    def __init__(self,con,conNumber):
        self.con = con
        self.conNumber = conNumber
class PointInfo:
    def __init__(self,x,y):
        self.x = x
        self.y = y
class FileExist(Exception):
    def __init__(self,msg):
        self.msg = msg
    def __str__(self):
        return self.msg
    

class SyllableJudgement:
    def __init__(self, fontFile, fontPath):

        self.middle_one = ['ㅏ','ㅑ','ㅓ','ㅕ','ㅣ','ㅐ']
        self.middle_two = ['ㅔ','ㅖ','ㅒ']
        self.middle_three = ['ㅗ','ㅛ','ㅜ','ㅠ','ㅡ']
        self.middle_four = ['ㅘ','ㅚ','ㅟ', 'ㅢ','ㅙ']
        self.middle_five = ['ㅝ']
        self.middle_six = ['ㅞ']

        tempFileName = fontPath.split('/')[-1]

        if tempFileName.split('.')[1] == 'ufo':
            try:
                tempFileName = fontPath.split('/')[-1]
                self.jsonFileName = os.path.dirname(os.path.abspath(__file__)) +'/jsonResource/'+ tempFileName.split('.')[0] + '_label.json'
                if os.path.exists(self.jsonFileName):
                    with open(self.jsonFileName, 'r') as jsonFile:
                        self.infoDict = json.load(jsonFile)
                    raise FileExist('라벨 파일은 이미 존재합니다')

                axis_x1 = list()
                axis_x2 = list()
                axis_x4 = list()
                axis_x5 = list()
                axis_x6 = list()

                axis_y1 = list()
                axis_y2 = list()
                axis_y4 = list()
                axis_y5 = list()
                axis_y6 = list()

                point_list1 = list()
                point_list2 = list()
                point_list4 = list()
                point_list5 = list()
                point_list6 = list()


                check_glyph1 = list()
                check_glyph2 = list()
                check_glyph4 = list()
                check_glyph5 = list()
                check_glyph6 = list()
                bar = ProgressBar('Analysis Progress',len(fontFile),'analysis...')
                barProcess = 0

                #각 케이스대로 데이터를 분류
                for gly in fontFile:
                    puc = parseUnicodeController(gly.unicode)
                    chars = puc.getChars()
                    barProcess += 1
                    #종성 케이스1의 경우
                    if (chars[1] in self.middle_one) and (chars[2] is not None):
                        for i,con in enumerate(gly.contours):
                            temp = getContourPosition(gly,con,10000,10000)
                            point_list1.append(PointInfo(temp[0],temp[1]))
                            axis_x1.append(temp[0])
                            axis_y1.append(temp[1])
                            check_glyph1.append([gly,i])                 
                    elif chars[1] in self.middle_two and (chars[2] is not None):
                        for i,con in enumerate(gly.contours):
                            temp = getContourPosition(gly,con,10000,10000)
                            point_list2.append(PointInfo(temp[0],temp[1]))
                            axis_x2.append(temp[0])
                            axis_y2.append(temp[1])
                            check_glyph2.append([gly,i])
                    elif chars[1] in self.middle_four and (chars[2] is not None):
                        for i,con in enumerate(gly.contours):
                            temp = getContourPosition(gly,con,10000,10000)
                            point_list4.append(PointInfo(temp[0],temp[1]))
                            axis_x4.append(temp[0])
                            axis_y4.append(temp[1])
                            check_glyph4.append([gly,i])
                    elif chars[1] in self.middle_five and (chars[2] is not None):
                        for i,con in enumerate(gly.contours):
                            temp = getContourPosition(gly,con,10000,10000)
                            point_list5.append(PointInfo(temp[0],temp[1]))
                            axis_x5.append(temp[0])
                            axis_y5.append(temp[1])
                            check_glyph5.append([gly,i])
                    elif chars[1] in self.middle_six and (chars[2] is not None):
                        for i,con in enumerate(gly.contours):
                            temp = getContourPosition(gly,con,10000,10000)
                            point_list6.append(PointInfo(temp[0],temp[1]))
                            axis_x6.append(temp[0])
                            axis_y6.append(temp[1])
                            check_glyph6.append([gly,i])

                    if barProcess % 10 == 0:
                        bar.tick(barProcess)

                #데이터 샘플 만들기
                np_axis_x1 = np.array(axis_x1)
                np_axis_y1 = np.array(axis_y1)
                self.samples1 = np.array(list(zip(np_axis_x1, np_axis_y1)))

                np_axis_x2 = np.array(axis_x2)
                np_axis_y2 = np.array(axis_y2)
                self.samples2 = np.array(list(zip(np_axis_x2, np_axis_y2)))

                np_axis_x4 = np.array(axis_x4)
                np_axis_y4 = np.array(axis_y4)
                self.samples4 = np.array(list(zip(np_axis_x4, np_axis_y4)))

                np_axis_x5 = np.array(axis_x5)
                np_axis_y5 = np.array(axis_y5)
                self.samples5 = np.array(list(zip(np_axis_x5, np_axis_y5)))

                np_axis_x6 = np.array(axis_x6)
                np_axis_y6 = np.array(axis_y6)
                self.samples6 = np.array(list(zip(np_axis_x6, np_axis_y6)))

                #각 데이터 포인트를 그룹화 할 labels을 생성
                self.labels1 = np.zeros(len(np_axis_x1))
                self.labels2 = np.zeros(len(np_axis_x2))
                self.labels4 = np.zeros(len(np_axis_x4))
                self.labels5 = np.zeros(len(np_axis_x5))
                self.labels6 = np.zeros(len(np_axis_x6))

                #model들의 생성
                self.labels1 = self.MakeLabel(1,self.samples1)
                self.labels2 = self.MakeLabel(2,self.samples2)
                self.labels4 = self.MakeLabel(4,self.samples4)
                self.labels5 = self.MakeLabel(5,self.samples5)
                self.labels6 = self.MakeLabel(6,self.samples6)
                bar.close()

                #종성의 라벨을 구함
                num = self.samples1[:,1].argmin()
                self.final_label1 = self.labels1[num]

                num = self.samples2[:,1].argmin()
                self.final_label2 = self.labels2[num]

                num = self.samples4[:,1].argmin()
                self.final_label4 = self.labels4[num]

                num = self.samples5[:,1].argmin()
                self.final_label5 = self.labels5[num]

                num = self.samples6[:,1].argmin()
                self.final_label6 = self.labels6[num]

                #각 라벨에 대한 정보를 json파일에 저장
                insert = dict()
                insert["final label1"] = int(self.final_label1)
                insert["final label2"] = int(self.final_label2)
                insert["final label4"] = int(self.final_label4)
                insert["final label5"] = int(self.final_label5)
                insert["final label6"] = int(self.final_label6)

                for i,content in enumerate(check_glyph1):
                    insert[content[0].name +'/' +str(content[1])] = int(self.labels1[i])
                for i,content in enumerate(check_glyph2):
                    insert[content[0].name +'/' + str(content[1])] = int(self.labels2[i])
                for i,content in enumerate(check_glyph4):
                    insert[content[0].name +'/' + str(content[1])] = int(self.labels4[i])
                for i,content in enumerate(check_glyph5):
                    insert[content[0].name +'/' + str(content[1])] = int(self.labels5[i])
                for i,content in enumerate(check_glyph6):
                    insert[content[0].name +'/' + str(content[1])] = int(self.labels6[i])
                        
                with open(self.jsonFileName,'w',encoding = 'utf-8') as make_file:
                    self.infoDict = insert
                    json.dump(insert,make_file,indent = '\t')
            except FileExist as e:
                print(e)

    def MakeLabel(self,case,samples):
        #case1
        if case == 1:
            model = KMeans(n_clusters = 3)
            model.fit(samples)
            labels = model.predict(samples)
            centers = model.cluster_centers_

            model = KMeans(n_clusters = 3, init = centers)
            model.fit(samples)
            labels = model.predict(samples)

        #case2
        if case == 2:
            model = KMeans(n_clusters = 3)
            model.fit(samples)
            labels = model.predict(samples)
            centers = model.cluster_centers_

            model = KMeans(n_clusters = 3, init = centers)
            model.fit(samples)
            labels = model.predict(samples)

        #case4
        if case == 4:
            model = KMeans(n_clusters = 3)
            model.fit(samples)
            labels = model.predict(samples)
            centers = model.cluster_centers_

            model = KMeans(n_clusters = 3, init = centers)
            model.fit(samples)
            labels = model.predict(samples)

        #case5
        if case == 5:
            model = KMeans(n_clusters = 4)
            model.fit(samples)
            labels = model.predict(samples)
            centers = model.cluster_centers_

            model = KMeans(n_clusters = 4, init = centers)
            model.fit(samples)
            labels = model.predict(samples)

        #case6
        if case == 6:
            model = KMeans(n_clusters = 4)
            model.fit(samples)
            labels = model.predict(samples)
            centers = model.cluster_centers_

            model = KMeans(n_clusters = 4, init = centers)
            model.fit(samples)
            labels = model.predict(samples)

        return labels

    def GetSyllable(self,RGlyph):
        """
        초, 중, 종성을 정렬하여 반환
        [[초성], [중성], [종성]]
        """

        resultList = list()
        resultDict = dict()
        
        puc = parseUnicodeController(RGlyph.unicode)
        chars = puc.getChars()
        
        if chars[2] is None:
            if chars[1] in self.middle_one:
                resultList = self.case1(RGlyph)
            elif chars[1] in self.middle_two:
                resultList = self.case3(RGlyph)
            elif chars[1] in self.middle_three:
                resultList = self.case5(RGlyph)
            elif chars[1] in self.middle_four:
                resultList = self.case7(RGlyph)
            elif chars[1] in self.middle_five:
                resultList = self.case9(RGlyph)
            elif chars[1] in self.middle_six:
                resultList = self.case11(RGlyph)
        else:
            if chars[1] in self.middle_one:
                resultList = self.case2(RGlyph)
            elif chars[1] in self.middle_two:
                resultList = self.case4(RGlyph)
            elif chars[1] in self.middle_three:
                resultList = self.case5(RGlyph)
            elif chars[1] in self.middle_four:
                resultList = self.case8(RGlyph)
            elif chars[1] in self.middle_five:
                resultList = self.case10(RGlyph)
            elif chars[1] in self.middle_six:
                resultList = self.case12(RGlyph)
                
        resultDict[str(RGlyph.unicode)] = resultList
        
        return resultDict




    def GetLabelJsonFileName(self):
        """
        라벨 정보 파일이름 반환
        """
        return self.jsonFileName


    """
    글리프 분석을 위한 case분류
    """
    def case1(self,glyph):
        """
        middle one , no final
        """
    
        point_list = list()
    
        first = list()
        middle = list()
        final = list()
        output = list()
    
        for i in range(0,len(glyph.contours)):
            temp_object = PositionState(glyph.contours[i],i)
            point_list.append(temp_object)
    
        result = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
    
        middle.append(result[-1].conNumber)
    
        for i in range(0, len(result) - 1):
            first.append(result[i].conNumber)
    
        output.append(first)
        output.append(middle)
        output.append(final)
    
        return output

    def case2(self,glyph):
        """
        middle one, exist final
        """
    
        point_list = list()
    
        first = list()
        middle = list()
        final = list()
        output = list()
    
        for i in range(0,len(glyph.contours)):
            if self.infoDict["final label1"] ==  self.infoDict[glyph.name + '/' + str(i)]:
                final.append(i)
            else:
                temp_object = PositionState(glyph.contours[i],i)
                point_list.append(temp_object)
                
        result = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
    
        middle.append(result[-1].conNumber)
    
        for i in range(0, len(result) - 1):
            first.append(result[i].conNumber)
    
        output.append(first)
        output.append(middle)
        output.append(final)
    
        return output

    def case3(self,glyph):
        """
        middle two, no final
        """
    
        point_list = list()
    
        first = list()
        middle = list()
        final = list()
        output = list()
    
        for i in range(0,len(glyph.contours)):
            temp_object = PositionState(glyph.contours[i],i)
            point_list.append(temp_object)
    
        result = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
    
        middle.append(result[-1].conNumber)
        middle.append(result[-2].conNumber)
    
        for i in range(0, len(result) - 2):
            first.append(result[i].conNumber)
    
        output.append(first)
        output.append(middle)
        output.append(final)
    
        return output

    def case4(self,glyph):
        """
        middle two, exist final
        """
    
        point_list = list()
    
        first = list()
        middle = list()
        final = list()
        output = list()
    
        for i in range(0,len(glyph.contours)):
            if self.infoDict["final label2"] ==  self.infoDict[glyph.name + '/' + str(i)]:
                final.append(i)
            else:
                temp_object = PositionState(glyph.contours[i],i)
                point_list.append(temp_object)
                
        result = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
    
        middle.append(result[-1].conNumber)
        middle.append(result[-2].conNumber)
    
        for i in range(0, len(result) - 2):
            first.append(result[i].conNumber)
    
        output.append(first)
        output.append(middle)
        output.append(final)
    
        return output


    def case5(self,glyph):
        """
        middle three, does not matter final
        """
    
        point_list = list()
    
        first = list()
        middle = list()
        final = list()
        output = list()
    
    
        for i in range(0,len(glyph.contours)):
            temp_object = PositionState(glyph.contours[i],i)
            point_list.append(temp_object)
                
        result = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
    
        #값이 가장 큰 것이 중성
        #중성 컨투어 중 miny값 이하면 종성 아니면 초성
        middle.append(result[-1].conNumber)
        cut_line = result[-1].con.bounds[1]
        del(result[-1])
    
        for i in range(0, len(result)):
            if result[i].con.bounds[1] >= cut_line:
                first.append(result[i].conNumber)
            else:
                final.append(result[i].conNumber)
    
        output.append(first)
        output.append(middle)
        output.append(final)
    
        return output

    def case7(self,glyph):
        """
        middle four, exist final
        """   
        point_list = list()
    
        first = list()
        middle = list()
        final = list()
        output = list()
    
    
        for i in range(0,len(glyph.contours)):
            temp_object = PositionState(glyph.contours[i],i)
            point_list.append(temp_object)
    
        result = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
    
        middle.append(result[-1].conNumber)
    
        for i in range(0,len(result)-1):
            first.append(result[i].conNumber)
    
        output.append(first)
        output.append(middle)
        output.append(final)
    
        return output

    def case8(self,glyph):
        """
        middle four, exist final
        """
    
        point_list = list()
    
        first = list()
        middle = list()
        final = list()
        output = list()
    
        for i in range(0,len(glyph.contours)):
            if self.infoDict["final label4"] ==  self.infoDict[glyph.name + '/' + str(i)]:
                final.append(i)
            else:
                temp_object = PositionState(glyph.contours[i],i)
                point_list.append(temp_object)
                
        result = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
    
        middle.append(result[-1].conNumber)
    
        for i in range(0, len(result) - 1):
            first.append(result[i].conNumber)
    
        output.append(first)
        output.append(middle)
        output.append(final)
    
        return output

    def case9(self,glyph):
        """
        middle five, no final
        """
    
        point_list = list()
    
        first = list()
        middle = list()
        final = list()
        output = list()
    
    
        for i in range(0,len(glyph.contours)):
            temp_object = PositionState(glyph.contours[i],i)
            point_list.append(temp_object)
    
        #중성을 찾는 과정            
        result1 = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
        middle.append(result1[-1].conNumber)
        del(result1[-1])
    
        result2 = sorted(result1, key = lambda PositionState: PositionState.con.bounds[1])
        middle.append(result2[0].conNumber)
        del(result2[0])
    
        for i in range(0, len(result2)):
            first.append(result2[i].conNumber)
    
        output.append(first)
        output.append(middle)
        output.append(final)
    
        return output

    def case10(self,glyph):
        """
        middle five, exist final
        """
    
        point_list = list()
    
        first = list()
        middle = list()
        final = list()
        output = list()
    
        for i in range(0,len(glyph.contours)):
            if self.infoDict["final label5"] ==  self.infoDict[glyph.name + '/' + str(i)]:
                final.append(i)
            else:
                temp_object = PositionState(glyph.contours[i],i)
                point_list.append(temp_object)
    
        #중성을 찾는 과정            
        result1 = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
        middle.append(result1[-1].conNumber)
        del(result1[-1])
    
        result2 = sorted(result1, key = lambda PositionState: PositionState.con.bounds[1])
        middle.append(result2[0].conNumber)
        del(result2[0])
    
        for i in range(0, len(result2)):
            first.append(result2[i].conNumber)
    
        output.append(first)
        output.append(middle)
        output.append(final)
    
        return output

    def case11(self,glyph):
        """
        middle six, no final
        """
    
        point_list = list()
    
        first = list()
        middle = list()
        final = list()
        output = list()
    
        for i in range(0,len(glyph.contours)):
            temp_object = PositionState(glyph.contours[i],i)
            point_list.append(temp_object)
    
        #중성을 찾는 과정            
        result1 = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
        middle.append(result1[-1].conNumber)
        del(result1[-1])
        middle.append(result1[-1].conNumber)
        del(result1[-1])
    
        result2 = sorted(result1, key = lambda PositionState: PositionState.con.bounds[1])
        middle.append(result2[0].conNumber)
        del(result2[0])
    
        for i in range(0, len(result2)):
            first.append(result2[i].conNumber)
    
        output.append(first)
        output.append(middle)
        output.append(final)
    
        return output

    def case12(self,glyph):
        """
        middle five, exist final
        """
        
        point_list = list()
    
        first = list()
        middle = list()
        final = list()
        output = list()
    
    
        for i in range(0,len(glyph.contours)):
            if self.infoDict["final label6"] ==  self.infoDict[glyph.name + '/' + str(i)]:
                final.append(i)
            else:
                temp_object = PositionState(glyph.contours[i],i)
                point_list.append(temp_object)
    
        #중성을 찾는 과정            
        result1 = sorted(point_list, key = lambda PositionState: PositionState.con.bounds[2])
        middle.append(result1[-1].conNumber)
        del(result1[-1])
        middle.append(result1[-1].conNumber)
        del(result1[-1])
    
        result2 = sorted(result1, key = lambda PositionState: PositionState.con.bounds[1])
        middle.append(result2[0].conNumber)
        del(result2[0])
    
        for i in range(0, len(result2)):
            first.append(result2[i].conNumber)
    
        output.append(first)
        output.append(middle)
        output.append(final)
    
        return output



