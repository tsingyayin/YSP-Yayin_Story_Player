#本函数库用于解决一些通用性质的操作
#本库标准名称是commonedit，建议import commonedit as comet
#我本来想写一点靠谱的异常报错来着，但是它貌似在Visual Studio开发环境下会直接跳转到异常定义行
#这就没意思了......

class SetERROR(Exception):
    pass

#把字符串的文本和数字分离：
ipt=""
def sepa(ipt,ways):
    len(ipt)
    insiderD=0
    if ways=="toga":
      opt1=""
      opt2=""
      while insiderD<len(ipt):
        if ipt[insiderD].isalpha()==1:
            opt1+=ipt[insiderD]
        elif ipt[insiderD].isalnum()==1:
            opt2+=ipt[insiderD]
        insiderD += 1
      return [opt1,opt2]         #先返回文本串，再返回数字串
    if ways=="sigl":
      opt1=[]
      opt2=[]
      while insiderD<len(ipt):
        if ipt[insiderD].isalpha()==1:
            opt1+=[ipt[insiderD]]
        elif ipt[insiderD].isalnum()==1:
            opt2+=[ipt[insiderD]]
        insiderD += 1
      return [opt1,opt2]         #先返回单个文本，再返回单个数字

#计算三角形面积
def triangle_area(a,b,c):
    import math as ma
    p=0.5*(a+b+c)
    area=ma.sqrt(p*(p-a)*(p-b)*(p-c))
    return area                    #返回三角形面积

#给输入限定范围
def inrange(num1,num2,operator_1,operator_2):
    op1=op2=0
    if operator_1.upper()=="T":
        insop1="等于"
        op1=1
    elif operator_1.upper()=="F":
        insop1=""
    else:
        raise SetERROR("没有正确使用布尔值（T或F）")
    if operator_2.upper()=="T":
        insop2="等于"
        op2=1
    elif operator_2.upper()=="F":
        insop2=""
    else:
        raise SetERROR("没有正确使用布尔值（T或F）")
    if num1 > num2:
        raise SetERROR("没有正确设置端点值，可能是左端点大于或大于等于了右端点")
                                             #这个函数有很多地方其实可以使用eval来解决，为了防止出现注入就舍弃了eval方法
    INPUT_END=0
    while INPUT_END==0:
        final=float(input("请输入数字，范围是大于{}{}且小于{}{}：".format(insop1,num1,insop2,num2)))
        if (op1==1 and final==num1) or (op2==1 and final==num2) or (final>num1 and final<num2):
            last=final
            INPUT_END=1
        else:
            print("您的输入不在范围内，请重新输入")
    return last

#给输入限定类型
#如果想的话，这个写法还能再简单一点
def intype(input_type):
    INPUT_END=0
    while INPUT_END==0:
         INPUTWRONG=0
         if input_type=="lower_text":
             back=input("请输入全小写字符")
             if back.islower()==1 : INPUT_END=1 
             else: INPUTWRONG=1
         elif input_type=="upper_text":
             back=input("请输入全大写字符")
             if back.isupper()==1 : INPUT_END=1
             else: INPUTWRONG=1
         elif input_type=="num":
             back=input("请输入数字")
             if back.isalnum()==1 : INPUT_END=1
             else: INPUTWRONG=1
         elif input_type=="alpha":
             back=input("请输入字母")
             if back.isalpha()==1 : INPUT_END=1
             else: INPUTWRONG=1
         else:
             raise SetERROR("没有设置正确的类型")
         if INPUTWRONG==1:
             print("您的输入不符合格式要求，请重新输入")
             INPUT_END=0
    return back

#运算兔子数列
def rabbit(num):
    if num<1:
        raise SetERROR("没有设置正确的斐波那契数列项数")
    i=0
    rab=[1,1]
    while i<(num//2):
        rab[1]+=rab[0]
        rab[0]+=rab[1]
        i += 1
    return rab[not num%2]             #别问为啥有个not，问就是上面的rab1和0写反了

#交换字典的值和键
dictionary={}
def dichange(dictionary):
    change=[(a,b) for b,a in dictionary.items()]
    return dict(change)

#首字母大写，后续小写
anytype=""
def firstword(anytype):
    return anytype[0].upper()+anytype[1:].lower()





