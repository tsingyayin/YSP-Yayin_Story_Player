#这个文件用来启动UI版对应核心。
import core.core0_3_5_U as core0_3_5_U
import core.core0_4_1_U_R as core0_4_1_U_R
import time as tm
from langcontrol import *
from global_value import warnline,texterrorline,numseterrorline,formatwarnline,nameerrorline
from PyQt5.QtCore import *

class STORYNAMERECIVE(QObject):
    def __init__(self):
        super(STORYNAMERECIVE,self).__init__()
    def get(self,StoryName):
        global Storyname
        Storyname=StoryName
        return

class SPAWN(QThread):
 can_update_chara=pyqtSignal(list,list,list,int,int) 
 update_chara_num=pyqtSignal(list,str,int,list)

 can_update_bg=pyqtSignal(list)
 update_num_bg=pyqtSignal(int,list)

 can_update_bgm=pyqtSignal(str,int)

 can_hide_hello=pyqtSignal(int)
 can_reprint_hello=pyqtSignal(int)

 can_show_title=pyqtSignal(list)

 need_to_choose=pyqtSignal(list)

 show_next=pyqtSignal()

 can_update_freedom=pyqtSignal(list,list)
 update_num_freedom=pyqtSignal(str)
 can_clear_freedom=pyqtSignal(int)

 def __init__(self):
     super(SPAWN,self).__init__()
     self.mutex=QMutex()
     self.mutex.lock()
     self.cond=QWaitCondition()
 def pause(self):
     self.cond.wait(self.mutex)

 def wake(self):
     self.cond.wakeAll()
 def run(self):
    global warnline,texterrorline,numseterrorline,formatwarnline,Storyname,nameerrorline
    Open=False
    while Open==False:
        try:       
            files=open(Storyname,"r")
            
        except IOError:
            print("sysinfo→"+msg("Spawn_Mode_Not_Found").format(Storyname))
            return
        else:
            Open=True
    self.can_hide_hello.emit(1)
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
                self.can_show_title.emit(Titlesetlst)
                self.pause()
            break

#重新打开文件，从头开始处理
    files=open(Storyname,"r")
    Storyname=Storyname.split(r"/")[-1]
    if Ver=="SPOL0.4.1":                                                         #遵循SPOL0.4.1标准的读取
        runing=1
        while runing!=0:
            runing=core0_4_1_U_R.SPOL(self,files,Storyname)
            files.close()
            try:
                files=open("story\\"+runing+".spol","r")
                Storyname=runing+".spol"
            except Exception:
                runing=0
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
    print("sysinfo→"+msg("Ui_Mode_End"))
    self.can_reprint_hello.emit(1)
    #self.mutex.unlock()