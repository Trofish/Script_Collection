"""
based on py3.8.1
1.将脚本放与配置收集.log文件同一目录运行
2.*.txt为预配，Check.txt为未启用认证的access接口列表(不检查trunk)
3.换配置文件后无需手动删除 .txt
2020-02-14  V1.1
"""

import re
import os

##遍历名为".log"的配置文件名

FName = os.popen("dir *.log | find \"log\" ")
FNameList = []
for i in FName:
    FNameList.append(i.split(" ")[-1].strip())


##生成新的输出配置文件名

Name = re.compile("[a-zA-Z].*")

#列表解析[i for i in range(1,10)],但第一个i做修改

FNameNew = [Name.findall(i)[0].replace("log","txt") for i in FNameList]
# print(FNameNew)

List = list(zip(FNameList, FNameNew)) #新旧文件名的元组列表
print(List)

##准备变量

Interface = re.compile("^interface .*/[0-9]{1,2}$")


##创建一个空文件用来记录未起认证的access接口
with open("Check.txt", "w+") as Check:
    pass


##funcction 接口配置收集
def prod(x,y):
    Flag = False #遍历接口配置用的Mark
    print(x, y)
    
    L1 = [] #存放接口配置
    L2 = [] #存放接口列表索引

    # with open(x,"r") as Conf, open(y, "w+") as PreConf:
    Conf = open(x,"r")
    PreConf = open(y, "w+")
    Check = open("Check.txt", "a+")

    for line in Conf:
        if line.startswith("hostname"):
            PreConf.write(line.split(" ")[1].strip()+"  !!!!!!!!\n\n\n")
            Check.write(line.split(" ")[1].strip() + "  !!!!!!!!\n\n\n")
        elif re.match(Interface, line):
            Flag = True
        elif line.startswith("!"):
            Flag = False

        if Flag:
            L1.append(line)

##funcction 为每接口创建列表索引
    for x,y in enumerate(L1):
        # print(L1)
        if str(y).startswith("interface"):
            L2.append(x)

    L2.append(len(L1) -1)
    # print(L2)

##将每接口配置放入list L3
    N = 0
    L3 = []

    while N < (len(L2)-1):
        # print(L2[N],L2[N+1])

        for i in range(L2[N],L2[N+1]):
            L3.append(L1[i].strip())


##从L3检查每接口配置并输出到文件

        if "switchport mode access" and "authentication port-control auto" in L3:
            PreConf.write(L3[0] + "\n" + "authentication violation replace\n\n")
            L3.clear()

        elif "switchport mode access" in L3 and "authentication port-control auto" not in L3:
            Check.write(L3[0] + "\n" )
            L3.clear()

        else:
            L3.clear()

        N += 1


    PreConf.close()
    Check.close()


for a,b in List:
    prod(a,b)





