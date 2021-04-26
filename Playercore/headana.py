#在我把窗体里面，尤其是PyQt下的编写整明白之前，
#先用这个工程完成基本的标准化剧情文件处理测试。
import sys
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore")
import core 
from aaspcommand import *

print("AASP命令提示符(伪)模式,用help查询现有命令")
programme_end=0
while programme_end==0 :
    Usript=input("Userinput→")

    if Usript=="help":
        print("""help\t用来查询支持的指令列表
spawn\t进入文件解释模式
line\t进入剧情文本单行测试模式
exit\t退出程序（或程序的任一一级）""")
    elif Usript=="":
        continue
    elif Usript=="spawn":
        spawn()
    elif Usript=="line":
        singletext()
    elif Usript=="exit":
        break
    else:
        print("sysinfo→未知的指令{}，请重试。".format(Usript))