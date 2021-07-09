import urllib.request
import os
import sys

def VersionList(Day,Edition):
    try:
        url = "https://qingyayin.lofter.com/"
        html = urllib.request.urlopen(url).read()
        f=open(".\\Latest.txt", "wb")
        f.write(html)
        f.close()
 
        file=open(".\\Latest.txt","r",encoding="UTF-8")
        editionlist=[]
        for i in file.readlines():
            if "宣布更新YSP程序" in i and "Ver" not in i:
                dayindex=i.index("宣布更新YSP程序")
                dayinfo=i[dayindex-8:dayindex]
            elif "宣布更新YSP程序内部版本到Ver" in i or "宣布更新YSP程序公开版本到Ver" in i:
                verindex_s=i.index("Ver")
                verindex_e=i.index("。")
                verinfo=i[verindex_s:verindex_e]

                if "Pre" in verinfo:
                    Subver="Pre"
                elif "Pub" in verinfo:
                    Subver="Pub"
                else:
                    Subver="Branch"

                if int(dayinfo)>=Day:
                    editionlist+=[[dayinfo,verinfo,Subver]]
        file.close()
        os.remove(".\\Latest.txt")
    except:
        return "ERROR"
    else:
        return editionlist