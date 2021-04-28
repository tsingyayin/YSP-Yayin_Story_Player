import time as tm

def SPOL0_3(files,timestart):
    
    #跨行注释状态确认
  textend=0
    #行计数和警告计数、被警告行存储等
  linecount=0

  warn=0
  warnline=[]

  texterror=0
  texterrorline=[]

  numseterror=0
  numseterrorline=[]

  formatwarn=0
  formatwarnline=[]

  bgdisplaymode={"0":"正常","1":"黑白","2":"褪色"}
  bgeffectmode={"0":"无","1":"场景抖动","2":"一次白闪","3":"两次白闪"}
  textmode={"L":"左对齐","M":"中对齐","R":"右对齐"}
  for line in files.readlines(): 
    linecount+=1
    #先看有没有回车，没有就给它加上，但是要提出警告
    if line[-1]!="\n":
        line+="\n"
        formatwarn+=1
        formatwarnline+=[[linecount,line[:-1]]]
    #不予判定的情况
    if (line[0]=="#" and line[0:3]!="###") or line[0]=="/" or line[0]=="\n" or line[0]==" " or line[0]==":":None

    #进行跨行注释的识别
    elif line[0:3]=="###" and textend==0:
        textend=1
    elif line[0:3]=="###" and textend==1:
        textend=0
    elif textend==1:
        continue

    #提取背景控制器，不标准的输入用默认值填充
    #背景控制器的几个数值是场景名称、显示模式、特效、淡入
    elif line[0]=="[":
        try:
            bgsetlstcount=len(line[1:-2].split(","))
            if bgsetlstcount>4:raise Exception
            bgsetlst=line[1:-2].split(",")+[""]*(4-bgsetlstcount)
            #填充空位
            if bgsetlst[0]=="":bgsetlst[0]="黑场"
            if bgsetlst[1]=="":bgsetlst[1]="0"
            if bgsetlst[2]=="":bgsetlst[2]="0"
            if bgsetlst[3]=="":bgsetlst[3]="0.5"   
            if type(eval(bgsetlst[1]))!=int or (not 0<=eval(bgsetlst[1])<=2):raise Exception
            if type(eval(bgsetlst[2]))!=int or (not 0<=eval(bgsetlst[2])<=3):raise Exception
            if (type(eval(bgsetlst[3]))!=int and type(eval(bgsetlst[3]))!=float) or 0>eval(bgsetlst[3]):raise Exception
            print(round(tm.time()-timestart,2),"秒")
            print("#################\n当前背景是{},显示模式为{},特效为{},淡入时间{}".format(bgsetlst[0],bgdisplaymode[bgsetlst[1]],bgeffectmode[bgsetlst[2]],bgsetlst[3]))
            print("#################\n")
        except Exception:
            numseterror+=1
            numseterrorline+=[[linecount,line[:-1]]]
            continue
        else:
            None

    #提取音频控制器，不标准的输入用默认值填充
    #音频控制器的参数是音频名称和音频音量
    elif line[0]=="{":
        try:
            musicsetlstcount=len(line[1:-2].split(",")) 
            if musicsetlstcount>2:raise Exception              
            musicsetlst=line[1:-2].split(",")+[""]*(2-musicsetlstcount)
            #填充空位
            if musicsetlst[0]=="":musicsetlst[0]="静音"
            if musicsetlst[1]=="":musicsetlst[1]="50"
            if (type(eval(musicsetlst[1]))!=int and type(eval(musicsetlst[1]))!=float) or not 0<=eval(musicsetlst[1])<=100:raise Exception
            print(round(tm.time()-timestart,2),"秒")
            print("#################\n当前BGM是{},音量是{}".format(musicsetlst[0],musicsetlst[1]))
            print("#################\n")
        except Exception:
            numseterror+=1
            numseterrorline+=[[linecount,line[:-1]]]
            continue
        else:
            None

    #讲述控制器
    elif line[0:3]==">>>":
        #首先判断是否符合要求，如若不符合要求则跳过这一行并录入错误传递列表
        if (":" not in line) or line.count(">>>")>2 :
            texterror+=1
            texterrorline+=[[linecount,line[:-1]]]
            continue
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
        try:
            if (type(eval(wordset[0]))!=int and type(eval(wordset[0]))!=float) or eval(wordset[0])<0:raise Exception
            if (type(eval(wordset[1]))!=int and type(eval(wordset[1]))!=float) or eval(wordset[0])<0:raise Exception
        except Exception:
            numseterror+=1
            numseterrorline+=[[linecount,line[:-1]]]
            continue
        else:
            None
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
        try:
            for i in inforaw:
                charapicsetcount=len(i.split(":")[0].split("/"))
                if charapicsetcount>5:raise Exception
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
                #对于不合要求的设置抛出异常
                if (charapic[-1][2]!="0" and charapic[-1][2]!="1"):raise Exception
                if (type(eval(charapic[-1][3]))!=int and type(eval(charapic[-1][3]))!=float) or eval(charapic[-1][3])<0:raise Exception
                if (type(eval(charapic[-1][4]))!=int and type(eval(charapic[-1][4]))!=float) or eval(charapic[-1][3])<0:raise Exception
        except Exception:
            numseterror+=1
            numseterrorline+=[[linecount,line[:-1]]]
            continue
        else:
            None
         
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

    #自由文本控制器
    elif line[0:3]==">^>":
        #首先判断是否符合要求，如若不符合要求则跳过这一行并录入错误传递列表
        if (":" not in line) or line.count(">^>")>1 :
            texterror+=1
            texterrorline+=[[linecount,line[:-1]]]
            continue
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
        try:
            if (type(eval(wordset[0]))!=int and type(eval(wordset[0]))!=float) or eval(wordset[0])<0:raise Exception
            if (type(eval(wordset[1]))!=int and type(eval(wordset[1]))!=float) or eval(wordset[0])<0:raise Exception
            #提取文本内容
            inforaw=[line[3:line.index(":")],line[line.index(":")+1:-1]]
            textsetcount=len(inforaw[0].split("/"))
            if textsetcount>3:raise Exception
            textset=inforaw[0].split("/")+[""]*(3-textsetcount)+[inforaw[1]]
            if textset[0]=="":textset[0]="960"
            if textset[1]=="":textset[1]="540"
            if textset[2]=="":textset[2]="M"
            if textset[3]=="":textset[3]=" "
            if type(eval(textset[0]))!=int or eval(textset[0])<0:raise Exception
            if type(eval(textset[1]))!=int or eval(textset[1])<0:raise Exception
            if textset[2] not in "LMR":raise Exception
        except Exception:
            numseterror+=1
            numseterrorline+=[[linecount,line[:-1]]]
            continue
        else:
            None
        print(round(tm.time()-timestart,2),"秒")
        print("（坐标是({},{})。采用{}）".format(textset[0],textset[1],textmode[textset[2]]))
        print("\t\t\t",end="")
        for i in textset[3]:
            print(i,end="")
            tm.sleep(eval(wordset[0]))
        tm.sleep(eval(wordset[1]))
        print()

    #把未能按类型识别的内容放入警告传递列表
    else :     
        warn+=1
        warnline+=[[linecount,line[:-1]]]

    #错误警示
  if warn!=0:
      print("读取过程共出现了{}个警告：".format(warn))
      for i in warnline:
          print("未能识别行{}的内容:“{}”，如果是注释请添加字符#".format(i[0],i[1]))
      print()
  if texterror!=0:
      print("读取过程共出现了{}个错误：".format(texterror))
      for i in texterrorline:
          print("行{}的内容:“{}”不符合解释器定义".format(i[0],i[1]))
      print()
  if formatwarn!=0:
      print("读取过程共出现了{}个格式警告：".format(formatwarn))
      for i in formatwarnline:
          print("行{}的内容:“{}”没有以回车（换行符）结尾".format(i[0],i[1]))
      print()
  if numseterror!=0:
      print("读取过程共发现了{}个参数设置错误：".format(numseterror))
      for i in numseterrorline:
          print("行{}的控制器“{}”遇到了参数错误：超出范围或超出参数个数上限".format(i[0],i[1]))
      print()

def SPOL_s_0_3(line):
    textmode={"L":"左对齐","M":"中对齐","R":"右对齐"}
    #剧情文本输出的解释器，只有文本输出控制器。
    if line=="\n":
        None
    #讲述控制器单行版
    elif line[0:3]==">>>":
        if (":" not in line) or line.count(">>>")>2 :
            print("sysinfo→有语法错误。")
            return
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
        try:
            if (type(eval(wordset[0]))!=int and type(eval(wordset[0]))!=float) or eval(wordset[0])<0:raise Exception
            if (type(eval(wordset[1]))!=int and type(eval(wordset[1]))!=float) or eval(wordset[0])<0:raise Exception
        except Exception:
            print("sysinfo→解释器遇到了参数错误。")
            return
        else:
            None

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
        try:
            charapicsetcount=len(i.split(":")[0].split("/"))
            if charapicsetcount>5:raise Exception
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
                #对于不合要求的设置抛出异常
            if (charapic[-1][2]!="0" and charapic[-1][2]!="1"):raise Exception
            if (type(eval(charapic[-1][3]))!=int and type(eval(charapic[-1][3]))!=float) or eval(charapic[-1][3])<0:raise Exception
            if (type(eval(charapic[-1][4]))!=int and type(eval(charapic[-1][4]))!=float) or eval(charapic[-1][3])<0:raise Exception
        except Exception:
            print("sysinfo→解释器遇到了参数错误。")
            return
        else:
            None

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

    #自由文本控制器单行版
    elif line[0:3]==">^>":
        #首先判断是否符合要求，如若不符合要求则跳过这一行并录入错误传递列表
        if (":" not in line) or line.count(">^>")>1 :
            print("sysinfo→有语法错误。")
            return
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
        try:
            if (type(eval(wordset[0]))!=int and type(eval(wordset[0]))!=float) or eval(wordset[0])<0:raise Exception
            if (type(eval(wordset[1]))!=int and type(eval(wordset[1]))!=float) or eval(wordset[0])<0:raise Exception
        except Exception:
            print("sysinfo→解释器遇到了参数错误。")
            return
        else:
            None
        try:
            inforaw=[line[3:line.index(":")],line[line.index(":")+1:-1]]
            textsetcount=len(inforaw[0].split("/"))
            if textsetcount>3:raise Exception
            textset=inforaw[0].split("/")+[""]*(3-textsetcount)+[inforaw[1]]
            if textset[0]=="":textset[0]="960"
            if textset[1]=="":textset[1]="540"
            if textset[2]=="":textset[2]="M"
            if textset[3]=="":textset[3]=" "
            if type(eval(textset[0]))!=int or eval(textset[0])<0:raise Exception
            if type(eval(textset[1]))!=int or eval(textset[1])<0:raise Exception
            if textset[2] not in "LMR":raise Exception
        except Exception:
            print("sysinfo→解释器遇到了参数错误。")
            return
        else:
            None
        print("（坐标是({},{})。采用{}）".format(textset[0],textset[1],textmode[textset[2]]))
        print("\t\t\t",end="")
        for i in textset[3]:
            print(i,end="")
            tm.sleep(eval(wordset[0]))
        tm.sleep(eval(wordset[1]))
        print()

    else : 
        print("Sysinfo→不能将文本“{}”识别为控制器".format(line[:-1]))
