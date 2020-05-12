from rbFontG.tools.parseUnicodeControll import *
from parseContour.positionCase import *


def getConfigureVersion1(RGlyph):    
    
    totalx = 0
    totaly = 0
    cnt = 0
    

    axis_x = []
    axis_y = []

    first_one = ['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
    first_two = ['ㄲ','ㄸ','ㅃ','ㅆ','ㅉ']

    middle_one = ['ㅏ','ㅑ','ㅓ','ㅕ','ㅣ']
    middle_two = ['ㅐ','ㅒ','ㅔ','ㅖ']
    middle_three = ['ㅗ','ㅛ','ㅜ','ㅠ','ㅡ']
    middle_four = ['ㅘ','ㅙ','ㅚ','ㅝ','ㅞ','ㅟ','ㅢ']

    final_one = ['ㄱ','ㄲ','ㄱㅅ','ㄴ','ㄴㅈ','ㄴㅎ','ㄷ','ㄹ','ㄹㄱ','ㄹㅁ','ㄹㅂ',
    'ㄹㅅ','ㄹㅌ','ㄹㅍ','ㄹㅎ','ㅁ','ㅂ','ㅂㅅ','ㅅ','ㅆ','ㅇ','ㅈ','ㅋ','ㅌ','ㅍ']
    final_two = ['ㅊ','ㅎ']
    #컨투어의 해당 음절을 뽑아내기
    
    '''g = CurrentGlyph()

    c = g.contours[2]
    c.selected = True
    
    puc = parseUnicodeController(g.unicode)
    chars = puc.getChars()

    if chars[2] == None:
        if chars[0] in first_one:
            if chars[1] in middle_one:
                print('case1')
                num = case1(g,c,chars)
            elif chars[1] in middle_two:
                print('case2')
                num = case2(g,c,chars)
            elif chars[1] in middle_four:
                print('case6')
                num = case6(g,c)
        elif chars[0] in first_two:
            if chars[1] in middle_one:
                print('case3')
                num = case3(g,c,chars)
            elif chars[1] in middle_two:
                print('case4')
                num = case4(g,c,chars)
            elif chars[1] in middle_three:
                print('case7')
                num = case7(g,c,chars)
            elif chars[1] in middle_four:
                print('case8')
                num = case8(g,c,chars)
    elif chars[2] != None:
        if chars[0] in first_one:
            if chars[1] in middle_one:
                print('case9')
                num = case9(g,c,chars)
            elif chars[1] in middle_two:
                print('case10')
                num = case10(g,c,chars)
            elif chars[1] in middle_four:
                print('case14')
                num = case14(g,c,chars)  
        elif chars[0] in first_two:
            if chars[1] in middle_one:
                print('case11')
                num = case11(g,c,chars)
            elif chars[1] in middle_two:
                print('case12')
                num = case12(g,c,chars)
            elif chars[1] in middle_four:
                print('case16')
                num = case16(g,c,chars)
    if num == -1:
        print('nothing')
    else:
        if(chars[num] == chars[1]):
            c.selected = True
    print(chars[num])'''
    
    puc = parseUnicodeController(RGlyph.unicode)
    chars = puc.getChars()
    idxs = puc.parseUnicode()

    num = -1
    syllableList = [[],[],[]]
    data = {}
    
    for c in RGlyph.contours:
        if chars[2] == None:
            if chars[0] in first_one:
                if chars[1] in middle_one:
                    print('case1')
                    num = case1(g,c,chars)
                elif chars[1] in middle_two:
                    print('case2')
                    num = case2(g,c,chars)
                elif chars[1] in middle_four:
                    print('case6')
                    num = case6(g,c,chars)
            elif chars[0] in first_two:
                if chars[1] in middle_one:
                    print('case3')
                    num = case3(g,c,chars)
                elif chars[1] in middle_two:
                    print('case4')
                    num = case4(g,c,chars)
                elif chars[1] in middle_three:
                    print('case7')
                    num = case7(g,c,chars)
                elif chars[1] in middle_four:
                    print('case8')
                    num = case8(g,c,chars)

        elif chars[2] != None:
            if chars[0] in first_one:
                if chars[1] in middle_one:
                    print('case9')
                    num = case9(g,c,chars)
                elif chars[1] in middle_two:
                    print('case10')
                    num = case10(g,c,chars)
                elif chars[1] in middle_four:
                    print('case14')
                    num = case14(g,c,chars)                               
            elif chars[0] in first_two:
                if chars[1] in middle_one:
                    print('case11')
                    num = case11(g,c,chars)
                elif chars[1] in middle_two:
                    print('case12')
                    num = case12(g,c,chars)
                elif chars[1] in middle_four:
                    print('case16')
                    num = case16(g,c,chars)    
        if num == -1:
            print('nothing')
        elif num == 0 or num == 1 or num == 2:
            syllableList[num].append(c.index)
    
    data[str(RGlyph.unicode)] = syllableList
    return data
        