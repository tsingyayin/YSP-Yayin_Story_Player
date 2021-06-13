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

import traceback

#立绘独立上隐效果
class AvgCover(QThread):
    def __init__(self,Current):
        super(AvgCover,self).__init__()
        self.Currentnow=Current

    def run(self):
      global threadeffect

      try:
        self.Picturename=".\\Visual\\source\\Chara\\"+self.Currentnow+".png"
        self.Currentnow+="_1"
        self.Picture=QImage(self.Picturename)
        X=self.Picture.width()
        Y=self.Picture.height()
        self.QIMAGE_N=QImage(X,Y,QImage.Format_ARGB32)
        for y in range(0,Y):
            for x in range(0,X):
                oldcolor=QColor(self.Picture.pixelColor(x,y))
                if 0<y<Y/3:
                    r=int(oldcolor.red()*0)
                    g=int(oldcolor.green()*0)
                    b=int(oldcolor.blue()*0)
                    a=oldcolor.alpha()
                    self.QIMAGE_N.setPixel(x,y,qRgba(r,g,b,a))
                elif Y/3<=y<=2*Y/3:
                    r=int(oldcolor.red()*((y-Y/3)/(Y/3)))
                    g=int(oldcolor.green()*((y-Y/3)/(Y/3)))
                    b=int(oldcolor.blue()*((y-Y/3)/(Y/3)))
                    a=oldcolor.alpha()
                    self.QIMAGE_N.setPixel(x,y,qRgba(r,g,b,a))
                elif 2*Y/3<y<Y:
                    r=int(oldcolor.red()*1)
                    g=int(oldcolor.green()*1)
                    b=int(oldcolor.blue()*1)
                    a=oldcolor.alpha()
                    self.QIMAGE_N.setPixel(x,y,qRgba(r,g,b,a))
        self.QIMAGE_N.save(".\\Visual\\cache\\Chara\\"+self.Currentnow+".png","PNG",50)
        print(msg("Effect_Build_Success"),self.Currentnow+".png")

      except Exception:
          print(msg("Effect_Build_Error"),self.Currentnow+".png")
          None
      else:
          None
      threadeffect-=1
      self.quit()

#立绘独立褪色效果
class AvgFade(QThread):
    def __init__(self,Current):
        super(AvgFade,self).__init__()
        self.Currentnow=Current

    def run(self):
      global threadeffect

      try:
        self.Picturename=".\\Visual\\source\\Chara\\"+self.Currentnow+".png"
        self.Currentnow+="_2"
        self.Picture=QImage(self.Picturename)
        X=self.Picture.width()
        Y=self.Picture.height()
        self.QIMAGE_N=QImage(X,Y,QImage.Format_ARGB32)
        for x in range(0,X):
            for y in range(0,Y):
                oldcolor=QColor(self.Picture.pixelColor(x,y))
                r=int(oldcolor.red())
                g=int(oldcolor.green())
                b=int(oldcolor.blue())
                a=oldcolor.alpha()

                rgbMax=max(r,g,b)
                rgbMin=min(r,g,b)
                delta=(rgbMax-rgbMin)/255
                value=(rgbMax+rgbMin)/255
                L=value/2
                if L<=0.5 : 
                    if value !=0:
                        S=delta/value
                    else:
                        S=delta/0.00001
                elif L>0.5 : 
                    if 2-value!=0:
                        S=delta/(2-value)
                    else:S=delta/0.00001
                if S-1>=1 : alpha=S
                else : alpha=2
                alpha=1/alpha-1

                r=int((L*255+(r-L*255)*(1+alpha))*0.75)
                g=int((L*255+(g-L*255)*(1+alpha))*0.8)
                b=int((L*255+(b-L*255)*(1+alpha))*0.8)
                self.QIMAGE_N.setPixel(x,y,qRgba(r,g,b,a))
        self.QIMAGE_N.save(".\\Visual\\cache\\Chara\\"+self.Currentnow+".png","PNG",50)
        print(msg("Effect_Build_Success"),self.Currentnow+".png")

      except Exception:
          print(msg("Effect_Build_Error"),self.Currentnow+".png")
          None
      else:
          None
      threadeffect-=1
      self.quit()

#立绘褪色上隐效果
class AvgFadeCover(QThread):
    def __init__(self,Current):
        super(AvgFadeCover,self).__init__()
        self.Currentnow=Current

    def run(self):
      global threadeffect

      try:
        self.Picturename=".\\Visual\\source\\Chara\\"+self.Currentnow+".png"
        self.Currentnow+="_3"
        self.Picture=QImage(self.Picturename)
        X=self.Picture.width()
        Y=self.Picture.height()
        self.QIMAGE_N=QImage(X,Y,QImage.Format_ARGB32)
        for y in range(0,Y):
            for x in range(0,X):
                oldcolor=QColor(self.Picture.pixelColor(x,y))
                if 0<y<Y/3:
                    r=int(oldcolor.red()*0)
                    g=int(oldcolor.green()*0)
                    b=int(oldcolor.blue()*0)
                    a=oldcolor.alpha()
                    self.QIMAGE_N.setPixel(x,y,qRgba(r,g,b,a))
                elif Y/3<=y<=2*Y/3:
                    r=int(oldcolor.red()*((y-Y/3)/(Y/3)))
                    g=int(oldcolor.green()*((y-Y/3)/(Y/3)))
                    b=int(oldcolor.blue()*((y-Y/3)/(Y/3)))
                    a=oldcolor.alpha()

                    rgbMax=max(r,g,b)
                    rgbMin=min(r,g,b)
                    delta=(rgbMax-rgbMin)/255
                    value=(rgbMax+rgbMin)/255
                    L=value/2
                    if L<=0.5 : 
                        if value !=0:
                            S=delta/value
                        else:
                            S=delta/0.00001
                    elif L>0.5 : 
                        if 2-value!=0:
                            S=delta/(2-value)
                        else:S=delta/0.00001
                    if S-1>=1 : alpha=S
                    else : alpha=2
                    alpha=1/alpha-1

                    r=int((L*255+(r-L*255)*(1+alpha))*0.75)
                    g=int((L*255+(g-L*255)*(1+alpha))*0.8)
                    b=int((L*255+(b-L*255)*(1+alpha))*0.8)
                    
                    self.QIMAGE_N.setPixel(x,y,qRgba(r,g,b,a))
                elif 2*Y/3<y<Y:
                    r=int(oldcolor.red()*1)
                    g=int(oldcolor.green()*1)
                    b=int(oldcolor.blue()*1)
                    a=oldcolor.alpha()

                    rgbMax=max(r,g,b)
                    rgbMin=min(r,g,b)
                    delta=(rgbMax-rgbMin)/255
                    value=(rgbMax+rgbMin)/255
                    L=value/2
                    if L<=0.5 : 
                        if value !=0:
                            S=delta/value
                        else:
                            S=delta/0.00001
                    elif L>0.5 : 
                        if 2-value!=0:
                            S=delta/(2-value)
                        else:S=delta/0.00001
                    if S-1>=1 : alpha=S
                    else : alpha=2
                    alpha=1/alpha-1

                    r=int((L*255+(r-L*255)*(1+alpha))*0.75)
                    g=int((L*255+(g-L*255)*(1+alpha))*0.8)
                    b=int((L*255+(b-L*255)*(1+alpha))*0.8)

                    self.QIMAGE_N.setPixel(x,y,qRgba(r,g,b,a))
        self.QIMAGE_N.save(".\\Visual\\cache\\Chara\\"+self.Currentnow+".png","PNG",50)
        print(msg("Effect_Build_Success"),self.Currentnow+".png")

      except Exception:
          print(msg("Effect_Build_Error"),self.Currentnow+".png")
          None
      else:
          None
      threadeffect-=1
      self.quit()

#立绘独立黑白效果
class AvgBAW(QThread):
    def __init__(self,Current):
        super(AvgBAW,self).__init__()
        self.Currentnow=Current

    def run(self):
      global threadeffect

      try:   
        self.Picturename=".\\Visual\\source\\Chara\\"+self.Currentnow+".png"
        self.Currentnow+="_4"
        self.Picture=QImage(self.Picturename)
        X=self.Picture.width()
        Y=self.Picture.height()
        self.QIMAGE_N=QImage(X,Y,QImage.Format_ARGB32)
        for x in range(0,X):
            for y in range(0,Y):
                oldcolor=QColor(self.Picture.pixelColor(x,y))
                r=int(oldcolor.red())
                g=int(oldcolor.green())
                b=int(oldcolor.blue())
                a=oldcolor.alpha()

                r=g=b=int((r+b+g)/3)

                self.QIMAGE_N.setPixel(x,y,qRgba(r,g,b,a))
        self.QIMAGE_N.save(".\\Visual\\cache\\Chara\\"+self.Currentnow+".png","PNG",50)
        print(msg("Effect_Build_Success"),self.Currentnow+".png")
        

      except Exception:
          print(msg("Effect_Build_Error"),self.Currentnow+".png")
          None
      else:
          None
      threadeffect-=1
      self.quit()

#立绘黑白上隐效果
class AvgBAWCover(QThread):
    def __init__(self,Current):
        super(AvgBAWCover,self).__init__()
        self.Currentnow=Current

    def run(self):
      global threadeffect

      try:
        self.Picturename=".\\Visual\\source\\Chara\\"+self.Currentnow+".png"
        self.Currentnow+="_5"
        self.Picture=QImage(self.Picturename)
        X=self.Picture.width()
        Y=self.Picture.height()
        self.QIMAGE_N=QImage(X,Y,QImage.Format_ARGB32)
        for y in range(0,Y):
            for x in range(0,X):
                oldcolor=QColor(self.Picture.pixelColor(x,y))
                if 0<y<Y/3:
                    r=int(oldcolor.red()*0)
                    g=int(oldcolor.green()*0)
                    b=int(oldcolor.blue()*0)
                    a=oldcolor.alpha()
                    self.QIMAGE_N.setPixel(x,y,qRgba(r,g,b,a))
                elif Y/3<=y<=2*Y/3:
                    r=int(oldcolor.red()*((y-Y/3)/(Y/3)))
                    g=int(oldcolor.green()*((y-Y/3)/(Y/3)))
                    b=int(oldcolor.blue()*((y-Y/3)/(Y/3)))
                    a=oldcolor.alpha()
                    r=g=b=int((r+g+b)/3)
                    
                    self.QIMAGE_N.setPixel(x,y,qRgba(r,g,b,a))
                elif 2*Y/3<y<Y:
                    r=int(oldcolor.red()*1)
                    g=int(oldcolor.green()*1)
                    b=int(oldcolor.blue()*1)
                    a=oldcolor.alpha()
                    r=g=b=int((r+g+b)/3)

                    self.QIMAGE_N.setPixel(x,y,qRgba(r,g,b,a))
        self.QIMAGE_N.save(".\\Visual\\cache\\Chara\\"+self.Currentnow+".png","PNG",50)
        print(msg("Effect_Build_Success"),self.Currentnow+".png")

      except Exception:
          print(msg("Effect_Build_Error"),self.Currentnow+".png")
          None
      else:
          None
      threadeffect-=1
      self.quit()

#双适用变暗效果
class BothDark(QThread):
    def __init__(self,Current,From):
        super(BothDark,self).__init__()
        self.Currentnow=Current
        self.Fromwhich=From

    def run(self):
      global threadeffect

      try:
        if self.Fromwhich=="Chara":
            if self.Currentnow.count("_")==1:
                self.Picturename=".\\Visual\\source\\Chara\\"+self.Currentnow+".png"
                self.Currentnow+="_0"
            elif self.Currentnow.count("_")==2:
                self.Picturename=".\\Visual\\cache\\Chara\\"+self.Currentnow+".png"
        elif self.Fromwhich=="BGP":
            self.BGPdata=self.Currentnow.split("_")
            if self.BGPdata[1]=="1":
                self.Picturename=".\\Visual\\source\\BGP\\"+self.BGPdata[0]+".png"
            elif self.BGPdata[1]=="3":
                self.Picturename=".\\Visual\\cache\\BGP\\"+self.BGPdata[0]+"-Fade.png"
            elif self.BGPdata[1]=="5":
                self.Picturename=".\\Visual\\cache\\BGP\\"+self.BGPdata[0]+"-BAW.png"
        self.Picture=QImage(self.Picturename)
        X=self.Picture.width()
        Y=self.Picture.height()
        self.QIMAGE_N=QImage(X,Y,QImage.Format_ARGB32)
        for x in range(0,X):
            for y in range(0,Y):
                oldcolor=QColor(self.Picture.pixelColor(x,y))
                r=int(oldcolor.red()*0.6)
                g=int(oldcolor.green()*0.6)
                b=int(oldcolor.blue()*0.6)
                a=oldcolor.alpha()
                if r<0:r=0
                if g<0:g=0
                if b<0:b=0
                #print(a)
                self.QIMAGE_N.setPixel(x,y,qRgba(r,g,b,a))
        if self.Fromwhich=="Chara":
            self.QIMAGE_N.save(".\\Visual\\cache\\Chara\\"+self.Currentnow+"-Dark.png","PNG",50)
            print(msg("Effect_Build_Success"),self.Currentnow+"-Dark.png")
        elif self.Fromwhich=="BGP":
            if self.BGPdata[1]=="1":
                self.QIMAGE_N.save(".\\Visual\\cache\\BGP\\"+self.BGPdata[0]+"-Dark.png","PNG",50)
                print(msg("Effect_Build_Success"),self.BGPdata[0]+"-Dark.png")
            elif self.BGPdata[1]=="3":
                self.QIMAGE_N.save(".\\Visual\\cache\\BGP\\"+self.BGPdata[0]+"-Fade-Dark.png","PNG",50)
                print(msg("Effect_Build_Success"),self.BGPdata[0]+"-Fade-Dark.png")
            elif self.BGPdata[1]=="5":
                self.QIMAGE_N.save(".\\Visual\\cache\\BGP\\"+self.BGPdata[0]+"-BAW-Dark.png","PNG",50)
                print(msg("Effect_Build_Success"),self.BGPdata[0]+"--BAW-Dark.png")
        

      except Exception:
          if self.Fromwhich=="Chara":
              print(msg("Effect_Build_Error"),self.Currentnow+"-Dark.png")
          elif self.Fromwhich=="BGP":
              if self.BGPdata[1]=="1":
                  print(msg("Effect_Build_Error"),self.BGPdata[0]+"-Dark.png")
              elif self.BGPdata[1]=="3":
                  print(msg("Effect_Build_Error"),self.BGPdata[0]+"-Fade-Dark.png")
              elif self.BGPdata[1]=="5":
                  print(msg("Effect_Build_Error"),self.BGPdata[0]+"-BAW-Dark.png")
      else:
          None
      threadeffect-=1
      self.quit()

#背景褪色效果
class BGPFade(QThread):
    def __init__(self,Current):
        super(BGPFade,self).__init__()
        self.Currentnow=Current

    def run(self):
      global threadeffect
      try:
        self.Picturename=".\\Visual\\source\\BGP\\"+self.Currentnow+".png"
        self.Picture=QImage(self.Picturename)
        X=self.Picture.width()
        Y=self.Picture.height()
        self.QIMAGE_N=QImage(X,Y,QImage.Format_ARGB32)
        for x in range(0,X):
            for y in range(0,Y):
                oldcolor=QColor(self.Picture.pixelColor(x,y))
                r=int(oldcolor.red())
                g=int(oldcolor.green())
                b=int(oldcolor.blue())
                a=oldcolor.alpha()

                rgbMax=max(r,g,b)
                rgbMin=min(r,g,b)
                delta=(rgbMax-rgbMin)/255
                value=(rgbMax+rgbMin)/255
                L=value/2
                if L<=0.5 : 
                    if value !=0:
                        S=delta/value
                    else:
                        S=delta/0.00001
                elif L>0.5 : 
                    if 2-value!=0:
                        S=delta/(2-value)
                    else:S=delta/0.00001
                if S-1>=1 : alpha=S
                else : alpha=2
                alpha=1/alpha-1

                r=int((L*255+(r-L*255)*(1+alpha))*0.75)
                g=int((L*255+(g-L*255)*(1+alpha))*0.8)
                b=int((L*255+(b-L*255)*(1+alpha))*0.8)
                self.QIMAGE_N.setPixel(x,y,qRgba(r,g,b,a))
        self.QIMAGE_N.save(".\\Visual\\cache\\BGP\\"+self.Currentnow+"-Fade.png","PNG",50)
        print(msg("Effect_Build_Success"),self.Currentnow+"-Fade.png")

      except Exception:
          print(msg("Effect_Build_Error"),self.Currentnow+"-Fade.png")
          None
      else:
          None
      threadeffect-=1
      self.quit()

#背景黑白效果
class BGPBAW(QThread):
    def __init__(self,Current):
        super(BGPBAW,self).__init__()
        self.Currentnow=Current

    def run(self):
      global threadeffect

      try:
        self.Picturename=".\\Visual\\source\\BGP\\"+self.Currentnow+".png"
        self.Picture=QImage(self.Picturename)
        X=self.Picture.width()
        Y=self.Picture.height()
        self.QIMAGE_N=QImage(X,Y,QImage.Format_ARGB32)
        for x in range(0,X):
            for y in range(0,Y):
                oldcolor=QColor(self.Picture.pixelColor(x,y))
                r=int(oldcolor.red())
                g=int(oldcolor.green())
                b=int(oldcolor.blue())
                a=oldcolor.alpha()

                r=g=b=int((r+b+g)/3)

                self.QIMAGE_N.setPixel(x,y,qRgba(r,g,b,a))
        self.QIMAGE_N.save(".\\Visual\\cache\\BGP\\"+self.Currentnow+"-BAW.png","PNG",50)
        print(msg("Effect_Build_Success"),self.Currentnow+"-BAW.png")
        

      except Exception:
          print(msg("Effect_Build_Error"),self.Currentnow+"-BAW.png")
          None
      else:
          None
      threadeffect-=1
      self.quit()

#接收目标文件参数
class LocalInfo(QObject):
    def __init__(self):
        super(LocalInfo,self).__init__()

    def get(self,storyname):
        global files,Storyname
        files=open(storyname,"r")
        Storyname=storyname

#逐行循环基本滤镜识别
def CNewEffect():
  global files,Storyname,threadeffect
  #线程计数
  threadeffect=0
  threadlst=[]
  
    #行计数
  linecount=0
  
  files=open(Storyname,"r",encoding="UTF-8")

  print(msg("Effect_Info_Searching"))
  for lineraw in files.readlines(): 
    linecount+=1
    
    #先看有没有回车，没有就给它加上，但是要提出警告

    if lineraw[-1]!="\n":
        lineraw+="\n"
    #不予判定的情况
    if lineraw[0]=="#" or lineraw[0]=="/" or lineraw[0]==" " or lineraw[0]==":" or lineraw[0]=="{" or lineraw[0:2]=="||":continue

    #在遍历所需文件的这个核心，对于小分支控制器直接去掉首字符“|”就行

    if lineraw[0]=="|":
        line=lineraw[1:]
    else:
        line=lineraw

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
            if not 0<=int(bgsetlst[1])<=5:raise Exception
            if not 0<=int(bgsetlst[2])<=3:raise Exception
            if 0>float(bgsetlst[3]):raise Exception
        except Exception:
            continue
        else:
            None
        if bgsetlst[1]=="2" or bgsetlst[1]=="3":
                try:
                    f=open(".\\Visual\\cache\\BGP\\"+bgsetlst[0]+"-Fade.png","r")
                except IOError:
                        print(msg("Effect_Info_Found").format(linecount,Storyname.split(r"/")[-1],bgsetlst[0]),"-Fade.png")
                        try:
                            f=open(".\\Visual\\cache\\BGP\\"+bgsetlst[0]+"-Fade.png","w+")
                            f.close()
                        except IOError:
                            print(msg("Effect_Info_Folder_Error"))
                            return
                        else:
                            threadlst+=[BGPFade(bgsetlst[0])]    
                            threadlst[-1].start()
                            threadeffect+=1
                else:
                    None

        elif bgsetlst[1]=="4" or bgsetlst[1]=="5":
                try:
                    f=open(".\\Visual\\cache\\BGP\\"+bgsetlst[0]+"-BAW.png","r")
                except IOError:
                        print(msg("Effect_Info_Found").format(linecount,Storyname.split(r"/")[-1],bgsetlst[0]),"-BAW.png")
                        try:
                            f=open(".\\Visual\\cache\\BGP\\"+bgsetlst[0]+"-BAW.png","w+")
                            f.close()
                        except IOError:
                            print(msg("Effect_Info_Folder_Error"))
                            return
                        else:
                            threadlst+=[BGPBAW(bgsetlst[0])]
                            threadlst[-1].start()
                            threadeffect+=1
                else:
                    None
     
    #音频控制器无图形处理，直接略过

    #讲述控制器
    elif line[0:3]==">>>":
        #首先判断是否符合要求，如若不符合要求则跳过这一行并录入错误传递列表
        if (":" not in line) or line.count(">>>")>2 :
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
        #分离每个人的立绘信息和语句，并把立绘信息拆分成人名、表情、翻转、特效和淡入、淡出、说话情况
        try:
            for i in inforaw:
                charapicsetcount=len(i.split(":")[0].split("/"))
                if charapicsetcount>6:raise Exception
                charapic+=[i.split(":")[0].split("/")+[""]*(7-charapicsetcount)]
                if charapic[-1][1]=="":charapic[-1][1]=""
                if charapic[-1][2]=="":charapic[-1][2]="0"
                if charapic[-1][3]=="":charapic[-1][3]="0"
                if charapic[-1][4]=="":charapic[-1][4]="0.5"
                if charapic[-1][5]=="":charapic[-1][5]="0.5"
                #把人物名称和所说的话传入字段
                if len(i.split(":"))==2:
                    charawords+=[[i.split(":")[0].split("/")[0],i.split(":")[1]]]
                elif len(i.split(":"))==3:
                    charawords+=[[i.split(":")[1],i.split(":")[2]]]
                #对于不合要求的设置抛出异常
                if (charapic[-1][2]!="0" and charapic[-1][2]!="1"):raise Exception
                if not 0<=int(charapic[-1][3])<=5:raise Exception
                if float(charapic[-1][4])<0:raise Exception
                if float(charapic[-1][5])<0:raise Exception
        except Exception:
            continue
        else:
            None
         

        #判定特效
        for i in charapic:
            
            if i[0]!="" and i[3]!="0":
                try:
                    f=open(".\\Visual\\cache\\Chara\\"+i[0]+"_"+i[1]+"_"+i[3]+".png","r")
                except IOError:
                    if i[0]!="":
                        print(msg("Effect_Info_Found").format(linecount,Storyname.split(r"/")[-1],i[0]+"_"+i[1]+"_"+i[3]),".png")
                        try:
                            f=open(".\\Visual\\cache\\Chara\\"+i[0]+"_"+i[1]+"_"+i[3]+".png","w+")
                            f.close()
                        except IOError:
                            print(msg("Effect_Info_Folder_Error"))
                            return
                        else:
                            if i[3]=="1":
                                threadlst+=[AvgCover(i[0]+"_"+i[1])]
                                threadlst[-1].start()
                            elif i[3]=="2":
                                threadlst+=[AvgFade(i[0]+"_"+i[1])]
                                threadlst[-1].start()
                            elif i[3]=="3":
                                threadlst+=[AvgFadeCover(i[0]+"_"+i[1])]
                                threadlst[-1].start()
                            elif i[3]=="4":
                                threadlst+=[AvgBAW(i[0]+"_"+i[1])]
                                threadlst[-1].start()
                            elif i[3]=="5":
                                threadlst+=[AvgBAWCover(i[0]+"_"+i[1])]
                                threadlst[-1].start()

                            threadeffect+=1
                else:
                    None
    #把未能按类型识别的内容放入警告传递列表
    else :     
        None
  while True:
      if threadeffect == 0:
          break
      tm.sleep(0.5)
  files.close()

#逐行识别变暗
def CNewDark():
  global files,Storyname,threadeffect
  #线程统计
  threadeffect=0
  threadlst=[]
  #行计数
  linecount=0

  files=open(Storyname,"r",encoding="UTF-8")
  
  for lineraw in files.readlines(): 
    linecount+=1
    #先看有没有回车，没有就给它加上，但是要提出警告

    if lineraw[-1]!="\n":
        lineraw+="\n"
    #不予判定的情况
    if lineraw[0]=="#" or lineraw[0]=="/" or lineraw[0]==" " or lineraw[0]==":" or lineraw[0]=="{" or lineraw[0:2]=="||":continue

    #在遍历所需文件的这个核心，对于小分支控制器直接去掉首字符“|”就行

    if lineraw[0]=="|":
        line=lineraw[1:]
    else:
        line=lineraw

    #讲述控制器
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
            if not 0<=int(bgsetlst[1])<=5:raise Exception
            if not 0<=int(bgsetlst[2])<=3:raise Exception
            if 0>float(bgsetlst[3]):raise Exception
        except Exception:
            continue
        else:
            None
        if bgsetlst[1]=="1":
                try:
                    f=open(".\\Visual\\cache\\BGP\\"+bgsetlst[0]+"-Dark.png","r")
                except IOError:
                        print(msg("Effect_Info_Found").format(linecount,Storyname.split(r"/")[-1],bgsetlst[0]),"-Dark.png")
                        try:
                            f=open(".\\Visual\\cache\\BGP\\"+bgsetlst[0]+"-Dark.png","w+")
                            f.close()
                        except IOError:
                            print(msg("Effect_Info_Folder_Error"))
                            return
                        else:
                            threadlst+=[BothDark(bgsetlst[0]+"_"+bgsetlst[1],"BGP")]    
                            threadlst[-1].start()
                            threadeffect+=1
                else:
                    None
        elif bgsetlst[1]=="3":
                try:
                    f=open(".\\Visual\\cache\\BGP\\"+bgsetlst[0]+"-Fade-Dark.png","r")
                except IOError:
                        print(msg("Effect_Info_Found").format(linecount,Storyname.split(r"/")[-1],bgsetlst[0]),"-Fade-Dark.png")
                        try:
                            f=open(".\\Visual\\cache\\BGP\\"+bgsetlst[0]+"-Fade-Dark.png","w+")
                            f.close()
                        except IOError:
                            print(msg("Effect_Info_Folder_Error"))
                            return
                        else:
                            threadlst+=[BothDark(bgsetlst[0]+"_"+bgsetlst[1],"BGP")]    
                            threadlst[-1].start()
                            threadeffect+=1
                else:
                    None

        elif bgsetlst[1]=="5":
                try:
                    f=open(".\\Visual\\cache\\BGP\\"+bgsetlst[0]+"-BAW-Dark.png","r")
                except IOError:
                        print(msg("Effect_Info_Found").format(linecount,Storyname.split(r"/")[-1],bgsetlst[0]),"-BAW-Dark.png")
                        try:
                            f=open(".\\Visual\\cache\\BGP\\"+bgsetlst[0]+"-BAW-Dark.png","w+")
                            f.close()
                        except IOError:
                            print(msg("Effect_Info_Folder_Error"))
                            return
                        else:
                            threadlst+=[BothDark(bgsetlst[0]+"_"+bgsetlst[1],"BGP")]    
                            threadlst[-1].start()
                            threadeffect+=1
                else:
                    None

    elif line[0:3]==">>>":
        #首先判断是否符合要求，如若不符合要求则跳过这一行并录入错误传递列表
        if (":" not in line) or line.count(">>>")>2 :
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
        #分离每个人的立绘信息和语句，并把立绘信息拆分成人名、表情、翻转、特效和淡入、淡出、说话情况
        try:
            for i in inforaw:
                charapicsetcount=len(i.split(":")[0].split("/"))
                if charapicsetcount>6:raise Exception
                charapic+=[i.split(":")[0].split("/")+[""]*(7-charapicsetcount)]
                if charapic[-1][1]=="":charapic[-1][1]=""
                if charapic[-1][2]=="":charapic[-1][2]="0"
                if charapic[-1][3]=="":charapic[-1][3]="0"
                if charapic[-1][4]=="":charapic[-1][4]="0.5"
                if charapic[-1][5]=="":charapic[-1][5]="0.5"
                #把人物名称和所说的话传入字段
                if len(i.split(":"))==2:
                    charawords+=[[i.split(":")[0].split("/")[0],i.split(":")[1]]]
                elif len(i.split(":"))==3:
                    charawords+=[[i.split(":")[1],i.split(":")[2]]]
                #对于不合要求的设置抛出异常
                if (charapic[-1][2]!="0" and charapic[-1][2]!="1"):raise Exception
                if not 0<=int(charapic[-1][3])<=5:raise Exception
                if float(charapic[-1][4])<0:raise Exception
                if float(charapic[-1][5])<0:raise Exception
        except Exception:
            continue
        else:
            None
         
        #判定立绘明暗状态
        #如果场上只有一人，无论说话与否均为明亮
        #如果场上有两人，只有在同时沉默的时候均为明亮，否则沉默者暗
        if charanum==2:
            if charawords[0][1]!="" and charawords[1][1]=="":
                try:
                    f=open(".\\Visual\\cache\\Chara\\"+charapic[1][0]+"_"+charapic[1][1]+"_"+charapic[1][3]+"-Dark.png","r")
                except IOError:
                    if charapic[1][0]!="":
                        print(msg("Effect_Info_Found").format(linecount,Storyname.split(r"/")[-1],charapic[1][0]+"_"+charapic[1][1]+"_"+charapic[1][3]),"-Dark.png")
                        try:
                            f=open(".\\Visual\\cache\\Chara\\"+charapic[1][0]+"_"+charapic[1][1]+"_"+charapic[1][3]+"-Dark.png","w+")
                            f.close()
                        except IOError:
                            print(msg("Effect_Info_Folder_Error"))
                            return
                        else:
                            if charapic[1][3]=="0":
                                threadlst+=[BothDark(charapic[1][0]+"_"+charapic[1][1],"Chara")]
                            else :
                                threadlst+=[BothDark(charapic[1][0]+"_"+charapic[1][1]+"_"+charapic[1][3],"Chara")]
                            threadlst[-1].start()
                            threadeffect+=1
                else:
                    None

            elif charawords[0][1]=="" and charawords[1][1]!="":
                try:
                    f=open(".\\Visual\\cache\\Chara\\"+charapic[0][0]+"_"+charapic[0][1]+"_"+charapic[0][3]+"-Dark.png","r")
                except IOError:
                    if charapic[1][0]!="":
                        print(msg("Effect_Info_Found").format(linecount,Storyname.split(r"/")[-1],charapic[0][0]+"_"+charapic[0][1]+"_"+charapic[0][3]),"-Dark.png")
                        try:
                            f=open(".\\Visual\\cache\\Chara\\"+charapic[0][0]+"_"+charapic[0][1]+"_"+charapic[0][3]+"-Dark.png","w+")
                            f.close()
                        except IOError:
                            print(msg("Effect_Info_Folder_Error"))
                            return
                        else:
                            if charapic[0][3]=="0":
                                threadlst+=[BothDark(charapic[0][0]+"_"+charapic[0][1],"Chara")]
                            else :
                                threadlst+=[BothDark(charapic[0][0]+"_"+charapic[0][1]+"_"+charapic[0][3],"Chara")]
                            threadlst[-1].start()
                            threadeffect+=1
                else:
                    None
    

    #把未能按类型识别的内容放入警告传递列表
    else :     
        None
  while True:
      if threadeffect == 0:
          break
      tm.sleep(0.5)
  files.close()