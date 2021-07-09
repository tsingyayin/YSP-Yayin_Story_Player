#我本想把实现显示和控件定义的相关东西分离，但是现在看来似乎不太可能。
#也就是说这个ArtificialUI会不可避免的很大

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *

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

        #传输选择
class USERCHOOSEBRANCH(QObject):
    UserChooseWhich=pyqtSignal(str)
    def __init__(self):
        super(USERCHOOSEBRANCH,self).__init__()

        #传输速度
class USERSPEEDEMIT(QObject):
    UserSpeedSet=pyqtSignal(str)
    def __init__(self):
        super(USERSPEEDEMIT,self).__init__()

        #音乐播放线程
class PlayBgm(QThread):
    def __init__(self,parent = None):
        super(PlayBgm,self).__init__(parent)
        
    def run(self):
        global glo_file,glo_volume
        self.play=QMediaPlayer()
        self.Filename=QMediaContent(QUrl.fromLocalFile(glo_file))
        self.play.setMedia(self.Filename)
        self.volumeself=glo_volume
        self.play.setVolume(self.volumeself)
        self.play.play()
        

    def fade(self):
        for i in range(self.volumeself,0,-1):
            self.play.setVolume(i)
            tm.sleep(0.01)
        self.play.pause()
        self.quit()

        #音效播放线程
class PlaySound(QThread):
    def __init__(self,parent = None):
        super(PlaySound,self).__init__(parent)
        
    def run(self):
        global glo_file,glo_volume
        self.play=QMediaPlayer()
        self.Filename=QMediaContent(QUrl.fromLocalFile(glo_file))
        self.play.setMedia(self.Filename)
        self.volumeself=glo_volume
        self.play.setVolume(self.volumeself)
        self.play.play()

    def fade(self):
        for i in range(self.volumeself,0,-1):
            self.play.setVolume(i)
            tm.sleep(0.01)
        self.play.pause()
        self.quit()

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

        self.UserChooseBranch=USERCHOOSEBRANCH()
        self.UserChooseBranchRecive=USERCHOOSEBRANCHRECIVE()

        self.SpeedRecive=USERSPEEDRECIVE()
        self.SetSpeed=USERSPEEDEMIT()

        self.PLAYSound=PlaySound()
        self.StopUnlock=LastContinue()
        self.WillStop=WillStop()

        self.StoryPlaying=STORYPLAYING()
        self.EmitStopPlay=EMITSTOPPLAYING()

        self.EmitJump=EMITJUMPLINE()
        self.Userswitchline=USERSWITCHLINE()

        #背景定义为黑色
        BackC=QPalette()
        BackC.setColor(BackC.Background,QColor(0,0,0))
        self.setPalette(BackC)

        #相对字体
        self.Fontsize90=str(int(self.Y*0.083333))+"px"
        self.Fontsize80=str(int(self.Y*0.074074))+"px"
        self.Fontsize60=str(int(self.Y*0.055555))+"px"
        self.Fontsize45=str(int(self.Y*0.041666))+"px"
        self.Fontsize40=str(int(self.Y*0.037037))+"px"
        self.Fontsize35=str(int(self.Y*0.032407))+"px"
        self.Fontsize30=str(int(self.Y*0.027777))+"px"


        
        #音频交替计数
        self.music_thread=0
        self.music_thread_lst=[]

        #背景交替计数
        self.changeBG=1

        #各个控件的基本声明
        self.Name_Label=QLabel(self)#姓名
        self.Word_Label=QLabel(self)#讲述内容
        self.Free_Label=QLabel(self)#自由文本

        self.Splashlst=Splashesstr
        self.Splashes_Label=QLabel(self)#Splashes文本
        
        self.TopTitle=QLabel(self)#顶标题
        self.MainTitle=QLabel(self)#标题
        self.SubTitle=QLabel(self)#副标题

        self.BG1=QLabel(self)#交替第一背景
        self.BG2=QLabel(self)#交替第二背景
        self.WhiteFlash=QLabel(self)#白色闪烁特效层

        self.Logo=QLabel(self)#派别Logo

        self.Frame=QLabel(self)#渐变遮罩
        self.BGR=QImage()#背景原始图像
        

        self.AVG_L=QLabel(self)#多人讲述左侧立绘
        self.AVG_M=QLabel(self)#单人讲述居中立绘
        self.AVG_R=QLabel(self)#多人讲述右侧立绘

        self.AVG_L_R=QImage()#上述三个立绘的待处理版本
        self.AVG_M_R=QImage()
        self.AVG_R_R=QImage()

        self.BGM=QLabel(self)#背景音乐（暂定）

        #分支选项
        self.BranchButton_4=QPushButton(self)
        self.BranchButton_3=QPushButton(self)
        self.BranchButton_2=QPushButton(self)
        self.BranchButton_1=QPushButton(self)

        #self.TestButtonIN=QPushButton(self)#测试背景淡入按钮
        #self.TestButtonOut=QPushButton(self)#测试背景淡出按钮
        self.Hellotext=QLabel(self)
        self.Run=QPushButton(self)#核心启动按钮
        self.Run.setObjectName("Run")
        

        #姓名和讲述内容文本框、自由文本文本框的样式定义
        self.Name_Label.setStyleSheet("QLabel{color:#AAAAAA;font-size:"+self.Fontsize45+";font-family:'SimHei';font-weight:bold}")
        self.Name_Label.setAlignment(Qt.AlignRight)
        self.Word_Label.setStyleSheet("QLabel{color:#FFF5F5;font-size:"+self.Fontsize35+";font-family:'SimHei';font-weight:bold}")
        self.Word_Label.setAlignment(Qt.AlignLeft)

        self.Free_Label.setStyleSheet("QLabel{color:#FFFFFF;font-size:"+self.Fontsize35+";font-family:'SimHei';font-weight:bold}")
        self.Free_Label.setAlignment(Qt.AlignCenter)

        self.OPFree_Label=QGraphicsOpacityEffect()
        self.OPFree_Label.setOpacity(0)
        self.Free_Label.setGraphicsEffect(self.OPFree_Label)

       
        #顶标题、主标题和副标题的格式定义
        self.TopTitle.setStyleSheet("QLabel{color:#FFFFFF;font-size:"+self.Fontsize45+";font-family:'Microsoft YaHei'}")
        self.TopTitle.setAlignment(Qt.AlignCenter)
        self.TopTitle.setText("SPOL STORY")

        self.MainTitle.setStyleSheet("QLabel{color:#FFFFFF;font-size:"+self.Fontsize90+";font-family:'Microsoft YaHei'}")
        self.MainTitle.setAlignment(Qt.AlignCenter)

        self.SubTitle.setStyleSheet("QLabel{color:#FFFFFF;font-size:"+self.Fontsize60+";font-family:'Microsoft YaHei'}")
        self.SubTitle.setAlignment(Qt.AlignCenter)

        self.Splashes_Label.setStyleSheet("QLabel{color:#FFFFFF;font-size:"+self.Fontsize30+";font-family:'SimHei';font-weight:bold}")
        self.Splashes_Label.setAlignment(Qt.AlignCenter)
        self.Splashes_Label.setGeometry(QRect(0,self.Y*0.85,self.X,self.Y*0.02777))

        self.OPSplashes_Label=QGraphicsOpacityEffect()
        self.OPSplashes_Label.setOpacity(0)
        self.Splashes_Label.setGraphicsEffect(self.OPSplashes_Label)

        #退出按钮
        self.ExitButton=QPushButton(self)
        self.ExitButton.setObjectName("ExitButton")
        self.ExitButton.setGeometry(QRect(int(self.X*0.4818),int(self.Y*0.8564),70,70))

        self.OPExitButton=QGraphicsOpacityEffect()
        self.OPExitButton.setOpacity(1)
        self.ExitButton.setGraphicsEffect(self.OPExitButton)

        self.QSSExitButton="""
           #ExitButton{
                    background-color:rgba(0,0,0,0);
                    background-image:url('./Visual/source/BaseUI/Button/ExitButton_N.png');
            }
            #ExitButton:hover{
                    background-color:rgba(0,0,0,0);
                    background-image:url('./Visual/source/BaseUI/Button/ExitButton_P.png');
            }
            #ExitButton:Pressed{
                    background-color:rgba(0,0,0,0);
                    background-image:url('./Visual/source/BaseUI/Button/ExitButton_C.png');
            }
        """
        self.ExitButton.setStyleSheet(self.QSSExitButton)
        self.ExitButton.clicked.connect(self.ExitProgram)

        #背景控件位置设置
        self.BG1.setGeometry(QRect(0,0,self.X,self.Y))
        self.BG2.setGeometry(QRect(0,0,self.X,self.Y))

        #白色闪屏定义
        self.WhiteFlashPixmap=QImage(self.X,self.Y,QImage.Format_ARGB32)
        self.WhiteFlashPixmap.fill(QColor(255,255,255,255))
        self.WhiteFlash.setPixmap(QPixmap(self.WhiteFlashPixmap))

        self.OPWhiteFlash=QGraphicsOpacityEffect()
        self.OPWhiteFlash.setOpacity(0)
        self.WhiteFlash.setGraphicsEffect(self.OPWhiteFlash)
        
        #播放控制按钮
        self.AutoButton=QPushButton(self)
        self.AutoButton.setObjectName("AutoButton")
        self.AutoButton.setGeometry(QRect(int(self.X*0.80729),int(self.Y*0.038),int(self.X*0.098125),int(self.Y*0.046296)))
        self.AutoButton.setText(msg("Ui_AutoButton_Auto"))
        self.AutoButtonTick=0
        
        self.NextButton=QPushButton(self)
        self.NextButton.setObjectName("NextButton")
        self.NextButton.setGeometry(QRect(int(self.X*0.902604),int(self.Y*0.8981),int(self.X*0.078125),int(self.Y*0.046296)))
        self.NextButton.setText(msg("Ui_NextButton"))
        self.SpeedButton=QPushButton(self)
        self.SpeedButton.setObjectName("SpeedButton")
        self.SpeedButton.setGeometry(QRect(int(self.X*0.902604),int(self.Y*0.038),int(self.X*0.078125),int(self.Y*0.046296)))
        self.SpeedButton.setText("1.0x")

        self.OPSpeedButton=QGraphicsOpacityEffect()
        self.OPSpeedButton.setOpacity(0)
        self.SpeedButton.setGraphicsEffect(self.OPSpeedButton)

        self.OPAutoButton=QGraphicsOpacityEffect()
        self.OPAutoButton.setOpacity(0)
        self.AutoButton.setGraphicsEffect(self.OPAutoButton)

        self.OPNextButton=QGraphicsOpacityEffect()
        self.OPNextButton.setOpacity(0)
        self.NextButton.setGraphicsEffect(self.OPNextButton)

        self.QSSAutoButton="""
        #AutoButton{
        background-color:rgba(0,0,0,0);
        color:#FFFFFF;
        font-size:"""+self.Fontsize40+""";
        font-family:'SimHei';
        font-weight:bold;
        text-align:left;
        }
        """
        self.AutoButton.setStyleSheet(self.QSSAutoButton)

        self.QSSNextButton="""
        #NextButton{
        background-color:rgba(0,0,0,0);
        color:#FFFFFF;
        font-family:'SimHei';
        font-size:"""+self.Fontsize40+""";
        font-weight:bold;
        text-align:left;
        }
        """
        self.NextButton.setStyleSheet(self.QSSNextButton)
 
        self.QSSSpeedButton="""
        #SpeedButton{
        background-color:rgba(0,0,0,0);
        font-size:"""+self.Fontsize40+""";
        font-family:'Microsoft YaHei';
        text-align:left;
        color:#FFFFFF;
        }
        """
        self.SpeedButton.setStyleSheet(self.QSSSpeedButton)

        self.SpeedNow=0 #循环取值初始化

        #启动核心的按钮的位置和文本信息
        self.Run.setGeometry(QRect(int(self.X*0.2083),int(self.Y*0.3703),260,260))
        self.QSSRun="""
            #Run{
                    background-color:rgba(0,0,0,0);
                    background-image:url('./Visual/source/BaseUI/Button/StartButton_N.png');
            }
            #Run:hover{
                    background-color:rgba(0,0,0,0);
                    background-image:url('./Visual/source/BaseUI/Button/StartButton_P.png');
            }
            #Run:Pressed{
                    background-color:rgba(0,0,0,0);
                    background-image:url('./Visual/source/BaseUI/Button/StartButton_C.png');
            }
            """
        self.Run.setStyleSheet(self.QSSRun)

        self.Hellotext.setGeometry(QRect(int(self.X*0.5208),int(self.Y*0.4629),700,80))
        self.Hellotext.setText(msg("UI_Msg_Current_Mode"))
        self.Hellotext.setStyleSheet("QLabel{color:#FFFFFF;font-size:"+self.Fontsize80+";font-family:'Microsoft YaHei'}")

        #分支按钮的背景图片定义
        self.BranchButton_1.setObjectName("Branchbutton")
        self.BranchButton_2.setObjectName("Branchbutton")
        self.BranchButton_3.setObjectName("Branchbutton")
        self.BranchButton_4.setObjectName("Branchbutton")

        self.QSSBranchButton="""
        #Branchbutton{
        color:#FFFFFF;
        font-size:25px;
        font-family:'SimHei';
        background-color:rgba(0,0,0,0);
        background-image:url('./Visual/source/BaseUI/Button/BranchButton_N.png');
        }
        #Branchbutton:hover{
        color:#FFFFFF;
        font-size:25px;
        font-family:'SimHei';
        background-color:rgba(0,0,0,0);
        background-image:url('./Visual/source/BaseUI/Button/BranchButton_P.png');
        }
        #Branchbutton:Pressed{
        color:#FFFFFF;
        font-size:25px;
        font-family:'SimHei';
        background-color:rgba(0,0,0,0);
        background-image:url('./Visual/source/BaseUI/Button/BranchButton_C.png');
        }

        """
        self.BranchButton_1.setStyleSheet(self.QSSBranchButton)
        self.BranchButton_2.setStyleSheet(self.QSSBranchButton)
        self.BranchButton_3.setStyleSheet(self.QSSBranchButton)
        self.BranchButton_4.setStyleSheet(self.QSSBranchButton)

        #分支按钮初始化
        self.OPBranchButton_1=QGraphicsOpacityEffect()
        self.OPBranchButton_1.setOpacity(0)
        self.BranchButton_1.setGraphicsEffect(self.OPBranchButton_1)
        self.OPBranchButton_2=QGraphicsOpacityEffect()
        self.OPBranchButton_2.setOpacity(0)
        self.BranchButton_2.setGraphicsEffect(self.OPBranchButton_2)
        self.OPBranchButton_3=QGraphicsOpacityEffect()
        self.OPBranchButton_3.setOpacity(0)
        self.BranchButton_3.setGraphicsEffect(self.OPBranchButton_3)
        self.OPBranchButton_4=QGraphicsOpacityEffect()
        self.OPBranchButton_4.setOpacity(0)
        self.BranchButton_4.setGraphicsEffect(self.OPBranchButton_4)

        #遮罩
        self.Frame.setGeometry(0,0,self.X,self.Y)
        self.Frame_R=QImage()
        self.Frame_R.load("./Visual/source/BaseUI/Frame/frame.png")
        self.Frame_R=self.Frame_R.scaled(self.X,self.Y,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
        self.Frame.setPixmap(QPixmap(self.Frame_R))

        #控件位置
        self.Name_Label.setGeometry(QRect(int(self.X*0.0),int(self.Y*0.86944),int(self.X*0.2078125),int(self.Y*0.042)))
        self.Word_Label.setGeometry(QRect(int(self.X*0.2609375),int(self.Y*0.87685),int(self.X*0.6875),int(self.Y*0.105)))
        self.AVG_L.setGeometry(QRect(int(self.X*-0.068229),int(self.Y*0.12),int(self.X*74635),int(self.X*0.75635)))
        self.AVG_M.setGeometry(QRect(int(self.X*0.127083),int(self.Y*0.12),int(self.X*0.74635),int(self.X*0.74635)))
        self.AVG_R.setGeometry(QRect(int(self.X*0.321354),int(self.Y*0.12),int(self.X*0.74635),int(self.X*0.74635)))
        self.TopTitle.setGeometry(QRect(int(self.X*0.333333),int(self.Y*0.30),int(self.X*0.333333),int(self.Y*0.1666666)))
        self.MainTitle.setGeometry(QRect(int(self.X*0.333333),int(self.Y*0.40),int(self.X*0.333333),int(self.Y*0.1666666)))
        self.SubTitle.setGeometry(QRect(int(self.X*0.333333),int(self.Y*0.5),int(self.X*0.333333),int(self.Y*0.1666666)))
        self.Logo.setGeometry(QRect(int(self.X*0.3671875),int(self.Y*0.222222),int(self.Y*0.4722222),int(self.Y*0.4722222)))
        
        #自选进度按钮
        self.LogButton=QPushButton(self)
        self.LogButtonPixRaw=QPixmap(".\\Visual\\source\\BaseUI\\Button\\LogButton_N.png")
        self.LogButtonPixRaw=self.LogButtonPixRaw.scaled(int(self.Y*0.055),int(self.Y*0.055),Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
        self.LogButton.setIcon(QIcon(self.LogButtonPixRaw))
        self.LogButton.setIconSize(QSize(int(self.Y*0.055),int(self.Y*0.055)))
        self.LogButton.setGeometry(QRect(int(self.X*0.030416),int(self.Y*0.033),int(self.Y*0.055),int(self.Y*0.055)))
        self.LogButton.setStyleSheet("QPushButton{background-color:rgba(0,0,0,0);}")
        self.OPLogButton=QGraphicsOpacityEffect()
        self.OPLogButton.setOpacity(0)
        self.LogButton.setGraphicsEffect(self.OPLogButton)

        #自选进度相关控件
        self.StoryScroll=QScrollBar(Qt.Vertical,self)
        self.StoryScroll.setGeometry(QRect(int(self.X*0.983),int(self.Y*0),int(self.X*0.015),int(self.Y)))
        self.OPStoryScroll=QGraphicsOpacityEffect()
        self.OPStoryScroll.setOpacity(0)
        self.StoryScroll.setGraphicsEffect(self.OPStoryScroll)
        self.QSSStoryScroll="""
            QScrollBar:vertical{
                background-color:rgba(0,0,0,0);
                margin:0px,0px,0px,0px;
                padding-top:0px;
                padding-bottom:0px;
            }
            QScrollBar::handle:vertical{
                background-color:rgba(255,255,255,1);
                border-radius:"""+str(self.X*0.005)+"""px;
            }
            QScrollBar::handle:vertical:hover{
                background-color:rgba(200,200,200,1); 
                border-radius:"""+str(self.X*0.005)+"""px;
            }
            QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{
                background-color:rgba(0,0,0,0);
            }
            QScrollBar::add-line:vertical{
                height:0px;
                width:0px;
                subcontrol-position:bottom;
            }
            QScrollBar::sub-line:vertical{
                height:0px;
                width:0px;
                subcontrol-position:top;
            }
        """
        self.StoryScroll.setStyleSheet(self.QSSStoryScroll)
        self.StoryScrollBG=QLabel(self)
        self.StoryScrollBGRaw=QImage(self.X,self.Y,QImage.Format_ARGB32)
        self.StoryScrollBGRaw.fill(QColor(0,0,0,180))
        self.StoryScrollBG.setPixmap(QPixmap(self.StoryScrollBGRaw))
        self.OPStoryScrollBG=QGraphicsOpacityEffect()
        self.OPStoryScrollBG.setOpacity(0)
        self.StoryScrollBG.setGraphicsEffect(self.OPStoryScrollBG)

        self.StoryBigPad=QLabel(self)
        self.OPStoryBigPad=QGraphicsOpacityEffect()
        self.OPStoryBigPad.setOpacity(0)
        self.StoryBigPad.setGraphicsEffect(self.OPStoryBigPad)
        self.StoryBigPad.setText("")
        self.StoryBigPad.setAlignment(Qt.AlignLeft)
        self.StoryBigPad.setGeometry(QRect(int(self.X*0.05),int(self.Y*0),int(self.X*0.9),int(self.Y*1)))
        self.StoryBigPad.setStyleSheet("QLabel{color:#FFFFFF;font-size:"+self.Fontsize30+";font-family:'SimHei';}")

        self.StoryLineNum=QLabel(self)
        self.OPStoryLineNum=QGraphicsOpacityEffect()
        self.OPStoryLineNum.setOpacity(0)
        self.StoryLineNum.setGraphicsEffect(self.OPStoryLineNum)
        self.StoryLineNum.setAlignment(Qt.AlignCenter)
        self.StoryLineNum.setGeometry(QRect(int(self.X*0.027),int(self.Y*0.3),int(self.X*0.07),int(self.Y*0.11111)))
        self.StoryLineNum.setText(msg("Ui_Current_Line")+"\n"+"0")
        self.StoryLineNum.setStyleSheet("QLabel{color:#DDDDDD;font-size:"+self.Fontsize60+";font-family:'SimHei'}")

        self.ToLineNum=QLabel(self)
        self.OPToLineNum=QGraphicsOpacityEffect()
        self.OPToLineNum.setOpacity(0)
        self.ToLineNum.setGraphicsEffect(self.OPToLineNum)
        self.ToLineNum.setAlignment(Qt.AlignCenter)
        self.ToLineNum.setGeometry(QRect(int(self.X*0.027),int(self.Y*0.6),int(self.X*0.07),int(self.Y*0.11111)))
        self.ToLineNum.setText(msg("Ui_To_Which_Line")+"\n"+"0")
        self.ToLineNum.setStyleSheet("QLabel{color:#DDDDDD;font-size:"+self.Fontsize60+";font-family:'SimHei'}")

        self.JumpEmitButton=QPushButton(self)
        self.OPJumpEmitButton=QGraphicsOpacityEffect()
        self.OPJumpEmitButton.setOpacity(0)
        self.JumpEmitButton.setGraphicsEffect(self.OPJumpEmitButton)
        self.JumpEmitButton.setObjectName("JumpEmitButton")
        self.JumpEmitButton.setGeometry(QRect(int(self.X*0.027),int(self.Y*0.71),int(self.X*0.07),int(self.Y*0.11111)))
        self.JumpEmitButton.setText(msg("Ui_Msg_Yes"))
        self.QSSJumpEmitButton="""
        #JumpEmitButton{
        background-color:rgba(0,0,0,0);
        color:#DDDDDD;
        font-size:"""+self.Fontsize40+""";
        font-family:'SimHei';
        font-weight:bold;
        text-align:centre;
        }
        #JumpEmitButton:hover{
        background-color:rgba(0,0,0,0);
        color:#66CCFF;
        font-size:"""+self.Fontsize40+""";
        font-family:'SimHei';
        font-weight:bold;
        text-align:centre;
        }
        """
        self.JumpEmitButton.setStyleSheet(self.QSSJumpEmitButton)

        #控件遮挡关系-默认情况
        self.BG2.raise_()
        self.BG1.raise_()
        self.AVG_L.raise_()
        self.AVG_M.raise_()
        self.AVG_R.raise_()
        self.WhiteFlash.raise_()
        self.Frame.raise_()
        self.Free_Label.raise_()
        self.BranchButton_1.raise_()
        self.BranchButton_2.raise_()
        self.BranchButton_3.raise_()
        self.BranchButton_4.raise_()
        self.Name_Label.raise_()
        self.Word_Label.raise_()
        self.Logo.raise_()
        self.TopTitle.raise_()
        self.MainTitle.raise_()
        self.SubTitle.raise_()
        self.AutoButton.raise_()
        self.NextButton.raise_()
        self.SpeedButton.raise_()
        self.LogButton.raise_()
        self.Run.raise_()
        self.Hellotext.raise_()
        self.ExitButton.raise_()

        #开始页面透明度初始化
        self.OPRun=QGraphicsOpacityEffect()
        self.OPRun.setOpacity(1)
        self.Run.setGraphicsEffect(self.OPRun)

        self.OPHellotext=QGraphicsOpacityEffect()
        self.OPHellotext.setOpacity(1)
        self.Hellotext.setGraphicsEffect(self.OPHellotext)

        #按钮信号和槽函数连接
        self.Run.clicked.connect(self.RUNCORE)
        self.EmitStopPlay.EmitStopPlaying.connect(self.StoryPlaying.get)
        self.EmitJump.EmitJumpLine.connect(self.Userswitchline.get)
        #背景透明度初始化
        self.OPBG1=QGraphicsOpacityEffect()
        self.OPBG1.setOpacity(1)
        self.BG1.setGraphicsEffect(self.OPBG1)

        self.OPBG2=QGraphicsOpacityEffect()
        self.OPBG2.setOpacity(0)
        self.BG2.setGraphicsEffect(self.OPBG2)

        #框架透明度初始化
        self.OPFrame=QGraphicsOpacityEffect()
        self.OPFrame.setOpacity(0)
        self.Frame.setGraphicsEffect(self.OPFrame)

        #标题相关控件初始化
        self.OPTopTitle=QGraphicsOpacityEffect()
        self.OPTopTitle.setOpacity(0)
        self.TopTitle.setGraphicsEffect(self.OPTopTitle)

        self.OPMainTitle=QGraphicsOpacityEffect()
        self.OPMainTitle.setOpacity(0)
        self.MainTitle.setGraphicsEffect(self.OPMainTitle)

        self.OPSubTitle=QGraphicsOpacityEffect()
        self.OPSubTitle.setOpacity(0)
        self.SubTitle.setGraphicsEffect(self.OPSubTitle)

        self.OPLogo=QGraphicsOpacityEffect()
        self.OPLogo.setOpacity(0)
        self.Logo.setGraphicsEffect(self.OPLogo)

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
        self.Inbranch=0

        #自动按钮基本文本处理函数
    def AutoChange(self):
        if self.Auto==1: 
            self.Auto=0
            self.QSSAutoButton="""
            #AutoButton{
            background-color:rgba(0,0,0,0);
            color:#FFFFFF;
            font-size:"""+self.Fontsize40+""";
            font-family:'SimHei';
            font-weight:bold;
            text-align:left;
            }
            """
            self.AutoButton.setText(msg("Ui_AutoButton_Auto_Off"))
            self.AutoButton.setStyleSheet(self.QSSAutoButton)
        elif self.Auto==0: 
            self.Auto=1
            self.AutoButtonTick=0
            self.QSSAutoButton="""
            #AutoButton{
            background-color:rgba(0,0,0,0);
            color:#FFFFFF;
            font-size:"""+self.Fontsize40+""";
            font-family:'SimHei';
            font-weight:bold;
            text-align:left;
            }
            """
            self.AutoButton.setText(msg("Ui_AutoButton_Auto"))
            self.AutoButton.setStyleSheet(self.QSSAutoButton)

         #处理自动按钮的动画
    def RepaintAutoButton(self):
        if self.Auto==1:
            if self.AutoButtonTick==0:
                self.AutoButton.setText(msg("Ui_AutoButton_Auto")+"")
                self.AutoButtonTick+=1
            elif self.AutoButtonTick==1:
                self.AutoButton.setText(msg("Ui_AutoButton_Auto")+"▶")
                self.AutoButtonTick+=1
            elif self.AutoButtonTick==2:
                self.AutoButton.setText(msg("Ui_AutoButton_Auto")+"▶▶")
                self.AutoButtonTick+=1
            elif self.AutoButtonTick==3:
                self.AutoButton.setText(msg("Ui_AutoButton_Auto")+"▶▶▶")
                self.AutoButtonTick=0

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
        self.Interpreter.can_update_chara.connect(self.setprintchara)
        self.Interpreter.can_update_bg.connect(self.setprintbg)
        self.Interpreter.update_num_bg.connect(self.UpdateBG)
        self.Interpreter.update_chara_num.connect(self.UpdateWords)
        self.Interpreter.can_hide_hello.connect(self.hidehello)
        self.Interpreter.can_reprint_hello.connect(self.reprinthello)
        self.Interpreter.can_show_title.connect(self.showtitle)
        self.Interpreter.can_hide_title.connect(self.hidetitle)
        self.Interpreter.can_prepare_play.connect(self.hidetitlelast)
        self.Interpreter.need_to_choose.connect(self.choosebranch)
        self.Interpreter.show_next.connect(self.ShowNext)
        self.Interpreter.can_update_bgm.connect(self.PlayBGM)
        self.Interpreter.can_update_sound.connect(self.Playsound)
        self.Interpreter.can_update_freedom.connect(self.setfreedom)
        self.Interpreter.update_num_freedom.connect(self.UpdateFreedom)
        self.Interpreter.can_clear_freedom.connect(self.ClearFreedom)
        self.Interpreter.inrunning.connect(self.StopUnlock.get)
        self.Interpreter.willstop.connect(self.WillStop.get)
        self.Interpreter.save_line_list.connect(self.savelinelist)
        self.Interpreter.clr_line_list.connect(self.clrlinelist)
        self.Interpreter.set_scroll_info.connect(self.setscrollinfo)
        self.Interpreter.now_which_line.connect(self.updatelinenum)
        self.UserChooseBranch.UserChooseWhich.connect(self.UserChooseBranchRecive.get)
        self.SetSpeed.UserSpeedSet.connect(self.SpeedRecive.get)

        self.Ticker.Tick.connect(self.RepaintAutoButton)
        #准备启动数值
        self.StoryName.StoryNameEmit.connect(self.StoryNameRecive.get)
        self.StoryName.StoryNameEmit.emit(self.Storyname)

        self.SpeedNow=0
        self.Speedfloat=1.0
        Speednum=1.0
        self.LogButtonIs=0

        #启动
        StoryShow=1
        self.Savelinelist=[]
        self.Auto=1
        self.Ticker.start()
        self.Interpreter.start()
        
         #初始控件隐藏
    def hidehello(self,num):
        if num==1:
            
            for i in range(1,100):
                self.OPRun=QGraphicsOpacityEffect()
                self.OPRun.setOpacity(1-i/100)
                self.Run.setGraphicsEffect(self.OPRun)
                self.Run.repaint()
                self.OPHellotext=QGraphicsOpacityEffect()
                self.OPHellotext.setOpacity(1-i/100)
                self.Hellotext.setGraphicsEffect(self.OPHellotext)
                self.Hellotext.repaint()
                self.OPExitButton=QGraphicsOpacityEffect()
                self.OPExitButton.setOpacity(1-i/100)
                self.ExitButton.setGraphicsEffect(self.OPExitButton)
                self.ExitButton.repaint()
                tm.sleep(0.01)
            #断开事件
            self.Run.clicked.disconnect(self.RUNCORE)
            self.ExitButton.clicked.disconnect(self.ExitProgram)
            

            global STOPUNLOCK
            STOPUNLOCK=True

        #初始控件复现
    def reprinthello(self,num):
        global StoryShow
        StoryShow=0
        self.Ticker.wait()

        del self.Ticker
        if num==1:

            #初始化音频播放
            if self.music_thread==1:
                self.playsound2.fade()
                self.playsound2.wait()
                del self.playsound2
            elif self.music_thread==2:
                self.playsound1.fade()
                self.playsound1.wait()
                del self.playsound1

            self.Interpreter.wait()
            del self.Interpreter

            self.music_thread=0

            self.OPAutoButton=QGraphicsOpacityEffect()
            self.OPAutoButton.setOpacity(0)
            self.AutoButton.setGraphicsEffect(self.OPAutoButton)

            self.OPNextButton=QGraphicsOpacityEffect()
            self.OPNextButton.setOpacity(0)
            self.NextButton.setGraphicsEffect(self.OPNextButton)

            self.OPSpeedButton=QGraphicsOpacityEffect()
            self.OPSpeedButton.setOpacity(0)
            self.SpeedButton.setGraphicsEffect(self.OPSpeedButton)

            self.OPLogButton=QGraphicsOpacityEffect()
            self.OPLogButton.setOpacity(0)
            self.LogButton.setGraphicsEffect(self.OPLogButton)

            self.BG2.raise_()
            self.BG1.raise_()
            self.AVG_L.raise_()
            self.AVG_M.raise_()
            self.AVG_R.raise_()
            self.WhiteFlash.raise_()
            self.Frame.raise_()
            self.BranchButton_1.raise_()
            self.BranchButton_2.raise_()
            self.BranchButton_3.raise_()
            self.BranchButton_4.raise_()
            self.Name_Label.raise_()
            self.Word_Label.raise_()
            self.Logo.raise_()
            self.MainTitle.raise_()
            self.SubTitle.raise_()
            self.Hellotext.raise_()
            self.AutoButton.raise_()
            self.NextButton.raise_()
            self.SpeedButton.raise_()
            self.LogButton.raise_()
            self.Run.raise_()
            self.ExitButton.raise_()


            self.Name_Label.setText("")
            self.Word_Label.setText("")

            self.BG1.setPixmap(QPixmap(""))
            self.BG2.setPixmap(QPixmap(""))
            self.AVG_L.setPixmap(QPixmap(""))
            self.AVG_M.setPixmap(QPixmap(""))
            self.AVG_R.setPixmap(QPixmap(""))

            self.OPFrame=QGraphicsOpacityEffect()
            self.OPFrame.setOpacity(0)
            self.Frame.setGraphicsEffect(self.OPFrame)

            self.BG1.repaint()
            self.BG2.repaint()
            self.Frame.repaint()
            self.Name_Label.repaint()
            self.Word_Label.repaint()

            for i in range(1,100):
                self.OPRun=QGraphicsOpacityEffect()
                self.OPRun.setOpacity(i/100)
                self.Run.setGraphicsEffect(self.OPRun)
                self.Run.repaint()
                self.OPHellotext=QGraphicsOpacityEffect()
                self.OPHellotext.setOpacity(i/100)
                self.Hellotext.setGraphicsEffect(self.OPHellotext)
                self.Hellotext.repaint()
                self.OPExitButton=QGraphicsOpacityEffect()
                self.OPExitButton.setOpacity(i/100)
                self.ExitButton.setGraphicsEffect(self.OPExitButton)
                self.ExitButton.repaint()
                tm.sleep(0.01)
                
            self.OPBG1=QGraphicsOpacityEffect()
            self.OPBG1.setOpacity(1)
            self.BG1.setGraphicsEffect(self.OPBG1)

            self.OPBG2=QGraphicsOpacityEffect()
            self.OPBG2.setOpacity(0)
            self.BG2.setGraphicsEffect(self.OPBG2)

            
            #关闭直接打开属性
            self.DirectOpen=0

            try:
                #断开事件
                self.AutoButton.clicked.disconnect(self.AutoChange)
                self.SpeedButton.clicked.disconnect(self.SpeedChange)
                self.LogButton.clicked.disconnect(self.ShowLog)
            except:
                None
            else:
                None

            #重新连接事件
            self.Run.clicked.connect(self.RUNCORE)
            self.ExitButton.clicked.connect(self.ExitProgram)

        #初始化行信息
    def clrlinelist(self):
        self.Savelinelist=[]

        #记忆行信息
    def savelinelist(self,listinfo):
        self.Savelinelist+=[listinfo]

        #设置滚动条信息(其实还有设置展示信息)
    def setscrollinfo(self):
        self.Lineinforaw=""
        self.StoryScroll.setMinimum(0)
        self.StoryScroll.setMaximum(len(self.Savelinelist)-1)
        self.StoryScroll.setSingleStep(1)

        for i in self.Savelinelist:
            self.Lineinforaw+=str(self.Savelinelist.index(i))+"\t"+i[1]+"\n\n"

        self.StoryBigPad.setText(self.Lineinforaw)
        self.StoryBigPad.setGeometry(QRect(self.X*0.12,self.Y*0.675,self.X*0.8,int(len(self.Savelinelist)*(self.Y*0.06111111))))
        self.StoryScroll.valueChanged.connect(self.MoveBigPad)

        #设置移动大剧情板的动画和跳转数值
    def MoveBigPad(self):
        self.StoryBigPad.setGeometry(QRect(self.X*0.12,self.Y*0.675-self.StoryScroll.value()*(self.Y*0.06111111),self.X*0.8,int(len(self.Savelinelist)*(self.Y*0.06111111))))
        self.ToLineNum.setText(msg("Ui_To_Which_Line")+"\n"+str(self.StoryScroll.value()))

        #当前行数值动画
    def updatelinenum(self,lineinfo):
        for i in range(0,len(self.Savelinelist)):
            if lineinfo==self.Savelinelist[i][0]:
                self.StoryLineNum.setText(msg("Ui_Current_Line")+"\n"+str(i+1))
                self.StoryScroll.setValue(i+1)

        #标题展示函数-前半段
    def showtitle(self,titlesetlst):
        #背景透明度初始化
        self.OPTopTitle=QGraphicsOpacityEffect()
        self.OPTopTitle.setOpacity(1)
        self.TopTitle.setGraphicsEffect(self.OPTopTitle)

        self.OPBG1=QGraphicsOpacityEffect()
        self.OPBG1.setOpacity(1)
        self.BG1.setGraphicsEffect(self.OPBG1)

        self.OPBG2=QGraphicsOpacityEffect()
        self.OPBG2.setOpacity(0)
        self.BG2.setGraphicsEffect(self.OPBG2)

        self.Splashes_Label.setText("")

        self.BG2.raise_()
        self.BG1.raise_()
        self.AVG_L.raise_()
        self.AVG_M.raise_()
        self.AVG_R.raise_()
        self.WhiteFlash.raise_()
        self.Frame.raise_()
        self.BranchButton_1.raise_()
        self.BranchButton_2.raise_()
        self.BranchButton_3.raise_()
        self.BranchButton_4.raise_()
        self.Name_Label.raise_()
        self.Word_Label.raise_()
        self.Logo.raise_()
        self.TopTitle.raise_()
        self.MainTitle.raise_()
        self.SubTitle.raise_()
        self.Splashes_Label.raise_()
        self.AutoButton.raise_()

        self.BG1.setPixmap(QPixmap(""))
        self.BG2.setPixmap(QPixmap(""))
        self.BG1.repaint()
        self.BG2.repaint()


        self.MainTitle.setText(titlesetlst[0])
        self.SubTitle.setText(titlesetlst[1])
        self.BGRaw=QImage()
        self.BGRaw.load("./Visual/source/BGP/"+titlesetlst[2]+".png")
        self.BGRaw=self.BGRaw.scaled(self.X,self.Y,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
        self.BG1.setPixmap(QPixmap(self.BGRaw))
        self.LogoRaw=QImage()
        self.LogoRaw.load("./Visual/source/Logo/"+titlesetlst[3]+".png")
        self.LogoRaw=self.LogoRaw.scaled(int(self.Y*0.4722222),int(self.Y*0.4722222),Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
        self.Logo.setPixmap(QPixmap(self.LogoRaw))

        self.OPLogo.setOpacity(1)
        self.Logo.setGraphicsEffect(self.OPLogo)
        
        self.BLBG1=QGraphicsBlurEffect()
        self.BLBG1.setBlurRadius(3)
        self.BG1.setGraphicsEffect(self.BLBG1)

        self.OPMainTitle.setOpacity(1)
        self.MainTitle.setGraphicsEffect(self.OPMainTitle)
        
        self.OPSubTitle.setOpacity(1)
        self.SubTitle.setGraphicsEffect(self.OPSubTitle)

        self.Splashlenth=len(self.Splashlst)
        self.Splashwhich=rnd.randint(0,self.Splashlenth-1)
        self.Splashes_Label.setText(self.Splashlst[self.Splashwhich])

        self.OPSplashes_Label=QGraphicsOpacityEffect()
        self.OPSplashes_Label.setOpacity(1)
        self.Splashes_Label.setGraphicsEffect(self.OPSplashes_Label)
        self.Splashes_Label.repaint()

        self.Logo.repaint()
        self.SubTitle.repaint()
        self.MainTitle.repaint()
        self.BG1.repaint()

        #标题显示函数-中半段
    def hidetitle(self):
        self.BG1.raise_()
        self.BG2.raise_()
        self.AVG_L.raise_()
        self.AVG_M.raise_()
        self.AVG_R.raise_()
        self.WhiteFlash.raise_()
        self.Frame.raise_()
        self.Name_Label.raise_()
        self.Word_Label.raise_()
        self.Logo.raise_()
        self.TopTitle.raise_()
        self.MainTitle.raise_()
        self.SubTitle.raise_()
        self.Splashes_Label.raise_()
        self.AutoButton.raise_()
        self.NextButton.raise_()
        self.SpeedButton.raise_()

        self.BG2_R=QImage(self.X,self.Y,QImage.Format_ARGB32)
        self.BG2_R.fill(QColor(0,0,0,255))
        self.BG2.setPixmap(QPixmap(self.BG2_R))

        self.OPSplashes_Label=QGraphicsOpacityEffect()
        self.OPSplashes_Label.setOpacity(0)
        self.Splashes_Label.setGraphicsEffect(self.OPSplashes_Label)
        self.Splashes_Label.repaint()

        for i in range(0,21):
            self.OPBG2=QGraphicsOpacityEffect()
            self.OPBG2.setOpacity(i/20)
            self.BG2.setGraphicsEffect(self.OPBG2)
            self.BG2.repaint()

        self.BG1.setPixmap(QPixmap(""))
        self.OPBG1=QGraphicsOpacityEffect()
        self.OPBG1.setOpacity(1)
        self.BG1.setGraphicsEffect(self.OPBG1)

        self.BG2.setPixmap(QPixmap(""))
        self.OPBG2=QGraphicsOpacityEffect()
        self.OPBG2.setOpacity(0)
        self.BG2.setGraphicsEffect(self.OPBG2)

        #标题显示函数-后半段
    def hidetitlelast(self):
        global Speednum
        self.OPTopTitle=QGraphicsOpacityEffect()
        self.OPTopTitle.setOpacity(0)
        self.TopTitle.setGraphicsEffect(self.OPTopTitle)

        self.OPMainTitle.setOpacity(0)
        self.MainTitle.setGraphicsEffect(self.OPMainTitle)
        
        self.OPSubTitle.setOpacity(0)
        self.SubTitle.setGraphicsEffect(self.OPSubTitle)

        self.OPLogo=QGraphicsOpacityEffect()
        self.OPLogo.setOpacity(0)
        self.Logo.setGraphicsEffect(self.OPLogo)

        self.Logo.repaint()
        self.SubTitle.repaint()
        self.MainTitle.repaint()

        self.BG2.raise_()
        self.BG1.raise_()
        self.AVG_L.raise_()
        self.AVG_M.raise_()
        self.AVG_R.raise_()
        self.Frame.raise_()
        self.Name_Label.raise_()
        self.Word_Label.raise_()
        self.Logo.raise_()
        self.TopTitle.raise_()
        self.MainTitle.raise_()
        self.SubTitle.raise_()
        self.Splashes_Label.raise_()

        self.SetSpeed.UserSpeedSet.emit("1")
        self.SpeedButton.setText("1.0x")

        self.OPAutoButton=QGraphicsOpacityEffect()
        self.OPAutoButton.setOpacity(1)
        self.AutoButton.setGraphicsEffect(self.OPAutoButton)

        self.OPSpeedButton=QGraphicsOpacityEffect()
        self.OPSpeedButton.setOpacity(1)
        self.SpeedButton.setGraphicsEffect(self.OPSpeedButton)

        self.OPNextButton=QGraphicsOpacityEffect()
        self.OPNextButton.setOpacity(0)
        self.NextButton.setGraphicsEffect(self.OPNextButton)

        self.OPLogButton=QGraphicsOpacityEffect()
        self.OPLogButton.setOpacity(1)
        self.LogButton.setGraphicsEffect(self.OPLogButton)

        self.AutoButton.raise_()
        self.NextButton.raise_()
        self.SpeedButton.raise_()
        self.LogButton.raise_()

        #链接事件
        self.AutoButton.clicked.connect(self.AutoChange)
        self.SpeedButton.clicked.connect(self.SpeedChange)
        self.LogButton.clicked.connect(self.ShowLog)

        #发送跳转选择
    def Emitlinenum(self):
        self.EmitJump.EmitJumpLine.emit(self.Savelinelist[self.StoryScroll.value()][0]-2)
        self.ShowLog()

        #展示\隐藏自选滚动
    def ShowLog(self):
        if self.LogButtonIs==0:
            if self.Auto==1:
                self.AutoChange()
                self.AutoContinue=1
            self.OPStoryScroll=QGraphicsOpacityEffect()
            self.OPStoryScroll.setOpacity(1)
            self.StoryScroll.setGraphicsEffect(self.OPStoryScroll)
            self.OPStoryScrollBG=QGraphicsOpacityEffect()
            self.OPStoryScrollBG.setOpacity(1)
            self.StoryScrollBG.setGraphicsEffect(self.OPStoryScrollBG)
            self.OPStoryBigPad=QGraphicsOpacityEffect()
            self.OPStoryBigPad.setOpacity(1)
            self.StoryBigPad.setGraphicsEffect(self.OPStoryBigPad)
            self.OPStoryLineNum=QGraphicsOpacityEffect()
            self.OPStoryLineNum.setOpacity(1)
            self.StoryLineNum.setGraphicsEffect(self.OPStoryLineNum)
            self.OPToLineNum=QGraphicsOpacityEffect()
            self.OPToLineNum.setOpacity(1)
            self.ToLineNum.setGraphicsEffect(self.OPToLineNum)
            self.OPJumpEmitButton=QGraphicsOpacityEffect()
            self.OPJumpEmitButton.setOpacity(1)
            self.JumpEmitButton.setGraphicsEffect(self.OPJumpEmitButton)

            self.JumpEmitButton.clicked.connect(self.Emitlinenum)

            self.StoryScrollBG.raise_()
            self.StoryBigPad.raise_()
            self.StoryScroll.raise_()
            self.LogButton.raise_()
            self.StoryLineNum.raise_()
            self.ToLineNum.raise_()
            self.JumpEmitButton.raise_()

            self.LogButtonIs=1
        elif self.LogButtonIs==1:
            if self.AutoContinue==1:
                self.AutoChange()
                self.ToNext()
                self.AutoContinue=0

            self.JumpEmitButton.clicked.disconnect(self.Emitlinenum)
            self.OPStoryScroll=QGraphicsOpacityEffect()
            self.OPStoryScroll.setOpacity(0)
            self.StoryScroll.setGraphicsEffect(self.OPStoryScroll)
            self.OPStoryScrolBGl=QGraphicsOpacityEffect()
            self.OPStoryScrollBG.setOpacity(0)
            self.StoryScrollBG.setGraphicsEffect(self.OPStoryScrollBG)
            self.OPStoryBigPad=QGraphicsOpacityEffect()
            self.OPStoryBigPad.setOpacity(0)
            self.StoryBigPad.setGraphicsEffect(self.OPStoryBigPad)
            self.OPStoryLineNum=QGraphicsOpacityEffect()
            self.OPStoryLineNum.setOpacity(0)
            self.StoryLineNum.setGraphicsEffect(self.OPStoryLineNum)
            self.OPToLineNum=QGraphicsOpacityEffect()
            self.OPToLineNum.setOpacity(0)
            self.ToLineNum.setGraphicsEffect(self.OPToLineNum)
            self.OPJumpEmitButton=QGraphicsOpacityEffect()
            self.OPJumpEmitButton.setOpacity(0)
            self.JumpEmitButton.setGraphicsEffect(self.OPJumpEmitButton)
            self.AVG_L.raise_()
            self.AVG_M.raise_()
            self.AVG_R.raise_()
            self.WhiteFlash.raise_()
            self.Frame.raise_()
            self.Name_Label.raise_()
            self.Word_Label.raise_()
            self.AutoButton.raise_()
            self.NextButton.raise_()
            self.SpeedButton.raise_()
            self.LogButton.raise_()
            self.LogButtonIs=0

        #分支设置函数
    def choosebranch(self,converlst):
        if self.LogButtonIs==1:
            self.ShowLog()

        self.OPLogButton=QGraphicsOpacityEffect()
        self.OPLogButton.setOpacity(0)
        self.LogButton.setGraphicsEffect(self.OPLogButton)
        self.LogButton.clicked.disconnect(self.ShowLog)

        self.Inbranch=1
        self.converlstlen=len(converlst)
        self.BranchButton_1.raise_()
        self.BranchButton_2.raise_()
        self.BranchButton_3.raise_()
        self.BranchButton_4.raise_()
        self.AutoButton.raise_()

        if self.converlstlen==1:
            self.BranchButton_1.setText(converlst[0].split(":")[1])
            self.BranchButton_1.raise_()
        if self.converlstlen==2:
            self.BranchButton_1.setText(converlst[0].split(":")[1])
            self.BranchButton_2.setText(converlst[1].split(":")[1])
            self.BranchButton_1.raise_()
            self.BranchButton_2.raise_()
        if self.converlstlen==3:
            self.BranchButton_1.setText(converlst[0].split(":")[1])
            self.BranchButton_2.setText(converlst[1].split(":")[1])
            self.BranchButton_3.setText(converlst[2].split(":")[1])
            self.BranchButton_1.raise_()
            self.BranchButton_2.raise_()
            self.BranchButton_3.raise_()
        if self.converlstlen==4:
            self.BranchButton_1.setText(converlst[0].split(":")[1])
            self.BranchButton_2.setText(converlst[1].split(":")[1])
            self.BranchButton_3.setText(converlst[2].split(":")[1])
            self.BranchButton_4.setText(converlst[3].split(":")[1])
            self.BranchButton_1.raise_()
            self.BranchButton_2.raise_()
            self.BranchButton_3.raise_()
            self.BranchButton_4.raise_()

        if self.converlstlen==1:
            self.BranchButton_1.setGeometry(QRect(int(self.X/2-317.5),int(self.Y*0.402777),635,70))
            self.OPBranchButton_1=QGraphicsOpacityEffect()
            self.OPBranchButton_1.setOpacity(1)
            self.BranchButton_1.setGraphicsEffect(self.OPBranchButton_1)
            self.BranchButton_1.clicked.connect(self.Chooselabel)

            self.BranchButton_1.repaint()
        if self.converlstlen==2:
            self.BranchButton_1.setGeometry(QRect(int(self.X/2-317.5),int(self.Y*0.337962963),635,70))
            self.OPBranchButton_1=QGraphicsOpacityEffect()
            self.OPBranchButton_1.setOpacity(1)
            self.BranchButton_1.setGraphicsEffect(self.OPBranchButton_1)
            self.BranchButton_1.clicked.connect(self.Chooselabel)

            self.BranchButton_2.setGeometry(QRect(int(self.X/2-317.5),int(self.Y*0.435185),635,70))
            self.OPBranchButton_2=QGraphicsOpacityEffect()
            self.OPBranchButton_2.setOpacity(1)
            self.BranchButton_2.setGraphicsEffect(self.OPBranchButton_2)
            self.BranchButton_2.clicked.connect(self.Chooselabel)

            self.BranchButton_1.repaint()
            self.BranchButton_2.repaint()
        if self.converlstlen==3:
            self.BranchButton_1.setGeometry(QRect(int(self.X/2-317.5),int(self.Y*0.273148),635,70))
            self.OPBranchButton_1=QGraphicsOpacityEffect()
            self.OPBranchButton_1.setOpacity(1)
            self.BranchButton_1.setGraphicsEffect(self.OPBranchButton_1)
            self.BranchButton_1.clicked.connect(self.Chooselabel)

            self.BranchButton_2.setGeometry(QRect(int(self.X/2-317.5),int(self.Y*0.37037037),635,70))
            self.OPBranchButton_2=QGraphicsOpacityEffect()
            self.OPBranchButton_2.setOpacity(1)
            self.BranchButton_2.setGraphicsEffect(self.OPBranchButton_2)
            self.BranchButton_2.clicked.connect(self.Chooselabel)

            self.BranchButton_3.setGeometry(QRect(int(self.X/2-317.5),int(self.Y*0.46759),635,70))
            self.OPBranchButton_3=QGraphicsOpacityEffect()
            self.OPBranchButton_3.setOpacity(1)
            self.BranchButton_3.setGraphicsEffect(self.OPBranchButton_3)
            self.BranchButton_3.clicked.connect(self.Chooselabel)

            self.BranchButton_1.repaint()
            self.BranchButton_2.repaint()
            self.BranchButton_3.repaint()
        if self.converlstlen==4:
            self.BranchButton_1.setGeometry(QRect(int(self.X/2-317.5),int(self.Y*0.2574074),635,70))
            self.OPBranchButton_1=QGraphicsOpacityEffect()
            self.OPBranchButton_1.setOpacity(1)
            self.BranchButton_1.setGraphicsEffect(self.OPBranchButton_1)
            self.BranchButton_1.clicked.connect(self.Chooselabel)

            self.BranchButton_2.setGeometry(QRect(int(self.X/2-317.5),int(self.Y*0.3546296),635,70))
            self.OPBranchButton_2=QGraphicsOpacityEffect()
            self.OPBranchButton_2.setOpacity(1)
            self.BranchButton_2.setGraphicsEffect(self.OPBranchButton_2)
            self.BranchButton_2.clicked.connect(self.Chooselabel)

            self.BranchButton_3.setGeometry(QRect(int(self.X/2-317.5),int(self.Y*0.45185185),635,70))
            self.OPBranchButton_3=QGraphicsOpacityEffect()
            self.OPBranchButton_3.setOpacity(1)
            self.BranchButton_3.setGraphicsEffect(self.OPBranchButton_3)
            self.BranchButton_3.clicked.connect(self.Chooselabel)

            self.BranchButton_4.setGeometry(QRect(int(self.X/2-317.5),int(self.Y*0.549074),635,70))
            self.OPBranchButton_4=QGraphicsOpacityEffect()
            self.OPBranchButton_4.setOpacity(1)
            self.BranchButton_4.setGraphicsEffect(self.OPBranchButton_4)
            self.BranchButton_4.clicked.connect(self.Chooselabel)

            self.BranchButton_1.repaint()
            self.BranchButton_2.repaint()
            self.BranchButton_3.repaint()
            self.BranchButton_4.repaint()
      
        #发送选择函数
    def Chooselabel(self):
        sender=self.sender()
        choosewhat=sender.text()
        self.UserChooseBranch.UserChooseWhich.emit(choosewhat)
        

        self.BG2.raise_()
        self.BG1.raise_()
        self.AVG_L.raise_()
        self.AVG_M.raise_()
        self.AVG_R.raise_()
        self.Frame.raise_()
        self.BranchButton_1.raise_()
        self.BranchButton_2.raise_()
        self.BranchButton_3.raise_()
        self.BranchButton_4.raise_()
        self.Name_Label.raise_()
        self.Word_Label.raise_()
        self.Logo.raise_()
        self.MainTitle.raise_()
        self.SubTitle.raise_()
        self.AutoButton.raise_()
        self.SpeedButton.raise_()
        self.LogButton.raise_()

        #断开链接
        if self.converlstlen==1:
            self.BranchButton_1.clicked.disconnect(self.Chooselabel)
        elif self.converlstlen==2:
            self.BranchButton_1.clicked.disconnect(self.Chooselabel)
            self.BranchButton_2.clicked.disconnect(self.Chooselabel)
        elif self.converlstlen==3:
            self.BranchButton_1.clicked.disconnect(self.Chooselabel)
            self.BranchButton_2.clicked.disconnect(self.Chooselabel)
            self.BranchButton_3.clicked.disconnect(self.Chooselabel)
        elif self.converlstlen==4:
            self.BranchButton_1.clicked.disconnect(self.Chooselabel)
            self.BranchButton_2.clicked.disconnect(self.Chooselabel)
            self.BranchButton_3.clicked.disconnect(self.Chooselabel)
            self.BranchButton_4.clicked.disconnect(self.Chooselabel)

        self.Inbranch=0
        #隐藏全部
        self.OPBranchButton_1=QGraphicsOpacityEffect()
        self.OPBranchButton_1.setOpacity(0)
        self.BranchButton_1.setGraphicsEffect(self.OPBranchButton_1)
        self.OPBranchButton_2=QGraphicsOpacityEffect()
        self.OPBranchButton_2.setOpacity(0)
        self.BranchButton_2.setGraphicsEffect(self.OPBranchButton_2)
        self.OPBranchButton_3=QGraphicsOpacityEffect()
        self.OPBranchButton_3.setOpacity(0)
        self.BranchButton_3.setGraphicsEffect(self.OPBranchButton_3)
        self.OPBranchButton_4=QGraphicsOpacityEffect()
        self.OPBranchButton_4.setOpacity(0)
        self.BranchButton_4.setGraphicsEffect(self.OPBranchButton_4)

        self.BranchButton_1.repaint()
        self.BranchButton_2.repaint()
        self.BranchButton_3.repaint()
        self.BranchButton_4.repaint()
        #空置文本
        self.BranchButton_1.setText("")
        self.BranchButton_2.setText("")
        self.BranchButton_3.setText("")
        self.BranchButton_4.setText("")

        self.OPLogButton=QGraphicsOpacityEffect()
        self.OPLogButton.setOpacity(1)
        self.LogButton.setGraphicsEffect(self.OPLogButton)
        self.LogButton.clicked.connect(self.ShowLog)

        self.Interpreter.wake()

        #背景控制器-原始图像装载函数
    def setprintbg(self,bgsetlst):
        if bgsetlst[0]=="黑场":
            self.BGR=QImage(self.X,self.Y,QImage.Format_ARGB32)
            self.BGR.fill(QColor(0,0,0,255))
        else:
            if bgsetlst[1]=="0":
                self.BGR=QImage()
                self.BGR.load("./Visual/source/BGP/"+bgsetlst[0]+".png")
                self.BGR=self.BGR.scaled(self.X,self.Y,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
            elif bgsetlst[1]=="1":
                self.BGR=QImage()
                self.BGR.load("./Visual/cache/BGP/"+bgsetlst[0]+"-Dark.png")
                self.BGR=self.BGR.scaled(self.X,self.Y,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
            elif bgsetlst[1]=="2":
                self.BGR=QImage()
                self.BGR.load("./Visual/cache/BGP/"+bgsetlst[0]+"-Fade.png")
                self.BGR=self.BGR.scaled(self.X,self.Y,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
            elif bgsetlst[1]=="3":
                self.BGR=QImage()
                self.BGR.load("./Visual/cache/BGP/"+bgsetlst[0]+"-Fade-Dark.png")
                self.BGR=self.BGR.scaled(self.X,self.Y,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
            elif bgsetlst[1]=="4":
                self.BGR=QImage()
                self.BGR.load("./Visual/cache/BGP/"+bgsetlst[0]+"-BAW.png")
                self.BGR=self.BGR.scaled(self.X,self.Y,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
            elif bgsetlst[1]=="5":
                self.BGR=QImage()
                self.BGR.load("./Visual/cache/BGP/"+bgsetlst[0]+"-BAW-Dark.png")
                self.BGR=self.BGR.scaled(self.X,self.Y,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)

        #背景控制器-屏幕刷新函数
    def UpdateBG(self,i,bgsetlst):
        if self.changeBG==1:
            if i==0:
                self.BG1.setPixmap(QPixmap(self.BGR))
                self.BG2.raise_()
                self.BG1.raise_()
                self.AVG_L.raise_()
                self.AVG_M.raise_()
                self.AVG_R.raise_()
                self.WhiteFlash.raise_()
                self.Frame.raise_()
                self.Name_Label.raise_()
                self.Word_Label.raise_()
                self.AutoButton.raise_()
                self.NextButton.raise_()
                self.SpeedButton.raise_()
                self.LogButton.raise_()
                self.OPBG1=QGraphicsOpacityEffect()
                self.OPBG1.setOpacity(0)
                self.BG1.setGraphicsEffect(self.OPBG1)
                self.BG1.repaint()
            elif i!=0 and i!=1:
                self.OPBG1=QGraphicsOpacityEffect()
                self.OPBG1.setOpacity(i)
                self.BG1.setGraphicsEffect(self.OPBG1)
                self.BG1.repaint()
            elif i>=1:
                self.changeBG=2
                self.BG2.setPixmap(QPixmap(""))
                self.OPBG1=QGraphicsOpacityEffect()
                self.OPBG1.setOpacity(1)
                self.BG1.setGraphicsEffect(self.OPBG1)
                self.BG1.repaint()
                tm.sleep(0.1)
                if bgsetlst[2]=="1":
                    self.ShakeFUNC=ShakeFunc(self.Speedfloat)
                    self.ShakeFUNC.shakeXY.connect(self.ShakeRect)
                    self.ShakeFUNC.start()
                elif bgsetlst[2]=="2":
                    self.effectuse=2
                    self.FlashFUNCFast=FlashFuncFast(self.Speedfloat)
                    self.FlashFUNCFast.FlashOPint.connect(self.Flashwhite)
                    self.FlashFUNCFast.start()
                elif bgsetlst[2]=="3":
                    self.effectuse=3
                    self.FlashFUNCSlow=FlashFuncSlow(self.Speedfloat)
                    self.FlashFUNCSlow.FlashOPint.connect(self.Flashwhite)
                    self.FlashFUNCSlow.start()
                else:
                    self.Interpreter.wake()

        elif self.changeBG==2:
            if i==0:
                self.BG2.setPixmap(QPixmap(self.BGR))
                self.BG1.raise_()
                self.BG2.raise_()
                self.AVG_L.raise_()
                self.AVG_M.raise_()
                self.AVG_R.raise_()
                self.WhiteFlash.raise_()
                self.Frame.raise_()
                self.Name_Label.raise_()
                self.Word_Label.raise_()
                self.AutoButton.raise_()
                self.NextButton.raise_()
                self.SpeedButton.raise_()
                self.LogButton.raise_()
                self.OPBG2=QGraphicsOpacityEffect()
                self.OPBG2.setOpacity(0)
                self.BG2.setGraphicsEffect(self.OPBG2)
                self.BG2.repaint()
            elif i!=0 and i!=1:
                self.OPBG2=QGraphicsOpacityEffect()
                self.OPBG2.setOpacity(i)
                self.BG2.setGraphicsEffect(self.OPBG2)
                self.BG2.repaint()
            elif i>=1:
                self.changeBG=1
                self.BG1.setPixmap(QPixmap(""))
                self.OPBG2=QGraphicsOpacityEffect()
                self.OPBG2.setOpacity(1)
                self.BG2.setGraphicsEffect(self.OPBG2)
                self.BG2.repaint()
                tm.sleep(0.1)
                if bgsetlst[2]=="1":
                    self.ShakeFUNC=ShakeFunc(self.Speedfloat)
                    self.ShakeFUNC.shakeXY.connect(self.ShakeRect)
                    self.ShakeFUNC.start()
                elif bgsetlst[2]=="2":
                    self.effectuse=2
                    self.FlashFUNCFast=FlashFuncFast(self.Speedfloat)
                    self.FlashFUNCFast.FlashOPint.connect(self.Flashwhite)
                    self.FlashFUNCFast.start()
                elif bgsetlst[2]=="3":
                    self.effectuse=3
                    self.FlashFUNCSlow=FlashFuncSlow(self.Speedfloat)
                    self.FlashFUNCSlow.FlashOPint.connect(self.Flashwhite)
                    self.FlashFUNCSlow.start()
                else:
                    self.Interpreter.wake()
                    
        #背景晃动刷新函数
    def ShakeRect(self,sX,sY,end):
        if self.changeBG==2:
            self.BG1.setGeometry(QRect(int((self.Y/1080)*sX),int((self.Y/1080)*sY),self.X,self.Y))
            self.BG1.repaint()
        elif self.changeBG==1:
            self.BG2.setGeometry(QRect(int((self.Y/1080)*sX),int((self.Y/1080)*sY),self.X,self.Y))
            self.BG2.repaint()
        if end==1:
            self.ShakeFUNC.wait()
            del self.ShakeFUNC
            self.Interpreter.wake()

        #闪烁特效刷新函数
    def Flashwhite(self,i,end):
        if end == 0:
            self.OPWhiteFlash=QGraphicsOpacityEffect()
            self.OPWhiteFlash.setOpacity(0)
            self.WhiteFlash.setGraphicsEffect(self.OPWhiteFlash)
            self.WhiteFlash.repaint()
        elif end==1:
            self.OPWhiteFlash=QGraphicsOpacityEffect()
            self.OPWhiteFlash.setOpacity(i)
            self.WhiteFlash.setGraphicsEffect(self.OPWhiteFlash)
            self.WhiteFlash.repaint()
        elif end == 2:
            self.OPWhiteFlash=QGraphicsOpacityEffect()
            self.OPWhiteFlash.setOpacity(0)
            self.WhiteFlash.setGraphicsEffect(self.OPWhiteFlash)
            self.WhiteFlash.repaint()

            if self.effectuse==2:
                self.FlashFUNCFast.wait()
                del self.FlashFUNCFast
                self.effectuse=0
            elif self.effectuse==3:
                self.FlashFUNCSlow.wait()
                del self.FlashFUNCSlow
                self.effectuse=0

            self.Interpreter.wake()

        #音乐控制器-音频启动函数
    def PlayBGM(self,filename,volume):
        global glo_file,glo_volume
        glo_file=".\\Visual\\source\\BGM\\"+filename+".mp3"
        glo_volume=volume
        if self.music_thread==0:
            self.playsound1=PlayBgm()
            self.playsound1.start()
            self.music_thread=2
        elif self.music_thread==1:
            self.playsound2.fade()
            self.playsound2.wait()
            del self.playsound2
            self.playsound1=PlayBgm()
            self.playsound1.start()
            self.music_thread=2
        elif self.music_thread==2:
            self.playsound1.fade()
            self.playsound1.wait()
            del self.playsound1
            self.playsound2=PlayBgm()
            self.playsound2.start()
            self.music_thread=1

        #音效控制器-音频启动函数
    def Playsound(self,filename,volume):
        global glo_file,glo_volume
        glo_file=".\\Visual\\source\\Sound\\"+filename+".mp3"
        glo_volume=volume
        self.music_thread_lst+=[PlaySound()]
        self.music_thread_lst[-1].start()
        
        #讲述控制器-屏幕更新承接函数、立绘刷新函数
    def setprintchara(self,charapic,charawords,wordset,charanum,BGblack):
        
        self.AVG_L.raise_()
        self.AVG_M.raise_()
        self.AVG_R.raise_()
        self.Frame.raise_()
        self.Name_Label.raise_()
        self.Word_Label.raise_()
        self.AutoButton.raise_()
        self.NextButton.raise_()
        self.SpeedButton.raise_()
        self.LogButton.raise_()

        #确认遮罩状态
        if BGblack==1:
            self.OPFrame.setOpacity(1)
            self.Frame.setGraphicsEffect(self.OPFrame)
            self.Frame.repaint()
        elif BGblack==0:
            self.OPFrame.setOpacity(0)
            self.Frame.setGraphicsEffect(self.OPFrame)
            self.Frame.repaint()

            self.Name_Label.setText("")
            self.Word_Label.setText("")
            self.Name_Label.repaint()
            self.Word_Label.repaint()
            self.AVG_L.setPixmap(QPixmap(""))
            self.AVG_M.setPixmap(QPixmap(""))
            self.AVG_R.setPixmap(QPixmap(""))
        #填充立绘
        if charanum==1:
            for i in charapic:
                if i[0]=="":
                    self.AVG_L.setPixmap(QPixmap(""))
                    self.AVG_R.setPixmap(QPixmap(""))
                    self.AVG_M.setPixmap(QPixmap(""))
                    self.AVG_L.repaint()
                    self.AVG_R.repaint()
                    self.AVG_M.repaint()
                    
                if i[0]!="":
                    self.AVG_L.setPixmap(QPixmap(""))
                    self.AVG_R.setPixmap(QPixmap(""))
                    if i[6]=="(暗，沉默)":
                        self.AVG_M_R.load("./Visual/cache/Chara/"+i[0]+"_"+i[1]+"_"+i[3]+"-Dark.png")
                    elif i[3]!="0":
                        self.AVG_M_R.load("./Visual/cache/Chara/"+i[0]+"_"+i[1]+"_"+i[3]+".png")
                    else:
                        self.AVG_M_R.load("./Visual/source/Chara/"+i[0]+"_"+i[1]+".png")
                    self.AVG_M_R=self.AVG_M_R.scaled(int(self.X*0.74635),int(self.X*0.74635),Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
                    if self.AVG_M.pixmap()!=self.AVG_M_R:
                        if i[2]=="0":self.AVG_M.setPixmap(QPixmap(self.AVG_M_R))
                        elif i[2]=="1":self.AVG_M.setPixmap(QPixmap(self.AVG_M_R.mirrored(True,False)))
                        self.AVG_M.repaint()
                    self.AVG_L.repaint()
                    self.AVG_R.repaint()
        elif charanum==2:
            self.AVG_M.setPixmap(QPixmap(""))
            self.AVG_M.repaint()
            if charapic[0][0]!="":
                if charapic[0][6]=="(暗，沉默)":
                    self.AVG_L_R.load("./Visual/cache/Chara/"+charapic[0][0]+"_"+charapic[0][1]+"_"+charapic[0][3]+"-Dark.png")
                elif charapic[0][3]!="0":
                    self.AVG_L_R.load("./Visual/cache/Chara/"+charapic[0][0]+"_"+charapic[0][1]+"_"+charapic[0][3]+".png")
                else:
                    self.AVG_L_R.load("./Visual/source/Chara/"+charapic[0][0]+"_"+charapic[0][1]+".png")
                self.AVG_L_R=self.AVG_L_R.scaled(int(self.X*0.74635),int(self.X*0.74635),Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
                if self.AVG_L.pixmap()!=self.AVG_L_R:
                    if charapic[0][2]=="0":self.AVG_L.setPixmap(QPixmap(self.AVG_L_R))
                    elif charapic[0][2]=="1":self.AVG_L.setPixmap(QPixmap(self.AVG_L_R.mirrored(True,False)))
                    self.AVG_L.repaint()
            if charapic[1][0]!="":
                if charapic[1][6]=="(暗，沉默)":
                    self.AVG_R_R.load("./Visual/cache/Chara/"+charapic[1][0]+"_"+charapic[1][1]+"_"+charapic[1][3]+"-Dark.png")
                elif charapic[1][3]!="0":
                    self.AVG_R_R.load("./Visual/cache/Chara/"+charapic[1][0]+"_"+charapic[1][1]+"_"+charapic[1][3]+".png")
                else:
                    self.AVG_R_R.load("./Visual/source/Chara/"+charapic[1][0]+"_"+charapic[1][1]+".png")
                self.AVG_R_R=self.AVG_R_R.scaled(int(self.X*0.74635),int(self.X*0.74635),Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
                if self.AVG_R.pixmap()!=self.AVG_R_R:
                    if charapic[1][2]=="0":self.AVG_R.setPixmap(QPixmap(self.AVG_R_R))
                    elif charapic[1][2]=="1":self.AVG_R.setPixmap(QPixmap(self.AVG_R_R.mirrored(True,False)))
                    self.AVG_R.repaint()     
            
        #讲述控制器-讲述刷新函数
    def UpdateWords(self,i,wordsALL,charanum,wordset):
        

        if i[0]=="" and charanum==1:#当槽位上没有姓名且场上只有一人，认为是旁白
            self.Name_Label.setText("")
            self.Name_Label.repaint()
            self.Word_Label.setText(wordsALL)
            self.Word_Label.repaint()
          
        elif i[1]=="" and charanum==1:
            self.Name_Label.setText(i[0])
            self.Word_Label.setText("")
            self.Name_Label.repaint()
            self.Word_Label.repaint()

        elif (i[0]!="" and i[1]!="") or (i[0]!="" and charanum==1):
            self.Name_Last=self.Name_Label.text()
            if self.Name_Last!= i[0]:
                self.Name_Label.setText(i[0])
                self.Name_Label.repaint()
            self.Word_Label.setText(wordsALL)
            self.Word_Label.repaint()

        #自由文本控制器-设置函数
    def setfreedom(self,textsetlst,wordset):
        
        self.Free_Label.setText("")
        self.Free_Label.raise_()
        self.Free_Label.repaint()

        self.OPFree_Label=QGraphicsOpacityEffect()
        self.OPFree_Label.setOpacity(0)
        self.Free_Label.setGraphicsEffect(self.OPFree_Label)

        self.Free_Label.setGeometry(QRect(int(self.X*float(textsetlst[0])),int(self.Y*float(textsetlst[1])),int(self.X*0.75),int(self.Y*0.0324074)))
        if textsetlst[2]=="L":
            self.Free_Label.setAlignment(Qt.AlignLeft)
        elif textsetlst[2]=="M":
            self.Free_Label.setAlignment(Qt.AlignCenter)
        elif textsetLst[2]=="R":
            self.Free_Label.setAlignment(Qt.AlignRight)
        
        self.OPFree_Label=QGraphicsOpacityEffect()
        self.OPFree_Label.setOpacity(1)
        self.Free_Label.setGraphicsEffect(self.OPFree_Label)

        #自由文本控制器-更新函数
    def UpdateFreedom(self,Words):
        self.Free_Label.setText(Words)
        self.Free_Label.repaint()

        #自由文本控制器-清理函数
    def ClearFreedom(self,end):
        
        self.Free_Label.setText("")

        self.OPFree_Label=QGraphicsOpacityEffect()
        self.OPFree_Label.setOpacity(0)
        self.Free_Label.setGraphicsEffect(self.OPFree_Label)

        None

        #速度设置函数
    def SpeedChange(self):
        global Speednum
        self.SpeedNow+=1
        if self.SpeedNow%4==1:
            self.SetSpeed.UserSpeedSet.emit("0.666")
            self.SpeedButton.setText("1.5x")
            self.Speedfloat=0.666
            Speednum=0.666
        elif self.SpeedNow%4==2:
            self.SetSpeed.UserSpeedSet.emit("0.5")
            self.SpeedButton.setText("2.0x")
            self.Speedfloat=0.5
            Speednum=0.5
        elif self.SpeedNow%4==3:
            self.SetSpeed.UserSpeedSet.emit("2")
            self.SpeedButton.setText("0.5x")
            self.Speedfloat=2
            Speednum=2
        elif self.SpeedNow%4==0:
            self.SetSpeed.UserSpeedSet.emit("1")
            self.SpeedButton.setText("1.0x")
            self.Speedfloat=1.0
            Speednum=1.0

        self.SpeedButton.repaint()

        #键盘事件
    def keyPressEvent(self,QKeyEvent):
        global StoryShow
        if QKeyEvent.key()==Qt.Key_Escape:
            if StoryShow==0:
                self.EmitStopPlay.EmitStopPlaying.emit(0)
                try:
                    if self.music_thread==1:
                        self.playsound2.fade()
                        self.playsound2.wait()
                        del self.playsound2
                    elif self.music_thread==2:
                        self.playsound1.fade()
                        self.playsound1.wait()
                        del self.playsound1
                except:
                    None
                else:
                    None
                self.close()
                StoryShow=0
                qApp=QApplication.instance()
                qApp.quit()

            elif StoryShow==1 and self.LogButtonIs==0:
                self.EmitStopPlay.EmitStopPlaying.emit(0)
                StoryShow=0

            elif StoryShow==1 and self.LogButtonIs==1:
                self.ShowLog()

        elif QKeyEvent.key()==Qt.Key_Q and StoryShow==1:
            self.ShowLog()

        elif QKeyEvent.key()==Qt.Key_Return:
            if StoryShow==1:
                if self.Inbranch==0 :
                    self.Interpreter.wake()
                    self.OPNextButton=QGraphicsOpacityEffect()
                    self.OPNextButton.setOpacity(0)
                    self.NextButton.setGraphicsEffect(self.OPNextButton)
                    try:
                        self.NextButton.clicked.disconnect(self.ToNext)
                    except:
                        None
                    else:
                        None
                    print(msg("Ui_Thread_Core_Wake"))

            if self.LogButtonIs==1:
                self.Emitlinenum()

        elif QKeyEvent.key()==Qt.Key_W and StoryShow==1:
            self.SpeedChange()

        elif QKeyEvent.key()==Qt.Key_A and StoryShow==1:
            self.AutoChange()

        #滚轮事件
    def wheelEvent(self, event): 
        if self.LogButtonIs==1:
            self.StoryScroll.setValue(self.StoryScroll.value()-int(event.angleDelta().y()/120))

        #向下一个页面（自动模式）
    def ShowNext(self):
        if self.Auto==1:

            global STOPUNLOCK
            while True:
                if STOPUNLOCK==False:
                    self.Interpreter.wake()
                    break

        if self.Auto==0:
            self.NextButton.clicked.connect(self.ToNext)
            if self.LogButtonIs==0:
                self.OPNextButton=QGraphicsOpacityEffect()
                self.OPNextButton.setOpacity(1)
                self.NextButton.setGraphicsEffect(self.OPNextButton)
            #用来处理某些自选滚动的遮罩异常
            if self.LogButtonIs==1:
                self.StoryScrollBG.raise_()
                self.StoryBigPad.raise_()
                self.StoryScroll.raise_()
                self.LogButton.raise_()
                self.StoryLineNum.raise_()
                self.ToLineNum.raise_()
                self.JumpEmitButton.raise_()

        #向下一个页面（手动模式）
    def ToNext(self):
        self.Interpreter.wake()
        self.OPNextButton=QGraphicsOpacityEffect()
        self.OPNextButton.setOpacity(0)
        self.NextButton.setGraphicsEffect(self.OPNextButton)

       
        

        try:
            self.NextButton.clicked.disconnect(self.ToNext)
        except:
            None
        else:
            None

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
            if self.music_thread==1:
                    self.playsound2.fade()
                    self.playsound2.wait()
                    del self.playsound2
            elif self.music_thread==2:
                    self.playsound1.fade()
                    self.playsound1.wait()
                    del self.playsound1
        except:
            None
        else:
            None
        StoryShow=0