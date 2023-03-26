
__author__ = "Yong Peng"
__version__ = "1.0"


import time
import re
import getpass
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

with open('./device_list.txt','r') as f:
    device_list = [i.strip() for i in f.readlines() if len(i.strip()) != 0]    # read the device list.


print("Data will be collected on below switches:")
for device in device_list:
    print(device)

go = input("\nPress y to continue: ")

if go != "y" and go != "Y":
    exit(2)

u_id = input("Please input login ID:")
factor_1 = getpass.getpass("ID Password for login:")

cmd_4_run = ['show run']

"""
配置检查标记.
"""
header = re.compile("^vlan \d{1,4} .* by port$")
check_point = "loop-detection"


def send_show_command(device, commands):
    OutputPath = 'c:/script/output/' + str(device['host']) + '.txt'
    result = open(OutputPath, 'w')
    flag = True
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            for command in commands:
                output = ssh.send_command(command,  strip_command=False, strip_prompt=False)
                result.write(output + "\n" + 30 * '+' + "\n" + "\n")

    except Exception as error:
        print(error)
        flag = False
    result.close()
    if flag:
        print("Data collection on %s is done. \n \n" % (i))
    else:
        print("Data collection for %s is NOT done. \n \n" % (i))

"""
配置检查函数. 逐行检查生成一个字典, 标志行为k, v为具体配置组成的列表.
如下例，读取标志行"vlan x name y by port"为key, 读取配置放入列表, 以"!"为界. 如:
!
vlan 100 name NetMGMT by port
 tagged lag 10 
 router-interface ve 100
 spanning-tree 802-1w
 loop-detection
!
vlan 148 name 10.71.148.0/22_NewPrinter by port
 tagged lag 10 
 spanning-tree 802-1w
 loop-detection
!
"""

def config_check():
    vlan_dict = dict()
    config_list = []
    flag = True
    with open('c:/script/output/' + str(i) + ".txt", "r") as f:
        for j in f.readlines():
            j = j.strip()
            if re.match(header, j):
                k = j
                vlan_dict[k] = config_list
                flag = False

            if not re.match(header, j) and not flag:
                if j == "!":
                    flag = True
                    config_list = []    # 清空列表，供下一轮使用
                    continue
                else:
                    vlan_dict[k].append(j)
    return vlan_dict

switch = {}
for i in device_list:
    switch["device_type"] = "ruckus_fastiron"
    switch["host"] = i
    switch["username"] = u_id
    factor_2 = input("Trying to login to %s, enter DUO Code:"%(i))
    switch["password"] = str(factor_1) + str(factor_2)
    switch['secret'] = ''
    switch['port'] = 22
    send_show_command(switch, cmd_4_run)    # "show run" collection

    check_result = config_check()   # check configuration

    with open("c:/script/output/check_result.txt", "a") as f:
        f.write("\n\n\n" + switch["host"] + ":\n")
        for x, y in check_result.items():
            if check_point not in y:
                f.write(x +"\n" + " loop-detection\n")


print("All collection is done.")