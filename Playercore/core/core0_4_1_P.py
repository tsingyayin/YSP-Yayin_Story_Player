#这个文件是解释器核心
#这个文件用来揪出所有需要预处理的图像
#我们心意已决不用任何GPU加速，所以我们要用CPU强算
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time as tm
import sys
from langcontrol import *
from global_value import warnline,texterrorline,numseterrorline,formatwarnline,nameerrorline
from PyQt5.QtCore import *
import numpy
import cv2

class USERCHOOSEBRANCHRECIVE(QObject):
    def __init__(self):
        super(USERCHOOSEBRANCHRECIVE,self).__init__()
    def get(self,BranchLabel):
        global branchlabel
        branchlabel=BranchLabel
        return

class FILEANDITSNAMERECIVE(QObject):
    def __init__(self):
        super(FILEANDITSNAMERECIVE,self).__init__()
        
    def get(self,filesIN,StorynameIN):
        global files,Storyname
        files=filesIN
        Storyname=StorynameIN
        return

class Current(QObject):
    def __init__(self):
        super(Current,self).__init__()

    def get(self,pic):
        global CurrentPicture
        CurrentPicture=pic
        return

class AvgDark(QThread):
    def __init__(self):
        super(AvgDark,self).__init__()

    def run(self):
        global CurrentPicture
        self.Picturename=CurrentPicture
        self.Picture=QImage(self.Picturename)
        X=self.Picture.width()
        Y=self.Picture.height()
        self.QIMAGE_N=QImage(X,Y,QImage.Format_ARGB32)
        for x in range(0,X):
            for y in range(0,Y):
                oldcolor=QColor(self.Picture.pixelColor(x,y))
                r=oldcolor.red()-50
                g=oldcolor.green()-50
                b=oldcolor.blue()-50
                a=oldcolor.alpha()
                if r<0:r=0
                if g<0:g=0
                if b<0:b=0
                #print(a)
                QIMAGE_N.setPixel(x,y,qRgba(r,g,b,a))
        self.Outputname=self.Picturename.split("/")[-1]
        self.QIMAGE_N.save(".\\Visual\\cache\\Chara\\"+self.Outputname+".png","PNG",100)
        
class FindNewEffect(QThread):
 def __init__(self):
  super(FindNewEffect,self).__init__()

 def run(self):
  global warnline,texterrorline,numseterrorline,formatwarnline,nameerrorline,branchlabel,files,Storyname
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
  for lineraw in files.readlines(): 
    linecount+=1
    #先看有没有回车，没有就给它加上，但是要提出警告
    if lineraw[-1]!="\n":
        lineraw+="\n"
        formatwarnline+=[[linecount,Storyname,lineraw[:-1]]]
    #不予判定的情况
    if lineraw[0]=="#" or lineraw[0]=="/" or lineraw[0]==" " or lineraw[0]==":" or lineraw[0]=="{" or lineraw[0:2]=="||":continue

    #在遍历所需文件的这个核心，对于小分支控制器直接去掉首字符“|”就行

    if lineraw[0:3]=="|":
        line=lineraw[1:]

    #提取背景控制器，不标准的输入用默认值填充
    #背景控制器的几个数值是场景名称、显示模式、特效、淡入
    if line[0]=="[":
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
            print(round(tm.time()-timestart,2),msg("Second"))
            self.can_update_bg.emit(bgsetlst)
            for i in range(0,21):
                tm.sleep(eval(bgsetlst[3])/20)
                self.update_num_bg.emit(i,bgsetlst)
            self.pause()
        except Exception:
            numseterrorline+=[[linecount,Storyname,line[:-1]]]
            continue
        else:
            None
        
            #音频控制器无图形处理，直接略过

    #讲述控制器
    elif line[0:3]==">>>":
        #首先判断是否符合要求，如若不符合要求则跳过这一行并录入错误传递列表
        if (":" not in line) or line.count(">>>")>2 :
            texterrorline+=[[linecount,Storyname,line[:-1]]]
            continue
        if line[-2]==")":
            line=line[0:line.rindex("(")+1]       #方便下面处理，将文本控制器（若有）从字符串中删去

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
                if (type(eval(charapic[-1][3]))!=int and type(eval(charapic[-1][3]))!=float) or eval(charapic[-1][3])<0:raise Exception
                if (type(eval(charapic[-1][4]))!=int and type(eval(charapic[-1][4]))!=float) or eval(charapic[-1][4])<0:raise Exception
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
    
    #把未能按类型识别的内容放入警告传递列表
    else :     
        None
  if Needjump==1:
      return Usrbranchinput
  else:
      return 0
