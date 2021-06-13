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

import core.core0_6_0_U as core0_6_0_U
import core.core0_6_0_P as core0_6_0_P
import core.core0_6_0 as core0_6_0

import time as tm
from langcontrol import *
from global_value import warnline,texterrorline,numseterrorline,formatwarnline,nameerrorline

#帮助
def aasphelp():
    print("about"+"\t"+msg("Help_In_Main_Page_about_"))
    print("clear"+"\t"+msg("Help_In_Main_Page_clear"))
    print("clrall"+"\t"+msg("Help_In_Main_Page_clearall"))
    print("exit"+"\t"+msg("Help_In_Main_Page_exit"))
    print("help"+"\t"+msg("Help_In_Main_Page_help"))
    print("line"+"\t"+msg("Help_In_Main_Page_line"))
    print("lang"+"\t"+msg("Help_In_Main_Page_lang"))
    print("spawn"+"\t"+msg("Help_In_Main_Page_spawn"))
    print("tospol"+"\t"+msg("Help_In_Main_Page_tospol"))
    print("ui"+"\t"+msg("Help_In_Main_Page_ui"))

#全文解释模式启动器
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
                files=open("story\\"+Storyname,"r",encoding="UTF-8")
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
    files=open("story\\"+Storyname,"r",encoding="UTF-8")

    if Ver=="SPOL0.6.0":                                                         #遵循SPOL0.6.0标准的读取
        run=1
        while run!=0:
            run=core0_6_0.SPOL(files,Storyname)
            files.close()
            try:
                files=open("story\\"+run+".spol","r",encoding="UTF-8")
                Storyname=run+".spol"
            except Exception:
                run=0
            else:
                None

    

    else:
        print(msg("Spawn_Mode_Version_Error").format(Ver))
        
      #错误警示
    print("#####################")
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
    print("#####################")

#单行解释模式启动器
def singletext():
    while True:
        print("sysinfo→"+msg("Single_Mode_Input_Version"))
        linestandard=input(r"Userinput\line→")
        if linestandard=="help":
            print(msg("Single_Mode_Version_List")+"\n"+"0.6.0")

        elif linestandard=="0.6.0":
            while True:
                Usrtextipt=input(r"Userinput\line\SPOL0.6.0→")
                if Usrtextipt=="exit":
                    break
                else:
                    core0_6_0.SPOL_s(Usrtextipt+"\n")


        elif linestandard=="exit":
            break
        else:
            print("sysinfo→"+msg("Single_Mode_Version_Error").format(linestandard))

#语言修改   
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

#显示程序信息    
def about():
    print(msg("About_Info_Version")+" Ver0.6.0.0_Pre2")
    print(msg("About_Info_Developers"))
    print(msg("About_Info_Environment"))
    print(msg("About_Info_Support"))
    print(msg("About_Info_Help"))
    print("\n这个版本仅限测试组内使用，不得传播给他人。")

#UI启动前屏幕像素判断函数
def ui():
    global X,Y
    #先判断屏幕大小是否符合
    class Monitor(QWidget):
        def __init__(self):
            super(Monitor,self).__init__()

        def run(self):
            global X,Y,monitornum
            self.desktop=QDesktopWidget()
            self.current_monitor=self.desktop.screenNumber(self)
            self.Display=self.desktop.screenGeometry(self.current_monitor)
            X=self.Display.width()
            Y=self.Display.height()
            monitornum=self.current_monitor

    monitor=Monitor()
    monitor.run()
    del monitor
    print("Sysinfo→"+msg("Main_Display_Size").format(X,Y))
    return [X,Y]

#空文件清理函数
def DeleteEmptyMap(num):
    print("Sysinfo→"+msg("File_Searching_Wrong"))
    filelst=[]
    for a,b,filename in os.walk(".\\Visual\\cache\\Chara\\"):
        for i in filename:
            filelst+=[".\\Visual\\cache\\Chara\\"+i]
    for a,b,filename in os.walk(".\\Visual\\cache\\BGP\\"):
        for i in filename:
            filelst+=[".\\Visual\\cache\\BGP\\"+i]
    for i in filelst:
        if int(os.path.getsize(i))==0:
            os.remove(i)
            print(msg("File_Info_Deleted"),i.split("\\")[-1])
    print("Sysinfo→"+msg("File_Searching_Wrong_End"))

#清理全部缓存
def DeleteAllCache(num):
    print("Sysinfo→"+msg("File_Delete_Cache"))
    filelst=[]
    for a,b,filename in os.walk(".\\Visual\\cache\\Chara\\"):
        for i in filename:
            filelst+=[".\\Visual\\cache\\Chara\\"+i]
    for a,b,filename in os.walk(".\\Visual\\cache\\BGP\\"):
        for i in filename:
            filelst+=[".\\Visual\\cache\\BGP\\"+i]
    for i in filelst:
        os.remove(i)
    print("Sysinfo→"+msg("File_Cache_Deleted"))

#文件系统保全函数
def ensuredirs(num):
    print("sysinfo→Checking the files in the directory")
    dirslst=[".\\CrashReport",".\\text",".\\story",".\\lang",".\\Visual\\cache\\BGP",".\\Visual\\cache\\Chara",".\\arknights\\cache"]
    for i in dirslst:
        if not os.path.exists(i):
            print("sysinfo→Directory '"+i+"' missed.Now rebuilding...")
            os.makedirs(i)
    print("sysinfo→Checked")

#Splash标语
splashlst=[]
def splashes():
    global splashlst
    splashlst=[]
    try:
        splashfile=open(".\\text\\splashes.txt","r",encoding="UTF-8")
    except IOError:
        splashlst+=["您有没有注意到您的标语文件丢失了？"]
    else:
        splashlst+=splashfile.readlines()
        splashfile.close
    if splashlst==[]:
        splashlst+=["您有没有注意到您的标语文件里面啥也没写？"]
    return splashlst
    #for i in splashlst:
        #print(i[:-1])
        