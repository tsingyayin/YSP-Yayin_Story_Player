import time as tm
import traceback

def CrashReport():
    timeinfo=""
    count=0
    for i in tm.localtime(tm.time()):
        if count == 6:break
        timeinfo+=str(i)+"_"
        count+=1
    timeinfo=timeinfo[:-1]
    traceback.print_exc()
    f=open(".\\CrashReport\\CrashReport"+timeinfo+".txt","w+")
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

