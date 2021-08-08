#我本想把实现显示和控件定义的相关东西分离，但是现在看来似乎不太可能。
#也就是说这个ArtificialUI会不可避免的很大

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from Visual.QtWordgame import *

from command.UICoreLauncher import *
from core.core0_6_0_U import *
from langcontrol import *
import time as tm
import sys
import random as rnd
from Visual.effect import *

sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore")
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore\Visual")

#下面两个类控制的内容用于指示唤醒函数
class WillStop(QObject):
    def __init__(self):
        super(WillStop,self).__init__()

    def get(self):
        global STOPUNLOCK
        STOPUNLOCK=False

class LastContinue(QObject):
    def __init__(self):
        super(LastContinue,self).__init__()

    def get(self):
        global STOPUNLOCK
        STOPUNLOCK=True
    
#告知解释器立即退出
class EMITSTOPPLAYING(QObject):
    EmitStopPlaying=pyqtSignal(int)
    def __init__(self):
        super(EMITSTOPPLAYING,self).__init__()
        
#告知解释器跳转行
class EMITJUMPLINE(QObject):
    EmitJumpLine=pyqtSignal(int)
    def __init__(self):
        super(EMITJUMPLINE,self).__init__()

        #传输文件名称
class STORYNAME(QObject):
    StoryNameEmit=pyqtSignal(str)
    def __init__(self):
        super(STORYNAME,self).__init__()

        #传输速度
class USERSPEEDEMIT(QObject):
    UserSpeedSet=pyqtSignal(str)
    def __init__(self):
        super(USERSPEEDEMIT,self).__init__()

        #通用动画数值线程
class TickThread(QThread):
    Tick=pyqtSignal()
    def __init__(self):
        super(TickThread,self).__init__()

    def run(self):
        global StoryShow,Speednum
        while StoryShow==1:
            self.Tick.emit()
            tm.sleep(Speednum*0.66)
        self.quit()

        #获得Splash内容
Splashesstr=[]
def SPLASHES(lst):
    global Splashesstr
    Splashesstr=lst
    return


#重构-字体
class Fontsize():
    def __init__(Y=1080):
        F90=str(int(Y*0.083333))+"px"
        F80=str(int(Y*0.074074))+"px"
        F60=str(int(Y*0.055555))+"px"
        F45=str(int(Y*0.041666))+"px"
        F40=str(int(Y*0.037037))+"px"
        F35=str(int(Y*0.032407))+"px"
        F30=str(int(Y*0.027777))+"px"


        #窗口内容定义
class UiMainWindow(QWidget):
    def setupUi(self):
        global Splashesstr,StoryShow

        StoryShow=0
        self.desktop=QDesktopWidget()
        self.current_monitor=self.desktop.screenNumber(self)
        self.Display=self.desktop.screenGeometry(self.current_monitor)
        self.X=self.Display.width()
        self.Y=self.Display.height()

        
        self.Spawn=SPAWN()

        self.StoryName=STORYNAME()
        self.StoryNameRecive=STORYNAMERECIVE()

        self.UserChooseBranchRecive=USERCHOOSEBRANCHRECIVE()

        self.SpeedRecive=USERSPEEDRECIVE()

        self.StopUnlock=LastContinue()
        self.WillStop=WillStop()

        self.StoryPlaying=STORYPLAYING()
        self.EmitStopPlay=EMITSTOPPLAYING()

        self.EmitJump=EMITJUMPLINE()
        self.Userswitchline=USERSWITCHLINE()

        #背景定义为黑色
        self.BackC=QPalette()
        self.BackC.setColor(self.BackC.Background,QColor(0,0,0))
        self.setPalette(self.BackC)

        #相对字体
        self.Fontsize90=str(int(self.Y*0.083333))+"px"
        self.Fontsize80=str(int(self.Y*0.074074))+"px"
        self.Fontsize60=str(int(self.Y*0.055555))+"px"
        self.Fontsize45=str(int(self.Y*0.041666))+"px"
        self.Fontsize40=str(int(self.Y*0.037037))+"px"
        self.Fontsize35=str(int(self.Y*0.032407))+"px"
        self.Fontsize30=str(int(self.Y*0.027777))+"px"

        #首页声明
        self.FirstPage=uFirstPage(self.X,self.Y,self)
        self.FirstPage.setOpacity(1)
        self.FirstPage.ChooseFileclicked.connect(self.RUNCORE)
        self.FirstPage.ExitProgramclicked.connect(self.ExitProgram)

        #标题页声明
        self.TitlePage=uTitlePage(self.X,self.Y,Splashesstr,self)

        #播放页声明
        self.PlayerPage=uPlayerPage(self.X,self.Y,self)
        self.PlayerPage.UserChooseWhich.connect(self.UserChooseBranchRecive.get)
        self.PlayerPage.UserSpeedSet.connect(self.SpeedRecive.get)
        self.PlayerPage.NeedWakeUp.connect(self.Wakeup)
        self.PlayerPage.LogPage.EmitJumpLine.connect(self.Userswitchline.get)
        #背景音乐播放
        self.PlayMusic=uSoundService()

        #音效播放列表
        self.music_thread_lst=[]

        self.BGM=QLabel(self)#背景音乐（暂定）
        

        self.PlayerPage.raise_()
        self.TitlePage.raise_()
        self.FirstPage.raise_()

        #按钮信号和槽函数连接
        self.EmitStopPlay.EmitStopPlaying.connect(self.StoryPlaying.get)

        self.DirectOpen=0

        #直接打开的情况下的参数设置
        if sys.argv.__len__() >=2:
            if os.path.exists(sys.argv[1]):
                self.DirectOpen=1
                self.Storyname=sys.argv[1]
                self.RUNCORE()
                del sys.argv[1]  ###############


        #主窗口功能定义
class MainWindow(UiMainWindow):

        #基本初始化
    def __init__(self,parent = None):
        super(MainWindow,self).__init__(parent)
        global StoryShow,Speednum
        Speednum=1.0
        self.setupUi()
        self.setWindowIcon(QIcon(".\\Visual\\source\\WinICO\\Story.ico"))
        self.setWindowTitle("YSP UI Mode")

        #核心启动函数
    def RUNCORE(self):
        global StoryShow
        if self.DirectOpen!=1: 
            self.ChooseStory = QFileDialog.getOpenFileName(self,msg("Choose_File"), "./Story","StoryFile(*.spol)")
            self.Storyname=self.ChooseStory[0]

        #给定线程
        self.Interpreter=SPAWN()
        self.Ticker=TickThread()

        #链接信号
        self.Interpreter.can_update_chara.connect(self.PlayerPage.setCurrentAvg)
        self.Interpreter.can_update_bg.connect(self.PlayerPage.setCurrentBGP)
        self.Interpreter.update_num_bg.connect(self.PlayerPage.updateCurrentBGP)
        self.Interpreter.update_chara_num.connect(self.PlayerPage.updateCurrentWords)
        self.Interpreter.can_hide_hello.connect(self.hidehello)
        self.Interpreter.can_reprint_hello.connect(self.reprinthello)
        self.Interpreter.can_show_title.connect(self.showtitle)
        self.Interpreter.can_hide_title.connect(self.hidetitle)
        self.Interpreter.can_prepare_play.connect(self.hidetitlelast)
        self.Interpreter.need_to_choose.connect(self.PlayerPage.setBranchButton)
        self.Interpreter.show_next.connect(self.PlayerPage.showNext)
        self.Interpreter.can_update_bgm.connect(self.PlayBGM)
        self.Interpreter.can_update_sound.connect(self.Playsound)
        self.Interpreter.can_update_freedom.connect(self.PlayerPage.setCurrentFree)
        self.Interpreter.update_num_freedom.connect(self.PlayerPage.updateCurrentFree)
        self.Interpreter.can_clear_freedom.connect(self.PlayerPage.clearCurrentFree)
        self.Interpreter.inrunning.connect(self.StopUnlock.get)
        self.Interpreter.willstop.connect(self.WillStop.get)
        self.Interpreter.save_line_list.connect(self.PlayerPage.LogPage.setLineList)
        self.Interpreter.set_scroll_info.connect(self.PlayerPage.LogPage.setScroll)
        self.Interpreter.now_which_line.connect(self.PlayerPage.LogPage.updatelinenum)

        self.Ticker.Tick.connect(self.PlayerPage.repaintAutoButton)
        #准备启动数值
        self.StoryName.StoryNameEmit.connect(self.StoryNameRecive.get)
        self.StoryName.StoryNameEmit.emit(self.Storyname)
           
        self.PlayerPage.initObject()
        self.PlayerPage.UserChooseWhich.connect(self.UserChooseBranchRecive.get)
        self.LogButtonIs=0

        #启动
        StoryShow=1
        self.music_thread=0
        self.Ticker.start()
        self.Interpreter.start()
        
         #初始控件隐藏
    def hidehello(self,num):
        if num==1:
            for i in range(1,100):
                self.FirstPage.setOpacity(1-i/100)
                self.FirstPage.repaint()
                tm.sleep(0.01)
            #断开事件
            self.FirstPage.ChooseFileclicked.disconnect(self.RUNCORE)
            self.FirstPage.ExitProgramclicked.disconnect(self.ExitProgram)

            global STOPUNLOCK
            STOPUNLOCK=True

        #初始控件复现
    def reprinthello(self,num):
        global StoryShow
        StoryShow=0
        self.PlayerPage.clearAll()
        self.Ticker.wait()
        del self.Ticker
        self.FirstPage.raise_()
        if num==1:

            #初始化音频播放
            try:
                self.PlayMusic.fadeMedia()
            except:
                None
            else:
                None
            self.Interpreter.wait()
            del self.Interpreter

            self.music_thread=0

            for i in range(1,100):
                self.FirstPage.setOpacity(i/100)
                self.FirstPage.repaint()
                tm.sleep(0.01)
            
            #关闭直接打开属性
            self.DirectOpen=0

            try:
                #断开事件
                self.LogButton.clicked.disconnect(self.ShowLog)
            except:
                None
            else:
                None

            #重新连接事件
            self.FirstPage.ChooseFileclicked.connect(self.RUNCORE)
            self.FirstPage.ExitProgramclicked.connect(self.ExitProgram)


        #标题展示函数-前半段
    def showtitle(self,titlesetlst):
        self.TitlePage.setTitleInfo(titlesetlst[0],titlesetlst[1],titlesetlst[2],titlesetlst[3])
        self.TitlePage.showPage()
        self.TitlePage.raise_()

        #标题显示函数-中半段
    def hidetitle(self):
        self.TitlePage.playAnimation()

        #标题显示函数-后半段
    def hidetitlelast(self):
        global Speednum
        self.TitlePage.hidePage()
        self.PlayerPage.raise_()
        self.PlayerPage.showPlayerPage()

        #音乐控制器-音频启动函数
    def PlayBGM(self,filename,volume):
        if self.music_thread==1:
            self.PlayMusic.fadeMedia()
        self.PlayMusic.loadfile(".//Visual//source//BGM//"+filename+".mp3",volume)
        self.PlayMusic.playMedia()
        self.music_thread=1

        #音效控制器-音频启动函数
    def Playsound(self,filename,volume):
        self.music_thread_lst+=[uSoundService()]
        self.music_thread_lst[-1].loadfile(".//Visual//source//Sound//"+filename+".mp3",volume)
        self.music_thread_lst[-1].playMedia()

        #键盘事件
    def keyPressEvent(self,QKeyEvent):
        global StoryShow
        if QKeyEvent.key()==Qt.Key_Escape:
            if StoryShow==0:
                self.EmitStopPlay.EmitStopPlaying.emit(0)
                try:
                    self.PlayMusic.fadeMedia()
                except:
                    None
                else:
                    None
                StoryShow=0
                qApp=QApplication.instance()
                qApp.quit()

            elif StoryShow==1 and self.PlayerPage.searchParameter("InLogPage")==0:
                self.EmitStopPlay.EmitStopPlaying.emit(0)
                StoryShow=0

            elif StoryShow==1 and self.PlayerPage.searchParameter("InLogPage")==1:
                self.PlayerPage.showLogPage()

        elif QKeyEvent.key()==Qt.Key_Q and StoryShow==1:
            self.PlayerPage.showLogPage()

        elif QKeyEvent.key()==Qt.Key_Return:
            if StoryShow==1:
                if self.PlayerPage.searchParameter("Inbranch")==0:
                    self.PlayerPage._ToNext()
                    print(msg("Ui_Thread_Core_Wake"))

            if self.PlayerPage.searchParameter("InLogPage")==1:
                self.PlayerPage.LogPage.EmitLineNum()
                self.PlayerPage.showLogPage()

        elif QKeyEvent.key()==Qt.Key_W and StoryShow==1:
            if self.PlayerPage.searchParameter("Inbranch")==0:
                self.PlayerPage._SpeedChange()

        elif QKeyEvent.key()==Qt.Key_A and StoryShow==1:
            if self.PlayerPage.searchParameter("Inbranch")==0:
                self.PlayerPage._AutoChange()

    def Wakeup(self):
        global STOPUNLOCK
        while True:
            if STOPUNLOCK==False:
                self.Interpreter.wake()
                break

        #正常退出程序
    def ExitProgram(self):
        global StoryShow
        self.close()
        qApp=QApplication.instance()
        qApp.quit()
        StoryShow=0

        #被强制关闭前停止相关线程
    def closeEvent(self,event):
        global StoryShow
        self.EmitStopPlay.EmitStopPlaying.emit(0)
        try:
            self.PlayMusic.fadeMedia()
        except:
            None
        else:
            None
        StoryShow=0