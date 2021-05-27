#这个文件用来诠释每个命令
#这个版本开始我们尝试重构core的加载逻辑
#原来所有的解释器核心文件全部写在core一个核心上
#从现在开始，为了尝试长时间支持老版本的核心
#我们把每个版本的核心独立成单个文件
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from Visual.ArtificialUI import *

import  core.core0_4_1 as core0_4_1
import time as tm
from langcontrol import *
from global_value import warnline,texterrorline,numseterrorline,formatwarnline,nameerrorline

def spawn():
    Open=False
    global warnline,texterrorline,numseterrorline,formatwarnline,nameerrorline
    while Open==False:
        try:
            print("sysinfo→"+msg("Spawn_Mode_Name_Of_File"))
            Storyname=input()
            if Storyname=="exit":
                return
            else:
                files=open("story\\"+Storyname,"r")
        except IOError:
            print("sysinfo→"+msg("Spawn_Mode_Not_Found").format(Storyname))
        else:
            Open=True

    Ver=""
    linecount=0

    for line in files.readlines():
        linecount+=1
        #先看有没有回车，没有就给它加上，但是要提出警告
        if line[-1]!="\n":
            line+="\n"
            formatwarnline+=[[linecount,Storyname,line[:-1]]]

        #查找版本号
        if line[0]=="/": 
            Ver=line[1:-1]
            print(msg("Spawn_Mode_Get_Version"),Ver)

        #获取标题控制器
        elif line[0]==":":
            if line.count(":")!=4:
                texterrorline+=[[linecount,Storyname,line[:-1]]]
                break
            try:
                Titlesetlst=line[1:-1].split(":")
                if len(Titlesetlst)!=4:raise Exception
            except Exception:
                numseterrorline+=[[linecount,Storyname,line[:-1]]]
                Ver="TitleERROR"
            else:
                print(msg("Spawn_Mode_Get_Title"),Titlesetlst[0])
                print(msg("Spawn_Mode_Get_Subtitle"),Titlesetlst[1])
            break


#重新打开文件，从头开始处理
    files=open("story\\"+Storyname,"r")

    if Ver=="SPOL0.4.1":                                                         #遵循SPOL0.4.1标准的读取
        run=1
        while run!=0:
            run=core0_4_1.SPOL(files,Storyname)
            files.close()
            try:
                files=open("story\\"+run+".spol","r")
                Storyname=run+".spol"
            except Exception:
                run=0
            else:
                None


    else:
        print(msg("Spawn_Mode_Version_Error").format(Ver))
        
      #错误警示
    if warnline!=[]:
      print(msg("Warning_Warn_Count").format(len(warnline)))
      for i in warnline:
          print(msg("Warning_Warn_Info").format(i[0],i[1],i[2]))
      print()
    if texterrorline!=[]:
      print(msg("Warning_Texterror_Count").format(len(texterrorline)))
      for i in texterrorline:
          print(msg("Warning_Texterror_Info").format(i[0],i[1],i[2]))
      print()
    if formatwarnline!=[]:
      print(msg("Warning_Formatwarn_Count").format(len(formatwarnline)))
      for i in formatwarnline:
          print(msg("Warning_Formatwarn_Info").format(i[0],i[1],i[2]))
      print()
    if numseterrorline!=[]:
      print(msg("Warning_Numseterror_Count").format(len(numseterrorline)))
      for i in numseterrorline:
          print(msg("Warning_Numseterror_Info").format(i[0],i[1],i[2]))
      print()
    if nameerrorline!=[]:
      print(msg("Warning_Nameerror_Count").format(len(nameerrorline)))
      for i in nameerrorline:
          print(msg("Warning_Nameerror_Info").format(i[0],i[1],i[2]))
      print()
    print("sysinfo→"+msg("Spawn_Mode_End"))
    input()

def singletext():
    while True:
        print("sysinfo→"+msg("Single_Mode_Input_Version"))
        linestandard=input(r"Userinput\line→")
        if linestandard=="help":
            print(msg("Single_Mode_Version_List")+"\n"+"0.4.1")

        elif linestandard=="0.4.1":
            while True:
                Usrtextipt=input(r"Userinput\line\SPOL0.4.1→")
                if Usrtextipt=="exit":
                    break
                else:
                    core0_4_1.SPOL_s(Usrtextipt+"\n")
        elif linestandard=="exit":
            break
        else:
            print("sysinfo→"+msg("Single_Mode_Version_Error").format(linestandard))
      
def langinput():
    print("sysinfo→"+msg("Lang_Input_Msg"))
    while True:
        usrinput=input("Userinput\lang→")
        if usrinput=="":
            continue
        if usrinput=="exit":
            return
        else:
            a=langset(usrinput)
            if a==1:
                break
            else :
                continue
    print("sysinfo→"+msg("Lang_Set_Success").format(usrinput))
    
def about():
    print(msg("About_Info_Version")+" Ver0.5.0_Pre1")
    print(msg("About_Info_Developers"))
    print(msg("About_Info_Environment"))
    print(msg("About_Info_Support"))
    print(msg("About_Info_Help"))
    print("\n这个版本仅限开发者本人和Ayano_Aishi对测试人员发布。禁止测试人员将本版传播给他人")

def ui():
    global X,Y
    #先判断屏幕大小是否符合
    class Monitor(QWidget):
        def __init__(self):
            super(Monitor,self).__init__()

        def run(self):
            global X,Y
            self.desktop=QDesktopWidget()
            self.current_monitor=self.desktop.screenNumber(self)
            self.Display=self.desktop.screenGeometry(self.current_monitor)
            X=self.Display.width()
            Y=self.Display.height()

    monitor=Monitor()
    monitor.run()
   
    print("Sysinfo→"+msg("Main_Display_Size").format(X,Y))
    return [X,Y]