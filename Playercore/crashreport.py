import time as tm
import traceback
import platform
import psutil
from command.aaspcommand import *

def CrashReport():
    timeinfo=""
    count=0
    for i in tm.localtime(tm.time()):
        if count == 6:break
        timeinfo+=str(i)+"_"
        count+=1
    timeinfo=timeinfo[:-1]
    traceback.print_exc()
    mem= psutil.virtual_memory()
    mem1=mem.total/1024/1024/1024
    mem2=mem.free/1024/1024/1024
    System_name=platform.platform()
    f=open(".\\CrashReport\\CrashReport"+timeinfo+".txt","w+")
    f.writelines("Program:"+Edition+"\n")
    f.writelines("System:"+System_name+"\n")
    f.writelines("CPU Physical Core:"+str(psutil.cpu_count(logical=False))+"\n")
    f.writelines("CPU Logical Core:"+str(psutil.cpu_count())+"\n")
    f.writelines("Total Memory:"+str(round(mem1,2))+"GiB\n")
    f.writelines("Free Memory:"+str(round(mem2,2))+"GiB\n")
    f.writelines("###################\n")
    f.writelines("Python Traceback Module\n")
    f.writelines("###################\n")
    traceback.print_exc(file=f)
    f.close()
    
    print("###########################")
    print("Oops!")
    print("哎呀！")
    print("###########################")
    print("YSP encountered a FATAL ERROR and CANNOT be recovered")
    print("程序遇到了无法恢复的致命性错误")
    print("###########################")
    print("The Infomation above may help you,we have saved it as a document:CrashReport"+timeinfo+".txt")
    print("上面的信息也许可以帮助你,我们已经将其保存入文件：CrashReport"+timeinfo+".txt")
    print("###########################")
    
    input()

