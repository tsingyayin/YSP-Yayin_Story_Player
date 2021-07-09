import os
import sys
import traceback
import time as tm
import math as ma
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from langcontrol import *
from command.aaspcommand import *
from crashreport import *
from arknights.HLtoSPOL import *
global TopwinControl
TopwinControl=""

class TopDef(QWidget):
    def setupUi(self):
        self.desktop=QDesktopWidget()
        self.current_monitor=self.desktop.screenNumber(self)
        self.Display=self.desktop.screenGeometry(self.current_monitor)
        self.X=self.Display.width()
        self.Y=self.Display.height()

        #基本圆角框架和半透明效果实现
        self.setGeometry(QRect(600,400,700,300))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.frame=QFrame()
        self.hl=QHBoxLayout()
        self.hl.setContentsMargins(10,10,10,10)
        self.setLayout(self.hl)
        self.hl.addWidget(self.frame)
        self.setStyleSheet("QWidget{background-color:rgba(255,255,255,200);border:none;border-radius:15px;}")

        
        #self.OPSelfFrame=QGraphicsBlurEffect()
        #self.OPSelfFrame.setBlurRadius(3)
        #self.frame.setGraphicsEffect(self.OPSelfWindow)

        self.SelfEffect=QGraphicsDropShadowEffect()
        self.SelfEffect.setOffset(4,4)
        self.SelfEffect.setColor(QColor(0,0,0,127))
        self.SelfEffect.setBlurRadius(15)
        self.frame.setGraphicsEffect(self.SelfEffect)

    def defObject(self):
        
        #Logo和Title的定义
        self.Iconlabel=QLabel(self)
        self.Iconlabel.setGeometry(QRect(50,15,270,270))
        self.LogoRaw=QImage()
        self.LogoRaw.load("./Visual/source/BaseUI/Image/Videotape_Win11.png")
        self.LogoRaw=self.LogoRaw.scaled(270,270,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
        self.Iconlabel.setPixmap(QPixmap(self.LogoRaw))
        self.Iconlabel.setStyleSheet("QLabel{background-color:rgba(255,255,255,0);border:none;border-radius:0px;}")

        self.Titlelabel=QLabel(self)
        self.Titlelabel.setText(msg("Ui_Msg_Title"))
        self.Titlelabel.setStyleSheet(
            """QLabel{
            background-color:rgba(255,255,255,0);
            border:none;
            border-radius:0px;
            color:#000000;
            font-family:'Microsoft YaHei';
            font-size:50px;
            }""")
        self.Titlelabel.setGeometry(QRect(300,100,400,100))
        self.Titlelabel.setAlignment(Qt.AlignCenter)

        self.OPTitlelabel=QGraphicsOpacityEffect()
        self.OPTitlelabel.setOpacity(1)
        self.Titlelabel.setGraphicsEffect(self.OPTitlelabel)

        self.AnyInfolabel=QLabel(self)
        self.AnyInfolabel.setText(("测试用文本测试用文本测试用文本"))
        self.AnyInfolabel.setStyleSheet(
            """QLabel{
            background-color:rgba(255,255,255,0);
            border:none;
            border-radius:0px;
            text-align:center;
            color:#4488FF;
            font-family:'Microsoft YaHei';
            font-size:30px;
            }""")
        self.AnyInfolabel.setGeometry(QRect(50,630,600,40))
        self.AnyInfolabel.setAlignment(Qt.AlignCenter)

        self.OPAnyInfolabel=QGraphicsOpacityEffect()
        self.OPAnyInfolabel.setOpacity(0)
        self.AnyInfolabel.setGraphicsEffect(self.OPAnyInfolabel)

        self.UIModeButton=QPushButton(self)
        self.UIModeButton.setGeometry(QRect(50,350,600,50))
        self.UIModeButton.setText(msg("Ui_Msg_LaunchUI"))
        self.UIModeButton.setStyleSheet(
            """QPushButton{
            color:#333333;
            background-color:rgba(255,255,255,210);
            text-align:center;
            font-size:32px;
            font-family:'Microsoft YaHei';
                }
            QPushButton:hover{
            color:#888888;
            background-color:rgba(255,255,255,255);
            text-align:center;
            font-size:36px;
            font-family:'Microsoft YaHei';
                }
            QPushButton:Pressed{
            color:#66ccff;
            background-color:rgba(255,255,255,255);
            text-align:center;
            font-size:32px;
            font-family:'Microsoft YaHei';
            }""")

        self.SettingsButton=QPushButton(self)
        self.SettingsButton.setGeometry(QRect(50,490,600,50))
        self.SettingsButton.setText(msg("Ui_Msg_Settings"))
        self.SettingsButton.setStyleSheet(
            """QPushButton{
            color:#333333;
            background-color:rgba(255,255,255,210);
            text-align:center;
            font-size:32px;
            font-family:'Microsoft YaHei';
                }
            QPushButton:hover{
            color:#888888;
            background-color:rgba(255,255,255,255);
            text-align:center;
            font-size:36px;
            font-family:'Microsoft YaHei';
                }
            QPushButton:Pressed{
            color:#66ccff;
            background-color:rgba(255,255,255,255);
            text-align:center;
            font-size:32px;
            font-family:'Microsoft YaHei';
            }""")

        self.ToolsButton=QPushButton(self)
        self.ToolsButton.setGeometry(QRect(50,420,600,50))
        self.ToolsButton.setText(msg("Ui_Msg_Tools"))
        self.ToolsButton.setStyleSheet(
            """QPushButton{
            color:#333333;
            background-color:rgba(255,255,255,210);
            text-align:center;
            font-size:32px;
            font-family:'Microsoft YaHei';
                }
            QPushButton:hover{
            color:#888888;
            background-color:rgba(255,255,255,255);
            text-align:center;
            font-size:36px;
            font-family:'Microsoft YaHei';
                }
            QPushButton:Pressed{
            color:#66ccff;
            background-color:rgba(255,255,255,255);
            text-align:center;
            font-size:32px;
            font-family:'Microsoft YaHei';
            }""")

        self.AboutButton=QPushButton(self)
        self.AboutButton.setGeometry(QRect(50,420,260,50))
        self.AboutButton.setText(msg("Ui_Msg_About_"))
        self.AboutButton.setStyleSheet(
            """QPushButton{
            color:#333333;
            background-color:rgba(255,255,255,210);
            text-align:center;
            font-size:32px;
            font-family:'Microsoft YaHei';
                }
            QPushButton:hover{
            color:#888888;
            background-color:rgba(255,255,255,255);
            text-align:center;
            font-size:36px;
            font-family:'Microsoft YaHei';
                }
            QPushButton:Pressed{
            color:#66ccff;
            background-color:rgba(255,255,255,255);
            text-align:center;
            font-size:32px;
            font-family:'Microsoft YaHei';
            }""")
        self.OPAboutButton=QGraphicsOpacityEffect()
        self.OPAboutButton.setOpacity(0)
        self.AboutButton.setGraphicsEffect(self.OPAboutButton)

        self.LangButton=QPushButton(self)
        self.LangButton.setGeometry(QRect(390,420,260,50))
        self.LangButton.setText(msg("Ui_Msg_Choose_Lang"))
        self.LangButton.setStyleSheet(
            """QPushButton{
            color:#333333;
            background-color:rgba(255,255,255,210);
            text-align:center;
            font-size:32px;
            font-family:'Microsoft YaHei';
                }
            QPushButton:hover{
            color:#888888;
            background-color:rgba(255,255,255,255);
            text-align:center;
            font-size:36px;
            font-family:'Microsoft YaHei';
                }
            QPushButton:Pressed{
            color:#66ccff;
            background-color:rgba(255,255,255,255);
            text-align:center;
            font-size:32px;
            font-family:'Microsoft YaHei';
            }""")
        self.OPLangButton=QGraphicsOpacityEffect()
        self.OPLangButton.setOpacity(0)
        self.LangButton.setGraphicsEffect(self.OPLangButton)

        self.ToSpolButton=QPushButton(self)
        self.ToSpolButton.setGeometry(QRect(390,420,260,50))
        self.ToSpolButton.setText(msg("Ui_Msg_To_Spol"))
        self.ToSpolButton.setStyleSheet(
            """QPushButton{
            color:#333333;
            background-color:rgba(255,255,255,210);
            text-align:center;
            font-size:32px;
            font-family:'Microsoft YaHei';
                }
            QPushButton:hover{
            color:#888888;
            background-color:rgba(255,255,255,255);
            text-align:center;
            font-size:36px;
            font-family:'Microsoft YaHei';
                }
            QPushButton:Pressed{
            color:#66ccff;
            background-color:rgba(255,255,255,255);
            text-align:center;
            font-size:32px;
            font-family:'Microsoft YaHei';
            }""")
        self.OPToSpolButton=QGraphicsOpacityEffect()
        self.OPToSpolButton.setOpacity(0)
        self.ToSpolButton.setGraphicsEffect(self.OPToSpolButton)

        self.ClrWrongButton=QPushButton(self)
        self.ClrWrongButton.setGeometry(QRect(50,350,260,50))
        self.ClrWrongButton.setText(msg("Ui_Msg_Clear_Wrong"))
        self.ClrWrongButton.setStyleSheet(
            """QPushButton{
            color:#333333;
            background-color:rgba(255,255,255,210);
            text-align:center;
            font-size:32px;
            font-family:'Microsoft YaHei';
                }
            QPushButton:hover{
            color:#888888;
            background-color:rgba(255,255,255,255);
            text-align:center;
            font-size:36px;
            font-family:'Microsoft YaHei';
                }
            QPushButton:Pressed{
            color:#66ccff;
            background-color:rgba(255,255,255,255);
            text-align:center;
            font-size:32px;
            font-family:'Microsoft YaHei';
            }""")
        self.OPClrWrongButton=QGraphicsOpacityEffect()
        self.OPClrWrongButton.setOpacity(0)
        self.ClrWrongButton.setGraphicsEffect(self.OPClrWrongButton)

        self.ClrCacheButton=QPushButton(self)
        self.ClrCacheButton.setGeometry(QRect(390,350,260,50))
        self.ClrCacheButton.setText(msg("Ui_Msg_Clear_All"))
        self.ClrCacheButton.setStyleSheet(
            """QPushButton{
            color:#333333;
            background-color:rgba(255,255,255,210);
            text-align:center;
            font-size:32px;
            font-family:'Microsoft YaHei';
                }
            QPushButton:hover{
            color:#888888;
            background-color:rgba(255,255,255,255);
            text-align:center;
            font-size:36px;
            font-family:'Microsoft YaHei';
                }
            QPushButton:Pressed{
            color:#66ccff;
            background-color:rgba(255,255,255,255);
            text-align:center;
            font-size:32px;
            font-family:'Microsoft YaHei';
            }""")
        self.OPClrCacheButton=QGraphicsOpacityEffect()
        self.OPClrCacheButton.setOpacity(0)
        self.ClrCacheButton.setGraphicsEffect(self.OPClrCacheButton)

        self.BackButton=QPushButton(self)
        self.BackButton.setGeometry(QRect(390,560,260,50))
        self.BackButton.setText(msg("Ui_Msg_Back"))
        self.BackButton.setStyleSheet(
            """QPushButton{
            color:#333333;
            background-color:rgba(255,220,220,210);
            text-align:center;
            font-size:32px;
            font-family:'Microsoft YaHei';
                }
            QPushButton:hover{
            color:#FFFFFF;
            background-color:rgba(255,230,230,255);
            text-align:center;
            font-size:36px;
            font-family:'Microsoft YaHei';
                }
            QPushButton:Pressed{
            color:#FF0000;
            background-color:rgba(240,200,200,255);
            text-align:center;
            font-size:32px;
            font-family:'Microsoft YaHei';
            }""")
        self.SABackButton=QGraphicsDropShadowEffect()
        self.SABackButton.setOffset(0,0)
        self.SABackButton.setColor(QColor(0,0,0,100))
        self.SABackButton.setBlurRadius(20)
        self.BackButton.setGraphicsEffect(self.SABackButton)

        self.ExitButton=QPushButton(self)
        self.ExitButton.setGeometry(QRect(50,560,260,50))
        self.ExitButton.setText(msg("Ui_Msg_Exit"))
        self.ExitButton.setStyleSheet(
            """QPushButton{
            color:#333333;
            background-color:rgba(255,255,255,210);
            text-align:center;
            font-size:32px;
            font-family:'Microsoft YaHei';
                }
            QPushButton:hover{
            color:#888888;
            background-color:rgba(255,255,255,255);
            text-align:center;
            font-size:36px;
            font-family:'Microsoft YaHei';
                }
            QPushButton:Pressed{
            color:#66ccff;
            background-color:rgba(255,255,255,255);
            text-align:center;
            font-size:32px;
            font-family:'Microsoft YaHei';
            }""")

        self.AboutLabel_FullVer=QLabel(self)
        self.AboutLabel_FullVer.setText(msg("About_Info_Version")+Edition)
        self.AboutLabel_FullVer.setGeometry(QRect(25,280,650,30))
        self.AboutLabel_FullVer.setAlignment(Qt.AlignCenter)
        self.AboutLabel_FullVer.setStyleSheet(
            """QLabel{
            background-color:rgba(255,255,255,0);
            border:none;
            border-radius:0px;
            color:#000000;
            font-family:'Microsoft YaHei';
            font-size:22px;
            }""")
        self.OPAboutLabel_FullVer=QGraphicsOpacityEffect()
        self.OPAboutLabel_FullVer.setOpacity(0)
        self.AboutLabel_FullVer.setGraphicsEffect(self.OPAboutLabel_FullVer)

        self.AboutLabel_MainVer=QLabel(self)
        self.AboutLabel_MainVer.setText(msg("About_Info_Main_Ver")+InsiderMainVer)
        self.AboutLabel_MainVer.setGeometry(QRect(60,320,300,30))
        self.AboutLabel_MainVer.setAlignment(Qt.AlignLeft)
        self.AboutLabel_MainVer.setStyleSheet(
            """QLabel{
            background-color:rgba(255,255,255,0);
            border:none;
            border-radius:0px;
            color:#000000;
            font-family:'Microsoft YaHei';
            font-size:22px;
            }""")
        self.OPAboutLabel_MainVer=QGraphicsOpacityEffect()
        self.OPAboutLabel_MainVer.setOpacity(0)
        self.AboutLabel_MainVer.setGraphicsEffect(self.OPAboutLabel_MainVer)

        self.AboutLabel_SubVer=QLabel(self)
        self.AboutLabel_SubVer.setText(msg("About_Info_Sub_Ver")+InsiderSubVer)
        self.AboutLabel_SubVer.setGeometry(QRect(360,320,300,30))
        self.AboutLabel_SubVer.setAlignment(Qt.AlignLeft)
        self.AboutLabel_SubVer.setStyleSheet(
            """QLabel{
            background-color:rgba(255,255,255,0);
            border:none;
            border-radius:0px;
            color:#000000;
            font-family:'Microsoft YaHei';
            font-size:22px;
            }""")
        self.OPAboutLabel_SubVer=QGraphicsOpacityEffect()
        self.OPAboutLabel_SubVer.setOpacity(0)
        self.AboutLabel_SubVer.setGraphicsEffect(self.OPAboutLabel_SubVer)

        self.AboutLabel_BuildVer=QLabel(self)
        self.AboutLabel_BuildVer.setText(msg("About_Info_Build_Ver")+InsiderBuildVer)
        self.AboutLabel_BuildVer.setGeometry(QRect(60,360,300,30))
        self.AboutLabel_BuildVer.setAlignment(Qt.AlignLeft)
        self.AboutLabel_BuildVer.setStyleSheet(
            """QLabel{
            background-color:rgba(255,255,255,0);
            border:none;
            border-radius:0px;
            color:#000000;
            font-family:'Microsoft YaHei';
            font-size:22px;
            }""")
        self.OPAboutLabel_BuildVer=QGraphicsOpacityEffect()
        self.OPAboutLabel_BuildVer.setOpacity(0)
        self.AboutLabel_BuildVer.setGraphicsEffect(self.OPAboutLabel_BuildVer)

        self.AboutLabel_SpolVer=QLabel(self)
        self.AboutLabel_SpolVer.setText(msg("About_Info_Spol_Ver")+InsiderSPOLVer)
        self.AboutLabel_SpolVer.setGeometry(QRect(360,360,300,30))
        self.AboutLabel_SpolVer.setAlignment(Qt.AlignLeft)
        self.AboutLabel_SpolVer.setStyleSheet(
            """QLabel{
            background-color:rgba(255,255,255,0);
            border:none;
            border-radius:0px;
            color:#000000;
            font-family:'Microsoft YaHei';
            font-size:22px;
            }""")
        self.OPAboutLabel_SpolVer=QGraphicsOpacityEffect()
        self.OPAboutLabel_SpolVer.setOpacity(0)
        self.AboutLabel_SpolVer.setGraphicsEffect(self.OPAboutLabel_SpolVer)

        self.AboutLabel_SpolEnvVer=QLabel(self)
        self.AboutLabel_SpolEnvVer.setText(msg("About_Info_Spol_Env_Ver")+InsiderSPOLEnvVer)
        self.AboutLabel_SpolEnvVer.setGeometry(QRect(60,400,650,30))
        self.AboutLabel_SpolEnvVer.setAlignment(Qt.AlignLeft)
        self.AboutLabel_SpolEnvVer.setStyleSheet(
            """QLabel{
            background-color:rgba(255,255,255,0);
            border:none;
            border-radius:0px;
            color:#000000;
            font-family:'Microsoft YaHei';
            font-size:22px;
            }""")
        self.OPAboutLabel_SpolEnvVer=QGraphicsOpacityEffect()
        self.OPAboutLabel_SpolEnvVer.setOpacity(0)
        self.AboutLabel_SpolEnvVer.setGraphicsEffect(self.OPAboutLabel_SpolEnvVer)

        self.AboutLabel_Developers=QLabel(self)
        self.AboutLabel_Developers.setText(msg("About_Info_Developers")+"青雅音")
        self.AboutLabel_Developers.setGeometry(QRect(60,440,600,30))
        self.AboutLabel_Developers.setAlignment(Qt.AlignLeft)
        self.AboutLabel_Developers.setStyleSheet(
            """QLabel{
            background-color:rgba(255,255,255,0);
            border:none;
            border-radius:0px;
            color:#000000;
            font-family:'Microsoft YaHei';
            font-size:22px;
            }""")
        self.OPAboutLabel_Developers=QGraphicsOpacityEffect()
        self.OPAboutLabel_Developers.setOpacity(0)
        self.AboutLabel_Developers.setGraphicsEffect(self.OPAboutLabel_Developers)

        self.AboutLabel_Support=QLabel(self)
        self.AboutLabel_Support.setText(msg("About_Info_Support")+"亿绪联合协会 UYXA")
        self.AboutLabel_Support.setGeometry(QRect(60,480,600,30))
        self.AboutLabel_Support.setAlignment(Qt.AlignLeft)
        self.AboutLabel_Support.setStyleSheet(
            """QLabel{
            background-color:rgba(255,255,255,0);
            border:none;
            border-radius:0px;
            color:#000000;
            font-family:'Microsoft YaHei';
            font-size:22px;
            }""")
        self.OPAboutLabel_Support=QGraphicsOpacityEffect()
        self.OPAboutLabel_Support.setOpacity(0)
        self.AboutLabel_Support.setGraphicsEffect(self.OPAboutLabel_Support)

        self.AboutLabel_Donate=QLabel(self)
        self.AboutLabel_Donate.setText(msg("About_Info_Donate").format("<A href='"+urlAFD+"'>"+urlAFD+"</a>"))
        self.AboutLabel_Donate.setOpenExternalLinks(False)
        self.AboutLabel_Donate.setGeometry(QRect(60,520,600,30))
        self.AboutLabel_Donate.setAlignment(Qt.AlignLeft)
        self.AboutLabel_Donate.setStyleSheet(
            """QLabel{
            background-color:rgba(255,255,255,0);
            border:none;
            border-radius:0px;
            color:#000000;
            font-family:'Microsoft YaHei';
            font-size:22px;
            }""")
        self.OPAboutLabel_Donate=QGraphicsOpacityEffect()
        self.OPAboutLabel_Donate.setOpacity(0)
        self.AboutLabel_Donate.setGraphicsEffect(self.OPAboutLabel_Donate)
        
        self.CheckUpdateButton=QPushButton(self)
        self.CheckUpdateButton.setGeometry(QRect(50,560,260,50))
        self.CheckUpdateButton.setText(msg("Ui_Msg_Check_Update"))
        self.CheckUpdateButton.setStyleSheet(
            """QPushButton{
            color:#333333;
            background-color:rgba(255,255,255,210);
            text-align:center;
            font-size:32px;
            font-family:'Microsoft YaHei';
                }
            QPushButton:hover{
            color:#888888;
            background-color:rgba(255,255,255,255);
            text-align:center;
            font-size:36px;
            font-family:'Microsoft YaHei';
                }
            QPushButton:Pressed{
            color:#66ccff;
            background-color:rgba(255,255,255,255);
            text-align:center;
            font-size:32px;
            font-family:'Microsoft YaHei';
            }""")
        self.OPCheckUpdateButton=QGraphicsOpacityEffect()
        self.OPCheckUpdateButton.setOpacity(0)
        self.CheckUpdateButton.setGraphicsEffect(self.OPCheckUpdateButton)

class UpdateWindow(QWidget):
    def __init__(self,NewVersion):
        super(UpdateWindow,self).__init__()
        self.desktop=QDesktopWidget()
        self.current_monitor=self.desktop.screenNumber(self)
        self.Display=self.desktop.screenGeometry(self.current_monitor)
        self.X=self.Display.width()
        self.Y=self.Display.height()

        #基本圆角框架和半透明效果实现
        self.setGeometry(QRect(500,400,900,300))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.frame=QFrame()
        self.hl=QHBoxLayout()
        self.hl.setContentsMargins(10,10,10,10)
        self.setLayout(self.hl)
        self.hl.addWidget(self.frame)
        self.setStyleSheet("QWidget{background-color:rgba(255,255,255,200);border:none;border-radius:15px;}")

        self.SelfEffect=QGraphicsDropShadowEffect()
        self.SelfEffect.setOffset(4,4)
        self.SelfEffect.setColor(QColor(0,0,0,127))
        self.SelfEffect.setBlurRadius(15)
        self.frame.setGraphicsEffect(self.SelfEffect)

        self.OopsLabel=QLabel(self)
        self.OopsLabel.setText(msg("Ui_Msg_Can_Update")+"UYXA")
        self.OopsLabel.setGeometry(QRect(50,50,800,40))
        self.OopsLabel.setAlignment(Qt.AlignCenter)
        self.OopsLabel.setStyleSheet(
            """QLabel{
            background-color:rgba(255,255,255,0);
            border:none;
            border-radius:0px;
            color:#4488FF;
            font-family:'Microsoft YaHei';
            font-size:30px;
            }""")

        self.Version=NewVersion
        self.NewVersionLabel=QLabel(self)
        self.Preurl="https://pan.baidu.com/s/1P2HXW0Y5G4piA7XUKXWWzg"
        self.Puburl="https://pan.baidu.com/s/1Zo_lZzEjpIaEsM4LdCohYQ"
        if "Pre" in self.Version:
            self.NewVersionLabel.setText(msg("Ui_Msg_New_Version")+"<A href='"+self.Preurl+"'>"+self.Version+"</a>")
        else:
            self.NewVersionLabel.setText(msg("Ui_Msg_New_Version")+"<A href='"+self.Puburl+"'>"+self.Version+"</a>")
        self.NewVersionLabel.setOpenExternalLinks(True)
        self.NewVersionLabel.setGeometry(QRect(50,120,800,40))
        self.NewVersionLabel.setAlignment(Qt.AlignCenter)
        self.NewVersionLabel.setStyleSheet(
            """QLabel{
            background-color:rgba(255,255,255,0);
            border:none;
            border-radius:0px;
            color:#000000;
            font-family:'Microsoft YaHei';
            font-size:20px;
            }""")

        self.BackButton=QPushButton(self)
        self.BackButton.setGeometry(QRect(50,190,800,50))
        self.BackButton.setText(msg("Ui_Msg_Back"))
        self.BackButton.setStyleSheet(
            """QPushButton{
            color:#333333;
            background-color:rgba(255,220,220,210);
            text-align:center;
            font-size:32px;
            font-family:'Microsoft YaHei';
                }
            QPushButton:hover{
            color:#FFFFFF;
            background-color:rgba(255,230,230,255);
            text-align:center;
            font-size:36px;
            font-family:'Microsoft YaHei';
                }
            QPushButton:Pressed{
            color:#FF0000;
            background-color:rgba(240,200,200,255);
            text-align:center;
            font-size:32px;
            font-family:'Microsoft YaHei';
            }""")
        self.SABackButton=QGraphicsDropShadowEffect()
        self.SABackButton.setOffset(0,0)
        self.SABackButton.setColor(QColor(0,0,0,100))
        self.SABackButton.setBlurRadius(20)
        self.BackButton.setGraphicsEffect(self.SABackButton)

        self.BackButton.clicked.connect(self.CloseDialog)

    def CloseDialog(self):
        self.close()

    def UpdateLang(self):
        self.OopsLabel.setText(msg("Ui_Msg_Can_Update")+"UYXA")
        if "Pre" in self.Version:
            self.NewVersionLabel.setText(msg("Ui_Msg_New_Version")+"<A href='"+self.Preurl+"'>"+self.Version+"</a>")
        else:
            self.NewVersionLabel.setText(msg("Ui_Msg_New_Version")+"<A href='"+self.Puburl+"'>"+self.Version+"</a>")
        self.BackButton.setText(msg("Ui_Msg_Back"))

class TopWindow(TopDef):
    def __init__(self,parent = None):
        super(TopWindow,self).__init__(parent)
        global TopwinControl
        TopwinControl=""
        self.setupUi()
        self.defObject()
        self.ShowFirstPage()
        self.setWindowIcon(QIcon(".\\Visual\\source\\WinICO\\Videotape_Win11.ico"))
        self.setWindowTitle("YSP User Page")
        self.Service=FrameWork()
        self.Service.AnyInfo.connect(self.ShowAnyInfo)
        self.FirstEnter=0

        #展示首页
    def ShowFirstPage(self):
        self.PageName="First_Page"
        self.SAUIModeButton=QGraphicsDropShadowEffect()
        self.SAUIModeButton.setOffset(0,0)
        self.SAUIModeButton.setColor(QColor(0,0,0,100))
        self.SAUIModeButton.setBlurRadius(20)
        self.UIModeButton.setGraphicsEffect(self.SAUIModeButton)

        self.SASettingsButton=QGraphicsDropShadowEffect()
        self.SASettingsButton.setOffset(0,0)
        self.SASettingsButton.setColor(QColor(0,0,0,100))
        self.SASettingsButton.setBlurRadius(20)
        self.SettingsButton.setGraphicsEffect(self.SASettingsButton)

        self.SAToolsButton=QGraphicsDropShadowEffect()
        self.SAToolsButton.setOffset(0,0)
        self.SAToolsButton.setColor(QColor(0,0,0,100))
        self.SAToolsButton.setBlurRadius(20)
        self.ToolsButton.setGraphicsEffect(self.SAToolsButton)

        self.SAExitButton=QGraphicsDropShadowEffect()
        self.SAExitButton.setOffset(0,0)
        self.SAExitButton.setColor(QColor(0,0,0,100))
        self.SAExitButton.setBlurRadius(20)
        self.ExitButton.setGraphicsEffect(self.SAExitButton)

        self.Titlelabel.raise_()
        self.Iconlabel.raise_()
        self.UIModeButton.raise_()
        self.SettingsButton.raise_()
        self.ToolsButton.raise_()
        self.ExitButton.raise_()
        self.BackButton.raise_()

        self.ExitButton.clicked.connect(self.FullExit)
        self.BackButton.clicked.connect(self.ExitPro)

        self.UIModeButton.clicked.connect(self.LaunchUI)
        self.SettingsButton.clicked.connect(self.ShowSettingsPage)
        self.SettingsButton.clicked.connect(self.HideFirstPage)
        self.ToolsButton.clicked.connect(self.ShowToolsPage)
        self.ToolsButton.clicked.connect(self.HideFirstPage)
        
        #隐藏首页
    def HideFirstPage(self):
        self.OPUIModeButton=QGraphicsOpacityEffect()
        self.OPUIModeButton.setOpacity(0)
        self.UIModeButton.setGraphicsEffect(self.OPUIModeButton)

        self.OPSettingsButton=QGraphicsOpacityEffect()
        self.OPSettingsButton.setOpacity(0)
        self.SettingsButton.setGraphicsEffect(self.OPSettingsButton)

        self.OPToolsButton=QGraphicsOpacityEffect()
        self.OPToolsButton.setOpacity(0)
        self.ToolsButton.setGraphicsEffect(self.OPToolsButton)

        self.OPExitButton=QGraphicsOpacityEffect()
        self.OPExitButton.setOpacity(0)
        self.ExitButton.setGraphicsEffect(self.OPExitButton)

        self.ExitButton.clicked.disconnect(self.FullExit)
        self.BackButton.clicked.disconnect(self.ExitPro)

        self.UIModeButton.clicked.disconnect(self.LaunchUI)
        self.SettingsButton.clicked.disconnect(self.HideFirstPage)
        self.SettingsButton.clicked.disconnect(self.ShowSettingsPage)
        self.ToolsButton.clicked.disconnect(self.HideFirstPage)
        self.ToolsButton.clicked.disconnect(self.ShowToolsPage)

        #展示设定页
    def ShowSettingsPage(self):
        self.PageName="Settings_Page"
        self.SALangButton=QGraphicsDropShadowEffect()
        self.SALangButton.setOffset(0,0)
        self.SALangButton.setColor(QColor(0,0,0,100))
        self.SALangButton.setBlurRadius(20)
        self.LangButton.setGraphicsEffect(self.SALangButton)

        self.SAAboutButton=QGraphicsDropShadowEffect()
        self.SAAboutButton.setOffset(0,0)
        self.SAAboutButton.setColor(QColor(0,0,0,100))
        self.SAAboutButton.setBlurRadius(20)
        self.AboutButton.setGraphicsEffect(self.SAAboutButton)

        self.BackButton.clicked.connect(self.ShowFirstPage)
        self.BackButton.clicked.connect(self.HideSettingsPage)
        self.LangButton.clicked.connect(self.ChooseLangFile)
        self.AboutButton.clicked.connect(self.ShowAboutPage)
        self.AboutButton.clicked.connect(self.HideSettingsPage)

        self.AboutButton.raise_()
        self.LangButton.raise_()

        #隐藏设定页
    def HideSettingsPage(self):
        self.OPLangButton=QGraphicsOpacityEffect()
        self.OPLangButton.setOpacity(0)
        self.LangButton.setGraphicsEffect(self.OPLangButton)

        self.OPAboutButton=QGraphicsOpacityEffect()
        self.OPAboutButton.setOpacity(0)
        self.AboutButton.setGraphicsEffect(self.OPAboutButton)
        
        self.BackButton.clicked.disconnect(self.ShowFirstPage)
        self.BackButton.clicked.disconnect(self.HideSettingsPage)
        self.LangButton.clicked.disconnect(self.ChooseLangFile)
        self.AboutButton.clicked.disconnect(self.ShowAboutPage)
        self.AboutButton.clicked.disconnect(self.HideSettingsPage)

        #展示关于页面
    def ShowAboutPage(self):
        self.OPAboutLabel_MainVer=QGraphicsOpacityEffect()
        self.OPAboutLabel_MainVer.setOpacity(1)
        self.AboutLabel_MainVer.setGraphicsEffect(self.OPAboutLabel_MainVer)

        self.OPAboutLabel_SubVer=QGraphicsOpacityEffect()
        self.OPAboutLabel_SubVer.setOpacity(1)
        self.AboutLabel_SubVer.setGraphicsEffect(self.OPAboutLabel_SubVer)

        self.OPAboutLabel_FullVer=QGraphicsOpacityEffect()
        self.OPAboutLabel_FullVer.setOpacity(1)
        self.AboutLabel_FullVer.setGraphicsEffect(self.OPAboutLabel_FullVer)

        self.OPAboutLabel_SpolVer=QGraphicsOpacityEffect()
        self.OPAboutLabel_SpolVer.setOpacity(1)
        self.AboutLabel_SpolVer.setGraphicsEffect(self.OPAboutLabel_SpolVer)

        self.OPAboutLabel_SpolEnvVer=QGraphicsOpacityEffect()
        self.OPAboutLabel_SpolEnvVer.setOpacity(1)
        self.AboutLabel_SpolEnvVer.setGraphicsEffect(self.OPAboutLabel_SpolEnvVer)

        self.OPAboutLabel_BuildVer=QGraphicsOpacityEffect()
        self.OPAboutLabel_BuildVer.setOpacity(1)
        self.AboutLabel_BuildVer.setGraphicsEffect(self.OPAboutLabel_BuildVer)

        self.OPAboutLabel_Developers=QGraphicsOpacityEffect()
        self.OPAboutLabel_Developers.setOpacity(1)
        self.AboutLabel_Developers.setGraphicsEffect(self.OPAboutLabel_Developers)

        self.OPAboutLabel_Support=QGraphicsOpacityEffect()
        self.OPAboutLabel_Support.setOpacity(1)
        self.AboutLabel_Support.setGraphicsEffect(self.OPAboutLabel_Support)

        self.OPAboutLabel_Donate=QGraphicsOpacityEffect()
        self.OPAboutLabel_Donate.setOpacity(1)
        self.AboutLabel_Donate.setGraphicsEffect(self.OPAboutLabel_Donate)

        self.SACheckUpdateButton=QGraphicsDropShadowEffect()
        self.SACheckUpdateButton.setOffset(0,0)
        self.SACheckUpdateButton.setColor(QColor(0,0,0,100))
        self.SACheckUpdateButton.setBlurRadius(20)
        self.CheckUpdateButton.setGraphicsEffect(self.SACheckUpdateButton)

        self.BackButton.clicked.connect(self.ShowSettingsPage)
        self.BackButton.clicked.connect(self.HideAboutPage)
        self.CheckUpdateButton.clicked.connect(self.CheckingUpdate)
        self.AboutLabel_Donate.setOpenExternalLinks(True)

        self.AboutLabel_BuildVer.raise_()
        self.AboutLabel_Developers.raise_()
        self.AboutLabel_Donate.raise_()
        self.AboutLabel_FullVer.raise_()
        self.AboutLabel_MainVer.raise_()
        self.AboutLabel_SpolEnvVer.raise_()
        self.AboutLabel_SpolVer.raise_()
        self.AboutLabel_SubVer.raise_()
        self.AboutLabel_Support.raise_()
        self.CheckUpdateButton.raise_()

        #隐藏关于页面
    def HideAboutPage(self):
        self.OPAboutLabel_MainVer=QGraphicsOpacityEffect()
        self.OPAboutLabel_MainVer.setOpacity(0)
        self.AboutLabel_MainVer.setGraphicsEffect(self.OPAboutLabel_MainVer)

        self.OPAboutLabel_SubVer=QGraphicsOpacityEffect()
        self.OPAboutLabel_SubVer.setOpacity(0)
        self.AboutLabel_SubVer.setGraphicsEffect(self.OPAboutLabel_SubVer)

        self.OPAboutLabel_FullVer=QGraphicsOpacityEffect()
        self.OPAboutLabel_FullVer.setOpacity(0)
        self.AboutLabel_FullVer.setGraphicsEffect(self.OPAboutLabel_FullVer)

        self.OPAboutLabel_SpolVer=QGraphicsOpacityEffect()
        self.OPAboutLabel_SpolVer.setOpacity(0)
        self.AboutLabel_SpolVer.setGraphicsEffect(self.OPAboutLabel_SpolVer)

        self.OPAboutLabel_SpolEnvVer=QGraphicsOpacityEffect()
        self.OPAboutLabel_SpolEnvVer.setOpacity(0)
        self.AboutLabel_SpolEnvVer.setGraphicsEffect(self.OPAboutLabel_SpolEnvVer)

        self.OPAboutLabel_BuildVer=QGraphicsOpacityEffect()
        self.OPAboutLabel_BuildVer.setOpacity(0)
        self.AboutLabel_BuildVer.setGraphicsEffect(self.OPAboutLabel_BuildVer)

        self.OPAboutLabel_Developers=QGraphicsOpacityEffect()
        self.OPAboutLabel_Developers.setOpacity(0)
        self.AboutLabel_Developers.setGraphicsEffect(self.OPAboutLabel_Developers)

        self.OPAboutLabel_Support=QGraphicsOpacityEffect()
        self.OPAboutLabel_Support.setOpacity(0)
        self.AboutLabel_Support.setGraphicsEffect(self.OPAboutLabel_Support)

        self.OPAboutLabel_Donate=QGraphicsOpacityEffect()
        self.OPAboutLabel_Donate.setOpacity(0)
        self.AboutLabel_Donate.setGraphicsEffect(self.OPAboutLabel_Donate)

        self.OPCheckUpdateButton=QGraphicsOpacityEffect()
        self.OPCheckUpdateButton.setOpacity(0)
        self.CheckUpdateButton.setGraphicsEffect(self.OPCheckUpdateButton)

        self.BackButton.clicked.disconnect(self.ShowSettingsPage)
        self.BackButton.clicked.disconnect(self.HideAboutPage)
        self.CheckUpdateButton.clicked.disconnect(self.CheckingUpdate)
        self.AboutLabel_Donate.setOpenExternalLinks(False)

        #展示小工具页
    def ShowToolsPage(self):
        self.PageName="Tools_Page"
        self.SAToSpolButton=QGraphicsDropShadowEffect()
        self.SAToSpolButton.setOffset(0,0)
        self.SAToSpolButton.setColor(QColor(0,0,0,100))
        self.SAToSpolButton.setBlurRadius(20)
        self.ToSpolButton.setGraphicsEffect(self.SAToSpolButton)

        self.SAClrWrongButton=QGraphicsDropShadowEffect()
        self.SAClrWrongButton.setOffset(0,0)
        self.SAClrWrongButton.setColor(QColor(0,0,0,100))
        self.SAClrWrongButton.setBlurRadius(20)
        self.ClrWrongButton.setGraphicsEffect(self.SAClrWrongButton)

        self.SAClrCacheButton=QGraphicsDropShadowEffect()
        self.SAClrCacheButton.setOffset(0,0)
        self.SAClrCacheButton.setColor(QColor(0,0,0,100))
        self.SAClrCacheButton.setBlurRadius(20)
        self.ClrCacheButton.setGraphicsEffect(self.SAClrCacheButton)

        self.BackButton.clicked.connect(self.ShowFirstPage)
        self.BackButton.clicked.connect(self.HideToolsPage)
        self.ToSpolButton.clicked.connect(self.ChooseToSpolFile)
        self.ClrWrongButton.clicked.connect(self.ClearWrongImage)
        self.ClrCacheButton.clicked.connect(self.ClearAllCacheImage)

        self.ClrCacheButton.raise_()
        self.ClrWrongButton.raise_()
        self.ToSpolButton.raise_()

        #隐藏小工具页
    def HideToolsPage(self):
        self.OPToSpolButton=QGraphicsOpacityEffect()
        self.OPToSpolButton.setOpacity(0)
        self.ToSpolButton.setGraphicsEffect(self.OPToSpolButton)

        self.OPClrWrongButton=QGraphicsOpacityEffect()
        self.OPClrWrongButton.setOpacity(0)
        self.ClrWrongButton.setGraphicsEffect(self.OPClrWrongButton)

        self.OPClrCacheButton=QGraphicsOpacityEffect()
        self.OPClrCacheButton.setOpacity(0)
        self.ClrCacheButton.setGraphicsEffect(self.OPClrCacheButton)

        self.BackButton.clicked.disconnect(self.ShowFirstPage)
        self.BackButton.clicked.disconnect(self.HideToolsPage)
        self.ToSpolButton.clicked.disconnect(self.ChooseToSpolFile)
        self.ClrWrongButton.clicked.disconnect(self.ClearWrongImage)
        self.ClrCacheButton.clicked.disconnect(self.ClearAllCacheImage)

        #返回启动UI命令
    def LaunchUI(self):
        global TopwinControl
        TopwinControl="ui"
        self.Shrink()
        tm.sleep(0.5)
        qApp=QApplication.instance()
        qApp.quit()

        #窗口展开实现函数
        #我去**的在另外线程实现for耗时操作，程序动画的时候别tm乱动！
    def Expand(self):
        self.OPTitlelabel=QGraphicsOpacityEffect()
        for i in range(0,101,2): 
            a=0.5*(1-ma.cos(i*0.0314159))
            self.setGeometry(QRect(600,int(400-a*200),700,int(300+a*350)))
            self.OPTitlelabel.setOpacity(1-i/100)
            self.Titlelabel.setGraphicsEffect(self.OPTitlelabel)
            self.Iconlabel.setGeometry(QRect(int(50+170*a),15,270,270))
            self.repaint()
            self.Titlelabel.repaint()
            self.Iconlabel.repaint()
            tm.sleep(0.01)

        #窗口收起实现函数
    def Shrink(self):
        self.OPTitlelabel=QGraphicsOpacityEffect()
        for i in range(100,-1,-2): 
            a=0.5*(1-ma.cos(i*0.0314159))
            self.setGeometry(QRect(600,int(400-a*200),700,int(300+a*350)))
            self.OPTitlelabel.setOpacity(1-i/100)
            self.Titlelabel.setGraphicsEffect(self.OPTitlelabel)
            self.Iconlabel.setGeometry(QRect(int(50+170*a),15,270,270))
            self.repaint()
            self.Titlelabel.repaint()
            self.Iconlabel.repaint()
            tm.sleep(0.01)

        #选择新的语言文件，并且刷新所有的Button文本
    def ChooseLangFile(self):
        self.LangFileDialog=QFileDialog.getOpenFileName(self,msg("Ui_Msg_Choose_Lang"), "./lang","Story Player Language(*.splang)")
        self.LangFileName=self.LangFileDialog[0].split("/")[-1].split(".")[0]
        self.Service.ui_langset(self.LangFileName)
        self.Titlelabel.setText(msg("Ui_Msg_Title"))
        self.BackButton.setText(msg("Ui_Msg_Back"))
        self.ExitButton.setText(msg("Ui_Msg_Exit"))
        self.AboutButton.setText(msg("Ui_Msg_About_"))
        self.LangButton.setText(msg("Ui_Msg_Choose_Lang"))
        self.ToolsButton.setText(msg("Ui_Msg_Tools"))
        self.SettingsButton.setText(msg("Ui_Msg_Settings"))
        self.UIModeButton.setText(msg("Ui_Msg_LaunchUI"))
        self.ToSpolButton.setText(msg("Ui_Msg_To_Spol"))
        self.ClrCacheButton.setText(msg("Ui_Msg_Clear_All"))
        self.ClrWrongButton.setText(msg("Ui_Msg_Clear_Wrong"))

        self.AboutLabel_FullVer.setText(msg("About_Info_Version")+Edition)
        self.AboutLabel_MainVer.setText(msg("About_Info_Main_Ver")+InsiderMainVer)
        self.AboutLabel_SubVer.setText(msg("About_Info_Sub_Ver")+InsiderSubVer)
        self.AboutLabel_BuildVer.setText(msg("About_Info_Build_Ver")+InsiderBuildVer)
        self.AboutLabel_SpolVer.setText(msg("About_Info_Spol_Ver")+InsiderSPOLVer)
        self.AboutLabel_SpolEnvVer.setText(msg("About_Info_Spol_Env_Ver")+InsiderSPOLEnvVer)
        self.AboutLabel_Developers.setText(msg("About_Info_Developers")+"青雅音")
        self.AboutLabel_Support.setText(msg("About_Info_Support")+"亿绪联合协会 UYXA")
        self.AboutLabel_Donate.setText(msg("About_Info_Donate").format("<A href='"+urlAFD+"'>"+urlAFD+"</a>"))
        self.CheckUpdateButton.setText(msg("Ui_Msg_Check_Update"))

        try:
            self.UpdateDialog.UpdateLang()
        except:
            None
        else:
            None
        #调用HL解释器把官方文件转换成SPOL
    def ChooseToSpolFile(self):
        self.LangFileDialog=QFileDialog.getOpenFileName(self,msg("Ui_Msg_To_Spol"), "./arknights/story","Arknights Official Story(*.txt)")
        self.LangFileName=self.LangFileDialog[0].split("/")[-1].split(".")[0]
        self.Service.ui_Tospol(self.LangFileName)

        #调用aaspcommand清理损坏图像
    def ClearWrongImage(self):
        self.Service.ui_DeleteEmptyMap()

        #调用aaspcommand清理所有缓存
    def ClearAllCacheImage(self):
        self.Service.ui_DeleteAllCache()

    def CheckingUpdate(self):
        Update=self.Service.ui_CheckUpdate()
        if Update!=0:
            self.UpdateDialog=UpdateWindow(Update)
            self.UpdateDialog.show()

        #键盘按下事件
    def keyPressEvent(self,QKeyEvent):
        #当首次展开执行完毕后允许使用快捷键
        if self.FirstEnter==1:
            if QKeyEvent.key()==Qt.Key_Escape:
                self.FullExit()

      #首次移入时展开页面
    def enterEvent(self, QEvent):
        if self.FirstEnter==0:
            self.Expand()
            self.FirstEnter=1
            
      #退出交互页面
    def ExitPro(self):
        self.Shrink()
        tm.sleep(0.5)
        self.close()
        qApp=QApplication.instance()
        qApp.quit()

        #退出整个程序
    def FullExit(self):
        global TopwinControl
        TopwinControl="exit"
        self.Shrink()
        tm.sleep(0.5)
        self.close()
        qApp=QApplication.instance()
        qApp.quit()

        #显示任意提示信息
    def ShowAnyInfo(self,infogroup=0,needtoshow="UNKNOWN INFO"):
        for i in range(0,101,8):
            a=0.5*(1-ma.cos(i*0.0314159))
            self.setGeometry(QRect(600,200,700,int(650+a*50)))
            self.repaint()
            tm.sleep(0.01)
        if infogroup==0:
            self.AnyInfolabel.setStyleSheet(
            """QLabel{
            background-color:rgba(255,255,255,0);
            border:none;
            border-radius:0px;
            text-align:center;
            color:#000000;
            font-family:'Microsoft YaHei';
            font-size:30px;
            }""")
        elif infogroup==1:
            self.AnyInfolabel.setStyleSheet(
            """QLabel{
            background-color:rgba(255,255,255,0);
            border:none;
            border-radius:0px;
            text-align:center;
            color:#4488FF;
            font-family:'Microsoft YaHei';
            font-size:30px;
            }""")
        elif infogroup==2:
            self.AnyInfolabel.setStyleSheet(
            """QLabel{
            background-color:rgba(255,255,255,0);
            border:none;
            border-radius:0px;
            text-align:center;
            color:#CC2211;
            font-family:'Microsoft YaHei';
            font-size:30px;
            }""")
        self.AnyInfolabel.setText(needtoshow)
        self.OPAnyInfolabel=QGraphicsOpacityEffect()
        self.OPAnyInfolabel.setOpacity(1)
        self.AnyInfolabel.setGraphicsEffect(self.OPAnyInfolabel)
        self.AnyInfolabel.repaint()
        tm.sleep(1.5)
        self.OPAnyInfolabel=QGraphicsOpacityEffect()
        self.OPAnyInfolabel.setOpacity(0)
        self.AnyInfolabel.setGraphicsEffect(self.OPAnyInfolabel)
        self.AnyInfolabel.setText("")
        self.AnyInfolabel.repaint()

        for i in range(101,2,-8):
            a=0.5*(1-ma.cos(i*0.0314159))
            self.setGeometry(QRect(600,200,700,int(650+a*50)))
            self.repaint()
            tm.sleep(0.01)

def TopWin():
    try:
        del app
    except:
        None
    else:
        None
    app=QApplication(sys.argv)
    ui=TopWindow()
    ui.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        None
    else:
        None   
    del app
    global TopwinControl
    return TopwinControl


