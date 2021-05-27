#我本想把实现显示和控件定义的相关东西分离，但是现在看来似乎不太可能。
#也就是说这个ArtificialUI会不可避免的很大

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *

from command.UICoreLauncher import *
from core.core0_4_1_R import *
from langcontrol import *
import time as tm
import sys
from Visual.effect import *
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore")
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore\Visual")

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

        #窗口内容定义
class UiMainWindow(QWidget):
    def setupUi(self):

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
        self.PLAYSound=PlaySound()

        #背景定义为黑色
        BackC=QPalette()
        BackC.setColor(BackC.Background,QColor(0,0,0))
        self.setPalette(BackC)

        #相对字体
        self.Fontsize90=str(int(self.Y*0.083333))+"px"
        self.Fontsize80=str(int(self.Y*0.074074))+"px"
        self.Fontsize60=str(int(self.Y*0.055555))+"px"
        self.Fontsize30=str(int(self.Y*0.027777))+"px"

        #引入操作
        self.FUNC=Function()
        
        #音频交替计数
        self.music_thread=0

        #背景交替计数
        self.changeBG=1

        #各个控件的基本声明
        self.Name_Label=QLabel(self)#姓名
        self.Word_Label=QLabel(self)#讲述内容
        self.Free_Label=QLabel(self)#自由文本
        self.MainTitle=QLabel(self)#标题
        self.SubTitle=QLabel(self)#副标题

        self.BG1=QLabel(self)#交替第一背景
        self.BG2=QLabel(self)#交替第二背景

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
        self.Name_Label.setStyleSheet("QLabel{color:#FFFFFF;font-size:"+self.Fontsize30+";}")
        self.Name_Label.setAlignment(Qt.AlignRight)
        self.Word_Label.setStyleSheet("QLabel{color:#AAAAAA;font-size:"+self.Fontsize30+";}")
        self.Word_Label.setAlignment(Qt.AlignLeft)

        self.Free_Label.setStyleSheet("QLabel{color:#FFFFFF;font-size:"+self.Fontsize30+";}")
        self.Free_Label.setAlignment(Qt.AlignCenter)

        self.OPFree_Label=QGraphicsOpacityEffect()
        self.OPFree_Label.setOpacity(0)
        self.Free_Label.setGraphicsEffect(self.OPFree_Label)

       
        #标题和副标题的格式定义
        self.MainTitle.setStyleSheet("QLabel{color:#FFFFFF;font-size:"+self.Fontsize90+";font-family:'Microsoft YaHei'}")
        self.MainTitle.setAlignment(Qt.AlignCenter)

        self.SubTitle.setStyleSheet("QLabel{color:#FFFFFF;font-size:"+self.Fontsize60+";font-family:'Microsoft YaHei'}")
        self.SubTitle.setAlignment(Qt.AlignCenter)

        #退出按钮
        self.ExitButton=QPushButton(self)
        self.ExitButton.setObjectName("ExitButton")
        self.ExitButton.setGeometry(QRect(int(self.X*0.4818),int(self.Y*0.8564),70,69))

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

        #播放控制按钮
        self.AutoButton=QPushButton(self)
        self.AutoButton.setObjectName("AutoButton")
        self.AutoButton.setGeometry(QRect(int(self.X*0.8333),int(self.Y*0.037),150,50))
        self.NextButton=QPushButton(self)
        self.NextButton.setObjectName("NextButton")
        self.NextButton.setGeometry(QRect(int(self.X*0.8333),int(self.Y*0.8981),150,50))

        self.OPAutoButton=QGraphicsOpacityEffect()
        self.OPAutoButton.setOpacity(0)
        self.AutoButton.setGraphicsEffect(self.OPAutoButton)

        self.OPNextButton=QGraphicsOpacityEffect()
        self.OPNextButton.setOpacity(0)
        self.NextButton.setGraphicsEffect(self.OPNextButton)

        self.QSSAutoButton="""
        #AutoButton{
        background-color:rgba(0,0,0,0);
        background-image:url('./Visual/source/BaseUI/Button/AutoButton_Au.png');
        }
        """
        self.AutoButton.setStyleSheet(self.QSSAutoButton)

        self.QSSNextButton="""
        #NextButton{
        background-color:rgba(0,0,0,0);
        background-image:url('./Visual/source/BaseUI/Button/NextButton_N.png');
        }
        """
        self.NextButton.setStyleSheet(self.QSSNextButton)

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
        self.Hellotext.setText("YSP UI Mode")
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
        font-family:'Microsoft YaHei';
        background-color:rgba(0,0,0,0);
        background-image:url('./Visual/source/BaseUI/Button/BranchButton_N.png');
        }
        #Branchbutton:hover{
        color:#FFFFFF;
        font-size:25px;
        font-family:'Microsoft YaHei';
        background-color:rgba(0,0,0,0);
        background-image:url('./Visual/source/BaseUI/Button/BranchButton_P.png');
        }
        #Branchbutton:Pressed{
        color:#FFFFFF;
        font-size:25px;
        font-family:'Microsoft YaHei';
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
        self.Name_Label.setGeometry(QRect(int(self.X*0.137),int(self.Y*0.888888),int(self.X*0.159),int(self.Y*0.277777)))
        self.Word_Label.setGeometry(QRect(int(self.X*0.3229166),int(self.Y*0.888888),int(self.X*0.5625),int(self.Y*0.083333)))
        self.AVG_L.setGeometry(QRect(int(self.X*0.046875),int(self.Y*0.2037037),int(self.X*0.46875),int(self.X*0.46875)))
        self.AVG_M.setGeometry(QRect(int(self.X*0.230729),int(self.Y*0.2037037),int(self.X*0.46875),int(self.X*0.46875)))
        self.AVG_R.setGeometry(QRect(int(self.X*0.414583),int(self.Y*0.2037037),int(self.X*0.46875),int(self.X*0.46875)))
        self.MainTitle.setGeometry(QRect(int(self.X*0.333333),int(self.Y*0.333333),int(self.X*0.333333),int(self.Y*0.1666666)))
        self.SubTitle.setGeometry(QRect(int(self.X*0.333333),int(self.Y*0.5),int(self.X*0.333333),int(self.Y*0.1666666)))
        self.Logo.setGeometry(QRect(int(self.X*0.3671875),int(self.Y*0.222222),int(self.Y*0.4722222),int(self.Y*0.4722222)))

        #控件遮挡关系-默认情况
        self.BG2.raise_()
        self.BG1.raise_()
        self.AVG_L.raise_()
        self.AVG_M.raise_()
        self.AVG_R.raise_()
        self.Frame.raise_()
        self.Free_Label.raise_()
        self.BranchButton_1.raise_()
        self.BranchButton_2.raise_()
        self.BranchButton_3.raise_()
        self.BranchButton_4.raise_()
        self.Name_Label.raise_()
        self.Word_Label.raise_()
        self.Logo.raise_()
        self.MainTitle.raise_()
        self.SubTitle.raise_()
        self.Run.raise_()
        self.Hellotext.raise_()
        self.AutoButton.raise_()
        self.NextButton.raise_()
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
        self.AutoButton.clicked.connect(self.AutoChange)
        
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

        #音频播放线程
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

        #主窗口功能定义
class MainWindow(UiMainWindow):

        #基本初始化
    def __init__(self,parent = None):
        super(MainWindow,self).__init__(parent)
        self.setupUi()
        self.setWindowIcon(QIcon(".\\Visual\\source\\WinICO\\Story.ico"))
        self.setWindowTitle("YSP UI Mode")

        #是否自动播放处理函数
    def AutoChange(self):
        if self.Auto==1: 
            self.Auto=0
            self.QSSAutoButton="""
        #AutoButton{
        background-color:rgba(0,0,0,0);
        background-image:url('./Visual/source/BaseUI/Button/AutoButton_Ar.png');
        }
        """
            self.AutoButton.setStyleSheet(self.QSSAutoButton)
        elif self.Auto==0: 
            self.Auto=1
            self.QSSAutoButton="""
        #AutoButton{
        background-color:rgba(0,0,0,0);
        background-image:url('./Visual/source/BaseUI/Button/AutoButton_Au.png');
        }
        """
            self.AutoButton.setStyleSheet(self.QSSAutoButton)

        #核心启动函数
    def RUNCORE(self):
        
        if self.DirectOpen!=1: 
            self.ChooseStory = QFileDialog.getOpenFileName(self,msg("Choose_File"), "./Story","StoryFile(*.spol)")
            self.Storyname=self.ChooseStory[0]

        #给定线程
        self.Interpreter=SPAWN()

        #链接信号
        self.Interpreter.can_update_chara.connect(self.setprintchara)
        self.Interpreter.can_update_bg.connect(self.setprintbg)
        self.Interpreter.update_num_bg.connect(self.UpdateBG)
        self.Interpreter.update_chara_num.connect(self.UpdateWords)
        self.Interpreter.can_hide_hello.connect(self.hidehello)
        self.Interpreter.can_reprint_hello.connect(self.reprinthello)
        self.Interpreter.can_show_title.connect(self.showtitle)
        self.Interpreter.need_to_choose.connect(self.choosebranch)
        self.Interpreter.show_next.connect(self.ShowNext)
        self.Interpreter.can_update_bgm.connect(self.Playsound)
        self.Interpreter.can_update_freedom.connect(self.setfreedom)
        self.Interpreter.update_num_freedom.connect(self.UpdateFreedom)
        self.Interpreter.can_clear_freedom.connect(self.ClearFreedom)
        self.UserChooseBranch.UserChooseWhich.connect(self.UserChooseBranchRecive.get)

        #准备启动数值
        self.StoryName.StoryNameEmit.connect(self.StoryNameRecive.get)
        self.StoryName.StoryNameEmit.emit(self.Storyname)

        #启动
        self.Auto=1
        self.Interpreter.start()
        
        #分支设置函数
    def choosebranch(self,converlst):
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
        self.Interpreter.wake()

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

        #标题展示函数
    def showtitle(self,titlesetlst):
        #背景透明度初始化
        self.OPBG1=QGraphicsOpacityEffect()
        self.OPBG1.setOpacity(1)
        self.BG1.setGraphicsEffect(self.OPBG1)

        self.OPBG2=QGraphicsOpacityEffect()
        self.OPBG2.setOpacity(0)
        self.BG2.setGraphicsEffect(self.OPBG2)

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

        self.Logo.repaint()
        self.SubTitle.repaint()
        self.MainTitle.repaint()
        self.BG1.repaint()

        tm.sleep(3)

        self.BG1.raise_()
        self.BG2.raise_()
        self.AVG_L.raise_()
        self.AVG_M.raise_()
        self.AVG_R.raise_()
        self.Frame.raise_()
        self.Name_Label.raise_()
        self.Word_Label.raise_()
        self.Logo.raise_()
        self.MainTitle.raise_()
        self.SubTitle.raise_()
        self.AutoButton.raise_()
        self.NextButton.raise_()

        self.BG2_R=QImage(self.X,self.Y,QImage.Format_ARGB32)
        self.BG2_R.fill(QColor(0,0,0,255))
        self.BG2.setPixmap(QPixmap(self.BG2_R))

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

        tm.sleep(1)
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
        self.MainTitle.raise_()
        self.SubTitle.raise_()
        self.Interpreter.wake()
        self.AutoButton.raise_()
        self.NextButton.raise_()

        self.OPAutoButton=QGraphicsOpacityEffect()
        self.OPAutoButton.setOpacity(1)
        self.AutoButton.setGraphicsEffect(self.OPAutoButton)

        self.OPNextButton=QGraphicsOpacityEffect()
        self.OPNextButton.setOpacity(0)
        self.NextButton.setGraphicsEffect(self.OPNextButton)

        self.AutoButton.raise_()
        self.NextButton.raise_()

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

        #初始控件复现
    def reprinthello(self,num):
        if num==1:

            #初始化音频播放
            if self.music_thread==1:
                self.playsound2.fade()
            elif self.music_thread==2:
                self.playsound1.fade()
            self.music_thread=0

            self.OPAutoButton=QGraphicsOpacityEffect()
            self.OPAutoButton.setOpacity(0)
            self.AutoButton.setGraphicsEffect(self.OPAutoButton)

            self.OPNextButton=QGraphicsOpacityEffect()
            self.OPNextButton.setOpacity(0)
            self.NextButton.setGraphicsEffect(self.OPNextButton)

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
            self.Run.raise_()
            self.Hellotext.raise_()
            self.AutoButton.raise_()
            self.NextButton.raise_()
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

            #重新连接事件
            self.Run.clicked.connect(self.RUNCORE)
            self.ExitButton.clicked.connect(self.ExitProgram)
        
        #背景控制器-原始图像装载函数
    def setprintbg(self,bgsetlst):
       self.BGR.load("./Visual/source/BGP/"+bgsetlst[0]+".png")
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
                self.Frame.raise_()
                self.Name_Label.raise_()
                self.Word_Label.raise_()
                self.AutoButton.raise_()
                self.NextButton.raise_()
            if eval(bgsetlst[3])!=0:
                self.OPBG1=QGraphicsOpacityEffect()
                self.OPBG1.setOpacity(i/20)
                self.BG1.setGraphicsEffect(self.OPBG1)
            elif eval(bgsetlst[3])==0:
                self.OPBG1=QGraphicsOpacityEffect()
                self.OPBG1.setOpacity(1)
                self.BG1.setGraphicsEffect(self.OPBG1)
            if i==20:
                self.changeBG=2
                self.BG2.setPixmap(QPixmap(""))
        elif self.changeBG==2:
            if i==0:
                self.BG2.setPixmap(QPixmap(self.BGR))
                self.BG1.raise_()
                self.BG2.raise_()
                self.AVG_L.raise_()
                self.AVG_M.raise_()
                self.AVG_R.raise_()
                self.Frame.raise_()
                self.Name_Label.raise_()
                self.Word_Label.raise_()
                self.AutoButton.raise_()
                self.NextButton.raise_()
            if eval(bgsetlst[3])!=0:
                self.OPBG2=QGraphicsOpacityEffect()
                self.OPBG2.setOpacity(i/20)
                self.BG2.setGraphicsEffect(self.OPBG2)
            elif eval(bgsetlst[3])==0:
                self.OPBG2=QGraphicsOpacityEffect()
                self.OPBG2.setOpacity(1)
                self.BG2.setGraphicsEffect(self.OPBG2)
            if i==20:
                self.changeBG=1
                self.BG1.setPixmap(QPixmap(""))
        self.Interpreter.wake()

        #音频控制器-音频启动函数
    def Playsound(self,filename,volume):
        global glo_file,glo_volume
        glo_file=".\\Visual\\source\\BGM\\"+filename+".mp3"
        glo_volume=volume
        if self.music_thread==0:
            self.playsound1=PlaySound()
            self.playsound1.start()
            self.music_thread=2
        elif self.music_thread==1:
            self.playsound2.fade()
            self.playsound1=PlaySound()
            self.playsound1.start()
            self.music_thread=2
        elif self.music_thread==2:
            self.playsound1.fade()
            self.playsound2=PlaySound()
            self.playsound2.start()
            self.music_thread=1

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
        #填充立绘
        if charanum==1:
            for i in charapic:
                if i[0]!="":
                    self.AVG_L.setPixmap(QPixmap(""))
                    self.AVG_R.setPixmap(QPixmap(""))
                    self.AVG_M_R.load("./Visual/source/Chara/"+i[0]+"_"+i[1]+".png")
                    self.AVG_M_R=self.AVG_M_R.scaled(int(self.X*0.46875),int(self.X*0.46875),Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
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
                self.AVG_L_R.load("./Visual/source/Chara/"+charapic[0][0]+"_"+charapic[0][1]+".png")
                self.AVG_L_R=self.AVG_L_R.scaled(int(self.X*0.46875),int(self.X*0.46875),Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
                if self.AVG_L.pixmap()!=self.AVG_L_R:
                    if charapic[0][2]=="0":self.AVG_L.setPixmap(QPixmap(self.AVG_L_R))
                    elif charapic[0][2]=="1":self.AVG_L.setPixmap(QPixmap(self.AVG_L_R.mirrored(True,False)))
                    self.AVG_L.repaint()
            if charapic[1][0]!="":
                self.AVG_R_R.load("./Visual/source/Chara/"+charapic[1][0]+"_"+charapic[1][1]+".png")
                self.AVG_R_R=self.AVG_R_R.scaled(int(self.X*0.46875),int(self.X*0.46875),Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
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
            
        elif i[0]!="" and i[1]!="":#当槽位上有姓名和讲述内容则填充进对应框
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

        self.Free_Label.setGeometry(QRect(int(self.X*eval(textsetlst[0])),int(self.Y*eval(textsetlst[1])),int(self.X*0.6),30))
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

        #向下一个页面（自动模式）
    def ShowNext(self):
        if self.Auto==1:
            self.Interpreter.wake()
        if self.Auto==0:
            self.NextButton.clicked.connect(self.ToNext)
            self.OPNextButton=QGraphicsOpacityEffect()
            self.OPNextButton.setOpacity(1)
            self.NextButton.setGraphicsEffect(self.OPNextButton)

        #向下一个页面（手动模式）
    def ToNext(self):
        self.Interpreter.wake()
        self.NextButton.clicked.disconnect(self.ToNext)
        self.OPNextButton=QGraphicsOpacityEffect()
        self.OPNextButton.setOpacity(0)
        self.NextButton.setGraphicsEffect(self.OPNextButton)

        #退出程序
    def ExitProgram(self):
        qApp=QApplication.instance()
        qApp.quit()