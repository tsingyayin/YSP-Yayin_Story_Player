#这个文件构成命令页交互
from command.aaspcommand import *
from arknights.HLtoSPOL import *
from langcontrol import *
from Visual.ArtificialUI import SPLASHES
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import platform
import traceback
import time as tm
import sys
import os
from crashreport import *

sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore")
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore\command")
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore\core")
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore\lang")
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore\Visual")

if __name__=="__main__":
    DirectOpen=0
    if sys.argv.__len__() >=2:
        DirectOpen=1
        Usript="ui"

try:
  #查看目录体系是否正常
  ensuredirs(0)

  #初始化语言
  langset(0)

  #启动时尝试清理损坏图像
  DeleteEmptyMap(0)

  print("sysinfo→"+msg("System_Info"),platform.platform())
 #系统版本判断
  System_name=platform.platform().split("-")[0]
  System_VersionMain=platform.version().split(".")[0]+"."+platform.version().split(".")[1]
  System_VersionNum=platform.version().split(".")[2]


  #if System_VersionMain!="10.0":
      #print(msg("System_Not_Win10").format(platform.version().split(".")[0]))
      #app=QApplication(sys.argv)
        
      #sys.exit(app.exec_())


  #if int(System_VersionNum)<16299 and System_VersionMain=="10.0":
      #print(msg("System_Win10_Too_Old").format(System_VersionNum))
      #app=QApplication(sys.argv)
        
    #sys.exit(app.exec_())
#第一指引
  print("sysinfo→"+msg("First_Print"))

#主识别循环
  programme_end=0

  while programme_end==0 :
    if DirectOpen!=1:
        Usript=input("Userinput→")

    if Usript=="help":
        aasphelp()

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

    elif Usript=="clear":
        DeleteEmptyMap(1)

    elif Usript=="clrall":
        DeleteAllCache(1)

    elif Usript=="tospol":
        HLtoSPOL()

    elif Usript=="exception":
        raise Exception

    elif Usript=="exit":
        break

    else:
        print("sysinfo→"+msg("Command_Error").format(Usript))

except:
   CrashReport()

else:
    print("Safety Exit")
