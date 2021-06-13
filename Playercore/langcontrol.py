#这个文件负责解决语言问题
import sys
import os
import time
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore")
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore\command")
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore\core")
sys.path.append(r"C:\Users\Administrator\source\repos\PlayerCore\PlayerCore\lang")
def langset(langname):
    langnameraw=langname
    #如果是初始化，就调用初始化
    if langnameraw==0:
        global languse
        langlast=open("lang\\base.ini","r")
        langname=langlast.readlines()[0][:-1]
        langlast.close()
    try:
        #尝试打开这个语言文件
        languse=open("lang\\"+langname+".splang","r")
    except IOError:
        #如果是用户问题就返回修改
        if langnameraw != 0:
            print("sysinfo→"+msg("Lang_Not_In_Support").format(langname))
            return 0
        #如果是初始化出问题就默认重置为zh_CN
        else:
            languse=open("lang\\zh_SC.splang","r")
            langname="zh_SC"
            os.remove("lang\\base.ini")
            langlast=open("lang\\base.ini","w+")
            langlast.write(langname)
            langlast.close()
    #如果没有任何问题且不是初始化就把用户键入记下来
    else:
        if langname !=0:
            os.remove("lang\\base.ini")
            langlast=open("lang\\base.ini","w+")
            langlast.write(langname+"\n")
            langlast.close()
    #把文件写入字典
    global msglist
    msglist={}
    languse=langname
    readlang=open("lang\\"+languse+".splang","r")
    loadlangtime=time.time()
    for line in readlang.readlines():
        try:
            if line[0]!="#" or line[0]!="\n" :
                if line[-1]!="\n":line+="\n"
                msgstandard=line[:line.index(":")]
                msginlang=line[line.index(":")+1:-1]
                msglist[msgstandard]=msginlang
        except Exception:
            msglist["UNKNOWNLIST"]="UNKNOWNMSG_IN_FILE"
        else:
            None
    print("sysinfo→"+msg("First_Print_Load_Lang_End").format(round(1000*(time.time()-loadlangtime),2)))
    #成功返回
    return 1
        

def msg(msginfo):
    global msglist
    try:
        return msglist[msginfo]
    except Exception:
        return "UNKNOWN_MSG:"+msginfo
    else:
        None