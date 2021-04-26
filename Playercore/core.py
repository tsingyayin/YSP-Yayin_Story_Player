import time as tm

def SPOL0_2_1(files):
  #用来确认一次性要素是否读取完毕
  TitleSure=0
  SubtitleSure=0

  #跨行注释状态确认
  textend=0

  bgdisplaymode={"0":"正常","1":"黑白","2":"褪色"}
  bgeffectmode={"0":"无","1":"场景抖动","2":"一次白闪","3":"两次白闪"}

  for line in files.readlines():
    #不予判定的情况——其实这意味着一行注释也可以用/甚至是空格打头，但不推荐这么做。
    if (line[0]=="#" and line[0:3]!="###") or line[0]=="/" or line[0]=="\n" or line[0]==" ":continue

    #标题和副标题，获取完毕后就用Sure锁死这两个elif
    elif line[0]==":"and TitleSure==0:
        Title=line[1:-1]
        print("剧情标题是:",Title)
        TitleSure=1
    elif line[0]==":"and SubtitleSure==0:
        Subtitle=line[1:-1]
        print("剧情标题副标题是:",Subtitle)
        TitleSure=1
        print("\n")
        timestart=tm.time()

    #进行跨行注释的识别
    elif line[0:3]=="###" and textend==0:
        textend=1
        continue
    elif line[0:3]=="###" and textend==1:
        textend=0
        continue
    elif textend==1:
        continue

    #提取背景控制器，不标准的输入用默认值填充
    #背景控制器的几个数值是场景名称、显示模式、特效、淡入
    elif line[0]=="[":
        bgsetlstcount=len(line[1:-2].split(","))               
        bgsetlst=line[1:-2].split(",")+[""]*(4-bgsetlstcount)
        #填充空位
        if bgsetlst[0]=="":bgsetlst[0]="黑场"
        if bgsetlst[1]=="":bgsetlst[1]="0"
        if bgsetlst[2]=="":bgsetlst[2]="0"
        if bgsetlst[3]=="":bgsetlst[3]="0.5"    
        print(round(tm.time()-timestart,2),"秒")
        print("#################\n当前背景是{},显示模式为{},特效为{},淡入时间{}".format(bgsetlst[0],bgdisplaymode[bgsetlst[1]],bgeffectmode[bgsetlst[2]],bgsetlst[3]))
        print("#################\n")

    #剧情文本输出的解释器
    elif line[0:3]==">>>":
        #首先提取文本控制器，若未发现则按默认值填充
        wordset=["",""]
        if line[-2]==")":
            wordsetcount=len(line[line.rindex("(")+1:-2].split(","))
            if wordsetcount ==1:
                wordset=[line[line.rindex("(")+1:-2],"1.5"]
            else:
                wordset=[line[line.rindex("(")+1:-2].split(",")[0],line[line.rindex("(")+1:-2].split(",")[1]]
            line=line[0:line.rindex("(")+1]       #方便下面处理，将文本控制器从字符串中删去
        #填充文本控制器空位
        if wordset[0]=="":wordset[0]="0.1"
        if wordset[1]=="":wordset[1]="1.5"

        #按下划线分割说话人和对应语句
        #下一句split从1开始是因为前面有一个空字符需要舍去
        inforaw=line[0:-1].split(">>>")[1:]      
        charanum=len(inforaw)   #获取人物个数
        charawords=[]       #用于存储人物姓名和对应语句
        charapic=[]           #用于存储立绘和说话状态——即立绘是否需要淡色
        BGblackcount=0   #用于控制是否需要渐变黑遮罩
        BGblack=1
        #分离每个人的立绘信息和语句，并把立绘信息拆分成人名、表情、翻转和淡入、淡出、说话情况
        charapic=[]
        for i in inforaw:
            charapicsetcount=len(i.split(":")[0].split("/"))
            charapic+=[i.split(":")[0].split("/")+[""]*(6-charapicsetcount)]
            if charapic[-1][1]=="":charapic[-1][1]=""
            if charapic[-1][2]=="":charapic[-1][2]="0"
            if charapic[-1][3]=="":charapic[-1][3]="0.5"
            if charapic[-1][4]=="":charapic[-1][4]="0.5"

            #把人物名称和所说的话传入字段
            if len(i.split(":"))==2:
                charawords+=[[i.split(":")[0].split("/")[0],i.split(":")[1]]]
            elif len(i.split(":"))==3:
                charawords+=[[i.split(":")[1],i.split(":")[2]]]
            

        #全空计数和全空个数计数,用于确定是否需要渐变黑遮罩
        for i in charapic:  
            if i[0]=="":BGblackcount+=1
        print(round(tm.time()-timestart,2),"秒")
        if BGblackcount==2 and charanum==2:
            BGblack=0
            print("无遮罩",end="")
        else:
            BGblack=1
            print("有遮罩",end="")

        #判定立绘明暗状态
        #如果场上只有一人，无论说话与否均为明亮
        #如果场上有两人，只有在同时沉默的时候均为明亮，否则沉默者暗
        if charanum==1:
            if charawords[0][1]=="":
                charapic[0][5]="(亮，沉默)"
            elif charawords[0][1]!="":
                charapic[0][5]="(亮，讲述)"
        elif charanum==2:
            if charawords[0][1]==charawords[1][1]=="":
                charapic[0][5]=charapic[1][5]="(亮，沉默)"
            elif charawords[0][1]!="" and charawords[1][1]=="":
                charapic[0][5]="(亮，讲述)"
                charapic[1][5]="(暗，沉默)"
            elif charawords[0][1]=="" and charawords[1][1]!="":
                charapic[0][5]="(暗，沉默)"
                charapic[1][5]="(亮，讲述)"

        #输出立绘
        for i in charapic:
            if i[0]!="" and  charanum != 1:       #人物个数不是一个且不是空立绘的时候
                if i[2]=="0":
                    print("\t\t{}立绘{}(淡入{}秒淡出{}秒)".format(i[0]+"_"+i[1],i[5],i[3],i[4]),end="")
                elif i[2]=="1":
                    print("\t\t{}翻转立绘{}(淡入{}秒淡出{}秒)".format(i[0]+"_"+i[1],i[5],i[3],i[4]),end="")
            elif i[0]!="" and charanum ==1:     #人物个数只有一个且不是空立绘的时候
                if i[2]=="0":
                    print("\t\t\t\t\t{}立绘{}(淡入{}秒淡出{}秒)".format(i[0]+"_"+i[1],i[5],i[3],i[4]),end="")
                elif i[2]=="1":
                    print("\t\t\t\t\t{}翻转立绘{}(淡入{}秒淡出{}秒)".format(i[0]+"_"+i[1],i[5],i[3],i[4]),end="")
            else:                                               #使用空立绘当做对齐手段或是旁白的时候
                print("\t\t\t\t\t\t\t",end="")

        print("\n")

        #按文本控制器指示输出文本，区分为旁白型和对话型
        for i in charawords:
            if i[0]=="" and charanum==1:
                print("{: ^10}\t".format(""),end="")#没有说话人，旁白型
                for words in i[1]:
                    print(words,end="")
                    tm.sleep(eval(wordset[0]))
            elif i[0]!="" and i[1]!="":
                print("{: ^10}\t".format(i[0]),end="")#有说话人在说话，对话型
                for words in i[1]:
                    print(words,end="")
                    tm.sleep(eval(wordset[0]))
            #有说话人但是沉默则直接略过
        print("\n")
        tm.sleep(eval(wordset[1]))
        print("\n")
    else : print(line)



def SPOL0_2(files):
  #用来确认一次性要素是否读取完毕
  TitleSure=0
  SubtitleSure=0

  bgdisplaymode={"0":"正常","1":"黑白","2":"褪色"}
  bgeffectmode={"0":"无","1":"场景抖动","2":"一次白闪","3":"两次白闪"}

  for line in files.readlines():
    #不予判定的情况——其实这意味着一行注释也可以用/甚至是空格打头，但不推荐这么做。
    if line[0]=="#" or line[0]=="/" or line[0]=="\n" or line[0]==" ":continue

    #标题和副标题，获取完毕后就用Sure锁死这两个elif
    elif line[0]==":"and TitleSure==0:
        Title=line[1:-1]
        print("剧情标题是:",Title)
        TitleSure=1
    elif line[0]==":"and SubtitleSure==0:
        Subtitle=line[1:-1]
        print("剧情标题副标题是:",Subtitle)
        TitleSure=1
        print("\n")

    #提取背景控制器，不标准的输入用默认值填充
    #背景控制器的几个数值是场景名称、显示模式、特效、淡入
    elif line[0]=="[":
        bgsetlstcount=len(line[1:-2].split(","))               
        bgsetlst=line[1:-2].split(",")+[""]*(4-bgsetlstcount)
        #填充空位
        if bgsetlst[0]=="":bgsetlst[0]="黑场"
        if bgsetlst[1]=="":bgsetlst[1]="0"
        if bgsetlst[2]=="":bgsetlst[2]="0"
        if bgsetlst[3]=="":bgsetlst[3]="0.5"    
        print("#################\n当前背景是{},显示模式为{},特效为{},淡入时间{}".format(bgsetlst[0],bgdisplaymode[bgsetlst[1]],bgeffectmode[bgsetlst[2]],bgsetlst[3]))
        print("#################\n")

    #剧情文本输出的解释器
    elif line[0:3]==">>>":
        #首先提取文本控制器，若未发现则按默认值填充
        wordset=["",""]
        if line[-2]==")":
            wordsetcount=len(line[line.rindex("(")+1:-2].split(","))
            if wordsetcount ==1:
                wordset=[line[line.rindex("(")+1:-2],"1.5"]
            else:
                wordset=[line[line.rindex("(")+1:-2].split(",")[0],line[line.rindex("(")+1:-2].split(",")[1]]
            line=line[0:line.rindex("(")+1]       #方便下面处理，将文本控制器从字符串中删去
        #填充文本控制器空位
        if wordset[0]=="":wordset[0]="0.1"
        if wordset[1]=="":wordset[1]="1.5"

        #按下划线分割说话人和对应语句
        #下一句split从1开始是因为前面有一个空字符需要舍去
        inforaw=line[0:-1].split(">>>")[1:]      
        charanum=len(inforaw)   #获取人物个数
        charawords=[]       #用于存储人物姓名和对应语句
        charapic=[]           #用于存储立绘和说话状态——即立绘是否需要淡色
        BGblackcount=0   #用于控制是否需要渐变黑遮罩
        BGblack=1
        #分离每个人的立绘信息和语句，并把立绘信息拆分成人名、表情、翻转和淡入、淡出、说话情况
        charapic=[]
        for i in inforaw:
            charapicsetcount=len(i.split(":")[0].split("/"))
            charapic+=[i.split(":")[0].split("/")+[""]*(6-charapicsetcount)]
            if charapic[-1][1]=="":charapic[-1][1]=""
            if charapic[-1][2]=="":charapic[-1][2]="0"
            if charapic[-1][3]=="":charapic[-1][3]="0.5"
            if charapic[-1][4]=="":charapic[-1][4]="0.5"

            #把人物名称和所说的话传入字段
            if len(i.split(":"))==2:
                charawords+=[[i.split(":")[0].split("/")[0],i.split(":")[1]]]
            elif len(i.split(":"))==3:
                charawords+=[[i.split(":")[1],i.split(":")[2]]]
            

        #全空计数和全空个数计数,用于确定是否需要渐变黑遮罩
        for i in charapic:  
            if i[0]=="":BGblackcount+=1
        if BGblackcount==2 and charanum==2:
            BGblack=0
            print("无遮罩",end="")
        else:
            BGblack=1
            print("有遮罩",end="")

        #判定立绘明暗状态
        #如果场上只有一人，无论说话与否均为明亮
        #如果场上有两人，只有在同时沉默的时候均为明亮，否则沉默者暗
        if charanum==1:
            if charawords[0][1]=="":
                charapic[0][5]="(亮，沉默)"
            elif charawords[0][1]!="":
                charapic[0][5]="(亮，讲述)"
        elif charanum==2:
            if charawords[0][1]==charawords[1][1]=="":
                charapic[0][5]=charapic[1][5]="(亮，沉默)"
            elif charawords[0][1]!="" and charawords[1][1]=="":
                charapic[0][5]="(亮，讲述)"
                charapic[1][5]="(暗，沉默)"
            elif charawords[0][1]=="" and charawords[1][1]!="":
                charapic[0][5]="(暗，沉默)"
                charapic[1][5]="(亮，讲述)"

        #输出立绘
        for i in charapic:
            if i[0]!="" and  charanum != 1:       #人物个数不是一个且不是空立绘的时候
                if i[2]=="0":
                    print("\t\t{}立绘{}(淡入{}秒淡出{}秒)".format(i[0]+"_"+i[1],i[5],i[3],i[4]),end="")
                elif i[2]=="1":
                    print("\t\t{}翻转立绘{}(淡入{}秒淡出{}秒)".format(i[0]+"_"+i[1],i[5],i[3],i[4]),end="")
            elif i[0]!="" and charanum ==1:     #人物个数只有一个且不是空立绘的时候
                if i[2]=="0":
                    print("\t\t\t\t\t{}立绘{}(淡入{}秒淡出{}秒)".format(i[0]+"_"+i[1],i[5],i[3],i[4]),end="")
                elif i[2]=="1":
                    print("\t\t\t\t\t{}翻转立绘{}(淡入{}秒淡出{}秒)".format(i[0]+"_"+i[1],i[5],i[3],i[4]),end="")
            else:                                               #使用空立绘当做对齐手段或是旁白的时候
                print("\t\t\t\t\t\t\t",end="")

        print("\n")

        #按文本控制器指示输出文本，区分为旁白型和对话型
        for i in charawords:
            if i[0]=="" and charanum==1:
                print("{: ^10}\t".format(""),end="")#没有说话人，旁白型
                for words in i[1]:
                    print(words,end="")
                    tm.sleep(eval(wordset[0]))
            elif i[0]!="" and i[1]!="":
                print("{: ^10}\t".format(i[0]),end="")#有说话人在说话，对话型
                for words in i[1]:
                    print(words,end="")
                    tm.sleep(eval(wordset[0]))
            #有说话人但是沉默则直接略过
        print("\n")
        tm.sleep(eval(wordset[1]))
        print("\n")
    else : print(line)



def SPOL0_1(files):
  #用来确认一次性要素是否读取完毕
  TitleSure=0
  SubtitleSure=0

  bgdisplaymode={"0":"正常","1":"黑白","2":"褪色"}
  bgeffectmode={"0":"无","1":"场景抖动","2":"一次白闪","3":"两次白闪"}

  for line in files.readlines():
    #不予判定的情况——其实这意味着一行注释也可以用/甚至是空格打头，但不推荐这么做。
    if line[0]=="#" or line[0]=="/" or line[0]=="\n" or line[0]==" ":continue

    #标题和副标题，获取完毕后就用Sure锁死这两个elif
    elif line[0]==":"and TitleSure==0:
        Title=line[1:-1]
        print("剧情标题是:",Title)
        TitleSure=1
    elif line[0]==":"and SubtitleSure==0:
        Subtitle=line[1:-1]
        print("剧情标题副标题是:",Subtitle)
        TitleSure=1
        print("\n")

    #提取背景控制器，不标准的输入用默认值填充
    #背景控制器的几个数值是场景名称、显示模式、特效、淡入、淡出
    elif line[0]=="[":
        bgsetlstcount=len(line[1:-2].split(","))               
        bgsetlst=line[1:-2].split(",")+[""]*(5-bgsetlstcount)
        #填充空位
        if bgsetlst[0]=="":bgsetlst[0]="黑场"
        if bgsetlst[1]=="":bgsetlst[1]="0"
        if bgsetlst[2]=="":bgsetlst[2]="0"
        if bgsetlst[3]=="":bgsetlst[3]="0.5"
        if bgsetlst[4]=="":bgsetlst[4]="0.5"      
        print("#################\n当前背景是{},显示模式为{},特效为{},淡入时间{}，淡出时间{}".format(bgsetlst[0],bgdisplaymode[bgsetlst[1]],bgeffectmode[bgsetlst[2]],bgsetlst[3],bgsetlst[4]))
        print("#################\n")

    #剧情文本输出的解释器
    elif line[0:3]==">>>":
        #首先提取文本控制器，若未发现则按默认值填充
        wordset=["",""]
        if line[-2]==")":
            wordsetcount=len(line[line.rindex("(")+1:-2].split(","))
            if wordsetcount ==1:
                wordset=[line[line.rindex("(")+1:-2],"1.5"]
            else:
                wordset=[line[line.rindex("(")+1:-2].split(",")[0],line[line.rindex("(")+1:-2].split(",")[1]]
            line=line[0:line.rindex("(")+1]       #方便下面处理，将文本控制器从字符串中删去
        #填充文本控制器空位
        if wordset[0]=="":wordset[0]="0.1"
        if wordset[1]=="":wordset[1]="1.5"

        #按下划线分割说话人和对应语句
        #下一句split从1开始是因为前面有一个空字符需要舍去
        inforaw=line[0:-1].split(">>>")[1:]      
        charanum=len(inforaw)   #获取人物个数
        charawords=[]       #用于存储人物姓名和对应语句
        charapic=[]           #用于存储立绘和说话状态——即立绘是否需要淡色
        BGblackcount=0   #用于控制是否需要渐变黑遮罩
        BGblack=1
        #分离每个人的立绘信息和语句，并把立绘信息拆分成人名、表情、翻转和淡入、淡出、说话情况
        charapic=[]
        for i in inforaw:
            charapicsetcount=len(i.split(":")[0].split("/"))
            charapic+=[i.split(":")[0].split("/")+[""]*(6-charapicsetcount)]
            if charapic[-1][1]=="":charapic[-1][1]=""
            if charapic[-1][2]=="":charapic[-1][2]="0"
            if charapic[-1][3]=="":charapic[-1][3]="0.5"
            if charapic[-1][4]=="":charapic[-1][4]="0.5"

            #把人物名称和所说的话传入字段
            if len(i.split(":"))==2:
                charawords+=[[i.split(":")[0].split("/")[0],i.split(":")[1]]]
            elif len(i.split(":"))==3:
                charawords+=[[i.split(":")[1],i.split(":")[2]]]
            

        #全空计数和全空个数计数,用于确定是否需要渐变黑遮罩
        for i in charapic:  
            if i[0]=="":BGblackcount+=1
        if BGblackcount==2 and charanum==2:
            BGblack=0
            print("无遮罩",end="")
        else:
            BGblack=1
            print("有遮罩",end="")

        #判定立绘明暗状态
        #如果场上只有一人，无论说话与否均为明亮
        #如果场上有两人，只有在同时沉默的时候均为明亮，否则沉默者暗
        if charanum==1:
            if charawords[0][1]=="":
                charapic[0][5]="(亮，沉默)"
            elif charawords[0][1]!="":
                charapic[0][5]="(亮，讲述)"
        elif charanum==2:
            if charawords[0][1]==charawords[1][1]=="":
                charapic[0][5]=charapic[1][5]="(亮，沉默)"
            elif charawords[0][1]!="" and charawords[1][1]=="":
                charapic[0][5]="(亮，讲述)"
                charapic[1][5]="(暗，沉默)"
            elif charawords[0][1]=="" and charawords[1][1]!="":
                charapic[0][5]="(暗，沉默)"
                charapic[1][5]="(亮，讲述)"

        #输出立绘
        for i in charapic:
            if i[0]!="" and  charanum != 1:       #人物个数不是一个且不是空立绘的时候
                if i[2]=="0":
                    print("\t\t{}立绘{}(淡入{}秒淡出{}秒)".format(i[0]+"_"+i[1],i[5],i[3],i[4]),end="")
                elif i[2]=="1":
                    print("\t\t{}翻转立绘{}(淡入{}秒淡出{}秒)".format(i[0]+"_"+i[1],i[5],i[3],i[4]),end="")
            elif i[0]!="" and charanum ==1:     #人物个数只有一个且不是空立绘的时候
                if i[2]=="0":
                    print("\t\t\t\t\t{}立绘{}(淡入{}秒淡出{}秒)".format(i[0]+"_"+i[1],i[5],i[3],i[4]),end="")
                elif i[2]=="1":
                    print("\t\t\t\t\t{}翻转立绘{}(淡入{}秒淡出{}秒)".format(i[0]+"_"+i[1],i[5],i[3],i[4]),end="")
            else:                                               #使用空立绘当做对齐手段或是旁白的时候
                print("\t\t\t\t\t\t\t",end="")

        print("\n")

        #按文本控制器指示输出文本，区分为旁白型和对话型
        for i in charawords:
            if i[0]=="" and charanum==1:
                print("{: ^10}\t".format(""),end="")#没有说话人，旁白型
                for words in i[1]:
                    print(words,end="")
                    tm.sleep(eval(wordset[0]))
            elif i[0]!="" and i[1]!="":
                print("{: ^10}\t".format(i[0]),end="")#有说话人在说话，对话型
                for words in i[1]:
                    print(words,end="")
                    tm.sleep(eval(wordset[0]))
            #有说话人但是沉默则直接略过
        print("\n")
        tm.sleep(eval(wordset[1]))
        print("\n")

    else : print(line)
