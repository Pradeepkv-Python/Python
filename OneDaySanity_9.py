import Modules
import adb
from time import sleep
import ElementsText as el
import logging

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler(r"F:\Automation_Logs\logs.txt")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)
#logging.info("====== New Session ========")


adbcmd = adb.AdbCommands(el.input["remoteIP"])
ptt = Modules.ModulesforPTT(el.input["remoteIP"])

driverslist = {}

for port, serial in ptt.Devicelist.items():
    ptt.adb_uninstall_builds(el.appium)
    #ptt.adb_launch(action='clear') 
    ptt.adb_launch(action='start') 
    driver = ptt.appium_driver(serial, el.input["remoteIP"], str(port))
    driverslist[port] = [driver, port, serial]
    

d1, s1 = driverslist[4723][0], driverslist[4723][2]
#ptt.activation(d1, s1)
def activation(driver, serialnumber):
    if el.input["bearer"] == "wifi":
        adbcmd.adb_launch(serialnumber, action="clear")
        ptt.wifiON(driver, serialnumber)  
        adbcmd.adb_launch(serialnumber, action="start")             
        ptt.activation(driver, serialnumber)
    if el.input["bearer"] == "3g":
        adbcmd.adb_launch(serialnumber, action="clear")
        ptt.wifiOFF(driver, serialnumber)
        ptt.Airplane_off(driver, serialnumber)         
        adbcmd.adb_launch(serialnumber, action="start")      
        ptt.activation(driver, serialnumber)
    if el.input["bearer"] == "both":
        adbcmd.adb_launch(serialnumber, action="clear")
        ptt.wifiON(driver, serialnumber)  
        adbcmd.adb_launch(serialnumber, action="start")             
        ptt.activation(driver, serialnumber)
        print("WIFI activation success")
        ptt.wifiOFF(driver, serialnumber)
        ptt.Airplane_off(driver, serialnumber)   
        adbcmd.adb_launch(serialnumber, action="start")
        print("3G activation success")            
        ptt.activation(driver, serialnumber)
ptt.copy_Logs(d1, s1)
