'''
Created on 23-Feb-2018

@author: kodiak
'''
import ElementsText as el
import os, subprocess
from time import sleep


class AdbCommands():
    '''
    This class contains Only adb commands functions
    
    TO WORK ON REMOTE MACHINE:
    In remote machine follow these steps
    1) stop already running adb server ==> adb kill-server
    2) run adb command : ==> adb -a -P <port number> nodaemon server
        ex: adb -a -P 5037 nodaemon server
    
    In local Machine
    1) All adb commands should be executed as below
        adb -H <IP of remote machine> -P <Port number where adb server started at remote machine> command
        ex: adb -H 10.0.5.27 -P 5037 devices
    '''
    devSerials = {}
    def __init__(self, IP):
        '''
        Constructor
        '''
        self.IP = IP
    
    def adb_uninstall_builds(self, serialnumber, build = el.Packages):
        for i, k in build.items():
            print("please wait uninstalling ", k)
            adb = "adb -H " + self.IP + " -s " + serialnumber
            adb = adb + " uninstall " + k 
            #os.system(adb)
            out = os.system(adb) 
            return out  
        print("<info> Uninstalled all the builds successfully")
    
    def adb_install_build(self, serialnumber, path=el.input["Path"]):
        print("Intsalling the build Please wait....\n given build path : ", path)
        adb = "adb -H " + self.IP + " -s " + serialnumber
        adb = adb + " install " + path
        out = os.system(adb) 
        return out   
        
    
    def adb_launch(self, serialnumber, package=el.input["package"], action='start'):
        '''Launching App through ADB commands'''
        adb = "adb -H " + self.IP + " -s " + serialnumber
        if package == 'att':
            package = el.Packages["att"]
        elif package == 'vzw':
            package = el.Packages["vzw"]
        elif package == 'sprint':
            package = el.Packages["sprint"]
        try:
            
            if action in ['start', 'Start']:
                adb = adb + " shell am start " + package +"/.StartupActivity"
            elif action in ['stop', 'Stop']:
                adb = adb + " shell am force-stop " + package
                
            elif action in ['clear', 'Clear']:
                adb = adb + " shell pm clear " + package
                
            #sleep(2)
            
            os.system(adb)
            sleep(8)
            return True
    
        except Exception as err:
            print(adb + "_launch(): Error occured \n", err)
            return False
    def adb_OSversion(self, serialnumber,):
        adb = "adb -H " + self.IP + " -s " + serialnumber
        Version = subprocess.getoutput(adb + " shell getprop ro.build.version.release")
        return int(Version[0])
    def adb_chrome_launcher(self, serialnumber,):
        adb = "adb -H " + self.IP + " -s " + serialnumber
        os.system('adb shell am start -n com.android.chrome/com.google.android.apps.chrome.Main')
        return True
    def adb_get_wifi_IP(self, serialnumber,):
        adb = "adb -H " + self.IP + " -s " + serialnumber
        ip = subprocess.getoutput(adb + " shell ifconfig wlan0")
        return ip
    def adb_get_data_IP(self, serialnumber,):
        adb = "adb -H " + self.IP + " -s " + serialnumber
        ip = subprocess.getoutput(adb + " shell ifconfig rmnet_data0")
        return ip
    def adb_switch_apptoBG(self, serialnumber, package=el.input["package"]):
        adb = "adb -H " + self.IP + " -s " + serialnumber
        try:
            os.system(adb + " shell input keyevent 3")
            print("<info> Application Moved to BG")
            sleep(5)
            return True
        except Exception:
            print("adb_switch_apptoBG(): Error occured \n")
    def adb_switch_apptoFG(self, serialnumber):
        adb = "adb -H " + self.IP + " -s " + serialnumber
        for i in range(3):
            if(self.adb_launch(serialnumber, action='start')):                    
                print("<info> Application Moved to FG")
                break
        sleep(5)
        return True
    def adb_log_timestamp(self, serialnumber,):
        adb = "adb -H " + self.IP + " -s " + serialnumber
        
        date = subprocess.getoutput(adb + " shell date +%m/%d%H:%M:%S")
        devtime = date[0:5] + ' '+date[5:13]
        print("dev time : ", devtime)
        return devtime
    def adb_ops_timestamp(self, serialnumber,):
        adb = "adb -H " + self.IP + " -s " + serialnumber
        time = subprocess.getoutput(adb + " shell date +%I:%M%p")
        return time
    def adb_exec_command(self, command, serialnumber=''):
        if serialnumber == '':
            adb = "adb -H " + self.IP + " "
        else:
            adb = "adb -H " + self.IP + " -s " + serialnumber + " "
        #print("commsnad : ", adb + command)
        out = subprocess.getoutput(adb + command)
        return out
    def adb_homekey(self, serialnumber):
        adb = "adb -H " + self.IP + " -s " + serialnumber
        out = subprocess.getoutput(adb + ' shell input keyevent 4')
        #print("home", out)
        return out
    
    def generate_seq(self):
        for i in range(1, 10):
            yield i
    
    def adb_Android_device_finder(self):
        
        var = self.adb_exec_command('devices')
        
        devicecount = 0
        #var = subprocess.getoutput(adb)
        #print(var)
        var = str(var)
        #print(var.splitlines())
        var2 = var.splitlines()
        #print(var2)
        a = self.generate_seq()
        for i in range(len(var2)):
            if var2[i] not in ['List of devices attached', '* daemon started successfully *', '* daemon not running. starting it now at tcp:5037 *']:
                ser = str(var2[i])
                print(ser)
                c = ser.find("\td") or ser.find("\to")
                self.devSerials[next(a)] = ser[0:c]
                devicecount += 1
                    
        print("Connected Device Count : {}\nDevices Serial numbers : {}\n".format(devicecount, self.devSerials))