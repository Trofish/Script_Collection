
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


# cmd_4_IOS = ['show version | in from','show stack','show flash',\
#              'show license', 'show boot-preference',\
#              'show ip bgp summ', 'show interface brief',\
#              'show ip inter', 'show vlan',\
#              'show vlan brief', 'show lag', 'show lag brief',\
#              'show lldp neighbor', 'show 802-1w', 'show ip route',\
#              'show run']
# cmd_4_IOS = ['show version | in from', 'show flash | in Pri Code|Sec Code']
# cmd_4_IOS = ['show vlan brief', 'show ip interface', 'show version | in from', 'show ip osp inter brief',
#              'show run']n
# cmd_4_IOS = ['show vlan id 464']
with open("temp.txt",'r') as f:
    cmd_4_IOS = [i.strip() for i in f.readlines()]

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

switch = {}
for i in device_list:
    switch["device_type"] = "ruckus_fastiron"
    switch["host"] = i
    switch["username"] = u_id
    factor_2 = input("Trying to login to %s, enter DUO Code:"%(i))
    switch["password"] = str(factor_1) + str(factor_2)
    switch['secret'] = '',
    switch['port'] = 22
    send_show_command(switch, cmd_4_IOS)

print("All collection is done.")