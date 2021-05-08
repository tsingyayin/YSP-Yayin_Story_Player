#我本想把实现显示和控件定义的相关东西分离，但是现在看来似乎不太可能。
#也就是说这个ArtificialUI会不可避免的很大

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from global_value import warnline,texterrorline,numseterrorline,formatwarnline
from command.aaspcommand import *
import time as tm
import sys
from Visual.effect import *
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore")
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore\Visual")

class ContinueInfo(QObject):
    Continue=pyqtSignal(int)

class ArtificialUI(QWidget):
    def __init__(self):
        self.Spawn=SPAWN()
        self.Wake=ContinueInfo()
        self.Wake.Continue.connect(self.Spawn.wake)
        
        super().__init__()
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

        self.BG1=QLabel(self)#第一背景
        self.BG2=QLabel(self)#备用背景
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

        #self.TestButtonIN=QPushButton(self)#测试背景淡入按钮
        #self.TestButtonOut=QPushButton(self)#测试背景淡出按钮
        self.Run=QPushButton(self)#核心启动按钮

        #姓名和讲述内容文本框的样式定义
        self.Name_Label.setStyleSheet("QLabel{color:#FFFFFF;font-size:30px}")
        self.Name_Label.setAlignment(Qt.AlignRight)
        self.Word_Label.setStyleSheet("QLabel{color:#AAAAAA;font-size:30px}")
        self.Word_Label.setAlignment(Qt.AlignLeft)

        #背景控件设置
        self.BG1.setGeometry(QRect(0,0,1920,1080))
        self.BG2.setGeometry(QRect(0,0,1920,1080))

        #测试背景变化的两个按钮的位置和文本信息
        #self.TestButtonIN.setGeometry(QRect(120,10,93,28))
        #self.TestButtonOut.setGeometry(QRect(230,10,93,28))
        #self.TestButtonIN.setText("显示图片")
        #self.TestButtonOut.setText("隐藏图片")

        #启动核心的按钮的位置和文本信息
        self.Run.setGeometry(QRect(10,10,93,28))
        self.Run.setText("启动核心")
  
        #基本框架
        self.Frame.setPixmap(QPixmap("./Visual/source/BaseUI/Frame/frame.png"))

        #控件位置
        self.Name_Label.setGeometry(QRect(220,960,300,30))
        self.Word_Label.setGeometry(QRect(620,960,1080,90))
        self.AVG_L.setGeometry(QRect(90,220,900,900))
        self.AVG_M.setGeometry(QRect(443,220,900,900))
        self.AVG_R.setGeometry(QRect(796,220,900,900))

        #控件遮挡关系-默认情况
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
        #按钮信号和槽函数连接
        self.Run.clicked.connect(self.RUNCORE)
        
        #背景透明度初始化
        self.OPBG1=QGraphicsOpacityEffect()
        self.OPBG1.setOpacity(0)
        self.BG1.setGraphicsEffect(self.OPBG1)

        self.OPBG2=QGraphicsOpacityEffect()
        self.OPBG2.setOpacity(0)
        self.BG2.setGraphicsEffect(self.OPBG2)
        #框架透明度初始化
        self.OPFrame=QGraphicsOpacityEffect()
        self.OPFrame.setOpacity(0)
        self.Frame.setGraphicsEffect(self.OPFrame)

        #测试灰暗效果
        #self.Dark=QGraphicsColorizeEffect()
        #self.Dark.setColor(QColor(0,0,0,10))
        #self.AVG_R.setGraphicsEffect(self.Dark)

        #启动核心的函数
    def RUNCORE(self):
        self.Interpreter=SPAWN()
        self.Interpreter.can_update_chara.connect(self.setprintchara)
        self.Interpreter.can_update_bg.connect(self.setprintbg)
        self.Interpreter.start()

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
                    self.OPBG1.setOpacity(i/20)
                    self.BG1.setGraphicsEffect(self.OPBG1)
                    self.BG1.repaint()
                    tm.sleep(eval(bgsetlst[3])/20)
            elif eval(bgsetlst[3])==0:
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
                    self.OPBG2.setOpacity(i/20)
                    self.BG2.setGraphicsEffect(self.OPBG2)
                    self.BG2.repaint()
                    tm.sleep(eval(bgsetlst[3])/20)
            elif eval(bgsetlst[3])==0:
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
