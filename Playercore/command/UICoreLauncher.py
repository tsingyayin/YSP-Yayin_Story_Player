#这个文件用来启动解释器线程
#支持解释器协议为 PLugin2

import core.core0_6_0_U as core0_6_0_U
import core.core0_6_0_P as core0_6_0_P

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
 can_update_chara=pyqtSignal(list,int,int) 
 update_chara_num=pyqtSignal(list,str,int,list)

 can_update_bg=pyqtSignal(list)
 update_num_bg=pyqtSignal(float,list)

 can_update_bgm=pyqtSignal(str,int)
 can_update_sound=pyqtSignal(str,int)

 can_hide_hello=pyqtSignal(int)
 can_reprint_hello=pyqtSignal(int)

 can_show_title=pyqtSignal(list)
 can_hide_title=pyqtSignal()
 can_prepare_play=pyqtSignal()

 need_to_choose=pyqtSignal(list)

 show_next=pyqtSignal()
 inrunning=pyqtSignal()
 willstop=pyqtSignal()

 can_update_freedom=pyqtSignal(list,list)
 update_num_freedom=pyqtSignal(str)
 can_clear_freedom=pyqtSignal(int)

 send_file_info=pyqtSignal(str)

 clr_line_list=pyqtSignal()
 save_line_list=pyqtSignal(list)
 set_scroll_info=pyqtSignal()

 now_which_line=pyqtSignal(int)

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
            files=open(Storyname,"r",encoding="UTF-8")
        except IOError:
            print("sysinfo→"+msg("Spawn_Mode_Not_Found").format(Storyname))
            return
        else:
            Open=True
    self.can_hide_hello.emit(1)
    Ver=""
    linecount=0
    Verlst=["",""]
    spolensure=0
    for line in files.readlines():
        linecount+=1
        #先看有没有回车，没有就给它加上，但是要提出警告
        if line[-1]!="\n":
            line+="\n"
            formatwarnline+=[[linecount,Storyname,line[:-1]]]

        #查找版本号
        if line[0]=="/": 
            Ver=line[1:-1]
            Verlst=[Ver.split("-")[0],Ver.split("-")[-1]]
            print(msg("Spawn_Mode_Get_Version"),Ver)
            spolensure=1
        #获取标题控制器
        elif line[0]==":" and spolensure==1:
            if line.count(":")!=4:
                texterrorline+=[[linecount,Storyname,line[:-1]]]
                break
            try:
                Titlesetlst=line[1:-1].split(":")
                if len(Titlesetlst)!=4:raise Exception
            except Exception:
                numseterrorline+=[[linecount,Storyname,line[:-1]]]
                Verlst[0]="TitleERROR"
            else:
                if Verlst[0]=="SPOL0.6.0" or Verlst[1]=="FollowNew":  
                    self.can_show_title.emit(Titlesetlst)
                    self.clr_line_list.emit()
                    tm.sleep(2)
                    self.giveinfo=core0_6_0_P.LocalInfo()
                    self.send_file_info.connect(self.giveinfo.get)
                    self.send_file_info.emit(Storyname)
                    finding1=core0_6_0_P.CNewEffect(self)
                    tm.sleep(1)
                    self.can_hide_title.emit()
                    finding2=core0_6_0_P.CNewDark(self)
                    self.set_scroll_info.emit()
                    tm.sleep(1)  
                    print(msg("Effect_Info_Searched").format(Storyname.split(r"/")[-1]))
                    self.can_prepare_play.emit()
            break
        
#重新打开文件，从头开始处理
    files=open(Storyname,"r",encoding="UTF-8")
    Storyname=Storyname.split(r"/")[-1]

    if Verlst[0]=="SPOL0.6.0" or  Verlst[1]=="FollowNew":                                                         #遵循SPOL0.6.0标准的读取
        runing=1
        count=0
        while runing!=0:
            count+=1
            if count==1:
                runing=core0_6_0_U.SPOL(self,files,Storyname)
                files.close()
            if count!=1:
                self.clr_line_list.emit()
                self.giveinfo=core0_6_0_P.LocalInfo()
                self.send_file_info.connect(self.giveinfo.get)
                self.send_file_info.emit("story\\"+runing+".spol")
                finding1=core0_6_0_P.CNewEffect(self)
                finding2=core0_6_0_P.CNewDark(self)
                self.set_scroll_info.emit()
                print(msg("Effect_Info_Searched").format(Storyname))
                runing=core0_6_0_U.SPOL(self,files,Storyname)
                files.close()
            try:
                files=open("story\\"+runing+".spol","r",encoding="UTF-8")
                Storyname=runing+".spol"
            except Exception:
                runing=0
                break
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
      del warnline[:]
      print()
    if texterrorline!=[]:
      print(msg("Warning_Texterror_Count").format(len(texterrorline)))
      for i in texterrorline:
          print(msg("Warning_Texterror_Info").format(i[0],i[1],i[2]))
      del texterrorline[:]
      print()
    if formatwarnline!=[]:
      print(msg("Warning_Formatwarn_Count").format(len(formatwarnline)))
      for i in formatwarnline:
          print(msg("Warning_Formatwarn_Info").format(i[0],i[1],i[2]))
      del formatwarnline[:]
      print()
    if numseterrorline!=[]:
      print(msg("Warning_Numseterror_Count").format(len(numseterrorline)))
      for i in numseterrorline:
          print(msg("Warning_Numseterror_Info").format(i[0],i[1],i[2]))
      del numseterrorline[:]
      print()
    if nameerrorline!=[]:
      print(msg("Warning_Nameerror_Count").format(len(nameerrorline)))
      for i in nameerrorline:
          print(msg("Warning_Nameerror_Info").format(i[0],i[1],i[2]))
      del nameerrorline[:]
      print()
    print("#####################")
    print("sysinfo→"+msg("Ui_Mode_End"))
    
    self.mutex.unlock()
    self.can_reprint_hello.emit(1)
    self.quit()