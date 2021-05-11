#我本想把实现显示和控件定义的相关东西分离，但是现在看来似乎不太可能。
#也就是说这个ArtificialUI会不可避免的很大

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from command.UICoreLauncher import *
from core.core0_4_1_U import *
from langcontrol import *
import time as tm
import sys
from Visual.effect import *
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore")
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore\Visual")

class STORYNAME(QObject):
    StoryNameEmit=pyqtSignal(str)
    def __init__(self):
        super(STORYNAME,self).__init__()

class USERCHOOSEBRANCH(QObject):
    UserChooseWhich=pyqtSignal(str)
    def __init__(self):
        super(USERCHOOSEBRANCH,self).__init__()

class ArtificialUI(QWidget):
    def __init__(self):
        super().__init__()

        self.Spawn=SPAWN()
        self.StoryName=STORYNAME()
        self.StoryNameRecive=STORYNAMERECIVE()
        self.UserChooseBranch=USERCHOOSEBRANCH()
        self.UserChooseBranchRecive=USERCHOOSEBRANCHRECIVE()
        #背景定义为黑色
        BackC=QPalette()
        BackC.setColor(BackC.Background,QColor(0,0,0))
        self.setPalette(BackC)

        #引入操作
        self.FUNC=Function()
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
        self.changeBG=1#背景交替数

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

        #姓名和讲述内容文本框的样式定义
        self.Name_Label.setStyleSheet("QLabel{color:#FFFFFF;font-size:30px;}")
        self.Name_Label.setAlignment(Qt.AlignRight)
        self.Word_Label.setStyleSheet("QLabel{color:#AAAAAA;font-size:30px;}")
        self.Word_Label.setAlignment(Qt.AlignLeft)

        #标题和副标题的格式定义
        self.MainTitle.setStyleSheet("QLabel{color:#FFFFFF;font-size:90px;font-family:'Microsoft YaHei'}")
        self.MainTitle.setAlignment(Qt.AlignCenter)

        self.SubTitle.setStyleSheet("QLabel{color:#FFFFFF;font-size:60px;font-family:'Microsoft YaHei'}")
        self.SubTitle.setAlignment(Qt.AlignCenter)

        #标题和副标题测试
        #self.MainTitle.setText("AA-TS-07-4R")
        #self.SubTitle.setText("副标题测试")
        #self.BG1.setPixmap(QPixmap("./Visual/source/BGP/洛天依家走廊.png"))

        #背景控件位置设置
        self.BG1.setGeometry(QRect(0,0,1920,1080))
        self.BG2.setGeometry(QRect(0,0,1920,1080))

        #测试背景变化的两个按钮的位置和文本信息
        #self.TestButtonIN.setGeometry(QRect(120,10,93,28))
        #self.TestButtonOut.setGeometry(QRect(230,10,93,28))
        #self.TestButtonIN.setText("显示图片")
        #self.TestButtonOut.setText("隐藏图片")

        #启动核心的按钮的位置和文本信息
        self.Run.setGeometry(QRect(400,400,260,260))
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

        self.Hellotext.setGeometry(QRect(1000,500,700,80))
        self.Hellotext.setText("YSP UI Mode")
        self.Hellotext.setStyleSheet("QLabel{color:#FFFFFF;font-size:80px;font-family:'Microsoft YaHei'}")

        #分支按钮的背景图片定义
        self.BranchButton_1.setObjectName("Branchbutton")
        self.BranchButton_2.setObjectName("Branchbutton")
        self.BranchButton_3.setObjectName("Branchbutton")
        self.BranchButton_4.setObjectName("Branchbutton")
        self.QSSBranchButton="""
        #Branchbutton{
        color:#FFFFFF;
        font-size:30px;
        font-family:'Microsoft YaHei';
        background-color:rgba(0,0,0,0);
        background-image:url('./Visual/source/BaseUI/Button/BranchButton_N.png');
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
        self.Frame.setPixmap(QPixmap("./Visual/source/BaseUI/Frame/frame.png"))

        #控件位置
        self.Name_Label.setGeometry(QRect(220,960,300,30))
        self.Word_Label.setGeometry(QRect(620,960,1080,90))
        self.AVG_L.setGeometry(QRect(90,220,900,900))
        self.AVG_M.setGeometry(QRect(443,220,900,900))
        self.AVG_R.setGeometry(QRect(796,220,900,900))
        self.MainTitle.setGeometry(QRect(640,360,640,180))
        self.SubTitle.setGeometry(QRect(640,540,640,180))
        self.Logo.setGeometry(QRect(705,240,510,510))

        #控件遮挡关系-默认情况
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

        #开始页面透明度初始化
        self.OPRun=QGraphicsOpacityEffect()
        self.OPRun.setOpacity(1)
        self.Run.setGraphicsEffect(self.OPRun)

        self.OPHellotext=QGraphicsOpacityEffect()
        self.OPHellotext.setOpacity(1)
        self.Hellotext.setGraphicsEffect(self.OPHellotext)

        #按钮信号和槽函数连接
        self.Run.clicked.connect(self.RUNCORE)
        
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
        #测试灰暗效果
        #self.Dark=QGraphicsColorizeEffect()
        #self.Dark.setColor(QColor(0,0,0,10))
        #self.AVG_R.setGraphicsEffect(self.Dark)

        #核心启动函数
    def RUNCORE(self):
        self.ChooseStory = QFileDialog.getOpenFileName(self,msg("Choose_File"), "./Story","StoryFile(*.spol)")
        Storyname=self.ChooseStory[0]
        
        self.Interpreter=SPAWN()
        self.Interpreter.can_update_chara.connect(self.setprintchara)
        self.Interpreter.can_update_bg.connect(self.setprintbg)
        self.Interpreter.can_hide_hello.connect(self.hidehello)
        self.Interpreter.can_reprint_hello.connect(self.reprinthello)
        self.Interpreter.can_show_title.connect(self.showtitle)
        self.Interpreter.need_to_choose.connect(self.choosebranch)
        self.UserChooseBranch.UserChooseWhich.connect(self.UserChooseBranchRecive.get)

        self.StoryName.StoryNameEmit.connect(self.StoryNameRecive.get)
        self.StoryName.StoryNameEmit.emit(Storyname)
        self.Interpreter.start()

        #分支选择函数
    def choosebranch(self,converlst):
        self.converlstlen=len(converlst)

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
        self.BranchButton_1.raise_()
        self.BranchButton_2.raise_()
        self.BranchButton_3.raise_()
        self.BranchButton_4.raise_()

        if self.converlstlen==1:
            self.BranchButton_1.setText(converlst[0].split(":")[1])
        if self.converlstlen==2:
            self.BranchButton_1.setText(converlst[0].split(":")[1])
            self.BranchButton_2.setText(converlst[1].split(":")[1])
        if self.converlstlen==3:
            self.BranchButton_1.setText(converlst[0].split(":")[1])
            self.BranchButton_2.setText(converlst[1].split(":")[1])
            self.BranchButton_3.setText(converlst[2].split(":")[1])
        if self.converlstlen==4:
            self.BranchButton_1.setText(converlst[0].split(":")[1])
            self.BranchButton_2.setText(converlst[1].split(":")[1])
            self.BranchButton_3.setText(converlst[2].split(":")[1])
            self.BranchButton_4.setText(converlst[3].split(":")[1])

        if self.converlstlen==1:
            self.BranchButton_1.setGeometry(QRect(640,435,635,70))
            self.OPBranchButton_1=QGraphicsOpacityEffect()
            self.OPBranchButton_1.setOpacity(1)
            self.BranchButton_1.setGraphicsEffect(self.OPBranchButton_1)
            self.BranchButton_1.clicked.connect(self.Chooselabel)

            self.BranchButton_1.repaint()
        if self.converlstlen==2:
            self.BranchButton_1.setGeometry(QRect(640,365,635,70))
            self.OPBranchButton_1=QGraphicsOpacityEffect()
            self.OPBranchButton_1.setOpacity(1)
            self.BranchButton_1.setGraphicsEffect(self.OPBranchButton_1)
            self.BranchButton_1.clicked.connect(self.Chooselabel)

            self.BranchButton_2.setGeometry(QRect(640,470,635,70))
            self.OPBranchButton_2=QGraphicsOpacityEffect()
            self.OPBranchButton_2.setOpacity(1)
            self.BranchButton_2.setGraphicsEffect(self.OPBranchButton_2)
            self.BranchButton_2.clicked.connect(self.Chooselabel)

            self.BranchButton_1.repaint()
            self.BranchButton_2.repaint()
        if self.converlstlen==3:
            self.BranchButton_1.setGeometry(QRect(640,295,635,70))
            self.OPBranchButton_1=QGraphicsOpacityEffect()
            self.OPBranchButton_1.setOpacity(1)
            self.BranchButton_1.setGraphicsEffect(self.OPBranchButton_1)
            self.BranchButton_1.clicked.connect(self.Chooselabel)

            self.BranchButton_2.setGeometry(QRect(640,400,635,70))
            self.OPBranchButton_2=QGraphicsOpacityEffect()
            self.OPBranchButton_2.setOpacity(1)
            self.BranchButton_2.setGraphicsEffect(self.OPBranchButton_2)
            self.BranchButton_2.clicked.connect(self.Chooselabel)

            self.BranchButton_3.setGeometry(QRect(640,505,635,70))
            self.OPBranchButton_3=QGraphicsOpacityEffect()
            self.OPBranchButton_3.setOpacity(1)
            self.BranchButton_3.setGraphicsEffect(self.OPBranchButton_3)
            self.BranchButton_3.clicked.connect(self.Chooselabel)

            self.BranchButton_1.repaint()
            self.BranchButton_2.repaint()
            self.BranchButton_3.repaint()
        if self.converlstlen==4:
            self.BranchButton_1.setGeometry(QRect(640,278,635,70))
            self.OPBranchButton_1=QGraphicsOpacityEffect()
            self.OPBranchButton_1.setOpacity(1)
            self.BranchButton_1.setGraphicsEffect(self.OPBranchButton_1)
            self.BranchButton_1.clicked.connect(self.Chooselabel)

            self.BranchButton_2.setGeometry(QRect(640,383,635,70))
            self.OPBranchButton_2=QGraphicsOpacityEffect()
            self.OPBranchButton_2.setOpacity(1)
            self.BranchButton_2.setGraphicsEffect(self.OPBranchButton_2)
            self.BranchButton_2.clicked.connect(self.Chooselabel)

            self.BranchButton_3.setGeometry(QRect(640,488,635,70))
            self.OPBranchButton_3=QGraphicsOpacityEffect()
            self.OPBranchButton_3.setOpacity(1)
            self.BranchButton_3.setGraphicsEffect(self.OPBranchButton_3)
            self.BranchButton_3.clicked.connect(self.Chooselabel)

            self.BranchButton_4.setGeometry(QRect(640,593,635,70))
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

        self.BG1.setPixmap(QPixmap(""))
        self.BG2.setPixmap(QPixmap(""))
        self.BG1.repaint()
        self.BG2.repaint()


        self.MainTitle.setText(titlesetlst[0])
        self.SubTitle.setText(titlesetlst[1])
        self.BGRaw=QImage()
        self.BGRaw.load("./Visual/source/BGP/"+titlesetlst[2]+".png")
        self.BGRaw=self.BGRaw.scaled(1920,1080,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
        self.BG1.setPixmap(QPixmap(self.BGRaw))
        self.Logo.setPixmap(QPixmap("./Visual/source/Logo/"+titlesetlst[3]+".png"))

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

        self.BG2.setPixmap(QPixmap("./Visual/source/BaseUI/Picture/黑场.png"))
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
                tm.sleep(0.01)
            #断开事件
            self.Run.clicked.disconnect(self.RUNCORE)

        #初始控件复现
    def reprinthello(self,num):
        if num==1:
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

            self.OPBG1=QGraphicsOpacityEffect()
            self.OPBG1.setOpacity(1)
            self.BG1.setGraphicsEffect(self.OPBG1)

            self.OPBG2=QGraphicsOpacityEffect()
            self.OPBG2.setOpacity(0)
            self.BG2.setGraphicsEffect(self.OPBG2)

            self.OPFrame=QGraphicsOpacityEffect()
            self.OPFrame.setOpacity(0)
            self.Frame.setGraphicsEffect(self.OPFrame)

            self.Name_Label.setText("")
            self.Word_Label.setText("")

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
                tm.sleep(0.01)
            #重新连接事件
            self.Run.clicked.connect(self.RUNCORE)
            self.Name_Label.setText("")
            self.Word_Label.setText("")

        #背景控制器-屏幕更新承接函数
    def setprintbg(self,bgsetlst):
       self.BGR.load("./Visual/source/BGP/"+bgsetlst[0]+".png")
       self.BGR=self.BGR.scaled(1920,1080,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
       if self.changeBG==1:
            self.BG1.setPixmap(QPixmap(self.BGR))
            #控件遮挡关系-BG1有用情况
            self.BG2.raise_()
            self.BG1.raise_()
            self.AVG_L.raise_()
            self.AVG_M.raise_()
            self.AVG_R.raise_()
            self.Frame.raise_()
            self.Name_Label.raise_()
            self.Word_Label.raise_()
            #self.TestButtonOut.raise_()
            #self.TestButtonIN.raise_()
            self.Run.raise_()
            if eval(bgsetlst[3])!=0:
                for i in range (0,20):
                    self.OPBG1=QGraphicsOpacityEffect()
                    self.OPBG1.setOpacity(i/20)
                    self.BG1.setGraphicsEffect(self.OPBG1)
                    self.BG1.repaint()
                    tm.sleep(eval(bgsetlst[3])/20)
            elif eval(bgsetlst[3])==0:
                self.OPBG1=QGraphicsOpacityEffect()
                self.OPBG1.setOpacity(1)
                self.BG1.setGraphicsEffect(self.OPBG1)
                self.BG1.repaint()
            self.changeBG=2
            self.BG2.setPixmap(QPixmap(""))
       elif self.changeBG==2:
            self.BG2.setPixmap(QPixmap(self.BGR))
            #控件遮挡关系-BG2有用情况
            self.BG1.raise_()
            self.BG2.raise_()
            self.AVG_L.raise_()
            self.AVG_M.raise_()
            self.AVG_R.raise_()
            self.Frame.raise_()
            self.Name_Label.raise_()
            self.Word_Label.raise_()
            #self.TestButtonOut.raise_()
            #self.TestButtonIN.raise_()
            self.Run.raise_()
            if eval(bgsetlst[3])!=0:
                for i in range (0,20):
                    self.OPBG2=QGraphicsOpacityEffect()
                    self.OPBG2.setOpacity(i/20)
                    self.BG2.setGraphicsEffect(self.OPBG2)
                    self.BG2.repaint()
                    tm.sleep(eval(bgsetlst[3])/20)
            elif eval(bgsetlst[3])==0:
                self.OPBG2=QGraphicsOpacityEffect()
                self.OPBG2.setOpacity(1)
                self.BG2.setGraphicsEffect(self.OPBG2)
                self.BG2.repaint()

            self.changeBG=1
            self.BG1.setPixmap(QPixmap(""))
       self.Interpreter.wake()

        #讲述控制器-屏幕更新承接函数
    def setprintchara(self,charapic,charawords,wordset,charanum,BGblack):
      class SetPrintChara(QThread):
        FUNC=Function()
        #确认遮罩状态
        if BGblack==1:
            self.OPFrame.setOpacity(1)
            self.Frame.setGraphicsEffect(self.OPFrame)
            self.Frame.repaint()
        elif BGblack==0:
            self.OPFrame.setOpacity(0)
            self.Frame.setGraphicsEffect(self.OPFrame)
            self.Frame.repaint()
        #初始化立绘
        self.AVG_L.setPixmap(QPixmap(""))
        self.AVG_M.setPixmap(QPixmap(""))
        self.AVG_R.setPixmap(QPixmap(""))
        #填充立绘
        if charanum==1:
            for i in charapic:
                if i[0]!="":
                    self.AVG_M_R.load("./Visual/source/Chara/"+i[0]+"_"+i[1]+".png")
                    if i[2]=="0":self.AVG_M.setPixmap(QPixmap(self.AVG_M_R))
                    elif i[2]=="1":self.AVG_M.setPixmap(QPixmap(self.AVG_M_R.mirrored(True,False)))
                    self.AVG_M.repaint()
        elif charanum==2:
            if charapic[0][0]!="":
                self.AVG_L_R.load("./Visual/source/Chara/"+charapic[0][0]+"_"+charapic[0][1]+".png")
                if charapic[0][2]=="0":self.AVG_L.setPixmap(QPixmap(self.AVG_L_R))
                elif charapic[0][2]=="1":self.AVG_L.setPixmap(QPixmap(self.AVG_L_R.mirrored(True,False)))
                self.AVG_L.repaint()
            if charapic[1][0]!="":
                self.AVG_R_R.load("./Visual/source/Chara/"+charapic[1][0]+"_"+charapic[1][1]+".png")
                if charapic[1][2]=="0":self.AVG_R.setPixmap(QPixmap(self.AVG_R_R))
                elif charapic[1][2]=="1":self.AVG_R.setPixmap(QPixmap(self.AVG_R_R.mirrored(True,False)))
                self.AVG_R.repaint()     
        #初始化姓名和讲述
        self.Name_Label.setText("")
        self.Name_Label.repaint()
        self.Word_Label.setText("")
        self.Word_Label.repaint()
        #填充姓名和讲述
        for i in charawords:
            if i[0]=="" and charanum==1:#当槽位上没有姓名且场上只有一人，认为是旁白
                wordsALL=""
                for words in i[1]:
                    wordsALL+=words
                    self.Word_Label.setText(wordsALL)
                    self.Word_Label.repaint()
                    tm.sleep(eval(wordset[0]))
                break#慎防多个台词，直接退出槽位识别循环
            elif i[0]!="" and i[1]!="":#当槽位上有姓名和讲述内容则填充进对应框
                self.Name_Label.setText(i[0])
                self.Name_Label.repaint()     
                wordsALL=""
                for words in i[1]: 
                    wordsALL+=words
                    self.Word_Label.setText(wordsALL)
                    self.Word_Label.repaint()
                    tm.sleep(eval(wordset[0]))
                break#慎防多个台词，直接退出槽位识别循环
        tm.sleep(eval(wordset[1]))
        self.Interpreter.wake()
