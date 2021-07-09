#这个文件构成命令页交互
#命令行作为直接交互的顶层交互逻辑已经弃用
#但是以指定命令作为调度程序各个方法的思路仍然保留
#这就是说，YSPMain作为TopWindow背后的功能实现平台。

from command.aaspcommand import *
from arknights.HLtoSPOL import *
from langcontrol import *
from Visual.ArtificialUI import *
from Visual.TopWindow import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import platform
import traceback
import threading
import time as tm
import sys
import os
from crashreport import *

sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore")
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore\command")
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore\core")
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore\lang")
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore\Visual")
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore\arknights")

DirectOpen=0
if sys.argv.__len__() >=2:
    DirectOpen=1
    Usript="ui"
else:
    DirectOpen=1
    Usript="window"

try:
  #查看目录体系是否正常
  ensuredirs(0)

  #初始化语言
  langset(0)

  #启动时尝试清理损坏图像
  DeleteEmptyMap(0)

  print("################")
  Checkupdate(0)
  print("################")

  print("sysinfo→"+msg("System_Info"),platform.platform())
  print("sysinfo→"+msg("About_Info_Version")+Edition)

 #系统版本判断
  System_name=platform.platform().split("-")[0]
  System_VersionMain=platform.version().split(".")[0]+"."+platform.version().split(".")[1]
  System_VersionNum=platform.version().split(".")[2]


  #下面两个if限制目标系统，应内测组要求暂时停用
  #不过鉴于开发过程已经迁移到Windows11，因此马上会开始限制系统为Windows10以上。
  #开发过程使用的Windows11内部构建号为22000.65，使用的最后一个Windows10内部构建号为21390.2025(21H2测试)
  #下文判断Windows10过老用的内部构建号是16299，这是2017年秋季更新内部构建号（如果没搞错的话）

  try:
      None
      if float(System_VersionMain)<10.0:
          print(msg("System_Not_Win10").format(platform.version().split(".")[0]))
          print("以上信息仅供测试系统限制，即将生效。\nThe information above is for testing system limitation only and will come into effect soon.")
          #raise Exception
      if int(System_VersionNum)<16299 and System_VersionMain=="10.0":
          print(msg("System_Win10_Too_Old").format(System_VersionNum))
          print("以上信息仅供测试系统限制，即将生效。\nThe information above is for testing system limitation only and will come into effect soon.")
          #raise Exception
  except:
      DirectOpen=1
      Usript="exit"
  else:
      None

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

    elif Usript=="lang":
        langinput()

    elif Usript=="about":
        about()

    elif Usript=="ui":
        LaunchUI()
        Usript="window"
        DirectOpen=1

    elif Usript=="window":
        Usript=TopWin()
        if Usript=="":
            DirectOpen=0
        else:
            DirectOpen=1

    elif Usript=="clear":
        DeleteEmptyMap(1)

    elif Usript=="clrall":
        DeleteAllCache(1)

    elif Usript=="tospol":
        HLtoSPOL(0)

    elif Usript=="update":
        Checkupdate(0)

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
    tm.sleep(0.5)
