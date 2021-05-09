#这个文件用来诠释每个命令
#这个版本开始我们尝试重构core的加载逻辑
#原来所有的解释器核心文件全部写在core一个核心上
#从现在开始，为了尝试长时间支持老版本的核心
#我们把每个版本的核心独立成单个文件
import  core.core0_3_5 as core0_3_5
import  core.core0_4_0 as core0_4_0
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
    #用来确标题是否读取完毕
    TitleSure=0
    SubtitleSure=0
    timestart=0

    for line in files.readlines():
        if (line[0]=="#" and line[0:3]!="###") or line[0]=="\n" or line[0]==" ":continue
        #用来确认遵循版本号
        elif line[0]=="/": 
            Ver=line[1:-1]
            print(msg("Spawn_Mode_Get_Version"),Ver)
        #标题和副标题，获取完毕后就用Sure锁死这两个elif
        elif line[0]==":"and TitleSure==0:
            Title=line[1:-1]
            print(msg("Spawn_Mode_Get_Title"),Title)
            TitleSure=1
        elif line[0]==":"and SubtitleSure==0:
            Subtitle=line[1:-1]
            print(msg("Spawn_Mode_Get_Subtitle"),Subtitle)
            TitleSure=1
            print("\n")
            break


#重新打开文件，从头开始处理
    files=open("story\\"+Storyname,"r")

    if Ver=="SPOL0.3.5":                                                         #遵循SPOL0.3.5标准的读取
        run=1
        while run!=0:
            run=core0_3_5.SPOL(files,Storyname)
            files.close()
            try:
                files=open("story\\"+run+".spol","r")
                Storyname=run+".spol"
            except Exception:
                run=0
            else:
                None

    if Ver=="SPOL0.4.0":                                                         #遵循SPOL0.4.0标准的读取
        run=1
        while run!=0:
            run=core0_4_0.SPOL(files,Storyname)
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
            print(msg("Single_Mode_Version_List")+"\n"+"0.3")
        elif linestandard=="0.3":
            while True:
                Usrtextipt=input(r"Userinput\line\SPOL0.3→")
                if Usrtextipt=="exit":
                    break
                else:
                    core0_3.SPOL_s(Usrtextipt+"\n")
        elif linestandard=="0.3.5":
            while True:
                Usrtextipt=input(r"Userinput\line\SPOL0.3.5→")
                if Usrtextipt=="exit":
                    break
                else:
                    core0_3_5.SPOL_s(Usrtextipt+"\n")
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
    print(msg("About_Info_Version")+" Interpreter_Ver0.4.0_Pre5;SPOL_0.3.5;UI0_0.1.0")
    print(msg("About_Info_Developers"))
    print(msg("About_Info_Environment"))
    print(msg("About_Info_Support"))
    print(msg("About_Info_Help"))