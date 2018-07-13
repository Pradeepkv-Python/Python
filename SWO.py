import xml.etree.ElementTree as ET
import QCServerlogin
from time import sleep
import os

Server = os.environ["Server"]
Operation = os.environ["Operation"]
ServerElement = os.environ["ServerElement"]

def xml_data(rootele, server, element):
    t = ET.parse('F:\AutomationData\\AutomationConfig.xml')
    t = t.getroot()
    #print(t)
    for i in t.iter(rootele):
        for j in i.iter(server):
            for k in j.iter(element):
                return element, k.text

    #t.write('F:\AutomationData\\AutomationConfig.xml')
cmd = "service kodiakDG status"
def server_cmd(cmd):
    ele, IP = xml_data("IP", Server, ServerElement)
    ssh = QCServerlogin.ServerLogin("10.0.24.51", IP)
    obj = ssh.Server_ssh()
    
    channel = obj.invoke_shell()
    ch_data = str()
    Value = True
    while Value:
        if channel.recv_ready():
            ch_data = channel.recv(9999)
            ch_data = ch_data.decode('ascii')
            print(ch_data)
        else:
            continue
        
        if ch_data.endswith("]$ "):
            sleep(1)
            #print("not a root user")
            channel.send("killall -u cliadmin")
            channel.send("\n")
            channel.send("su")
            
            channel.send("\n")
            sleep(2)
        elif ch_data.endswith("Password: "):
            #print("pwd")
            channel.send("kodiak")
            channel.send("\n")
            sleep(2)
            
        elif ch_data.endswith("]# "):
            print("<Info> Logged in as a root user")
            channel.send(cmd)
            channel.send("\n")
            sleep(2)
            print("<Info> '{}' command executed ".format(cmd))

            Value = False
    
    ch_data = channel.recv(9999)
    #print(type(ch_data))
    print(ch_data.decode("ascii", "ignore"))
    channel.send("exit")
    channel.send("\n")
    sleep(2)
    ch_data = channel.recv(9999)
    print(ch_data.decode("ascii", "ignore"))
    channel.close()
    
def server_status(Server, ServerElement):
    ele, IP = xml_data("IP", Server, ServerElement)
    ssh = QCServerlogin.ServerLogin("10.0.24.51", IP)
    obj = ssh.Server_ssh()
    
    stdin, stdout, stderr = obj.exec_command("tail -20 /DGlogs/softmanagerinit.log")
    sleep(2)
    #print("ll")
    data = stdout.readlines()
    data = " ".join(data)
    data = data.splitlines()
    print("------------------------------------------------------------------")
    #with open()
    stat = []
    for event in data:
        if "Received Active Event" in event or "Received Standby Event" in event or "Killing Process" in event or "Initializing the Database" in event or "Exiting the Software Manager" in event or "Waiting for SM_START_COMPLETE" in event:
            stat.append(event)
        #print(stat)
            
    try:
        status = stat.pop()
        stat.clear()
        #print(status)
        if "Active" in status:
            print("Received Active Event")
            obj.close()
            return "Active", ele, IP
        elif "Standby" in status:
            print("Received Standby Event")
            obj.close()
            return "Standby", ele, IP
        elif "Killing Process" in status:
            print("<Info> Server is restarting/stopped")
            obj.close()
            return "Service Shutting down in progress..", ele, IP
        
        elif "Initializing the Database" in status:
            print("<Info> Server restarting in Progress")
            obj.close()
            return "Restarting/Initializing in Progress", ele, IP
        
        elif "Exiting the Software Manager" in status:
            print("<Info> Server restarting in Progress")
            obj.close()
            return "Server Completely in stopped state", ele, IP
        
        elif "Waiting for SM_START_COMPLETE" in status:
            print("<Info> Server restarting in Progress")
            obj.close()
            return "Waiting for SM_START_COMPLETE message", ele, IP
        
        else:
            print("Could not able to find status of Server")
            obj.close()
            return "NULL", ele, IP
    except Exception as err:
        print("<Error> Server pop error \n", err)

def all_server_status(Server, Serverlist=None):
    placeholder = "%s (%s) => %s"
    Status = {}
    if Serverlist == None:
        Serverlist = ["PPOC", "PMedia", "SPOC", "GPOC", "GMedia"]
    else:
        Serverlist = [Serverlist]
    for i in Serverlist:
        try:
            serstatus, server, IP = server_status(Server, i)
            print(placeholder % (server, IP, serstatus))
            print("------------------------------------------------------------------")
            
            Status[i]=serstatus
        except Exception as err:
            print("<Error> Nothing returned from server_status()")
            print("------------------------------------------------------------------")
    print("<Status> Servers Status")
    print("**********************************")
    for i, k in sorted(Status.items(), reverse = True):
        print(i + " ===> " + k)
    print("**********************************")

if Operation == "Status":
    all_server_status(Server)
    exit()
if Operation == "Stop":
    s, r, i = server_status(Server, ServerElement)
    cmd = "service kodiakDG stop"
    if s == "Active":
        print("<info> Executing 'STOP' command.. please wait")
        server_cmd(cmd)
        print("<info> Please WAIT as rechecking the status of server after 15 sec")
        sleep(15)
        all_server_status(Server)
        print("<Info> PLEASE CHECK STATUS OPTION FOR FURTHER STATUS")
    else:
        print("<Warning> Server not in active state to do SWO")
if Operation == "Start":
    s, r, i = server_status(Server, ServerElement)
    cmd = "service kodiakDG start"
    if s == "Active":
        print("<Warning> Server already in active state")
        exit()
        
    else:
        print("<info> Executing 'START' command.. please wait")
        server_cmd(cmd)
        print("<info> Please WAIT as rechecking the status of server after 15 sec")
        sleep(10)
        all_server_status(Server)
        print("<Info> PLEASE CHECK STATUS OPTION FOR FURTHER STATUS")
        exit()
if Operation == "Restart":
    s, r, i = server_status(Server, ServerElement)
    cmd = "service kodiakDG restart"
    if s == "Active" or s == "Standby":
        print("<info> Executing 'START' command.. please wait")
        server_cmd(cmd)
        print("<info> Please WAIT as rechecking the status of server after 15 sec")
        sleep(15)
        all_server_status(Server)
        print("<Info> PLEASE CHECK STATUS OPTION FOR FURTHER STATUS")
        exit()
        
    else:
        print("<Warning> Server not in active/Standby state to restart")
        