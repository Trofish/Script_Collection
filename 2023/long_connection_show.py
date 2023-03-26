__author__ = "Yong Peng"
__version__ = "1.0"


import time
import re
import getpass
import time
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

device_name = "xxx-co-01"
u_id = "yong.peng@xxx"
factor_1 = getpass.getpass("Please input pwd for ID:")
factor_2 = input("Please input DUO code:")
pwd = str(factor_1) + str(factor_2)
commands = ['show clock', 'ping 8.8.8.8 source 10.xx.xx.1 count 10', 'ping 10.xx.x.x source 10.xx.xx.1 count 10']

def send_show_command(device, commands):
    outputPath = device_name + '.txt'
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        while True:
            result = open(outputPath, 'a')
            for cmd in commands:
                output = ssh.send_command(cmd,  strip_command=False, strip_prompt=False)
                result.write(output + "\n" + 30 * '+' + "\n" + "\n")
            result.close()
            time.sleep(30)

switch = {}
switch["device_type"] = "cisco_ios"
switch["host"] = device_name
switch["username"] = u_id
switch["password"] = pwd
switch['secret'] = '',
switch['port'] = 22
send_show_command(switch, commands)
