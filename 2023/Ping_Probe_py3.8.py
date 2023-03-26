#!/usr/bin/env python

import os
import multiprocessing
import time
import requests


Test_Target = {
"txx-04-fl-idb-3":"172.xx.xx.59",
"txx-04-fl-ida-9":"172.xx.xx.73",
"txx-02-fl-idb-21":"172.xx.xx.177",
"txx-04-fl-idc-9":"172.xx.xx.84",
"txx-02-fl-idr-fw-9":"172.x.x.253",
"txx-02-fl-ida-36":"172.x.x.236"
}

def Ping_Test(Name,IP_Addr):
    # Ping_Result = os.popen("ping -c 10 %s"%(IP_Addr))
    Ping_Result = os.popen("ping -n 10 %s"%(IP_Addr))
    with open("%s.txt"%(Name),'a') as f:
        f.write(time.strftime("%y-%m-%d_%H:%M:%S"))
        for i in Ping_Result.readlines():
            f.write(i)
        f.write("\n\n\n")

if __name__ == '__main__':
    multiprocessing.freeze_support()
    multiprocessing.set_start_method('spawn')
    M = multiprocessing.Manager()
    MultiPro_Dict = M.dict()
    for k, v in Test_Target.items():
        MultiPro_Dict[k] = v

    while True:
        for k,v in MultiPro_Dict.items():
            r1 = multiprocessing.Process(target=Ping_Test,args=(k,v))
            r1.start()

        time.sleep(60)