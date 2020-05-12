import pandas as pd 
import matplotlib.pylab as plt
from rbFontG.tools.parseUnicodeControll import *
from parseSyllable.utility.contourDistributionChart import *
"""
2020/03/05
create by Kim Heesup
"""       	
if __name__ == '__main__':

    
    testFont = CurrentFont()

    totalx = 0
    totaly = 0
    cnt = 0
    

    axis_x = []
    axis_y = []

    first_one = ['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
    first_two = ['ㄲ','ㄸ','ㅃ','ㅆ','ㅉ']
    first_one_prime = ['ㅎ']

    middle_one = ['ㅏ','ㅑ','ㅓ','ㅕ','ㅣ']
    middle_two = ['ㅐ','ㅒ','ㅔ','ㅖ']
    middle_three = ['ㅗ','ㅛ','ㅜ','ㅠ','ㅡ']
    middle_four = ['ㅘ','ㅙ','ㅚ','ㅝ','ㅞ','ㅟ','ㅢ']
    middle_four_prime = ['ㅚ','ㅝ','ㅟ','ㅙ']

    final_one = ['ㄱ','ㄲ','ㄱㅅ','ㄴ','ㄴㅈ','ㄴㅎ','ㄷ','ㄹ','ㄹㄱ','ㄹㅁ','ㄹㅂ',
    'ㄹㅅ','ㄹㅌ','ㄹㅍ','ㄹㅎ','ㅁ','ㅂ','ㅂㅅ','ㅅ','ㅆ','ㅇ','ㅈ','ㅋ','ㅌ','ㅍ']
    final_two = ['ㅊ','ㅎ']

    for gly in testFont:
        puc = parseUnicodeController(gly.unicode)
        chars = puc.getChars()
        if(chars[2] in final_one) and (chars[0] in first_one) and (chars[1] in middle_one):
            print(chars)
            for con in gly:
                temp = getContourPosition(gly,con,10000,10000)
                axis_x.append(temp[0])
                axis_y.append(temp[1])

    # DataFrame 만들기

    db = pd.DataFrame(
        {'axis_x': axis_x, 'axis_y': axis_y}
    )

    plt.scatter(db['axis_x'], db['axis_y'], label = "data")

    plt.legend(loc = "best")
    plt.xlabel('weight')
    plt.ylabel('height')
    plt.show()