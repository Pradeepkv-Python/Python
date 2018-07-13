'''
Created on 14-Mar-2018

@author: kodiak
'''
import Modules
import os
from time import sleep
import adb
import logging

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler("F:\Automation_Logs\logs.txt")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)
sleep(20)

appium = {}
appium["unlock"] = 'io.appium.unlock'

key1 = "input keyevent 26"
key2 = "input keyevent 82"

IP = os.environ["IP"]
UpTime = int(os.environ["UpTime"])
DownTime = int(os.environ["DownTime"])
Count = int(os.environ["Count"])
Build = os.environ["Build"]
NetworkOperationType = os.environ["NetworkOperationType"]

cmd = adb.AdbCommands(IP)
cmd.adb_Android_device_finder()
#print(cmd.devSerials)
cmd.adb_exec_command(key1)
cmd.adb_exec_command(key2)
for sn in range(len(cmd.devSerials.items())):
    sn = sn+1
    cmd.adb_uninstall_builds(cmd.devSerials[sn], build=appium)
    
ptx = Modules.ModulesforPTT(IP)


print("======Given Details======")
print("System IP : ", IP)
print("UP time : ", UpTime)
print("DOWN time : ", DownTime)
print("Iteration count : ", Count)
print("Build is : ", Build)
print("NetworkOperationType is : ", NetworkOperationType)
print("========================\n")


def network_Simulation(UpTime, DownTime, Count):
    #print(UPtime, DOWNtime, count)
    
    flag = bool(ptx.Devicelist)
    if flag == False:
        print("No devices are connected!!.. Please connect and try again.")
        logger.warning("No devices are connected!!.. Please connect and try again.")
        exit()
         
    serialnumber = ptx.Devicelist[1]    
    driver = ptx.appium_driver(ptx.Devicelist[1], IP, '4723', package=Build)
    
    
    
    
    
    for loop in range(Count):
        #for input in range(len(Tuple)):
        print("\n>>>> Iteration number : {0} and Device time is : {1}".format(loop, cmd.adb_ops_timestamp(serialnumber)))
            #logger.info("\n>>>> Iteration number : %s and Device time is : %s", i, cmd.adb_ops_timestamp(s1))
        if NetworkOperationType == '1':
            #print("TC 1")
            ptx.Airplane_on(driver, serialnumber)
            ptx.wifiOFF(driver, serialnumber)
            print("<info> Running DownTime : ", DownTime)
            sleep(DownTime)
            ptx.wifiON(driver, serialnumber)
            print("<info> Running UpTime : ", UpTime)
            sleep(UpTime)
            
        if NetworkOperationType == '2':
            #print("TC 2")
            if loop == 0:
                val = ptx.check_network(driver)
                if val == 1:
                    ptx.Airplane_off(driver, serialnumber)
                    sleep(5)
                val = ptx.check_network(driver)
                if val == 6:
                    ptx.wifiOFF(driver, serialnumber)
                    sleep(5)
                val = ptx.check_network(driver)
                if val != 4:
                    print("<info> Data not turned on. Please Turn on data")
                    exit()
            
            ptx.Airplane_off(driver, serialnumber)
            print("<info> Running DownTime : ", DownTime)
            sleep(DownTime)
            ptx.Airplane_on(driver, serialnumber)
            print("<info> Running UpTime : ", UpTime)
            sleep(UpTime)
        
        if NetworkOperationType == '3':
            #print("TC 3")
            
            if loop == 0:
                #print("count ", Count)
                val = ptx.check_network(driver)
                if val == 1:
                    ptx.Airplane_off(driver, serialnumber)
                    sleep(5)
                val = ptx.check_network(driver)
                if val == 6:
                    ptx.ptx.wifiOFF(driver, serialnumber)
                    sleep(5)
                if val != 4:
                    print("<info> Data not turned on. Please Turn on data")
                    exit()
            ptx.wifiOFF(driver, serialnumber)
            print("<info> Running DownTime : ", DownTime)
            sleep(DownTime)
            ptx.wifiON(driver, serialnumber)
            print("<info> Running UpTime : ", UpTime)
            sleep(UpTime)
            
        if NetworkOperationType == '4':
            ptx.Airplane_off(driver, serialnumber)
            sleep(DownTime)
            ptx.wifiON(driver, serialnumber)
            sleep(UpTime)
            ptx.wifiOFF(driver, serialnumber)
            sleep(DownTime)
            ptx.Airplane_on(driver, serialnumber)
            sleep(UpTime)
            ptx.wifiON(driver, serialnumber)
            sleep(UpTime)
                

network_Simulation(UpTime, DownTime, Count)


