import core
import time as tm
def spawn():
    Open=False
    while Open==False:
        try:
            print("sysinfo→请输入剧情文件名称，或者用exit退出")
            Storyname=input(r"Userinput\spawn→")
            files=open(Storyname,"r")
        except IOError:
            print("sysinfo→找不到文件{}，请检查输入是否正确或文件是否存在。请注意文档名不区分大小写。".format(Storyname))
        else:
            Open=True
    Ver=""
    #用来确标题是否读取完毕
    TitleSure=0
    SubtitleSure=0
    timestart=0

    for line in files.readlines():
        if (line[0]=="#" and line[0:3]!="###") or line[0]=="\n" or line[0]==" ":continue
        #用来确认遵循版本号
        elif line[0]=="/": 
            Ver=line[1:-1]
            print("文档的版本是",Ver)
        #标题和副标题，获取完毕后就用Sure锁死这两个elif
        elif line[0]==":"and TitleSure==0:
            Title=line[1:-1]
            print("剧情标题是:",Title)
            TitleSure=1
        elif line[0]==":"and SubtitleSure==0:
            Subtitle=line[1:-1]
            print("剧情标题副标题是:",Subtitle)
            TitleSure=1
            print("\n")
            timestart=tm.time()
            break


#重新打开文件，从头开始处理
    files=open(Storyname,"r")

    if Ver=="SPOL0.3":                                                         #遵循SPOL0.3标准的读取
        core.SPOL0_3(files,timestart)

    elif Ver=="SPOL0.2.5":                                                    #遵循SPOL0.2.5标准的读取
        print("sysinfo→由于SPOL0.3增强了程序对异常的抗性，为了防止测试0.3过程中造成不必要崩溃，所以0.2.5版本直接移除。")

    else:
        print("没有在解释器中找到{}这个版本，请检查拼写，或者检查本版程序是否支持这个版本".format(Ver))
        print("解释器内曾把所有的AASD，AASP前缀全部替换成了SPOL，请检查您的前缀是否为SPOL")


    files.close()
    print("sysinfo→读取完毕,按下回车键回到首页面")
    input()

def singletext():
    while True:
        print("sysinfo→请指定使用标准，输入help查询标准")
        linestandard=input(r"Userinput\line→")
        if linestandard=="help":
            print("""现在支持版本如下：
0.3
0.2.5（已停止支持）""")
        elif linestandard=="0.2.5":
            print("sysinfo→由于SPOL0.3增强了程序对异常的抗性，为了防止测试0.3过程中造成不必要崩溃，所以0.2.5版本直接移除。")
        elif linestandard=="0.3":
            while True:
                Usrtextipt=input(r"Userinput\line\SPOL0.3→")
                if Usrtextipt=="exit":
                    break
                else:
                    core.SPOL_s_0_3(Usrtextipt+"\n")
        elif linestandard=="exit":
            break
        else:
            print("sysinfo→未能将“{}”识别为可用版本或程序指令".format(linestandard))
