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

#重构-初始页面整体控件
class uFirstPage(QWidget):

    ChooseFileclicked=pyqtSignal()
    ExitProgramclicked=pyqtSignal()
    def __init__(self,X,Y,parent=None):
        super().__init__(parent)
        self.X=X
        self.Y=Y
        self.BackC=QPalette()
        self.BackC.setColor(self.BackC.Background,QColor(0,0,0))
        self.setPalette(self.BackC)
        self.UIModeTextLabel=QLabel(self)
        self.UIModeTextLabel.setGeometry(QRect(int(self.X*0.5208),int(self.Y*0.44),int(self.Y*0.648148),int(self.Y*0.10185185)))
        self.UIModeTextLabel.setAlignment(Qt.AlignCenter)
        self.UIModeTextLabel.setText(msg("UI_Msg_Current_Mode"))
        self.UIModeTextLabel.setStyleSheet("QLabel{color:#FFFFFF;font-size:"+str(int(Y*0.074074))+"px;font-family:'Microsoft YaHei'}")
        self.OPUIModeTextLabel=QGraphicsOpacityEffect()
        self.OPUIModeTextLabel.setOpacity(0)
        self.UIModeTextLabel.setGraphicsEffect(self.OPUIModeTextLabel)

        self.ChooseFileButton=QPushButton(self)#核心启动按钮
        self.ChooseFileButton.setObjectName("ChooseFileButton")
        self.ChooseFileButton.setGeometry(QRect(int(self.X*0.2083),int(self.Y*0.3703),260,260))
        self.QSSChooseFileButton="""
            #ChooseFileButton{
                    background-color:rgba(0,0,0,0);
                    background-image:url('./Visual/source/BaseUI/Button/StartButton_N.png');
            }
            #ChooseFileButton:hover{
                    background-color:rgba(0,0,0,0);
                    background-image:url('./Visual/source/BaseUI/Button/StartButton_P.png');
            }
            #ChooseFileButton:Pressed{
                    background-color:rgba(0,0,0,0);
                    background-image:url('./Visual/source/BaseUI/Button/StartButton_C.png');
            }
            """
        self.ChooseFileButton.setStyleSheet(self.QSSChooseFileButton)
        self.OPChooseFileButton=QGraphicsOpacityEffect()
        self.OPChooseFileButton.setOpacity(0)
        self.ChooseFileButton.setGraphicsEffect(self.OPChooseFileButton)
        

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

        self.ChooseFileButton.clicked.connect(self.chooseFileClicked)
        self.ExitButton.clicked.connect(self.exitProgramClicked)

    def setOpacity(self,opacity_float):
        """
        设置首页的透明度
        setOpacity(self,opacity_float)
        self，透明度数值（0~1）
        ----------
        您可以尝试使用for i in range (1,100)来实现淡入和淡出
            -->您必须在range内对本uFirstPage使用repaint()
        """
        self.OPChooseFileButton.setOpacity(opacity_float)
        self.OPUIModeTextLabel.setOpacity(opacity_float)
        self.OPExitButton.setOpacity(opacity_float)
        self.ChooseFileButton.setGraphicsEffect(self.OPChooseFileButton)
        self.UIModeTextLabel.setGraphicsEffect(self.OPUIModeTextLabel)
        self.ExitButton.setGraphicsEffect(self.OPExitButton)

    def raise_i(self):
        """
        设置对象内各个控件的层级顺序
        raise_i(self)
        self，无其他参数
        ----------
        执行后，退出按钮在最上，文字其次，选择文件按钮在最下
        如果没有遇到层级错误，请不要调用此函数
        """
        self.ChooseFileButton.raise_()
        self.UIModeTextLabel.raise_()
        self.ExitButton.raise_()

    def chooseFileClicked(self):
        """发送选择文件信号"""
        self.ChooseFileclicked.emit()

    def exitProgramClicked(self):
        """退出程序信号"""
        self.ExitProgramclicked.emit()

#重构-标题页面整体控件
class uTitlePage(QWidget):
    """
    标题页面整体控件
    uTitlePage(self,X,Y,SplashList,parent)
    self,屏幕宽，屏幕高，闪烁标语列表，父对象
    ----------
    如有必要，可以传入含有闪烁标语的列表。不使用闪烁标语时请传入空列表
    如果不建立新窗口，请务必不要忘了传入self作为父对象
    """
    def __init__(self,X,Y,SplashList=[],parent=None):
        super().__init__(parent)
        self.X=X
        self.Y=Y
        self.Splashlst=SplashList

        self.Fontsize90=str(int(self.Y*0.083333))+"px"
        self.Fontsize60=str(int(self.Y*0.055555))+"px"
        self.Fontsize45=str(int(self.Y*0.041666))+"px"
        self.Fontsize30=str(int(self.Y*0.027777))+"px"

        #标题背景板
        self.TitleBackGroundLabel=QLabel(self)
        self.TitleBackGroundLabel.setGeometry(QRect(0,0,self.X,self.Y))
        self.OPTitleBackGroundLabel=QGraphicsOpacityEffect()
        self.OPTitleBackGroundLabel.setOpacity(0)
        self.TitleBackGroundLabel.setGraphicsEffect(self.OPTitleBackGroundLabel)
        self.BGRaw=QImage()
        
        #动画遮掩板
        self.BlackHideLabel=QLabel(self)
        self.BlackHideLabel.setGeometry(QRect(0,0,self.X,self.Y))
        self.BlackHide=QImage(self.X,self.Y,QImage.Format_ARGB32)
        self.BlackHide.fill(QColor(0,0,0,255))
        self.BlackHideLabel.setPixmap(QPixmap(self.BlackHide))
        self.OPBlackHideLabel=QGraphicsOpacityEffect()
        self.OPBlackHideLabel.setOpacity(0)
        self.BlackHideLabel.setGraphicsEffect(self.OPBlackHideLabel)

        #派别Logo
        self.Logo=QLabel(self)
        self.Logo.setGeometry(QRect(int(self.X*0.3671875),int(self.Y*0.222222),int(self.Y*0.4722222),int(self.Y*0.4722222)))
        self.LogoRaw=QImage()

        #顶标题
        self.TopTitle=QLabel(self)
        self.TopTitle.setStyleSheet("QLabel{color:#FFFFFF;font-size:"+self.Fontsize45+";font-family:'Microsoft YaHei'}")
        self.TopTitle.setGeometry(QRect(int(self.X*0.333333),int(self.Y*0.30),int(self.X*0.333333),int(self.Y*0.1666666)))
        self.TopTitle.setAlignment(Qt.AlignCenter)
        self.TopTitle.setText("SPOL STORY")
        self.OPTopTitle=QGraphicsOpacityEffect()
        self.OPTopTitle.setOpacity(0)
        self.TopTitle.setGraphicsEffect(self.OPTopTitle)

        #标题
        self.MainTitle=QLabel(self)
        self.MainTitle.setStyleSheet("QLabel{color:#FFFFFF;font-size:"+self.Fontsize90+";font-family:'Microsoft YaHei'}")
        self.MainTitle.setGeometry(QRect(int(self.X*0.333333),int(self.Y*0.40),int(self.X*0.333333),int(self.Y*0.1666666)))
        self.MainTitle.setAlignment(Qt.AlignCenter)
        self.OPMainTitle=QGraphicsOpacityEffect()
        self.OPMainTitle.setOpacity(0)
        self.MainTitle.setGraphicsEffect(self.OPMainTitle)

        #副标题
        self.SubTitle=QLabel(self)
        self.SubTitle.setStyleSheet("QLabel{color:#FFFFFF;font-size:"+self.Fontsize60+";font-family:'Microsoft YaHei'}")
        self.SubTitle.setGeometry(QRect(int(self.X*0.333333),int(self.Y*0.5),int(self.X*0.333333),int(self.Y*0.1666666)))
        self.SubTitle.setAlignment(Qt.AlignCenter)
        self.OPSubTitle=QGraphicsOpacityEffect()
        self.OPSubTitle.setOpacity(0)
        self.SubTitle.setGraphicsEffect(self.OPSubTitle)

        #Splashes文本
        self.Splashes_Label=QLabel(self)
        self.Splashes_Label.setStyleSheet("QLabel{color:#FFFFFF;font-size:"+self.Fontsize30+";font-family:'SimHei';font-weight:bold}")
        self.Splashes_Label.setAlignment(Qt.AlignCenter)
        self.Splashes_Label.setGeometry(QRect(0,self.Y*0.85,self.X,self.Y*0.02777))
        self.OPSplashes_Label=QGraphicsOpacityEffect()
        self.OPSplashes_Label.setOpacity(0)
        self.Splashes_Label.setGraphicsEffect(self.OPSplashes_Label)    

    def setTitleInfo(self,Main_Title,Sub_Title,Background,Logo):
        """
        设置标题内容
        setTitleInfo(self,Main_Title,Sub_Title,Background,Logo)
        self，主标题文字，副标题文字，背景图像名称，Logo图像名称
        ----------
        内部使用路径 ./Visual/source/BGP/+背景图像名称+.png
        以及 ./Visual/source/Logo/+Logo图像名称+.png
        传入的图像名称不要带路径，也不要带后缀
        """
        self.MainTitle.setText(Main_Title)
        self.SubTitle.setText(Sub_Title)
        self.BGRaw.load("./Visual/source/BGP/"+Background+".png")
        self.BGRaw=self.BGRaw.scaled(self.X,self.Y,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
        self.TitleBackGroundLabel.setPixmap(QPixmap(self.BGRaw))
        self.LogoRaw.load("./Visual/source/Logo/"+Logo+".png")
        self.LogoRaw=self.LogoRaw.scaled(int(self.Y*0.4722222),int(self.Y*0.4722222),Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
        self.Logo.setPixmap(QPixmap(self.LogoRaw))
        self.Splashlenth=len(self.Splashlst)
        self.Splashwhich=rnd.randint(0,self.Splashlenth-1)
        self.Splashes_Label.setText(self.Splashlst[self.Splashwhich])

    def showPage(self):
        """
        展示标题页
        showPage(self)
        self，无其他参数
        ----------
        调用此函数来显示标题页面。
        不要尝试直接控制本uTitlePage类整体的Opacity数值，会造成绘制事件阻塞
        """
        self.BLTitleBackGroundLabel=QGraphicsBlurEffect()
        self.BLTitleBackGroundLabel.setBlurRadius(5)
        self.TitleBackGroundLabel.setGraphicsEffect(self.BLTitleBackGroundLabel)

        self.OPTopTitle.setOpacity(1)
        self.TopTitle.setGraphicsEffect(self.OPTopTitle)

        self.OPMainTitle.setOpacity(1)
        self.MainTitle.setGraphicsEffect(self.OPMainTitle)

        self.OPSubTitle.setOpacity(1)
        self.SubTitle.setGraphicsEffect(self.OPSubTitle)

        self.OPSplashes_Label.setOpacity(1)
        self.Splashes_Label.setGraphicsEffect(self.OPSplashes_Label)

        self.OPBlackHideLabel.setOpacity(0)
        self.BlackHideLabel.setGraphicsEffect(self.OPBlackHideLabel)

    def playAnimation(self):
        """
        隐藏背景和闪烁标语
        playAnimation(self)
        self，无其他参数
        ----------
        在合适的时间调用本函数，使标题显示进入下一个状态\n
        !!!请注意，本函数内含耗时操作，执行期间会造成事件阻塞
        """
        self.OPSplashes_Label.setOpacity(0)
        self.Splashes_Label.setGraphicsEffect(self.OPSplashes_Label)
        self.Splashes_Label.repaint()
        self.Splashes_Label.setText("")

        for i in range(0,21):
            self.OPBlackHideLabel.setOpacity(i/20)
            self.BlackHideLabel.setGraphicsEffect(self.OPBlackHideLabel)
            self.BlackHideLabel.repaint()

        self.TitleBackGroundLabel.setPixmap(QPixmap(""))
        self.BlackHideLabel.setPixmap(QPixmap(""))

    def hidePage(self):
        self.OPTitleBackGroundLabel=QGraphicsOpacityEffect()
        self.OPTitleBackGroundLabel.setOpacity(0)
        self.TitleBackGroundLabel.setGraphicsEffect(self.OPTitleBackGroundLabel)

        self.OPTopTitle.setOpacity(0)
        self.TopTitle.setGraphicsEffect(self.OPTopTitle)

        self.OPMainTitle.setOpacity(0)
        self.MainTitle.setGraphicsEffect(self.OPMainTitle)

        self.OPSubTitle.setOpacity(0)
        self.SubTitle.setGraphicsEffect(self.OPSubTitle)

        self.OPSplashes_Label.setOpacity(0)
        self.Splashes_Label.setGraphicsEffect(self.OPSplashes_Label)

        self.OPBlackHideLabel.setOpacity(0)
        self.BlackHideLabel.setGraphicsEffect(self.OPBlackHideLabel)

#重构-播放页面整体控件(不含跳转大板子)
class uPlayerPage(QWidget): 
    UserSpeedSet=pyqtSignal(str)
    UserChooseWhich=pyqtSignal(str)
    NowInBranch=pyqtSignal()
    NeedWakeUp=pyqtSignal()
    NowInLog=pyqtSignal()
    #窗口内容定义
    def __init__(self,X,Y,parent=None,UseLogPage=True):
        super().__init__(parent)
        self.X=X
        self.Y=Y
        self.UseLogPage=UseLogPage
        self.Fontsize90=str(int(self.Y*0.083333))+"px"
        self.Fontsize80=str(int(self.Y*0.074074))+"px"
        self.Fontsize60=str(int(self.Y*0.055555))+"px"
        self.Fontsize45=str(int(self.Y*0.041666))+"px"
        self.Fontsize40=str(int(self.Y*0.037037))+"px"
        self.Fontsize35=str(int(self.Y*0.032407))+"px"
        self.Fontsize30=str(int(self.Y*0.027777))+"px"

        self.BG2=QLabel(self)#交替第二背景
        self.BG1=QLabel(self)#交替第一背景
        
        self.BG2.setGeometry(QRect(0,0,self.X,self.Y))
        self.BG1.setGeometry(QRect(0,0,self.X,self.Y))

        self.OPBG1=QGraphicsOpacityEffect()
        self.OPBG1.setOpacity(0)
        self.BG1.setGraphicsEffect(self.OPBG1)

        #白色闪烁特效层
        self.WhiteFlash=QLabel(self)
        self.WhiteFlashPixmap=QImage(self.X,self.Y,QImage.Format_ARGB32)
        self.WhiteFlashPixmap.fill(QColor(255,255,255,255))
        self.WhiteFlash.setPixmap(QPixmap(self.WhiteFlashPixmap))

        self.OPWhiteFlash=QGraphicsOpacityEffect()
        self.OPWhiteFlash.setOpacity(0)
        self.WhiteFlash.setGraphicsEffect(self.OPWhiteFlash)

        self.AVG_L=QLabel(self)#多人讲述左侧立绘
        self.AVG_M=QLabel(self)#单人讲述居中立绘
        self.AVG_R=QLabel(self)#多人讲述右侧立绘

        self.AVG_L.setGeometry(QRect(int(self.X*-0.068229),int(self.Y*0.12),int(self.X*0.74635),int(self.X*0.75635)))
        self.AVG_M.setGeometry(QRect(int(self.X*0.127083),int(self.Y*0.12),int(self.X*0.74635),int(self.X*0.74635)))
        self.AVG_R.setGeometry(QRect(int(self.X*0.321354),int(self.Y*0.12),int(self.X*0.74635),int(self.X*0.74635)))

        self.Frame=QLabel(self)#渐变遮罩
        self.Frame.setGeometry(0,0,self.X,self.Y)
        self.Frame_R=QImage()
        self.Frame_R.load("./Visual/source/BaseUI/Frame/frame.png")
        self.Frame_R=self.Frame_R.scaled(self.X,self.Y,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
        self.Frame.setPixmap(QPixmap(self.Frame_R))
        self.OPFrame=QGraphicsOpacityEffect()
        self.OPFrame.setOpacity(0)
        self.Frame.setGraphicsEffect(self.OPFrame)

        self.Name_Label=QLabel(self)#姓名
        self.Word_Label=QLabel(self)#讲述内容

        self.Name_Label.setStyleSheet("QLabel{color:#AAAAAA;font-size:"+self.Fontsize45+";font-family:'SimHei';font-weight:bold}")
        self.Name_Label.setAlignment(Qt.AlignRight)
        self.Name_Label.setGeometry(QRect(int(self.X*0.0),int(self.Y*0.86944),int(self.X*0.2078125),int(self.Y*0.042)))

        self.Word_Label.setStyleSheet("QLabel{color:#FFF5F5;font-size:"+self.Fontsize35+";font-family:'SimHei';font-weight:bold}")
        self.Word_Label.setAlignment(Qt.AlignLeft)
        self.Word_Label.setGeometry(QRect(int(self.X*0.2609375),int(self.Y*0.87685),int(self.X*0.6875),int(self.Y*0.105)))

        #如果必要，这是一层用于盖住除了自由文本和按钮之外其他所有部件的灰色层
        self.BlackCover=QLabel(self)
        self.BlackCoverPixmap=QImage(self.X,self.Y,QImage.Format_ARGB32)
        self.BlackCoverPixmap.fill(QColor(0,0,0,128))
        self.BlackCover.setPixmap(QPixmap(self.BlackCoverPixmap))
        self.OPBlackCover=QGraphicsOpacityEffect()
        self.OPBlackCover.setOpacity(0)
        self.BlackCover.setGraphicsEffect(self.OPBlackCover)

        #自由文本
        self.Free_Label=QLabel(self)
        
        self.Free_Label.setStyleSheet("QLabel{color:#FFFFFF;font-size:"+self.Fontsize35+";font-family:'SimHei';font-weight:bold}")
        self.Free_Label.setAlignment(Qt.AlignCenter)
        self.Free_Label.setGeometry(QRect(int(self.X*2),-int(self.Y*0.033),int(self.X*0.75),int(self.Y*0.0324074)))
        self.OPFree_Label=QGraphicsOpacityEffect()
        self.OPFree_Label.setOpacity(0)
        self.Free_Label.setGraphicsEffect(self.OPFree_Label)

        #分支按钮
        self.BranchButton_4=QPushButton(self)#分支按钮1
        self.BranchButton_3=QPushButton(self)#分支按钮2
        self.BranchButton_2=QPushButton(self)#分支按钮3
        self.BranchButton_1=QPushButton(self)#分支按钮4

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

        self.BranchButton_1.setGeometry(QRect(-640,-80,635,70))
        self.BranchButton_2.setGeometry(QRect(-640,-80,635,70))
        self.BranchButton_3.setGeometry(QRect(-640,-80,635,70))
        self.BranchButton_4.setGeometry(QRect(-640,-80,635,70))

        self.BranchButton_1.clicked.connect(self._Chooselabel)
        self.BranchButton_2.clicked.connect(self._Chooselabel)
        self.BranchButton_3.clicked.connect(self._Chooselabel)
        self.BranchButton_4.clicked.connect(self._Chooselabel)

        #先决变换装载图像
        self.BGR=QImage()
        self.AVG_L_R=QImage()
        self.AVG_M_R=QImage()
        self.AVG_R_R=QImage()
       
        #播放控制按钮

        #自动按钮
        self.AutoButton=QPushButton(self)
        self.AutoButton.setObjectName("AutoButton")
        self.AutoButton.setGeometry(QRect(-int(self.X*0.80729),-int(self.Y*0.038),int(self.X*0.098125),int(self.Y*0.046296)))
        self.AutoButton.setText(msg("Ui_AutoButton_Auto"))
        self.AutoButtonTick=0
        self.AutoButton.clicked.connect(self._AutoChange)

        #下一页按钮
        self.NextButton=QPushButton(self)
        self.NextButton.setObjectName("NextButton")
        self.NextButton.setGeometry(QRect(-int(self.X*0.902604),int(self.Y*0.8981),int(self.X*0.078125),int(self.Y*0.046296)))
        self.NextButton.setText(msg("Ui_NextButton"))
        self.NextButton.clicked.connect(self._ToNext)

        #速度按钮
        self.SpeedButton=QPushButton(self)
        self.SpeedButton.setObjectName("SpeedButton")
        self.SpeedButton.setGeometry(QRect(-int(self.X*0.902604),-int(self.Y*0.038),int(self.X*0.078125),int(self.Y*0.046296)))
        self.SpeedButton.setText("1.0x")
        self.SpeedButton.clicked.connect(self._SpeedChange)

        self.QSSNSButton="""
        QPushButton{
        background-color:rgba(0,0,0,0);
        color:#FFFFFF;
        font-family:'SimHei';
        font-size:"""+self.Fontsize40+""";
        font-weight:bold;
        text-align:left;
        }
        """
        self.AutoButton.setStyleSheet(self.QSSNSButton)
        self.NextButton.setStyleSheet(self.QSSNSButton)
 
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

        if self.UseLogPage==True:
            self.LogPage=uScrollPage(self.X,self.Y,self)
            self.LogPage.setGeometry(QRect(-self.X,self.Y,self.X,self.Y))
            self.LogPage.JumpEmitButton.clicked.connect(self.showLogPage)

        #自选进度按钮
        self.LogButton=QPushButton(self)
        self.LogButtonPixRaw=QPixmap(".\\Visual\\source\\BaseUI\\Button\\LogButton_N.png")
        self.LogButtonPixRaw=self.LogButtonPixRaw.scaled(int(self.Y*0.055),int(self.Y*0.055),Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
        self.LogButton.setIcon(QIcon(self.LogButtonPixRaw))
        self.LogButton.setIconSize(QSize(int(self.Y*0.055),int(self.Y*0.055)))
        self.LogButton.setGeometry(QRect(-int(self.X*0.030416),int(self.Y*0.033),int(self.Y*0.055),int(self.Y*0.055)))
        self.LogButton.setStyleSheet("QPushButton{background-color:rgba(0,0,0,0);}")
        self.LogButton.clicked.connect(self.showLogPage)
        
    #播放前调用以初始化数值
    def initObject(self):
        self.changeBG=1
        self.SpeedNow=0
        self.Speedfloat=1.0
        self.Inbranch=0
        self.InLogPage=0
        self.Auto=1
        self.AutoButtonTick=0
        self.UserSpeedSet.emit("1")
        self.SpeedButton.setText("1.0x")
        
        if self.UseLogPage==True:
            self.LogPage.initObject()

    #查询需要的内部数值
    def searchParameter(self,Parametername):
        if Parametername=="Auto":
            return self.Auto
        elif Parametername=="Inbranch":
            return self.Inbranch
        elif Parametername=="InLogPage":
            return self.InLogPage
        else:
            return -1

    #自动按钮文字切换
    def _AutoChange(self):
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

    #供程序刻刷新自动按钮的动画
    def repaintAutoButton(self):
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
    
    #速度按钮文字切换
    def _SpeedChange(self):
        global Speednum
        self.SpeedNow+=1
        if self.SpeedNow%4==1:
            self.UserSpeedSet.emit("0.666")
            self.SpeedButton.setText("1.5x")
            self.Speedfloat=0.666
            Speednum=0.666
        elif self.SpeedNow%4==2:
            self.UserSpeedSet.emit("0.5")
            self.SpeedButton.setText("2.0x")
            self.Speedfloat=0.5
            Speednum=0.5
        elif self.SpeedNow%4==3:
            self.UserSpeedSet.emit("2")
            self.SpeedButton.setText("0.5x")
            self.Speedfloat=2
            Speednum=2
        elif self.SpeedNow%4==0:
            self.UserSpeedSet.emit("1")
            self.SpeedButton.setText("1.0x")
            self.Speedfloat=1.0
            Speednum=1.0

        self.SpeedButton.repaint()

    #用户设置分支按钮
    def setBranchButton(self,BranchList):
        self.Inbranch=1
        self.NowInBranch.emit()
        self.converlstlen=len(BranchList)

        if self.converlstlen>0:
            self.BranchButton_1.setText(BranchList[0].split(":")[1])
        if self.converlstlen>1:
            self.BranchButton_2.setText(BranchList[1].split(":")[1])
        if self.converlstlen>2:
            self.BranchButton_3.setText(BranchList[2].split(":")[1])
        if self.converlstlen>3:
            self.BranchButton_4.setText(BranchList[3].split(":")[1])

        if self.converlstlen==1:
            self.BranchButton_1.setGeometry(QRect(int(self.X/2-317.5),int(self.Y*0.402777),635,70))

        if self.converlstlen==2:
            self.BranchButton_1.setGeometry(QRect(int(self.X/2-317.5),int(self.Y*0.337962963),635,70))
            self.BranchButton_2.setGeometry(QRect(int(self.X/2-317.5),int(self.Y*0.435185),635,70))

        if self.converlstlen==3:
            self.BranchButton_1.setGeometry(QRect(int(self.X/2-317.5),int(self.Y*0.273148),635,70))
            self.BranchButton_2.setGeometry(QRect(int(self.X/2-317.5),int(self.Y*0.37037037),635,70))
            self.BranchButton_3.setGeometry(QRect(int(self.X/2-317.5),int(self.Y*0.46759),635,70))

        if self.converlstlen==4:
            self.BranchButton_1.setGeometry(QRect(int(self.X/2-317.5),int(self.Y*0.2574074),635,70))
            self.BranchButton_2.setGeometry(QRect(int(self.X/2-317.5),int(self.Y*0.3546296),635,70))
            self.BranchButton_3.setGeometry(QRect(int(self.X/2-317.5),int(self.Y*0.45185185),635,70))
            self.BranchButton_4.setGeometry(QRect(int(self.X/2-317.5),int(self.Y*0.549074),635,70))

    #发送选择信号
    def _Chooselabel(self):
        self.WhichButtonSend=self.sender()
        self.UserChooseWhich.emit(self.WhichButtonSend.text())

        self.BranchButton_1.setGeometry(QRect(-640,-80,635,70))
        self.BranchButton_2.setGeometry(QRect(-640,-80,635,70))
        self.BranchButton_3.setGeometry(QRect(-640,-80,635,70))
        self.BranchButton_4.setGeometry(QRect(-640,-80,635,70))

        self.BranchButton_1.setText("")
        self.BranchButton_2.setText("")
        self.BranchButton_3.setText("")
        self.BranchButton_4.setText("")

        self.Inbranch=0
        self.showNext()

    #用户要求展示页面
    def showPlayerPage(self):
        self.AutoButton.setGeometry(QRect(int(self.X*0.80729),int(self.Y*0.038),int(self.X*0.098125),int(self.Y*0.046296)))
        self.SpeedButton.setGeometry(QRect(int(self.X*0.902604),int(self.Y*0.038),int(self.X*0.078125),int(self.Y*0.046296)))
        if self.UseLogPage==True:
            self.LogButton.setGeometry(QRect(int(self.X*0.030416),int(self.Y*0.033),int(self.Y*0.055),int(self.Y*0.055)))

    #用户设置当前页立绘信息
    def setCurrentAvg(self,CharaPicList,Charanum,BGBlack):
        #刷新框架透明度。如果框架透明那么顺便清理掉其他内容。
        if BGBlack==1:
            self.OPFrame.setOpacity(1)
            self.Frame.setGraphicsEffect(self.OPFrame)
        elif BGBlack==0:
            self.OPFrame.setOpacity(0)
            self.Frame.setGraphicsEffect(self.OPFrame)
            self.Name_Label.setText("")
            self.Word_Label.setText("")
            self.AVG_L.setPixmap(QPixmap(""))
            self.AVG_M.setPixmap(QPixmap(""))
            self.AVG_R.setPixmap(QPixmap(""))

        if Charanum==1:
            for i in CharaPicList:
                if i[0]=="":
                    self.AVG_L.setPixmap(QPixmap(""))
                    self.AVG_R.setPixmap(QPixmap(""))
                    self.AVG_M.setPixmap(QPixmap(""))
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
        elif Charanum==2:
            self.AVG_M.setPixmap(QPixmap(""))
            if CharaPicList[0][0]!="":
                if CharaPicList[0][6]=="(暗，沉默)":
                    self.AVG_L_R.load("./Visual/cache/Chara/"+CharaPicList[0][0]+"_"+CharaPicList[0][1]+"_"+CharaPicList[0][3]+"-Dark.png")
                elif CharaPicList[0][3]!="0":
                    self.AVG_L_R.load("./Visual/cache/Chara/"+CharaPicList[0][0]+"_"+CharaPicList[0][1]+"_"+CharaPicList[0][3]+".png")
                else:
                    self.AVG_L_R.load("./Visual/source/Chara/"+CharaPicList[0][0]+"_"+CharaPicList[0][1]+".png")
                self.AVG_L_R=self.AVG_L_R.scaled(int(self.X*0.74635),int(self.X*0.74635),Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
                if self.AVG_L.pixmap()!=self.AVG_L_R:
                    if CharaPicList[0][2]=="0":self.AVG_L.setPixmap(QPixmap(self.AVG_L_R))
                    elif CharaPicList[0][2]=="1":self.AVG_L.setPixmap(QPixmap(self.AVG_L_R.mirrored(True,False)))
            if CharaPicList[1][0]!="":
                if CharaPicList[1][6]=="(暗，沉默)":
                    self.AVG_R_R.load("./Visual/cache/Chara/"+CharaPicList[1][0]+"_"+CharaPicList[1][1]+"_"+CharaPicList[1][3]+"-Dark.png")
                elif CharaPicList[1][3]!="0":
                    self.AVG_R_R.load("./Visual/cache/Chara/"+CharaPicList[1][0]+"_"+CharaPicList[1][1]+"_"+CharaPicList[1][3]+".png")
                else:
                    self.AVG_R_R.load("./Visual/source/Chara/"+CharaPicList[1][0]+"_"+CharaPicList[1][1]+".png")
                self.AVG_R_R=self.AVG_R_R.scaled(int(self.X*0.74635),int(self.X*0.74635),Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
                if self.AVG_R.pixmap()!=self.AVG_R_R:
                    if CharaPicList[1][2]=="0":self.AVG_R.setPixmap(QPixmap(self.AVG_R_R))
                    elif CharaPicList[1][2]=="1":self.AVG_R.setPixmap(QPixmap(self.AVG_R_R.mirrored(True,False)))

    #用户要求更新姓名和讲述文本
    def updateCurrentWords(self,i_List,WordsCurrent,Charanum,Wordset):
        if i_List[0]=="" and Charanum==1:
            self.Name_Label.setText("")
            self.Word_Label.setText(WordsCurrent)
          
        elif i_List[1]=="" and Charanum==1:
            self.Name_Label.setText(i_List[0])
            self.Word_Label.setText("")

        elif (i_List[0]!="" and i_List[1]!="") or (i_List[0]!="" and Charanum==1):
            self.Name_Last=self.Name_Label.text()
            if self.Name_Last!= i_List[0]:
                self.Name_Label.setText(i_List[0])
            self.Word_Label.setText(WordsCurrent)

    #用户设置当前页面背景信息
    def setCurrentBGP(self,BGPSetList):
        if BGPSetList[0]=="黑场":
            self.BGR=QImage(self.X,self.Y,QImage.Format_ARGB32)
            self.BGR.fill(QColor(0,0,0,255))
        else:
            if BGPSetList[1]=="0":
                self.BGR=QImage()
                self.BGR.load("./Visual/source/BGP/"+BGPSetList[0]+".png")
                self.BGR=self.BGR.scaled(self.X,self.Y,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
            elif BGPSetList[1]=="1":
                self.BGR=QImage()
                self.BGR.load("./Visual/cache/BGP/"+BGPSetList[0]+"-Dark.png")
                self.BGR=self.BGR.scaled(self.X,self.Y,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
            elif BGPSetList[1]=="2":
                self.BGR=QImage()
                self.BGR.load("./Visual/cache/BGP/"+BGPSetList[0]+"-Fade.png")
                self.BGR=self.BGR.scaled(self.X,self.Y,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
            elif BGPSetList[1]=="3":
                self.BGR=QImage()
                self.BGR.load("./Visual/cache/BGP/"+BGPSetList[0]+"-Fade-Dark.png")
                self.BGR=self.BGR.scaled(self.X,self.Y,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
            elif BGPSetList[1]=="4":
                self.BGR=QImage()
                self.BGR.load("./Visual/cache/BGP/"+BGPSetList[0]+"-BAW.png")
                self.BGR=self.BGR.scaled(self.X,self.Y,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
            elif BGPSetList[1]=="5":
                self.BGR=QImage()
                self.BGR.load("./Visual/cache/BGP/"+BGPSetList[0]+"-BAW-Dark.png")
                self.BGR=self.BGR.scaled(self.X,self.Y,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)

    #用户要求播放背景对应动画
    def updateCurrentBGP(self,Opacity_Float,BGSetList):
        if self.changeBG==1:
            if Opacity_Float==0:
                self.BG1.setPixmap(QPixmap(self.BGR))
                self.OPBG1.setOpacity(0)
                self.BG1.setGraphicsEffect(self.OPBG1)
            elif Opacity_Float!=0 and Opacity_Float!=1:
                self.OPBG1.setOpacity(Opacity_Float)
                self.BG1.setGraphicsEffect(self.OPBG1)
            elif Opacity_Float>=1:
                self.OPBG1.setOpacity(1)
                self.BG1.setGraphicsEffect(self.OPBG1)
                self.changeBG=2

                if BGSetList[2]=="1":
                    self.ShakeFUNC=ShakeFunc(self.Speedfloat)
                    self.ShakeFUNC.shakeXY.connect(self._ShakeRect)
                    self.ShakeFUNC.start()
                elif BGSetList[2]=="2":
                    self.effectuse=2
                    self.FlashFUNCFast=FlashFuncFast(self.Speedfloat)
                    self.FlashFUNCFast.FlashOPint.connect(self._Flashwhite)
                    self.FlashFUNCFast.start()
                elif BGSetList[2]=="3":
                    self.effectuse=3
                    self.FlashFUNCSlow=FlashFuncSlow(self.Speedfloat)
                    self.FlashFUNCSlow.FlashOPint.connect(self._Flashwhite)
                    self.FlashFUNCSlow.start()
                else:
                    self.showNext()

        elif self.changeBG==2:
            if Opacity_Float==0:
                self.BG2.setPixmap(QPixmap(self.BGR))
                self.OPBG1.setOpacity(1)
                self.BG1.setGraphicsEffect(self.OPBG1)
            elif Opacity_Float!=0 and Opacity_Float!=1:
                self.OPBG1.setOpacity(1-Opacity_Float)
                self.BG1.setGraphicsEffect(self.OPBG1)
            elif Opacity_Float>=1:
                self.OPBG1.setOpacity(0)
                self.BG1.setGraphicsEffect(self.OPBG1)
                self.changeBG=1

                if BGSetList[2]=="1":
                    self.ShakeFUNC=ShakeFunc(self.Speedfloat)
                    self.ShakeFUNC.shakeXY.connect(self._ShakeRect)
                    self.ShakeFUNC.start()
                elif BGSetList[2]=="2":
                    self.effectuse=2
                    self.FlashFUNCFast=FlashFuncFast(self.Speedfloat)
                    self.FlashFUNCFast.FlashOPint.connect(self._Flashwhite)
                    self.FlashFUNCFast.start()
                elif BGSetList[2]=="3":
                    self.effectuse=3
                    self.FlashFUNCSlow=FlashFuncSlow(self.Speedfloat)
                    self.FlashFUNCSlow.FlashOPint.connect(self._Flashwhite)
                    self.FlashFUNCSlow.start()
                else:
                    self.showNext()

    #背景晃动
    def _ShakeRect(self,sX,sY,end):
        if self.changeBG==2:
            self.BG1.setGeometry(QRect(int((self.Y/1080)*sX),int((self.Y/1080)*sY),self.X,self.Y))
            self.BG1.repaint()
        elif self.changeBG==1:
            self.BG2.setGeometry(QRect(int((self.Y/1080)*sX),int((self.Y/1080)*sY),self.X,self.Y))
            self.BG2.repaint()
        if end==1:
            self.ShakeFUNC.wait()
            del self.ShakeFUNC
            self.showNext()

    #白色闪烁
    def _Flashwhite(self,i,end):
        if end == 0:
            self.OPWhiteFlash.setOpacity(0)
            self.WhiteFlash.setGraphicsEffect(self.OPWhiteFlash)
        elif end==1:
            self.OPWhiteFlash.setOpacity(i)
            self.WhiteFlash.setGraphicsEffect(self.OPWhiteFlash)
            self.WhiteFlash.repaint()
        elif end==2:
            self.OPWhiteFlash.setOpacity(0)
            self.WhiteFlash.setGraphicsEffect(self.OPWhiteFlash)
            if self.effectuse==2:
                self.FlashFUNCFast.wait()
                del self.FlashFUNCFast
                self.effectuse=0
            elif self.effectuse==3:
                self.FlashFUNCSlow.wait()
                del self.FlashFUNCSlow
                self.effectuse=0
            self.showNext()

    #用户设置自由文本
    def setCurrentFree(self,textsetlst,wordset):
        
        self.Free_Label.setText("")

        self.OPFree_Label.setOpacity(0)
        self.Free_Label.setGraphicsEffect(self.OPFree_Label)

        self.Free_Label.setGeometry(QRect(int(self.X*float(textsetlst[0])),int(self.Y*float(textsetlst[1])),int(self.X*0.75),int(self.Y*0.0324074)))
        if textsetlst[2]=="L":
            self.Free_Label.setAlignment(Qt.AlignLeft)
        elif textsetlst[2]=="M":
            self.Free_Label.setAlignment(Qt.AlignCenter)
        elif textsetlst[2]=="R":
            self.Free_Label.setAlignment(Qt.AlignRight)
        
        self.OPFree_Label.setOpacity(1)
        self.Free_Label.setGraphicsEffect(self.OPFree_Label)

    #用户要求更新自由文本
    def updateCurrentFree(self,Words):
        self.Free_Label.setText(Words)
        self.Free_Label.repaint()

    #用户需调用以清除自由文本
    def clearCurrentFree(self,end):
        
        self.Free_Label.setText("")
        self.OPFree_Label.setOpacity(0)
        self.Free_Label.setGraphicsEffect(self.OPFree_Label)

        None

    #用户需在播放完毕后调用以清除所有内容
    def clearAll(self):
        self.Name_Label.setText("")
        self.Word_Label.setText("")
        self.Free_Label.setText("")
        self.AVG_L.setPixmap(QPixmap())
        self.AVG_M.setPixmap(QPixmap())
        self.AVG_R.setPixmap(QPixmap())
        self.BG1.setPixmap(QPixmap())
        self.BG2.setPixmap(QPixmap())
        
        self.AutoButton.setGeometry(QRect(-int(self.X*0.80729),-int(self.Y*0.038),int(self.X*0.098125),int(self.Y*0.046296)))
        self.SpeedButton.setGeometry(QRect(-int(self.X*0.902604),-int(self.Y*0.038),int(self.X*0.078125),int(self.Y*0.046296)))
        self.NextButton.setGeometry(QRect(-int(self.X*0.902604),int(self.Y*0.8981),int(self.X*0.078125),int(self.Y*0.046296)))
        if self.UseLogPage==True:
            self.LogButton.setGeometry(QRect(-int(self.X*0.030416),int(self.Y*0.033),int(self.Y*0.055),int(self.Y*0.055)))

    #向下一个页面（自动模式）
    def showNext(self):
        if self.Auto==1:
            self.NeedWakeUp.emit()
        if self.Auto==0:
            self.NextButton.setGeometry(QRect(int(self.X*0.902604),int(self.Y*0.8981),int(self.X*0.078125),int(self.Y*0.046296)))

        #向下一个页面（手动模式）
    def _ToNext(self):
        self.NeedWakeUp.emit()
        self.NextButton.setGeometry(QRect(-int(self.X*0.902604),-int(self.Y*0.8981),int(self.X*0.078125),int(self.Y*0.046296)))

        #展示剧情跳转页面
    def showLogPage(self):
        if self.InLogPage==0:
            self.NowInLog.emit()
            if self.Auto==1:
                self._AutoChange()
            self.LogPage.setGeometry(QRect(0,0,self.X,self.Y))
            self.InLogPage=1
        elif self.InLogPage==1:
            if self.Auto==0:
                self._AutoChange()
            if self.NextButton.geometry()==QRect(int(self.X*0.902604),int(self.Y*0.8981),int(self.X*0.078125),int(self.Y*0.046296)):
                self._ToNext()
            self.LogPage.setGeometry(QRect(-self.X,-self.Y,self.X,self.Y))
            self.InLogPage=0

    def wheelEvent(self, event): 
        if self.InLogPage==1:
            self.LogPage.StoryScroll.setValue(self.LogPage.StoryScroll.value()-int(event.angleDelta().y()/120))

#重构-剧情跳转页面整体控件（跳转大板子）
class uScrollPage(QWidget):
    EmitJumpLine=pyqtSignal(int)
    def __init__(self,X,Y,parent=None):
        super().__init__(parent)
        self.X=X
        self.Y=Y
        self.Fontsize60=str(int(self.Y*0.055555))+"px"
        self.Fontsize40=str(int(self.Y*0.037037))+"px"
        self.Fontsize30=str(int(self.Y*0.027777))+"px"

        #背景板板
        self.BlackCover=QLabel(self)
        self.BlackCoverPixmap=QImage(self.X,self.Y,QImage.Format_ARGB32)
        self.BlackCoverPixmap.fill(QColor(0,0,0,128))
        self.BlackCover.setPixmap(QPixmap(self.BlackCoverPixmap))

        self.StoryBigPad=QLabel(self)
        self.StoryBigPad.setText("")
        self.StoryBigPad.setAlignment(Qt.AlignLeft)
        self.StoryBigPad.setGeometry(QRect(int(self.X*0.05),int(self.Y*0),int(self.X*0.9),int(self.Y*1)))
        self.StoryBigPad.setStyleSheet("QLabel{color:#FFFFFF;font-size:"+self.Fontsize30+";font-family:'SimHei';}")

        self.StoryLineNum=QLabel(self)
        self.StoryLineNum.setAlignment(Qt.AlignCenter)
        self.StoryLineNum.setGeometry(QRect(int(self.X*0.027),int(self.Y*0.3),int(self.X*0.07),int(self.Y*0.11111)))
        self.StoryLineNum.setText(msg("Ui_Current_Line")+"\n"+"0")
        self.StoryLineNum.setStyleSheet("QLabel{color:#DDDDDD;font-size:"+self.Fontsize60+";font-family:'SimHei'}")

        self.ToLineNum=QLabel(self)
        self.ToLineNum.setAlignment(Qt.AlignCenter)
        self.ToLineNum.setGeometry(QRect(int(self.X*0.027),int(self.Y*0.6),int(self.X*0.07),int(self.Y*0.11111)))
        self.ToLineNum.setText(msg("Ui_To_Which_Line")+"\n"+"0")
        self.ToLineNum.setStyleSheet("QLabel{color:#DDDDDD;font-size:"+self.Fontsize60+";font-family:'SimHei'}")

        self.JumpEmitButton=QPushButton(self)
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
        self.JumpEmitButton.clicked.connect(self.EmitLineNum)

        self.StoryScroll=QScrollBar(Qt.Vertical,self)
        self.StoryScroll.setGeometry(QRect(int(self.X*0.983),int(self.Y*0),int(self.X*0.015),int(self.Y)))
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

        self.SaveLineList=[]
        self.LineListForDisplay=""

    def initObject(self):
        self.SaveLineList=[]
        self.LineListForDisplay=""

    def setLineList(self,StoryLine):
        self.SaveLineList+=[StoryLine]

    def setScroll(self):
        self.StoryScroll.setMinimum(0)
        self.StoryScroll.setMaximum(len(self.SaveLineList)-1)
        self.StoryScroll.setSingleStep(1)

        for i in self.SaveLineList:
            self.LineListForDisplay+=str(self.SaveLineList.index(i))+"\t"+i[1]+"\n\n"

        self.StoryBigPad.setText(self.LineListForDisplay)
        self.StoryBigPad.setGeometry(QRect(self.X*0.12,self.Y*0.675,self.X*0.8,int(len(self.SaveLineList)*(self.Y*0.06111111))))
        self.StoryScroll.valueChanged.connect(self.MoveBigPad)

    #设置移动大剧情板的动画和跳转数值
    def MoveBigPad(self):
        self.StoryBigPad.setGeometry(QRect(self.X*0.12,self.Y*0.675-self.StoryScroll.value()*(self.Y*0.06111111),self.X*0.8,int(len(self.SaveLineList)*(self.Y*0.06111111))))
        self.ToLineNum.setText(msg("Ui_To_Which_Line")+"\n"+str(self.StoryScroll.value()))

        #当前行数值动画
    def updatelinenum(self,lineinfo):
        for i in range(0,len(self.SaveLineList)):
            if lineinfo==self.SaveLineList[i][0]:
                self.StoryLineNum.setText(msg("Ui_Current_Line")+"\n"+str(i+1))
                self.StoryScroll.setValue(i+1)

#发送跳转选择
    def EmitLineNum(self):
        self.EmitJumpLine.emit(self.SaveLineList[self.StoryScroll.value()][0]-2)

#重构-音频放送服务
class uSoundService(QObject):
    def __init__(self,parent=None):
        super().__init__(parent)
     
    #装载文件
    def loadfile(self,Filename,Volume):
        try:
            del self.MediaPlayer
        except:
            None
        else:
            None
        self.MediaPlayer=QMediaPlayer()
        self.Filename=QMediaContent(QUrl.fromLocalFile(Filename))
        self.MediaPlayer.setMedia(self.Filename)
        self.Volume=Volume
        self.MediaPlayer.setVolume(Volume)

    #播放
    def playMedia(self):
        self.MediaPlayer.play()

    #停止
    def fadeMedia(self):
        for i in range(self.Volume,0,-1):
            self.MediaPlayer.setVolume(i)
            self.Volume-=1
            tm.sleep(0.01)
        self.MediaPlayer.stop()
