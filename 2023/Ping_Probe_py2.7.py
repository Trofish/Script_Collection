#!/usr/bin/env python

import os
import multiprocessing
import time
import requests


Test_Target = {
"txx-02-fcr-3-2":"x.x.156.103",
"txx-02-fcr-7-1":"x.x.153.2",
"txx-04-fcr-18-3":"x.x.207.103",
"txx-04-fcr-13-1":"x.x.206.3",
}

def Ping_Test(item_pair):
    Ping_Result = os.popen("ping -c 10 %s"%(item_pair[1]))
    # Ping_Result = os.popen("ping -n 10 %s"%(IP_Addr))
    with open("%s.txt"%(item_pair[0]),'a') as f:
        f.write(time.strftime("%y-%m-%d_%H:%M:%S\n"))
        for i in Ping_Result.readlines():
            f.write(i)
        f.write("\n\n\n")

if __name__ == '__main__':
    # multiprocessing.freeze_support()
    # multiprocessing.set_start_method('spawn')
    M = multiprocessing.Manager()
    MultiPro_Dict = M.dict()
    for k, v in Test_Target.items():
        MultiPro_Dict[k] = v

    while True:
        pool = multiprocessing.Pool(processes=len(MultiPro_Dict))
        for i in MultiPro_Dict.items():
            r1 = multiprocessing.Process(target=Ping_Test, args=(i,))
            r1.start()

        time.sleep(60)