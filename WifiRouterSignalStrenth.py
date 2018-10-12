'''
Created on 28-Sep-2018

@author: kodiak
'''

import os, subprocess
import telnetlib
from time import sleep
import re

ip = "10.0.5.49"

cmdlist = []
clientdbm = ['-1','-4', '2', '5', '8', '11', '14', 'maximum', 'local']
txdbm = ['-1','-4', '2', '5', '8', 'maximum', '2']

def rssi():
    l = []
    subprocess.getstatusoutput(r"adb shell dumpsys wifi > C:\Users\kodiak\test.txt")
    with open(r"C:\Users\kodiak\test.txt", "r+") as f:
        for line in f:
            if "Current band = 5GHz bandcurrent RSSI is: " in line:
                l.append(line)
    try:
        #print(l[-1])
        r = re.search("RSSI is:\s-\d{1,3}", l[-1])
        print(r.group())
    except Exception:
        print("<Error> No signal strenth measures found in device log files")
def chnage_signal_level(t):
    t.write(b'configure terminal' + b"\n")
    sleep(2)
    t.write(b'interface dot11radio 1' + b"\n")
    sleep(2)
    print(t.read_until(b"#").decode("utf-8"))
    flag = True
    for txlevel in txdbm:
        print("="*40)
        if flag == False:
            t.write(b'configure terminal' + b"\n")
            sleep(2)
            t.write(b'interface dot11radio 1' + b"\n")
        t.write(b'power local '+ bytes(txlevel, 'utf8') + b"\n")
        sleep(2)
        print(t.read_until(b"#").decode("utf-8"))
        '''flag = True
            for clientlevel in clientdbm:
            print("="*40)
            #print(clientlevel)
            if flag == False:
                t.write(b'configure terminal' + b"\n")
                sleep(2)
                t.write(b'interface dot11radio 1' + b"\n")
            t.write(b'power client '+ bytes(clientlevel, 'utf8') + b"\n")
            sleep(2)
            print(t.read_until(b"#").decode("utf-8"))'''
        sleep(2)
        t.write(b'end' + b"\n")
        print("in end")
        sleep(2)
        print(t.read_until(b"#").decode("utf-8"))
        print(">> Executed Transimitter power and Client power : ",txlevel)
        sleep(60)
        rssi()
        flag = False
def close_client_connection(t, operation):
    if operation == "close":
        cmd = b"shut int"
    else:
        cmd = b"no shut"
    t.write(b'configure terminal' + b"\n")
    print("con")
    sleep(2)
    t.write(b'interface dot11radio 1' + b"\n")
    print(t.read_until(b"#").decode("utf-8"))
    if operation == "close":
        t.write(b'shut' + b"\n")
        print("cwon")
    else:
        t.write(b'no shut' + b"\n")
        print("won")
    sleep(2)
def check_interface_status(t):
    t.write(b'show ip interface brief' + b"\n")
    print(t.read_until(b"#").decode("utf-8"))
    
    
            
try:
    def telnet():
        t = telnetlib.Telnet(ip)
        print(t.read_until(b"Username:"))
        t.write(b'Cisco' + b"\n")
        print(t.read_until(b"Password:"))
        t.write(b'Cisco' + b"\n")
        print(t.read_until(b"AP-Standalone>"))
        sleep(2)
        t.write(b'en' + b"\n")
        sleep(2)
        t.read_until(b"Password:")
        sleep(2)
        t.write(b'Cisco' + b"\n")
        sleep(2)
        print(t.read_until(b"AP-Standalone#").decode("utf-8"))
        return t
    t=telnet()
    chnage_signal_level(t)
    '''t=telnet()
    close_client_connection(t, "start")
    t=telnet()
    check_interface_status(t)'''
finally:
    t.close()
    

            
