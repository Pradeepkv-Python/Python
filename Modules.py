'''
Created on 27-Dec-2017

@author: kodiak
'''
#import sqlite3
import os
import subprocess

from appium import webdriver

from selenium.common.exceptions import NoSuchElementException
from appium.webdriver.common.touch_action import TouchAction


from time import sleep
import ElementsText as el
import adb

import logging
from xml.etree import ElementTree as ET
try:
    os.remove("F:\Automation_Logs\logs.txt")
except FileNotFoundError:
    pass
logger = logging.getLogger(__name__)
hdlr = logging.FileHandler("F:\Automation_Logs\logs.txt")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)
print("====== New Session ========")


def ele_from_xml(self, ele):
    rt = ET.parse(r"F:\AutomationData\Elements_att.xml")
    root = rt.getroot()
    print(root.tag)
    for el in root.findall(ele):
        return el.text

class ModulesforPTT():
    '''
    It Included all functions of PTT.
    '''
    
    Devicelist = {}
    ActivationStatus = [el.Status["Contacting"], el.Status["UseWifi"], el.Status["Reconnecting"], el.Status["Information"], el.Status["Syncstarted"], el.lcms["importantmessage"]]
    InAppStatus = [el.Status["Information"], el.Status["Syncstarted"], el.Call["MissedCallAlert"], el.Status["Pleasewait"], el.Status["Reconnecting"], el.Call["Notnow"], el.CopyLog["Menu"], el.CopyLog["Back"], el.Call["CallEnd"], el.lcms["importantmessage"], el.Status["Confirm"], el.Status["EmergencyAlert"]]
    ptxstatus = [el.Status["Contacting"], el.Status["Information"], el.Status["Syncstarted"], el.Status["Pleasewait"], el.Call["MissedCallAlert"], el.Call["CallEnd"], el.lcms["importantmessage"], el.Status["Confirm"]]
    def __init__(self, IP):
        '''
        Constructor
        '''
        self.ip = IP
        self.android_command = adb.AdbCommands(self.ip)
    
        try:
            self.adb_Android_device_finder()
            '''for sn in range(len(self.Devicelist.items())):
                sn = sn+1
                self.android_command.adb_uninstall_builds(self.Devicelist[sn], build=el.appium)'''
        except IndexError:
            print(" ADB server not running at remote system !!!")
            exit()
    def logs(self, msg=None):
        logger = logging.getLogger(__name__)
        hdlr = logging.FileHandler("F:\Automation_Logs\logs.txt")
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.DEBUG) 
    
    def appium_driver(self, deviceserialNumber, ip, port, package=el.Packages[el.input["package"]]):
        
        print("<Info> Please wait for 10 sec... Appium trying to launch the client")
        logger.info("<Info> Please wait for 10 sec... Appium trying to launch the client")
        desired_cap = {}
        desired_cap['platformName'] = 'Android'
        desired_cap['deviceName'] = 'SAMSUNG-SM-N900A'
        #desired_cap['platformVersion'] = int(Version)
        desired_cap['udid'] = deviceserialNumber
        desired_cap['autoLaunch'] = 'false'        
        desired_cap['newCommandTimeout'] = 300
        #desired_cap['skipUnlock'] = 'true'
        #desired_cap['app'] = 'F:\Software-WB\Android_08_003_00_26E-CDE_08_003_00_00_25P-UI_08_03_00_10C-1-att.apk'
        desired_cap['appPackage'] = package
        desired_cap['appActivity'] = '.StartupActivity'
        desired_cap['automationName'] = 'Appium'
        desired_cap['noReset'] = 'true'
        desired_cap['unicodeKeyboard'] = 'true'
        desired_cap['resetKeyboard'] = 'true'
        desired_cap['clearSystemFiles'] = 'true'

        http = "http://" + ip +":" + port+ "/wd/hub"
        print(http)
        try:
            driver = webdriver.Remote(http, desired_cap)
        except Exception as err:
            print("**** Driver creation failed!!! ****** \n Please start Appium Server and Re-run the script \n")
            logger.error("** Driver creation failed!!! ****** \n Please start Appium Server and Re-run the script \n")
            print(err)
            logger.error(err)
            exit()
            return False
            
        print ("PTT Application Launched Successfully!!! \n")
        logger.info("PTT Application Launched Successfully!!! %s \n", driver)
        
        
        return driver
    def generate_seq(self):
        for i in range(4723, 4730):
            yield i
    def adb_Android_device_finder(self):
        adb = "adb -H " + self.ip + " devices"
        devicecount = 0
        var = subprocess.getoutput(adb)
        var2 = var.splitlines()
        a = self.generate_seq()
        for i in range(len(var2)):
            if var2[i] not in ['List of devices attached', '* daemon started successfully *', '* daemon not running. starting it now at tcp:5037 *']:
                ser = str(var2[i])
                c = ser.find("\to")
                d = ser.find("\td")
                
                if c == -1:
                    c=d
                    
                self.Devicelist[next(a)] = ser[0:c]
                devicecount += 1
        logger.info("\n====== New Session ======")
        print("Connected Device Count : {}\nDevices Serial numbers : {}\n".format(devicecount, self.Devicelist))
        logger.info("Connected Device Count : %s \nDevices Serial numbers : %s\n", devicecount, self.Devicelist)

    def adb_uninstall_builds(self, build = el.Packages):
        for i, k in build.items():
            print("please wait uninstalling ", k)
            adb = "adb uninstall " + k 
            os.system(adb)

    def adb_install_build(self, path=el.input["Path"]):
        logger.info("Intsalling the build Please wait....\n given build path : ", path)
        adb = "adb install " + path
        os.system(adb)    
        
    
    def adb_launch(self, package=el.input["package"], action='start'):
        '''Launching App through ADB commands'''
        if package == 'att':
            package = el.Packages["att"]
        elif package == 'vzw':
            package = el.Packages["vzw"]
        elif package == 'sprint':
            package = el.Packages["sprint"]
        try:
            
            if action in ['start', 'Start']:
                adb = "adb shell am start " + package +"/.StartupActivity"
            elif action in ['stop', 'Stop']:
                adb = "adb shell am force-stop " + package
                
            elif action in ['clear', 'Clear']:
                adb = "adb shell pm clear " + package
                
            #sleep(2)
            
            os.system(adb)
            sleep(8)
            return True

        except Exception as err:
            print("adb_launch(): Error occured \n", err)
            logger.error("adb_launch(): Error occured \n", err)
            return False
    def adb_OSversion(self):
        Version = subprocess.getoutput("adb shell getprop ro.build.version.release")
        return int(Version[0])
    
    def adb_switch_apptoBGandFG(self, driver, package=el.input["package"]):
        try:
            driver.background_app(3)
            os.system("adb shell input keyevent 3")
            print("<info> Application Moved to BG")
            sleep(5)
            for i in range(3):
                if(self.adb_launch()):                    
                    print("<info> Application Moved to FG")
                    break
            sleep(5)
        except Exception:
            print("switch_apptoBGandFG(): Error occured \n")
                
    def deviceTime(self, driver):
        driver.tdevices()        
        date = subprocess.getoutput("adb shell date +%m/%d%H:%M:%S")
        devtime = date[0:5] + ' '+date[5:13]
        return devtime
    def ptxdeviceTime(self):

        time = subprocess.getoutput("adb shell date +%I:%M%p")
        return time

    def activation(self, driver, serialnumber):
        Version = self.android_command.adb_OSversion(serialnumber)
        if Version >= 6:
            try:
                print ("Allowing Permissions for Android M onwards")
                for i in range(1,7):
                    driver.find_element_by_id("com.android.packageinstaller:id/permission_allow_button").click()
                sleep(10)   
            except Exception:
                pass
            try:
                sleep(3)
                f = driver.find_element_by_id("android:id/button1").is_displayed()
                if f == True:
                    driver.find_element_by_id("android:id/button1").click()
                    print("Allowing battery permission")
            except Exception:
                pass
        for i in range(4):
            try:
                sleep(5)
                cond = driver.find_element_by_xpath(el.Activation['Accept']).is_displayed()
                if cond == True:
                    print("Accepting EULA")
                    driver.find_element_by_xpath(el.Activation['Accept']).click()
                    break
                
            except Exception:
                print("Waiting for EULA screen....")
                continue
                print ("Accept button not found")
        #sleep(5)
        self.status_check(driver, self.ActivationStatus)
        
        
        for i in range(3):
            try:
                flag = driver.find_element_by_xpath(el.Activation["Yes"]).is_displayed()
                if flag == True:
                    driver.find_element_by_xpath(el.Activation["Yes"]).click()
                
            except Exception:
                sleep(5)
                continue
                pass
        self.status_check(driver, self.ActivationStatus)
        try:
            flag = driver.find_element_by_xpath(el.Activation["EnterCode"]).is_displayed()
            if flag == True:
                driver.find_element_by_xpath(el.Activation["EnterCode"]).click()
                Code = input("<inof> please enter Activation Code: ")
                try:
                    activation_key = driver.find_element_by_xpath(el.Activation["EditText1"])
                except Exception:
                    activation_key = driver.find_element_by_xpath(el.Activation["EditText"])
                            
                sleep(3)
                activation_key.send_keys(Code)
                sleep(2)
                driver.find_element_by_xpath(el.Activation["OK"]).click()
        except Exception:
            print("<info> Performing SMS based activation!!")

        self.status_check(driver, self.ActivationStatus)
        try:
            flag = driver.find_element_by_xpath(el.Activation["Error"]).is_displayed()
            if flag == True:
                print(" Activation Failed!!! \n ")
                driver.find_element_by_xpath(el.Activation["Exit"]).click()
                
        except Exception:
            pass
        try:        
            sleep(2)
            driver.find_element_by_xpath(el.Activation["SkipTutorial"]).click()
            print("<Success> Activation success")
            return True
        except Exception:
            print ("<Error> Activation Failed!!!!")
            return False
            

    
    def swipe(self, driver):
        try:
            driver.swipe(start_x=540, start_y=1275, end_x=540, end_y=681, duration=1000)
            sleep(2)
        except:
            print("Device screen Swipe failed...")
    
    def longPress(self, driver, ele, duration = 4000):
        for i in range(2):
            try:
                L = driver.find_element_by_xpath(ele)
                 
                action = TouchAction(driver)
                action.long_press(L).wait(duration).release()     
                action.perform() 
                return True
            except Exception:
                #print("<error> Failed to do long press on element...")
                print("<info> Element not identified in longpress() function and will try one more..")
                #self.swipe(driver)
                #self.status_check(driver, self.InAppStatus)
                continue
        

    def destpath(self, serialnumber, Opsname = "Keerthi_DT"):
        '''To select local/system path to copy logs with devitime attached'''
        devtime=self.android_command.adb_ops_timestamp(serialnumber)
        devtime=devtime[0:2]+devtime[3:]
        '''dirlist = ["E:\Automation_folder", "D:\Automation_folder", "F:\Automation_folder"]
        for i in range(3):
            try:
                var = dirlist[i]
                os.makedirs(dirlist[i])
            except FileExistsError:
                print("<info> {0} directory already exist. So Copying logs in same folder.".format(var))
                break
            except FileNotFoundError:
                print("<info> {0} drive not present and trying to create directory in available drive".format(var))
                continue'''
        
        var = "F:\Automation_folder"
        dest_path=var + "\PTT_{0}_{1}".format(devtime, Opsname)
        print("<Log Path> : ", dest_path)
        return dest_path
    
    def copy_Logs(self, driver, serialnumber, carrier=el.input["package"], Opsname = "NoSpecificOps"):
        '''copylogs to local drive
        carrier= att, vzw, bell etc'''
        print("Copying the Logs ... Please Wait")
        try:
            cmd = 'shell rm -rf /sdcard/PTT/*'
            self.android_command.adb_exec_command(cmd, serialnumber)
        except Exception:
            print("/sdcard/PPT folder not exist to delete existing files")
        sleep (2)
        try:
            if self.status_check(driver, self.InAppStatus) == False:
                self.android_command.adb_switch_apptoBG(serialnumber)
                self.android_command.adb_switch_apptoFG(serialnumber)
            driver.find_element_by_xpath(el.CopyLog["Menu"]).click()
            sleep(3)
           
            try:
                driver.find_element_by_xpath(el.CopyLog["ManualDial"]).click()
            except Exception:
                driver.find_element_by_id("Manual dial").click()
           
            keysend = driver.find_element_by_xpath(el.CopyLog["EneterNumber"])
            #print(el.Secretcode[carrier])
            keysend.send_keys(el.Secretcode[carrier])
            
            sleep(1)
            driver.find_element_by_xpath(el.CopyLog["PTTCall"]).click()
            for i in range(5):
                try:
                    found = driver.find_element_by_xpath(el.CopyLog["CopyPTTfiles"]).is_displayed()
                    
                    if found == True:
                        driver.find_element_by_xpath(el.CopyLog["CopyPTTfiles"]).click()
                        break
                except Exception:
                    self.swipe(driver)
                    continue
            
            sleep(5)

            driver.find_element_by_xpath(el.CopyLog["Yes"]).click()
            try:
                sleep(5)
                driver.find_element_by_id(el.CopyLog["allow"]).click()
            except Exception:
                pass
            sleep(5)
            self.backbutton(driver, 2)
            cmd = 'pull /sdcard/PTT {0}'.format(self.destpath(serialnumber, Opsname))    
            #print(cmd)
            self.android_command.adb_exec_command(cmd, serialnumber)
            print("logs copied successfully to local Drive")
        except Exception as err:
            print("copy_Logs(): Error in copying the logs from device \n", err)

        
    def openchrome(self, driver, url):
        '''for PTX security. will open chrome in device and search for uri'''
        
        if url == False:
            print("EXITING : Url returned False...")
            exit()
        try:
            self.adb_chrome_launcher()
            print("openchrome: Browser launched Succefully")
            sleep(2)
            driver.find_element_by_accessibility_id(el.PtxSecurity['moreoption']).click()
            sleep(3)
            driver.find_element_by_accessibility_id(el.PtxSecurity['Newtab']).click()
            sleep(5)
            sendurl = driver.find_element_by_xpath(el.PtxSecurity["typeurl"]).clear()
            sendurl.send_keys(url)
            driver.keyevent(66)
            sleep(5)
            '''
            try:
                print("in try")
                driver.find_elements_by_xpath("//android.widget.Button[@text='ADVANCED']").click()
                sleep(2)
                ip = self.getdeviceIP()
                ele = "//android.view.View[@text='PROCEED TO " + ip +" (UNSAFE)']"
                print (ele)
                driver.find_elements_by_xpath(ele).click()
                sleep(3)
            except Exception as err:
                print(err)
                pass'''
        except Exception as err:
            print("openchrome(): error occured \n", err)
            
    def chromeresponse(self, driver, url):
        try:
            res = {'ERR_ADDRESS_UNREACHABLE':"//android.view.View[@text='ERR_ADDRESS_UNREACHABLE']", 'ERR_CONNECTION_REFUSED':"//android.view.View[@text='ERR_CONNECTION_REFUSED']", 'ERR_CONNECTION_TIMED_OUT':"//android.view.View[@text='ERR_CONNECTION_TIMED_OUT']"}
            loop = 0
            for i, k in res.items():
                loop+=1
                try:
                    found = driver.find_element_by_xpath(k).is_displayed()
                    if found == True:
                        if i in ['ERR_ADDRESS_UNREACHABLE', 'ERR_CONNECTION_TIMED_OUT']:
                            print("Network Error : Either netwrok is slow or remote server is not reachable")
                        elif i in ['ERR_CONNECTION_REFUSED']:
                            print("Url is not accessible and response is : ",i)
                        break
                except Exception:
                    if loop >= 3:
                        print ("PTX data is accessible from url".upper(), url)
                        
                    continue
        except Exception as err:
            print("chromeresponse(): error occured \n", err)
            
    def getdeviceIP(self, driver, serialnumber):
        network1 = driver.network_connection
        if network1 == 6:
            #print("Device connected to WIFI")
            ipofdevice = self.android_command.adb_get_wifi_IP(serialnumber)
            str = ipofdevice
            #print(ipofdevice)
            ip = str.replace("r:", '/')
            ip = ip.replace(" ", "/")
            ip = ip.split("/")
            ipv4 = ip[20]
            ipv6 = ip[38]
            
            
            print("Device connected to WIFI and IPv4 : {0} and IPv6 : {1}".format(ipv4,ipv6))
            return ipv4
        if network1 == 4:
            print("Device connected to 3G/LTE")
            ipofdevice = self.android_command.adb_get_data_IP(serialnumber)
            str = ipofdevice
            #print(ipofdevice)
            ip = str.replace("r:", '/')
            ip = ip.replace(" ", "/")
            ip = ip.split("/")
            ipv4 = ip[21]
            ipv6 = ip[39]
            print("Device connected to 3G/LTE and IPv4 : {0} and IPv6 : {1}".format(ipv4,ipv6))
            return ipv4
        
    
    def ptxmsgStatus(self, driver, serialnumber, msgtype):
        print("<info> Checking message status. please wait...")
        '''msgtype = "image", "video", "location", "audio", "text"'''
        if msgtype == "text":
            msgtype = ", , Welcome to Kodiak Networks., , "
        if msgtype in ["image", "video", "location", "audio"]:
            msgtype = ", , , " + msgtype + ", "
        PTXStatus = ['pending', 'sent', 'delivered', 'permanentfailure', 'null']
        First = "You, &nbsp"
        time = self.android_command.adb_ops_timestamp(serialnumber)
        time = time.lower()
        if time[0] == '0':
            time = time[1:]
        time = time + ', '
        #print(time)
        param = msgtype
        sleep(2)
        try:
            for i in PTXStatus[:]:
                status = i
                sleep(2)
                finalele = First+time+param+status
                #finaleletext = "//android.view.View[@text='"+ finalele + "']"
                finalelecontent = "//android.view.View[@content-desc='"+ finalele + "']"
                try:
                    #print(finalele)
                    flag = driver.find_element_by_xpath(finalelecontent).is_displayed()
                    #print(">>>msg status using ID")
                except NoSuchElementException:
                    continue
                    
                if flag == True:
                    print ("         PTX Message progress Status : {0} and Device time is {1}".format(i.upper(), time[:-2]))
                    return i
                    break
            sleep(2)
        except NoSuchElementException:
            print("Checking status : {0} = {1}".format(i, flag))
    
    def verifyContactPresence(self, driver, mdn):

            PresenceStatus = ["Available", "Offline", "Do Not Disturb", "unavailable"]
            First = "Contact Name "
            Second = ", Contact presence "
            Third = ", Contact avatar Default Avatar, , "
            for i in PresenceStatus:
                
                final_element = First+mdn+Second+i+Third
                final_elementid = "//android.view.View" + "[@content-desc='" + final_element + "']"
                final_elementtext = "//android.view.View" + "[@text='" + final_element + "']"
                #print("text: ", final_elementtext)
                #print(final_elementid)
                try:
                    try:
                        flag = driver.find_element_by_xpath(final_elementid).is_displayed()
                        final_element = final_elementid
                        #print("flag in content", flag)
                    except Exception:
                        try:
                            flag = driver.find_element_by_xpath(final_elementtext).is_displayed()
                            final_element = final_elementtext
                            #print("flag in text", flag)
                            
                        except Exception:
                            continue

                    print ("Given Contact Status is : ", i)
                    return True, final_element, i
                    break
                except Exception:
                    
                    continue

                
    def moveto_contact(self, driver, serialnumber):
        try:
            if (self.status_check(driver, self.InAppStatus) == False):
                self.android_command.adb_switch_apptoBG(self, serialnumber)
                self.android_command.adb_switch_apptoFG(self, serialnumber)
            driver.find_element_by_xpath(el.Tab["Contact"]).click()
            return True
        except Exception:
            print("could not able to move to contact tab")
            return False
            
    def moveto_group(self, driver, serialnumber):
        try:
            if (self.status_check(driver, self.InAppStatus) == False):
                self.android_command.adb_switch_apptoBG(self, serialnumber)
                self.android_command.adb_switch_apptoFG(self, serialnumber)
            try:
                driver.find_element_by_xpath(el.Tab["Group"]).click()
            except Exception:
                driver.find_element_by_id("ext-tab-4").click()
            return True
        except Exception:
            print("could not able to move to Group tab")
            return False
            
    def moveto_History(self, driver, serialnumber):
        try:
            if (self.status_check(driver, self.InAppStatus) == False):
                self.android_command.adb_switch_apptoBG(self, serialnumber)
                self.android_command.adb_switch_apptoFG(self, serialnumber)
            driver.find_element_by_xpath(el.Tab["History"]).click()
            return True
        except Exception:
            print("could not able to move to History tab")
            return False
    
    def moveto_Favorite(self, driver):
        try:
            
            driver.find_element_by_xpath(el.Tab["Favorite"]).click()
            return True
        except Exception:
            print("could not able to move to Favorite tab")
            return False
    
    def moveto_MapTab(self, driver):
        try:
            
            driver.find_element_by_xpath(el.Tab["MapTab"]).click()
            return True
        except Exception:
            print("could not able to move to MapTab tab")
            return False
        
    def search_group(self, driver, grp_name = el.input["grp"]):
        try:
            try:
                driver.find_element_by_xpath(el.Cat["delete"]).click()
            except Exception:
                pass
            Search = driver.find_element_by_xpath(el.Activation["grpsearch"])
            sleep(2)
            Search.clear()
            Search.send_keys(grp_name)
            sleep(3)
            First = "Group Name "
            Second = grp_name
            Last = ", Group Avator Default Avatar, , , , , , , , "

            if(self.isExistContactorGroup(driver) != False):
                
                Ele = First+Second+Last
                Eleid = "//android.view.View[@content-desc='" + Ele + "']"
                Eletext = "//android.view.View[@text='" + Ele + "']"
                try:
                    driver.find_element_by_xpath(Eleid).click()
                except Exception:
                    driver.find_element_by_xpath(Eletext).click()
                except Exception:
                    print("<Error> Failed to click on group")
                    return False
                return True
        except Exception:
            print("groupsearch(): Error in searching")
            return False
            
    def search_mdn(self, driver, mdn = el.input["MDN"]):
        sleep(2)
        try:
            try:
                driver.find_element_by_xpath(el.Cat["Clear"]).click()
                #print("in clear")
            except Exception:
                pass
            Search = driver.find_element_by_xpath(el.Activation["EditText"])
            sleep(2)
            Search.clear()
            Search.send_keys(mdn)
            sleep(3)
            flag, ele, presence = self.verifyContactPresence(driver, mdn=mdn)
            if flag == True:
                driver.find_element_by_xpath(ele).click()
                sleep(3)
                return True, presence
        except Exception:
            print("searchmdn(): error occured while searching mdn")
            return False
        
    
    def isExistContactorGroup(self, driver):
        nocontact = ['No matches found', 'No Groups']
        for i in nocontact:
            try:
                Nomatch = driver.find_element_by_id(i).is_displayed()
                if Nomatch == True:
                    print("Given Contact/Group Not in Contact/group list")
                    print("Please add Contact/group and try Again!!!")
                    return True
                    
            except Exception:
                continue
                return False
                
    def ptx_sendImage(self, driver):
        sleep(3)
        try:
            driver.find_element_by_xpath(el.PTX["Sendimageorvideo"]).click()
            sleep(2)
            try:
                driver.find_element_by_xpath(el.PTX["Takephoto"]).click()
            except Exception:
                driver.find_element_by_xpath(el.PTX["VzwTakePhoto"]).click()
            sleep(4)
            try:
                driver.find_element_by_xpath(el.PTX["photoShutter"]).click()
                sleep(10)
            except:
                self.status_check(driver, self.ptxstatus)
                print("photoShutter button not found...")
                
                
            for i in range(1):
                try:
                    driver.find_element_by_xpath(el.PTX["OK"]).click()
                    sleep(2)
                    driver.find_element_by_xpath(el.PTX["OK"]).click()
                    sleep(2)
                except Exception:
                    driver.find_element_by_xpath(el.PTX["CamOK"]).click()
            sleep(4)
            self.status_check(driver, self.ptxstatus)
                   
            print ("<<PTX>> Image sent Successfully")
            return True
        except Exception as err:
            self.status_check(driver, self.ptxstatus)
            print("ptx_sendImage(): error occured \n", err)
            return False
        
    def ptx_sendLocation(self, driver):
        sleep(3)
        try:
            try:
                driver.find_element_by_xpath(el.PTX["Sendlocation"]).click()
            except Exception:
                driver.find_element_by_xpath(el.PTX["MyLocation"]).click()
            for i in range(3):
                try:
                    Found = driver.find_element_by_xpath(el.PTX["share"]).is_displayed()
                    if Found == True:
                        driver.find_element_by_xpath(el.PTX["share"]).click()
                        print ("<<PTX>> Location Sent Successfully")
                        return True
                except Exception:
                    sleep(5)
                    if i==2:
                        print ("ptx_sendLocation(): Failed to send location as MAP taken too much time to load.. \n")
                        return False
                    continue
                    
            
        except Exception as err:
            self.status_check(driver, self.ptxstatus)
            print("ptx_sendLocation(): error occured \n", err)
            return False
            
    def ptx_sendAlert(self, driver):
        sleep(3)
        try:
            try:
                driver.find_element_by_xpath(el.PTX["Alert"]).click()
            except Exception:
                driver.find_element_by_xpath(el.PTX["SendAlert"]).click()
            sleep(3)
            
            print(">>Alert sent Successfully")
            return True
        except Exception as err:
            self.status_check(driver, self.ptxstatus)
            print("ptx_sendAlert(): error occured \n", err)
            return False
        
            
    def ptx_sendvideo(self, driver): 
        sleep(2)
        
        try:   
            sleep(5)
            driver.find_element_by_xpath(el.PTX["Sendimageorvideo"]).click()
            sleep(2)
            
            try:
                driver.find_element_by_xpath(el.PTX["RecordVideo"]).click()
            except Exception:
                driver.find_element_by_xpath(el.PTX["VzwRecordVideo"]).click()
            
            sleep(4)
            try:
                driver.find_element_by_xpath(el.PTX["videoShutter"]).click()
            except Exception:
                driver.find_element_by_xpath(el.PTX["Startrecording"]).click()
            sleep(10)
            try:
                driver.find_element_by_xpath(el.PTX["Stoprecording"]).click()
                
            except Exception:
                driver.find_element_by_xpath(el.PTX["stoprecord"]).click()
            sleep(5)
            try:
                driver.find_element_by_xpath(el.PTX["OK"]).click()
                sleep(2)
            except Exception:
                pass
            try:
                driver.find_element_by_xpath(el.PTX["OK"]).click()
                sleep(2)

            except Exception:
                driver.find_element_by_xpath(el.PTX["CamOK"]).click()
            sleep(4)
            
            print ("<<PTX>> Video sent Successfully")
            return True
                        
        except Exception as err:
            self.status_check(driver, self.ptxstatus)
            print("ptx_sendvideo(): error in occured \n", err )
            return False
    def ptx_sendVoiceMessage(self, driver):
        sleep(3)
        try:
            try:
                driver.find_element_by_xpath(el.PTX["VOICEMESSAGE"]).click()
            except Exception:
                driver.find_element_by_xpath(el.PTX["Sendvoicemessage"]).click()
            self.longPress(driver, el.PTX["record"], duration=50000)
            sleep(2)
            driver.find_element_by_xpath(el.PTX["recordOK"]).click()
            sleep(0.3)
            print("<<PTX>> Voice message sent successfully")
            return True
        except Exception as err:
            self.status_check(driver, self.ptxstatus)
            print("ptx_sendVoiceMessage(): error occured \n ", err)
            return False
            
    def ptx_sendText(self, driver):
        try:
            sleep(3)
            try:
                driver.find_element_by_xpath(el.PTX["Sendtext"]).click()
            except Exception:
                pass
            sleep(2)
            driver.find_element_by_xpath(el.PTX["EnterText"]).click()
            string = '''Welcome to Kodiak Networks.A regular expression in a programming language is a special text string used for describing a search pattern. It is extremely useful for extracting '''
            text = driver.find_element_by_xpath(el.PTX["EnterText"])
            text.send_keys(string)
            sleep(3)
            driver.find_element_by_xpath(el.PTX["SendPTXMessage"]).click()
            print("<<PTX>> Text sent successfully")
            return True
        
        except Exception as err:
            print("ptx errr")
            self.status_check(driver, self.ptxstatus)
            print("ptx_sendText(): error occured \n ", err)
            return False
            
    def CBLlogAnalysisForPTX(self, DeviceTime, CBLlogPath, flag=0):
        try:
            Var1=0
            ptxlist = ["IMG-", "VID-"]
            sleep(.01)
            print("Entering into CBLlogAnalysisForPTX function...")
            CBLlogPath1=CBLlogPath+"\cbl_logs.txt"
            CblHandler=open(CBLlogPath1,"r")
            sleep(.01)
            if(CblHandler):
                for line in CblHandler:
                    if DeviceTime in line:
                        flag=1
                    if flag==1:
                        for Ptxtype in ptxlist:
                            if((Ptxtype in line) and ("https://127.0.0.1" in line)):
                                Var1=1
                                print("PTX uri Log line:",line)
                                print("Splitting log line into uri...")
                                uri=line.split("https://127.0.0.1:")
                                uri="https://127.0.0.1:"+uri[1]
                                CblHandler.close()
                                sleep(1)
                                print("Split uri:",uri)
                                print("Exiting from CBLlogAnalysisForPTX function...")
                                return uri
                            else:
                                print('{0} not found'.format(Ptxtype))
                                continue
                            
                if Var1==0:
                    print("PTX uri not found in CBL logs...")
                    print("Exiting from CBLlogAnalysisForPTX function...")
                    CblHandler.close()
                    return False
            else:
                print("File not found...")
                print("Exiting from CBLlogAnalysisForPTX function...")
        except Exception as err:
            print("CBLlogAnalysisForPTX(): Error occured \n", err)
       
    def ChangeUriIP(self, PTXuri, NewUriIp):
        print("Enters into ChangeUriIP function...")
        if "127.0.0.1" in PTXuri:
            PTXuri=PTXuri.replace("127.0.0.1",NewUriIp)
            print("Replace uri:",PTXuri)
            print("Exiting from ChangeUriIP function...")
            return PTXuri
        else:
            print("IP:127.0.0.1 not found in PTX uri...")
            print("Exiting from ChangeUriIP function...")
            return False
        
    def ishistoryexist(self, driver):
        try:
            ishistoryempty = driver.find_element_by_id("No History Exists").is_displayed()
            if ishistoryempty == True:
                print("'EMPTY SCREEN', Not seeing sent messages")
        except Exception:
            pass
        
    def logout(self, driver):
        sleep(2)
        
        try:
            driver.find_element_by_xpath(el.CopyLog["Menu"]).click()
            sleep(2)
            
            try:
                #sleep(2)
                driver.find_element_by_xpath(el.Settings["Settings"]).click()
                
            except Exception:
                print("except")
                driver.find_element_by_id("Settings").click()
                
                
    
            for i in range(7):
                try:
                    #self.swipe(driver)
                    res = driver.find_element_by_xpath(el.Settings["Logout"]).is_displayed()
                    print(res)
                    if res == True:
                        #self.swipe(driver)
                        driver.find_element_by_xpath(el.Settings["Logout"]).click()
                        print("in if")
                        break
                except Exception:
                    self.swipe(driver)
                    sleep(1)
                    continue
            sleep(2)
            driver.find_element_by_xpath(el.CopyLog["Yes"]).click()
            
        except Exception:
            print("Failed")
            
    def forwardbutton(self, driver):
        try:
            driver.find_element_by_xpath(el.CopyLog["Details"]).click()
        except Exception as err:
            print("forwardbutton(): Details element not found \n", err)
            
    def backbutton(self, driver, count):
        sleep(5)
        try:
            for i in range(count):
                driver.find_element_by_xpath(el.CopyLog["Back"]).click()
        except Exception as err:
            print("backbutton(): Back element not found \n", err)
            
    def element_find(self, driver, ele):
        try:
            found = driver.find_element_by_xpath(ele).is_displayed()
            #print("ele find", found)
            return found
        except Exception as err:
            pass
    def call_end_displayed(self, driver, ele=el.Call["CallEnd"]):
        try:
            flag = driver.find_element_by_xpath(ele).is_displayed()
            print("<Call Success> Call End button found")
            return True
        except Exception as err:
            print("<Call Failure> Call End button not found")
            return False
    def home_screen(self, driver):  
        print("in home function")
        #el = self.element_find(driver, )
        el = driver.find_element_by_xpath(el.CopyLog["Menu"]).is_displayed()
        #print("ll", el)
        #return el
    def status_check(self, driver, statuslist):
        #print(statuslist)
        print("<info> Checking Status of client Please wait....")
        #home = self.home_screen(driver)
        #print("home", home)
        home = False
        if home == True:
            #print("in first")
            print("<Status> Client in Home Screen")
            return True
        elif home == False:
            for j in range(10):
                isexist = 0
                for i in range(len(statuslist)):
                    sleep(2)
                    res = self.element_find(driver, statuslist[i])
                    if res == True:
                        Status = statuslist[i]
                        #print(Status)
                        isexist = 1
                        break
                    else:
                        continue
                if isexist == 0:
                    print("<Status> Nothing shown on screen")
                    return False
                if Status in [el.lcms["importantmessage"]]:
                    print("<Status> Got LCMS message pop up.. ")
                    try:
                        driver.find_element_by_xpath(el.lcms["checkbox"]).click()
                        sleep(1)
                        driver.find_element_by_xpath(el.lcms["Dismiss"]).click()
                        sleep(2)
                    except Exception as err:
                        print("<error> Could not able to dismiss LCMS pop up.\n", err)
                if Status in [el.Status["Confirm"]]:
                    print("<Status> Got Discard pop up.. ")
                    try:
                        driver.find_element_by_xpath(el.Cat["Yes"]).click()
                        sleep(1)
                    except Exception as err:
                        print("<error> Could not able to dismiss Discard pop up.\n", err)
                if Status in [el.Status["EmergencyAlert"]]:
                    print("<Status> Got Emergency Alert pop up.. ")
                    try:
                        driver.find_element_by_xpath(el.lcms["Dismiss"]).click()
                        sleep(2)
                    except Exception as err:
                        print("<error> Could not able to dismiss LCMS pop up.\n", err)
                
                if Status in [el.Status["Contacting"], el.Status["Reconnecting"]]:
                    print("<Status> Client in Contacting server/ Reconnecting will sleep 10sec")
                    sleep(5)
                    isexist = 1
                    
                elif Status in [el.Status["UseWifi"]]:
                    try:
                        print("<Status> Got confirm pop-up")
                        driver.find_element_by_xpath(el.Status["UseWifi"]).click()
                        sleep(3)
                        driver.find_element_by_xpath(el.Activation["OK"]).click()
                        isexist = 1
                        return True
                    except NoSuchElementException:
                        print ("****Element not found in Confirm pop-up")
                elif Status in [el.Status["Information"], el.Status["Syncstarted"]]:
                    
                    print("<Status> Client in Showing information/Sync pop-up....")
                    try:
                        try:
                            driver.find_element_by_xpath(el.Cat["OK"]).click()
                        except Exception:
                            driver.find_element_by_xpath(el.Status["Yes"]).click()
                        isexist = 1
    
                    except Exception:
                        print("<Status> Syncronization is going on waiting for 5 sec")
                        sleep(5)
    
                elif Status == el.CopyLog["Menu"]:
                    print("<Status> Client in Home Screen")
                    return True
                    
                elif Status == el.Call["CallEnd"]:
                    print("<Status> Found Ongoing call")
                    driver.find_element_by_xpath(el.Call["CallEnd"]).click()
                    sleep(2)
                    
                    
                elif Status in [el.Call["MissedCallAlert"], el.Call["Notnow"]]:
                    print("<Status> Found Missed Call Alert")
                    driver.find_element_by_xpath(el.Call["Notnow"]).click()
                    sleep(2)
    
                elif Status == el.CopyLog["Back"]:
                    self.backbutton(driver, 1)
                    
                elif Status == el.Status["Pleasewait"]:
                    sleep(2)

    def delete_contacts(self, driver, contactcount=300):
        
        name = list(range(1, contactcount+1))
        for i in range(0, len(name)):
            try:     
                delete = driver.find_element_by_xpath(el.Activation["EditText"])
                sleep(2)
                delete.clear()
                delete.send_keys(name[i])
                sleep(3)
                
                FirstPart = "Contact Name "
                SecondPart = str(name[i])
                ThirdPart = ", Contact presence unavailable, Contact avatar Default Avatar, , "
                Elem = FirstPart+SecondPart+ThirdPart
                final_elementtext = "//android.view.View" + "[@text='" + Elem + "']"
                #print(final_elementtext)
                
                self.longPress(driver, final_elementtext, 3000)
            except Exception:
                #print("Failed: {0} : Conatct is not found and continue to delete existing contacts".format(name[i]))
                try:
                    self.status_check(driver, self.InAppStatus)
                    driver.find_element_by_xpath(el.Cat["Clear"]).click()
                    continue
                except Exception:
                    pass
            
            try:
                driver.find_element_by_xpath(el.Cat["Delete"]).click()
                sleep(2)
                driver.find_element_by_xpath(el.Activation["OK"]).click()
                sleep(10)
                print("{0} : Conatct is found and Deleted Successfully".format(name[i]))
            except Exception:
                print("Failed {0} : Conatct Deletion Failed".format(name[i]))
                self.status_check(driver, self.InAppStatus)
                continue
                
    def add_contacts(self, driver, contactcount=300):
        skip = 0
        print("Adding contacts please wait...")
        name = list(range(1, contactcount+1))
        max = 9998881000 + contactcount + 1
        num = list(range(9998881000, max))
        try:        
            for i in range(len(name)):
                try:

                    sleep(2)
                    driver.find_element_by_xpath(el.Cat["AddContact"]).click()
                    if self.toast_status(driver) == "Connection Unavailable":
                        print("<Info> Connection is Unavailable try after sometime!!")
                        break
                    sleep(2)
                    driver.find_element_by_xpath(el.Cat["NewContact"]).click()
                    sleep(2)
                    try:
                        driver.find_element_by_xpath(el.Cat["Clear"]).click()
                    except Exception:
                        pass
                    EnterName = driver.find_element_by_xpath(el.Cat["EnterName"])
                    EnterName.send_keys(name[i])
                    sleep(2)
                    MDN = driver.find_element_by_xpath(el.Cat["MDN"])
                    MDN.send_keys(num[i])
                    sleep(2)
                    
                    driver.find_element_by_xpath(el.Cat["Save"]).click()
                    self.status_check(driver, self.InAppStatus)
                    
                    try:
                        sleep(2)
                        driver.find_element_by_xpath(el.Cat["Cancel"]).click()
                        print("Contact Already exist, Going back")
                        sleep(2)
                        driver.find_element_by_xpath(el.Cat["Yes"]).click()
                        sleep(2)
                    
                    except Exception:
                        skip = 1
                    if skip == 1:
                        print("{0} contact added sucessfully".format(i+1))
                except Exception:
                    print("{0} Fail to add contact".format(i+1))
                    continue
        except Exception as err:
            print("add_contact(): error occured \n ", err)
            self.status_check(driver, self.InAppStatus)
            
    def add_group(self, driver, groupcount=1):
        
        print("Given group count to add is %d ...please wait", groupcount)
        grpname = list(range(1, groupcount+1))
        max = 9998881000 + groupcount+1
        num = list(range(9998881000, max))
        
        for i in range(len(grpname)):
            try:
                sleep(4)
                driver.find_element_by_xpath(el.Cat["AddGroup"]).click()
                sleep(2)
                try:
                    driver.find_element_by_xpath(el.Cat["Clear"]).click()
                except Exception:
                    pass
                EnterName = driver.find_element_by_xpath(el.Cat["EnterName"])
                EnterName.send_keys(grpname[i])
                sleep(2)
                try:
                    driver.find_element_by_xpath(el.Cat["AddMember"]).click()
                except Exception:
                    driver.find_element_by_xpath(el.Cat["AddMembers"]).click()
                except Exception:
                    pass
                self.grp_addmembers(driver)
                sleep(2)
                if True:
                    try:
                        #sleep(2)
                        driver.find_element_by_xpath(el.Cat["Cancel"]).click()
                        print("Contact Already exist, Going back")
                        sleep(2)
                        driver.find_element_by_xpath(el.Cat["Yes"]).click()
                        sleep(2)
                    except Exception:
                        print("{0} group added successfully".format(i+1))
                        pass
                
            except Exception:
                print("add_group(): error occured ")
                self.status_check(driver, self.InAppStatus)
                continue
    def delete_grp(self, driver, groupcount=1):
        
        print("Deleting Groups please wait...")
        grpname = list(range(1, groupcount+1))
        
        First = "Group Name "
        Last = ", Group Avator Default Avatar, , , , , , , "
        
        for i in range(groupcount):
            try:
                try:
                    driver.find_element_by_xpath(el.Cat["delete"]).click()
                except Exception:
                    print("Enetr text Field already Empty...No need to clear")
                 
                try:
                    EnterName = driver.find_element_by_xpath(el.Cat["EnterName"])
                except Exception:                    
                    EnterName = driver.find_element_by_xpath(el.Cat["Searchintab"])

                EnterName.send_keys(grpname[i])
                #print(First, Last, grpname[i])
                Ele = First + str(grpname[i]) + Last
                #print(Ele)
                Eleid = "//android.view.View[@content-desc='" + Ele + "']"
                #Eletext = "//android.view.View[@text='" + Ele + "']"
                Contact = "Group Name " + str(i+1) + "," 
                Eletext = "//android.view.View[contains(@text, '" + Contact+ "')]"
                #print(Eletext)
                sleep(2)
                if self.longPress(driver, ele=Eletext) == True:
                    #print("22")
                    driver.find_element_by_xpath(el.Cat["DeleteGroup"]).click()
                    sleep(2)
                    driver.find_element_by_xpath(el.Cat["OK"]).click()
                    sleep(6)
                    print("{0} is deleted successfully".format(grpname[i]))
                else:
                    print(" Failed to delete {0} group".format(grpname[i]))
                    continue
            except Exception as err:
                print(err)
                #self.status_check(driver, self.InAppStatus)
                print(" Failed to delete {0} group".format(grpname[i]))
                continue
            
        
    def grp_addmembers(self, driver, count=1):
        sleep(2)
        PresenceStatus = ["unavailable", "Available", "Offline", "Do Not Disturb"]
        print("<info> Adding group member started")
        First = "Contact Name "
        Second = ", Contact presence "
        Third = ", Contact avatar Default Avatar, , Checkbox UnChecked"
        for i in range(1, count+1):
            sleep(2)
            try:
                try:
                    driver.find_element_by_xpath(el.Cat["delete"]).click()
                   
                except Exception:
                    pass
                Search = driver.find_element_by_xpath(el.Activation["EditText"])
                Search.clear()
                Search.send_keys(i)
                sleep(2)
                

                '''for j in range(len(PresenceStatus)):
                   
                    final_element = First+str(i)+Second+PresenceStatus[j]+Third
                    #print(final_element)
                    final_elementid = "//android.view.View[@content-desc='" + final_element + "']"
                    final_elementtext = "//android.view.View[@text='" + final_element + "']"'''
                final_elementtext = "//android.view.View[contains(@text, ', Checkbox UnChecked')]"
                try:
                    driver.find_element_by_xpath(final_elementtext).click()
                    
                    #break

                except Exception:
                    driver.find_element_by_xpath(final_elementtext).click()
                    #break
                #print("selected")
                sleep(3)
                #print("i ", i)
                #if i == count:
                # print("i ", i)
                driver.find_element_by_xpath(el.Cat["Save"]).click()
                sleep(3)
                driver.find_element_by_xpath(el.Cat["Save"]).click()
                sleep(2)
                #print("3")

                #print("Saving {0} group ".format(i+1))

                '''if (self.status_check(driver, self.InAppStatus) == False):
                    try:
                        sleep(2)
                        driver.find_element_by_xpath(el.Cat["Cancel"]).click()
                        print("Contact Already exist, Going back")
                        sleep(2)
                        driver.find_element_by_xpath(el.Cat["Yes"]).click()
                        sleep(2)
                    except Exception:
                        pass
                else:
                    print("Members added successfully")
                    self.status_check(driver, self.InAppStatus)'''
            except Exception:
                
                continue
    
      
    def myprsence_check(self, driver, serialnumber):
        P = {"Available": el.Presence["Available"], "Do Not Disturb": el.Presence["DND"], "No Connection": el.Presence["NoConnection"]}

        if self.status_check(driver, self.InAppStatus) == False:
            self.android_command.adb_switch_apptoBG(self, serialnumber)
            self.android_command.adb_switch_apptoFG(self, serialnumber)
        #print("a")
        for key, value in P.items():
            try:
                try:
                    print(value)
                    flag = driver.find_element_by_xpath(value).is_displayed()
                    #print("1", flag)
                except Exception:
                    print(key)
                    flag = driver.find_element_by_id(key).is_displayed()
                    #print("2", flag)
                if flag == True:
                    print("Self presence is: ", str(key).upper())
                    print(key, value)
                    return key, value
            except Exception as err:
                continue
                print("myprsence_check(): Error Occured \n", err)
            
            
                
    def mypresence_switch(self, driver):
        
        try:
            key, value = self.myprsence_check(driver)
        except Exception:
            print("<Error> Failed to get self presence")
        
        #print(key)
        try:
            if key == "Available":
                driver.find_element_by_xpath(el.Presence["Available"]).click()
                sleep(2)
                driver.find_element_by_xpath(el.Presence["setDND"]).click()
                sleep(2)
                #self.myprsence_check(driver)
                
            elif key == "Do Not Disturb":
                #print("DND")
                driver.find_element_by_xpath(el.Presence["DND"]).click()
                sleep(2)
                driver.find_element_by_xpath(el.Presence["setAvailable"]).click()
                sleep(2)
                #self.myprsence_check(driver)
            else:
                print("Network Connection is down !!\n")
        except Exception as err:
            print("mypresence_switch(): Error Occured \n", err)
            

    def network_switch(self, driver, serialnumber):
        network = driver.network_connection
        print('network value', network)
        logger.info('network value %s', network)
        
        if network == 6 or network == 2:
            print("Device Connected to wifi")
            logger.info("Device Connected to wifi")
            self.wifiOFF(driver, serialnumber)
            #sleep(2)
            #subprocess.getoutput('adb shell am start -n "com.android.settings/.Settings\"\$\"DataUsageSummaryActivity"')
            sleep(3)
            if network != 6:
                self.switch_data(driver, serialnumber)
            #subprocess.getoutput("adb shell input keyevent 3")
        if network == 4:
            print("<Network Status> Device Connected to 3G/4G")
            logger.info("<Network Status> Device Connected to 3G/4G")
            self.wifiON(driver, serialnumber)
            
        if network == 0:
            print("Device not connected to any network so making wifi only UP/DOWN")
            logger.info("Device not connected to any network so making wifi only UP/DOWN")
            self.wifiOFF(driver, serialnumber)
            self.wifiON(driver, serialnumber)
        if network == 1:
            #print("<info> Turning off Airplane mode.. please wiat")
            self.Airplane_off(driver, serialnumber)
            
    def Airplane_off(self, driver, serialnumber):
        val = self.check_network(driver)
        if val != 1:
            print("<info> Already Airplane mode is OFF")
        else:
            for i in range(1):
                try:
                    print("<info> Turning off Airplane mode.. please wiat")
                    logger.info("<info> Turning off Airplane mode.. please wiat")
                    command = 'shell am start -a android.settings.AIRPLANE_MODE_SETTINGS'
                    self.android_command.adb_exec_command(command, serialnumber)
                    sleep(2)
                    if self.android_command.adb_OSversion(serialnumber) < 6:
                        com1 = "shell settings put global airplane_mode_on 0"
                        com2 = "shell am broadcast -a android.intent.action.AIRPLANE_MODE"
                        self.android_command.adb_exec_command(com1, serialnumber)
                        self.android_command.adb_exec_command(com2, serialnumber)
                    else:
                        try:
                            driver.find_element_by_xpath(el.Network['ON']).click()
                        except Exception:
                            driver.find_element_by_class_name("android.widget.Switch").click()
                    print("Turned off Airplane mode")
                    logger.info("Turned off Airplane mode")
                    self.android_command.adb_homekey(serialnumber)
                    break
                except Exception:
                    print("<Error> Got some pop/message on screen")
                    try:
                        driver.find_element_by_xpath(el.Network['OK']).click()
                        sleep(2)
                        driver.find_element_by_xpath(el.Network['Navigate']).click()
                        continue
                    except Exception:
                        self.android_command.adb_homekey(serialnumber)
                        print("<info> Try to close pop but 'OK' button not found")
                    sleep(5)
            
    def Airplane_on(self, driver, serialnumber):
        val = self.check_network(driver)
        if val == 1:
            print("<info> Already Airplane mode is ON")
        else:
            for i in range(1):
                try:
                    print("<info> Turning on Airplane mode.. please wiat")
                    logger.info("<info> Turning on Airplane mode.. please wiat")
                    command = 'shell am start -a android.settings.AIRPLANE_MODE_SETTINGS'
                    self.android_command.adb_exec_command(command, serialnumber)
                    sleep(2)

                    if self.android_command.adb_OSversion(serialnumber) < 6:
                        com1 = "shell settings put global airplane_mode_on 1"
                        com2 = "shell am broadcast -a android.intent.action.AIRPLANE_MODE"
                        self.android_command.adb_exec_command(com1, serialnumber)
                        self.android_command.adb_exec_command(com2, serialnumber)
                    else:
                        try:
                            driver.find_element_by_xpath(el.Network['OFF']).click()
                        except Exception:
                            driver.find_element_by_class_name("android.widget.Switch").click()
                    print("Turned on Airplane mode")
                    logger.info("Turned on Airplane mode")
                    self.android_command.adb_homekey(serialnumber)
                    break
                except Exception:
                    print("<Error> Got some pop/message on screen")
                    try:
                        driver.find_element_by_xpath(el.Network['OK']).click()
                        sleep(2)
                        driver.find_element_by_xpath(el.Network['Navigate']).click()
                        continue
                    except Exception:
                        self.android_command.adb_homekey(serialnumber)
                        print("<info> Try to close pop but 'OK' button not found")
                    sleep(5)
                
    def wifiOFF(self, driver, serialnumber):
        print("<info>Turning off the wifi")
        logger.info("<info>Turning off the wifi")
        command = 'shell am start -a android.intent.action.MAIN -n com.android.settings/.wifi.WifiSettings'
        self.android_command.adb_exec_command(command, serialnumber)

        net = self.check_network(driver)
        if net in [2, 6]:
            try:
                for i in range(10):
                    sleep(2)
                    try:
                        driver.find_element_by_xpath(el.Network['OFF']).click()
                    except Exception:
                        driver.find_element_by_class_name("android.widget.Switch").click()
                    sleep(2)
                    try:
                        conn = driver.find_element_by_xpath(el.Network['Connected']).is_displayed()
                        print(conn)
                        if conn == True:
                            print("<WIFI> Trying to turnoff the wifi ")
                            logger.info("<WIFI> Trying to turnoff the wifi ")
                            continue
                    except Exception:
                            print("<WIFI> WIFI Turned OFF")
                            logger.info("<WIFI> WIFI Turned OFF")
                            #print("homebutton")
                            self.android_command.adb_homekey(serialnumber)
                            break
                    
            except Exception:
                print("wifiOFF(): Error in turning off the wifi")
                logger.error("wifiOFF(): Error in turning off the wifi")
                self.android_command.adb_homekey(serialnumber)
                pass

        else:
            print("<WIFI> WIFI already turned off")
            logger.info("<WIFI> WIFI already turned off")
            self.android_command.adb_homekey(serialnumber)
        
    def wifiON(self, driver, serialnumber):
        print("<info> Turning on the wifi")
        logger.info("<info> Turning on the wifi")
        command = 'shell am start -a android.intent.action.MAIN -n com.android.settings/.wifi.WifiSettings'
        self.android_command.adb_exec_command(command, serialnumber)
        #subprocess.getoutput('adb shell am start -a android.intent.action.MAIN -n com.android.settings/.wifi.WifiSettings')

        net = self.check_network(driver)
        #print("net : ",net)
        if net != [2, 6]:
            try:
                for i in range(10):
                    try:
                        driver.find_element_by_xpath(el.Network['ON']).click()
                    except Exception:
                        driver.find_element_by_class_name("android.widget.Switch").click()
                    sleep(10)
                    try:
                        
                        conn = driver.find_element_by_xpath(el.Network['Connected']).is_displayed()
                       
                        if conn == True:
                            print("<WIFI> WIFI Turned ON and connected")
                            logger.info("<WIFI> WIFI Turned ON and connected")
                            self.android_command.adb_homekey(serialnumber)
                            break
                    except Exception:
                        sleep(8)
                        if i >= 1:
                            print("<Caution> Connecting to WIFI is taking more time....")
                            logger.warning("<Caution> Connecting to WIFI is taking more time....")
                        continue
                        if i >8:
                            print("<error> Failed to coonect to WIFI, Please check passwords are enetered for wifi")
                            logger.error("Failed to coonect to WIFI, Please check passwords are enetered for wifi")
            except Exception:
                #driver.find_element_by_xpath(el.Network['ON']).click()
                print("wifiON():  error in Turning on the wifi")
                logger.error("wifiON():  error in Turning on the wifi")
        else:
            print("<info> Mobile already connected to WIFI")
            logger.info("<info> Mobile already connected to WIFI")
            
    def check_network(self, driver):
        try:
            net = driver.network_connection
            #print("in check : ",net)
            return net
        except Exception as e:
            print("Error in getting network connection \n", e)
    def switch_data(self, driver, serialnumber):
        command = 'shell am start -n "com.android.settings/.Settings\"\$\"DataUsageSummaryActivity"'
        self.android_command.adb_exec_command(command, serialnumber)
        print(" <Info> Enabling the Data please wait...")
        logger.info("Enabling the Data please wait...")
        for i in range(5):
            net = self.check_network(driver)
            if net != 4:
                try:
                    driver.find_element_by_xpath("//android.widget.TextView[@text='Cellular data']").click()
                    sleep(2)
                    try:
                        for i in range(2):
                            sleep(2)
                            driver.find_element_by_id("android:id/button1").click()
                    except Exception:
                        pass
                    sleep(2)
                    net1 = self.check_network(driver)
                    if net1 == 4:
                        print(" <Mobile Data> Turned on DATA")
                        logger.info(" <Mobile Data> Turned on DATA")
                        break
                    else:
                        continue
                except Exception:
                    continue
                    print(" Failed to Turn on DATA")
                    logger.error(" Failed to Turn on DATA")
            if net == 4:
                try:
                    driver.find_element_by_xpath("//android.widget.TextView[@text='Cellular data']").click()
                    sleep(2)
                    try:
                        driver.find_element_by_id("android:id/button1").click()
                    except Exception:
                        pass
                    sleep(2)
                    net1 = self.check_network(driver)
                    if net1 != 4:
                        print(" <Mobile Data> Turned off DATA")
                        logger.info("<Mobile Data> Turned off DATA")
                        break
                    else:
                        continue
                except Exception:
                    continue
                    print(" Failed to Turn on DATA")
                    logger.error(" Failed to Turn on DATA")
                
        sleep(1)
        self.android_command.adb_homekey(serialnumber)
        
    def call(self, driver):
        
        try:
            sleep(3)
            if(self.longPress(driver, el.Call["Call"], 60000)):
                print("<info> Floor is Released now")
            
            else:
                print("Error: Call failed/Connection Unavailable")
                self.status_check(driver, self.InAppStatus)
                self.backbutton(driver, 1)
                return False
            
        except Exception as err:
            print("call(): Error occured \n", err)
            self.backbutton(driver, 1)
            return False
        
    def call_end(self, driver):
        try:
            driver.find_element_by_xpath(el.Call["CallEnd"]).click()
            print("<Call> Call was sucessfull")
            self.backbutton(driver, 1)
            return True
        except Exception:
            try:
                flag = driver.find_element_by_xpath(el.Status["Information"]).is_displayed()
            except Exception:
                print("Error: Call failed and sent Voice message")
                self.backbutton(driver, 1)
                return False                        
            if flag == True:
                print("<Warning> User/Participants Unavailable pop displayed and call failed")
                        

    def call_adhoc(self, driver):
        #print("<info> Making Adhoc call")
        try:
            sleep(3)
            driver.find_element_by_xpath(el.Call["addparticipent"]).click()
            sleep(3)
        except Exception:
            print("Error: Add participents Failed!!")
            pass

    def toast_status(self, driver):
        msg = {'Connection Unavailable':el.Toast["ConnUNavailable"]}
        
        for i, k in msg.items():
            try:
                flag = driver.find_element_by_xpath(k).is_displayed()
                if flag == True:
                    return i
            except Exception:
                continue
                                                 
        
    def call_broadcast(self, driver):
        for i in range(10):
            try:
                print(i)
                sleep(2)
                driver.find_element_by_xpath(el.broadcast['group']).click()
                
                print("clicked")
                sleep(2)
                driver.find_element_by_xpath(el.broadcast['brdcall']).click()
            except NoSuchElementException:

                self.swipe(driver)
                print("swiped")
                continue
            
    def merge_logs(self, fp, file):
        fp = el.Log["folderpath"]
        merge = fp+'\merge.txt'
        Analysis = fp+'\Analysis.txt'
        new = '\poc_app_logs.txt'
        old = '\poc_app_logs_old.txt'
        print("<info> Merging logs started from ", file)
        sleep(2)
        try:
            Mfile = open(merge, 'a+')
            Rfile = open(fp + file, 'r')
            size = os.path.getsize(merge)
            lines = Rfile.readlines()
            flag = True
            if size == 0:
                flag = False
            for line in lines:
                if flag or self.start_time in line:
                    Mfile.write(line)
                    flag = True 
                    if self.end_time in line:
                        flag = False
                        size = os.path.getsize(merge)
                        print("<Info> finished merging logs and size of is {0} \n".format(size))
                        return "stop"  
                    
        except FileNotFoundError:
            print("<Error> File path does not exist")
            exit()
        finally:
            Mfile.close()
            Rfile.close()    

            