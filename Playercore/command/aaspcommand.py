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
from arknights.HLtoSPOL import *
import time as tm
from langcontrol import *
from global_value import warnline,texterrorline,numseterrorline,formatwarnline,nameerrorline
from command.checkupdate import *

Day=20210709
Edition="Ver0.7.0.0_Pre4(Build85.0)_SPOL0.6.0;Py_Qt"
InsiderMainVer=Edition[Edition.index("Ver")+3:Edition.index("_P")]
InsiderSubVer=Edition[Edition.index("_P")+1:Edition.index("(Build")]
InsiderBuildVer=Edition[Edition.index("(Build")+6:Edition.index(")")]
InsiderSPOLVer=Edition[Edition.index("SPOL")+4:Edition.index(";Py_Qt")]
InsiderSPOLEnvVer="Python_PyQt"

urlGithub="https://github.com/tsingyayin/YSP-Yayin_Story_Player"
urlAFD="https://afdian.net/@ysp_Dev?tab=home"

#提供TopWindow的各项功能的标准执行-返回讯息框架
class FrameWork(QObject):
    AnyInfo=pyqtSignal(int,str)
    def __init__(self):
        super(FrameWork,self).__init__()

    def send(self,group,text):
        self.AnyInfo.emit(group,text)

    def ui_aasphelp(self):
        aasphelp()

    def ui_Tospol(self,fileipt):
        func=HLtoSPOL(fileipt)
        if func==True:
            self.AnyInfo.emit(1,msg("Ui_To_Spol_End"))
        else :
            self.AnyInfo.emit(2,msg("Ui_To_Spol_End_Error"))

    def ui_langset(self,filename):
        langset(filename)
        self.AnyInfo.emit(1,msg("Lang_Set_Success").format(filename))

    def ui_DeleteEmptyMap(self):
        DeleteEmptyMap(0)
        self.AnyInfo.emit(1,msg("File_Searching_Wrong_End"))

    def ui_DeleteAllCache(self):
        DeleteAllCache(0)
        self.AnyInfo.emit(1,msg("File_Cache_Deleted"))

    def ui_CheckUpdate(self):
        INFO=Checkupdate(0)
        if INFO[0]==1:
            self.AnyInfo.emit(1,msg("Check_Update_Info_New"))
        elif INFO[0]==2:
            self.AnyInfo.emit(1,msg("Check_Update_Info_Insider"))
        return INFO[1]

#帮助
def aasphelp():
    print("about"+"\t"+msg("Help_In_Main_Page_about_"))
    print("clear"+"\t"+msg("Help_In_Main_Page_clear"))
    print("clrall"+"\t"+msg("Help_In_Main_Page_clearall"))
    print("exit"+"\t"+msg("Help_In_Main_Page_exit"))
    print("help"+"\t"+msg("Help_In_Main_Page_help"))
    print("lang"+"\t"+msg("Help_In_Main_Page_lang"))
    print("tospol"+"\t"+msg("Help_In_Main_Page_tospol"))
    print("ui"+"\t"+msg("Help_In_Main_Page_ui"))
    print("window"+"\t"+msg("Help_In_Main_Page_window"))

#语言修改   
def langinput(num=1):
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
    print(msg("About_Info_Main_Ver")+InsiderMainVer)
    print(msg("About_Info_Sub_Ver")+InsiderSubVer)
    print(msg("About_Info_Build_Ver")+InsiderBuildVer)
    print(msg("About_Info_Spol_Ver")+InsiderSPOLVer)
    print(msg("About_Info_Spol_Env_Ver")+InsiderSPOLEnvVer)
    print(msg("About_Info_Developers")+"青雅音 Tsing Yayin")
    print(msg("About_Info_Environment")+"Visual Studio 2019")
    print(msg("About_Info_Support")+"亿绪联合协会 UYXA")
    print(msg("About_Info_Help").format(urlGithub))
    print(msg("About_Info_Donate").format(urlAFD))

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

#启动播放页
def LaunchUI():
            try:
                del app
            except:
                None
            else:
                None
            app=QApplication(sys.argv)
            monitor_range=ui()
            if monitor_range[0]<1366 or monitor_range[1]<768:
                print("sysinfo→"+msg("Screen_Too_Small").format(monitor_range[0],monitor_range[1]))
                #break
            else:
                SPLASHES(splashes())
                Mainwindow=MainWindow()
                Mainwindow.showFullScreen()
                try:
                    sys.exit(app.exec_())
                except SystemExit:
                    None
                else:
                    None   
                DirectOpen=0

 #启动HL子核心
def HLtoSPOL(fileipt):
  if fileipt==0:
    print("sysinfo→官方资源文件转SPOL程序")
    print("sysinfo→请输入需要转换的资源文件的名称")
  while True:
    if fileipt==0:
        filename=input(r"Userinput\tospol→")
    else:
        filename=fileipt
    try:
        if filename=="exit":
            return
        file=open(".\\arknights\\story\\"+filename+".txt","r",encoding="UTF-8")
    except IOError:
        print("sysinfo→找不到文件",filename)
        if fileipt!=0:
            return False
    else:
        print("sysinfo→已经找到文件",filename)
        break

  try:
    os.remove(r".\\story\\"+filename+".spol")
  except Exception:
    None
  else:
    None
  ToSPOL(filename,file)
  return True

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
    dirslst=[".\\CrashReport",".\\text",".\\story",".\\lang",".\\Visual\\cache\\BGP",".\\Visual\\cache\\Chara",".\\arknights\\cache",".\\arknights\\story"]
    for i in dirslst:
        if not os.path.exists(i):
            print("sysinfo→Directory '"+i+"' missed.Now rebuilding...")
            os.makedirs(i)
    print("sysinfo→Checked")

#检查更新
def Checkupdate(num):
    VerList=VersionList(Day,Edition)
    if type(VerList)!=list:
        if VerList=="ERROR":
            print("sysinfo→"+msg("Check_Update_Info_Net_Error"))
            return [4,0]
    elif type(VerList)==list:
        try:
            Prelist=[]
            Publist=[]
            for Verinfo in VerList:
                if Verinfo[2]=="Pre":
                    Prelist+=[Verinfo]
                elif Verinfo[2]=="Pub" or Verinfo[2]=="Branch":
                    Publist+=[Verinfo]
            if "Pre" in InsiderSubVer:
                print("sysinfo→"+msg("Check_Update_Info_Pre"))
                LatestVer=Prelist[0]
            elif "Pub" in InsiderSubVer:
                print("sysinfo→"+msg("Check_Update_Info_Pub"))
                LatestVer=Publist[0]
            else:
                print("sysinfo→"+msg("Check_Update_Info_Branch"))
                LatestVer=Publist[0]
            LatestBuildVer=LatestVer[1][LatestVer[1].index("(Build")+6:LatestVer[1].index(")")]
            if float(LatestBuildVer)>float(InsiderBuildVer):
                print("sysinfo→"+msg("Check_Update_Info_Latest").format(LatestVer[0],LatestVer[1]))
                return [0,LatestVer[1]]
            elif float(LatestBuildVer)==float(InsiderBuildVer):
                print("sysinfo→"+msg("Check_Update_Info_New"))
                return [1,0]
            elif float(LatestBuildVer)<float(InsiderBuildVer):
                print("sysinfo→"+msg("Check_Update_Info_Insider"))
                return [2,0]
        except:
            print("sysinfo→"+msg("Check_Update_Info_Ver_Error"))
            return [3,0]
    else:
        print("sysinfo→"+msg("Check_Update_Info_Net_Error"))
        return [4,0]

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
