if __name__ == '__main__':
    originPath = "/Users/font/Desktop/WorkSpace_HS/YoonMyungjoPro740.ufo"
    origin = OpenFont(originPath,showInterface = False)
    
    testPath = "/Users/font/Desktop/groupTest 2.ufo"
    testFont = OpenFont(testPath,showInterface = False)
    
    f = open("/Users/font/Desktop/commonHangul.txt","r",encoding = 'UTF-8')
    
    comList = []
    comListOp = []
    
    while True:
        line = f.readline()
        if not line:
            break;
        comList.append(line[0])
        
    f.close()
    
    for i in range(0,len(comList)):
        comListOp.append(hex(ord(comList[i])).upper()[2:])
    
    check = 0
        
    for i in range(0,len(comListOp)):
        check = check +1
        for g in origin:
            temp = hex(g.unicode).upper()[2:]
            if(temp == comListOp[i]):
                new = g.copy()
                testFont.insertGlyph(new)            
        print(check)
            