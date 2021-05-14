#这个文件构成命令页交互
import sys
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore")
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore\command")
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore\core")
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore\lang")
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore\Visual")
from command.aaspcommand import *
from langcontrol import *
from Visual.ArtificialUI import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
#初始化语言
langset(0)
#第一指引
print("sysinfo→"+msg("First_Print"))

if __name__=="__main__":
    DirectOpen=0
    if sys.argv.__len__() >=2:
        DirectOpen=1
        Usript="ui"

#主识别循环
programme_end=0
while programme_end==0 :
    if DirectOpen!=1:
        Usript=input("Userinput→")

    if Usript=="help":
        print("help"+"\t"+msg("Help_In_Main_Page_help"))
        print("spawn"+"\t"+msg("Help_In_Main_Page_spawn"))
        print("line"+"\t"+msg("Help_In_Main_Page_line"))
        print("exit"+"\t"+msg("Help_In_Main_Page_exit"))
        print("lang"+"\t"+msg("Help_In_Main_Page_lang"))
        print("about"+"\t"+msg("Help_In_Main_Page_about_"))
        print("ui"+"\t"+msg("Help_In_Main_Page_ui"))
    elif Usript=="":
        continue
    elif Usript=="spawn":
        spawn()
    elif Usript=="line":
        singletext()
    elif Usript=="lang":
        langinput()
    elif Usript=="about":
        about()
    elif Usript=="ui":
        if __name__=="__main__":
            app=QApplication(sys.argv)
            Mainwindow=MainWindow()
            Mainwindow.showFullScreen()
            sys.exit(app.exec_())
    elif Usript=="exit":
        break
    
    else:
        print("sysinfo→"+msg("Command_Error").format(Usript))

