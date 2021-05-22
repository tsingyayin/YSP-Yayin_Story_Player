#这个文件构成命令页交互
import sys
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore")
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore\command")
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore\core")
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore\lang")
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore\Visual")
from command.aaspcommand import *
from langcontrol import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import platform

#初始化语言
langset(0)

print("sysinfo→"+msg("System_Info"),platform.platform())


if __name__=="__main__":
    DirectOpen=0
    if sys.argv.__len__() >=2:
        DirectOpen=1
        Usript="ui"


#系统版本判断
System_name=platform.platform().split("-")[0]
System_VersionMain=platform.version().split(".")[0]+"."+platform.version().split(".")[1]
System_VersionNum=platform.version().split(".")[2]


if System_VersionMain!="10.0":
    print(msg("System_Not_Win10").format(platform.version().split(".")[0]))
    app=QApplication(sys.argv)
        
    sys.exit(app.exec_())


if int(System_VersionNum)<16299 and System_VersionMain=="10.0":
    print(msg("System_Win10_Too_Old").format(System_VersionNum))
    app=QApplication(sys.argv)
        
    sys.exit(app.exec_())
#第一指引
print("sysinfo→"+msg("First_Print"))

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
            monitor_range=ui()
            if monitor_range[0]<1440 or monitor_range[1]<900:
                print("sysinfo→"+msg("Screen_Too_Small").format(monitor_range[0],monitor_range[1]))
                #break
            else:
                Mainwindow=MainWindow()
                Mainwindow.showFullScreen()
                sys.exit(app.exec_())
    elif Usript=="exit":
        break
    
    else:
        print("sysinfo→"+msg("Command_Error").format(Usript))

