#这个文件构成最顶层交互
import sys
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore")
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore\command")
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore\core")
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore\lang")
from core.core0_3 import *
from command.aaspcommand import *
from langcontrol import *
langset(0)
print(msg("First_Print"))
programme_end=0
while programme_end==0 :
    Usript=input("Userinput→")

    if Usript=="help":
        print("help"+"\t"+msg("Help_In_Main_Page_help"))
        print("spawn"+"\t"+msg("Help_In_Main_Page_spawn"))
        print("line"+"\t"+msg("Help_In_Main_Page_line"))
        print("exit"+"\t"+msg("Help_In_Main_Page_exit"))
        print("lang"+"\t"+msg("Help_In_Main_Page_lang"))
        print("about"+"\t"+msg("Help_In_Main_Page_about_"))
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
    elif Usript=="exit":
        break
    
    else:
        print("sysinfo→"+msg("Command_Error").format(Usript))