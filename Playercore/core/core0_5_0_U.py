#这个文件是解释器核心
#这个是给UI用的版本
import time as tm
import sys
from langcontrol import *
from global_value import warnline,texterrorline,numseterrorline,formatwarnline,nameerrorline
from PyQt5.QtCore import *

class USERCHOOSEBRANCHRECIVE(QObject):
    def __init__(self):
        super(USERCHOOSEBRANCHRECIVE,self).__init__()
    def get(self,BranchLabel):
        global branchlabel
        branchlabel=BranchLabel
        return

def SPOL(self,files,Storyname):
  global warnline,texterrorline,numseterrorline,formatwarnline,nameerrorline,branchlabel
    #跨行注释状态确认
  textend=0
    #行计数
  linecount=0
    #对话分支状态确认
  conver=0
  convertag=0
  converjump=1
  #判断解释器是自行终止还是分支需要终止
  Needjump=0

  bgdisplaymode={"0":msg("Bgp_Display_Mode_Normal"),"1":msg("Bgp_Display_Mode_Fade"),"2":msg("Bgp_Display_Mode_B&W")}
  bgeffectmode={"0":msg("Bgp_Effect_Mode_Normal"),"1":msg("Bgp_Effect_Mode_Shake"),"2":msg("Bgp_Effect_Mode_W1"),"3":msg("Bgp_Effect_Mode_W2")}
  textmode={"L":msg("Freedom_Text_Mode_L"),"M":msg("Freedom_Text_Mode_M"),"R":msg("Freedom_Text_Mode_R")}
  timestart=tm.time()
  for lineraw in files.readlines(): 
    linecount+=1
    #先看有没有回车，没有就给它加上，但是要提出警告
    if lineraw[-1]!="\n":
        lineraw+="\n"
        formatwarnline+=[[linecount,Storyname,lineraw[:-1]]]
    #不予判定的情况
    if (lineraw[0]=="#" and lineraw[0:3]!="###") or lineraw[0]=="/" or lineraw[0]==" " or lineraw[0]==":":continue

    #先来看看这一行是不是对话分支的一部分
    #这一部分思路是这样的
    #首先|||是开头结尾没啥好说的
    #剩下的话，对比||行是否和输入一样
    #如果一样，那么就确认读到这一个分支convertag=1
    #那么|后面的就正常读写
    #遇到下一个||的时候让convertag=0，不再不写
    #简而言之convertag的1和0是读写准许与跳过
    #其他情况就正常传入，没啥好说的

    if lineraw[0:3]=="|||" and conver==0 :
        conver=1
        convertag=0
        converlst=lineraw[3:-1].split("|||")
        try:
            if len(converlst)>4:raise Exception
            convernum=[]
            for k in converlst:
                i=k.split(":")
                if len(i)!=2:raise Exception
                print("{}:{}".format(i[0],i[1]))
                convernum+=i[0]       
        except Exception:
            numseterrorline+=[[linecount,Storyname,lineraw[:-1]]]
            areajump=1
        else:
            areajump=0
            self.need_to_choose.emit(converlst)
            self.willstop.emit()
            self.pause()
            self.inrunning.emit()
            self.usript=""
            for i in converlst:
                if branchlabel==i.split(":")[1]:
                    self.usript=i.split(":")[0]
            None
        continue

    elif lineraw[0:2]=="||" and lineraw[0:3]!="|||" and convertag==0 and areajump==0:
        if lineraw[2:-1] not in convernum:
            nameerrorline+=[[linecount,Storyname,lineraw[:-1]]]
        if lineraw[2:-1]==self.usript:
            convertag=1
        continue
    elif lineraw[0:2]=="||"and lineraw[0:3]!="|||"  and convertag==1 and areajump==0:
        if lineraw[2:-1] not in convernum:
            nameerrorline+=[[linecount,Storyname,lineraw[:-1]]]
        convertag=0
        continue
    elif lineraw[0]=="|" and lineraw[0:3]!="|||" and lineraw[0:2]!="||" and convertag==1 and areajump==0:
        line=lineraw[1:]
    elif lineraw[0]=="|" and lineraw[0:3]!="|||" and lineraw[0:2]!="||" and convertag==0 and areajump==0:
        continue
    elif (lineraw[0:3]=="|||" or lineraw[0]=="\n") and conver==1:
        conver=0
        convertag=0
        continue
    elif conver==0:
        line=lineraw[:]


    #进行跨行注释的识别
    if line[0:3]=="###" and textend==0:
        textend=1
    elif line[0:3]=="###" and textend==1:
        textend=0
    elif textend==1:
        continue
    elif line[0]=="\n" :
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
            if not 0<=int(bgsetlst[1])<=2:raise Exception
            if not 0<=int(bgsetlst[2])<=3:raise Exception
            if 0>float(bgsetlst[3]):raise Exception
            print(round(tm.time()-timestart,2),msg("Second"))
            self.can_update_bg.emit(bgsetlst)
            if bgsetlst[3]!="0" :
                for i in range(0,21):
                    tm.sleep(float(bgsetlst[3])/20)
                    self.update_num_bg.emit(i,bgsetlst)
                self.willstop.emit()
                self.pause()
                self.inrunning.emit()
            else :
                self.update_num_bg.emit(0,bgsetlst)
                self.update_num_bg.emit(20,bgsetlst)
                self.willstop.emit()
                self.pause()
                self.inrunning.emit()

        except Exception:
            numseterrorline+=[[linecount,Storyname,line[:-1]]]
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
            if not 0<=int(musicsetlst[1])<=100:raise Exception
            print(round(tm.time()-timestart,2),msg("Second"))
            print("#################\n"+msg("Bgm_Setting_Info").format(musicsetlst[0],musicsetlst[1]))
            print("#################\n")
            self.can_update_bgm.emit(musicsetlst[0],int(musicsetlst[1]))
        except Exception:
            numseterrorline+=[[linecount,Storyname,line[:-1]]]
            continue
        else:
            None


    #音效控制器
    elif line[0]=="<":
        try:
            soundsetlstcount=len(line[1:-2].split(",")) 
            if soundsetlstcount>2:raise Exception              
            soundsetlst=line[1:-2].split(",")+[""]*(2-soundsetlstcount)
            #填充空位
            if soundsetlst[0]=="":soundsetlst[0]="静音"
            if soundsetlst[1]=="":soundsetlst[1]="50"
            if not 0<=int(soundsetlst[1])<=100:raise Exception
            print(round(tm.time()-timestart,2),msg("Second"))
            print("#################\n"+msg("Sound_Setting_Info").format(soundsetlst[0],soundsetlst[1]))
            print("#################\n")
            self.can_update_sound.emit(soundsetlst[0],int(soundsetlst[1]))
        except Exception:
            numseterrorline+=[[linecount,Storyname,line[:-1]]]
            continue
        else:
            None

    #讲述控制器
    elif line[0:3]==">>>":
        #首先判断是否符合要求，如若不符合要求则跳过这一行并录入错误传递列表
        if (":" not in line) or line.count(">>>")>2 :
            texterrorline+=[[linecount,Storyname,line[:-1]]]
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
            if float(wordset[0])<0:raise Exception
            if float(wordset[1])<0:raise Exception
        except Exception:
            numseterrorline+=[[linecount,Storyname,line[:-1]]]
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
                if float(charapic[-1][3])<0:raise Exception
                if float(charapic[-1][4])<0:raise Exception
        except Exception:
            numseterrorline+=[[linecount,Storyname,line[:-1]]]
            continue
        else:
            None
         
            #全空计数和全空个数计数,用于确定是否需要渐变黑遮罩
        for i in charapic:  
            if i[0]=="":BGblackcount+=1
        print(round(tm.time()-timestart,2),msg("Second"))
        if BGblackcount==2 and charanum==2:
            BGblack=0
        else:
            BGblack=1

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
        self.can_update_chara.emit(charapic,charawords,wordset,charanum,BGblack)
        wordsall=""
        for i in charawords:
            if i[0]=="" and charanum==1:
                alphacount=0
                if i[1]=="":
                    self.update_chara_num.emit(i,wordsall,charanum,wordset)
                elif i[1]!="":
                    for word in i[1]:
                        tm.sleep(float(wordset[0]))
                        if '\u4e00' <= word <= '\u9fff' or "\u3040" <= word <= "\u309f" or "\u30a0" <= word <= "\u30ff":
                            alphacount+=2
                        else:
                            alphacount+=1
                        if alphacount>=58:
                            wordsall+="\n"
                            alphacount=0
                        wordsall+=word
                        self.update_chara_num.emit(i,wordsall,charanum,wordset)
                break
            elif i[1]=="" and charanum==1:
                self.update_chara_num.emit(i,wordsall,charanum,wordset)
                break
            elif (i[0]!="" and i[1]!="") or (i[0]!="" and charanum==1) :
                alphacount=0
                for word in i[1]:
                    tm.sleep(float(wordset[0]))
                    if '\u4e00' <= word <= '\u9fff':
                        alphacount+=2
                    else:
                        alphacount+=1
                    if alphacount>=58:
                        wordsall+="\n"
                        alphacount=0
                    wordsall+=word
                    
                    self.update_chara_num.emit(i,wordsall,charanum,wordset)

                break 
        self.willstop.emit()
        tm.sleep(float(wordset[1]))
        self.show_next.emit()
        self.pause()
        self.inrunning.emit()

    #自由文本控制器
    elif line[0:3]==">^>":
        #首先判断是否符合要求，如若不符合要求则跳过这一行并录入错误传递列表
        if (":" not in line) or line.count(">^>")>1 :
            texterrorline+=[[linecount,Storyname,line[:-1]]]
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
            if float(wordset[0])<0:raise Exception
            if float(wordset[1])<0:raise Exception
            testset=[]
            #提取文本内容
            inforaw=[line[3:line.index(":")],line[line.index(":")+1:-1]]
            textsetcount=len(inforaw[0].split("/"))
            if textsetcount>3:raise Exception
            textset=inforaw[0].split("/")+[""]*(3-textsetcount)+[inforaw[1]]
            if textset[0]=="":textset[0]="0.2"
            if textset[1]=="":textset[1]="0.444"
            if textset[2]=="":textset[2]="M"
            if textset[3]=="":textset[3]=" "
            if float(textset[0])<0:raise Exception
            if float(textset[1])<0:raise Exception
            if textset[2] not in "LMR":raise Exception
            
        except Exception:
            numseterrorline+=[[linecount,Storyname,line[:-1]]]
            continue
        else:
            self.can_update_freedom.emit(textset,wordset)
            wordsall=""
            alphacount=0
            for word in textset[3]:
                tm.sleep(float(wordset[0]))
                if '\u4e00' <= word <= '\u9fff' or "\u3040" <= word <= "\u309f" or "\u30a0" <= word <= "\u30ff":
                    alphacount+=2
                else:
                    alphacount+=1
                if alphacount>=58:
                    wordsall+="\n"
                    alphacount=0
                wordsall+=word
                self.update_num_freedom.emit(wordsall)
        tm.sleep(float(wordset[1]))
        self.show_next.emit()
        self.willstop.emit()
        self.pause()
        self.inrunning.emit()
        self.can_clear_freedom.emit(1)
       
    #分支选项解释器
    elif line[0:3]=="-->":
        #判断是否符合语法定义
        if (":" not in line) or line.count("-->")>4:
            texterrorline+=[[linecount,Storyname,line[:-1]]]
            continue
        inforaw=line[:-1].split("-->")[1:]
        branchinfo=[]
        branchname=[]
        #提取行的内容
        for i in inforaw:
            try:
                if i.count(":")!=2: raise Exception
            except Exception:
                numseterror+=[[linecount,Storyname,line[:-1]]]
                continue
            else:
                branchinfo+=[[i.split(":")[0]+":"+i.split(":")[1],i.split(":")[2]]]
                branchname+=[i.split(":")[0]+":"+i.split(":")[1]]
        for i in branchinfo:
            print(msg("Branch_Info_Msg").format(i[0],i[1]))
        
        self.need_to_choose.emit(branchname)
        self.willstop.emit()
        self.pause()
        self.inrunning.emit()

        for i in branchname:
            if branchlabel in i.split(":")[1]:
                Usrbranchinput=branchinfo[branchname.index(i)][1]
                Needjump=1
        break

    #把未能按类型识别的内容放入警告传递列表
    else :     
        warnline+=[[linecount,Storyname,line[:-1]]]

  if Needjump==1:
      return Usrbranchinput
  else:
      return 0
