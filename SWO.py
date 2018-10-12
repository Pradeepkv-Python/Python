import xml.etree.ElementTree as ET
import QCServerlogin
from time import sleep
import os


Server = os.environ["Server"]
Operation = os.environ["Operation"]
ServerElement = os.environ["ServerElement"]

def xml_data(rootele, server, element):
    t = ET.parse(r'C:\Users\kodiak\eclipse-workspace\MPTT\src\AutomationConfig.xml')
    t = t.getroot()
    #print(t)
    for i in t.iter(rootele):
        for j in i.iter(server):
            for k in j.iter(element):
                #print(element, k.text)
                return element, k.text

    #t.write('F:\AutomationData\\AutomationConfig.xml')
cmd = "service kodiakDG status"
mcmd = "systemctl status MediaServer"
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
    if ele in ["PMedia", "GMedia"]:
        #print("in Media part : ", ele)
        stdin, stdout, stderr = obj.exec_command("systemctl status MediaServer")
        data = stdout.read().decode("ascii", "ignore")
        #print(data)
        import re 
        data = re.search("Active\S\s(\w+)", data)
        data = data.group(1)
        data = data.capitalize()
        stat = []
        stat.append(data)
    else:
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
    status, servername, serverip = server_status(Server, ServerElement)
    if servername in ["PMedia", "GMedia"]:
        cmd = "systemctl stop MediaServer"
    else:
        cmd = "service kodiakDG stop"
    if status == "Active" or servername == "SPOC":
        print("<info> Executing 'STOP' command.. please wait")
        print("Command : ",cmd)
        server_cmd(cmd)
        print("<info> Please WAIT as rechecking the status of server after 15 sec")
        sleep(15)
        all_server_status(Server)
        print("<Info> PLEASE CHECK STATUS OPTION FOR FURTHER STATUS")
    else:
        print("<Warning> Server not in active state to do SWO")
if Operation == "Start":
    status, servername, serverip = server_status(Server, ServerElement)
    if servername in ["PMedia", "GMedia"]:
        cmd = "systemctl start MediaServer"
    else:
        cmd = "service kodiakDG start"
    
    if status == "Active":
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
    status, servername, serverip = server_status(Server, ServerElement)
    if servername in ["PMedia", "GMedia"]:
        cmd = "systemctl restart MediaServer"
    else:
        cmd = "service kodiakDG restart"
    if status == "Active" or status == "Standby":
        print("<info> Executing 'RESTART' command.. please wait")
        server_cmd(cmd)
        print("<info> Please WAIT as rechecking the status of server after 15 sec")
        sleep(10)
        all_server_status(Server)
        print("<Info> PLEASE CHECK STATUS OPTION FOR FURTHER STATUS")
        exit()
        
    else:
        print("<Warning> Server not in active/Standby state to restart")
        
class AutoSWO:
    
    def __init__(self, server, opsflag=0):
        self.server = server
        self.opsflag = opsflag
        
    def xml_data(self, rootele, server, serverelement):
        t = ET.parse(r'C:\Users\kodiak\eclipse-workspace\MPTT\src\AutomationConfig.xml')
        t = t.getroot()
        for i in t.iter(rootele):
            for j in i.iter(server):
                for k in j.iter(serverelement):
                    return serverelement, k.text
        
    def server_status(self, serverelement):
        serverele, IP = self.xml_data("IP", self.server, serverelement)
        ssh = QCServerlogin.ServerLogin("10.0.24.51", IP)
        obj = ssh.Server_ssh()
        if serverele in ["PMedia", "GMedia"]:
            stdin, stdout, stderr = obj.exec_command("systemctl status MediaServer")
            data = stdout.read().decode("ascii", "ignore")
            #print(data)
            import re 
            data = re.search("Active\S\s(\w+)", data)
            data = data.group(1)
            data = data.capitalize()
            stat = []
            stat.append(data)
        else:
            stdin, stdout, stderr = obj.exec_command("tail -20 /DGlogs/softmanagerinit.log")
            sleep(2)
            #print("ll")
            data = stdout.readlines()
            data = " ".join(data)
            data = data.splitlines()
            print("------------------------------------------------------------------")
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
                return "Active", serverele, IP
            elif "Standby" in status:
                print("Received Standby Event")
                obj.close()
                return "Standby", serverele, IP
            elif "Killing Process" in status:
                print("<Info> Server is restarting/stopped")
                obj.close()
                return "Service Shutting down in progress..", serverele, IP
            
            elif "Initializing the Database" in status:
                print("<Info> Server restarting in Progress")
                obj.close()
                return "Restarting/Initializing in Progress", serverele, IP
            
            elif "Exiting the Software Manager" in status:
                print("<Info> Server restarting in Progress")
                obj.close()
                return "Server Completely in stopped state", serverele, IP
            
            elif "Waiting for SM_START_COMPLETE" in status:
                print("<Info> Server restarting in Progress")
                obj.close()
                return "SM_START_COMPLETE", serverele, IP
            
            else:
                print("Could not able to find status of Server")
                obj.close()
                return "NULL", serverele, IP
        except Exception as err:
            print("<Error> Server pop error \n", err)
        
    def server_cmd(self, cmd, ServerElement):
        serverele, IP = self.xml_data("IP", self.Server, ServerElement)
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
        return True
    
    def checkserversflag(self, Serverlist):
        l = []
        for serverelement, status in Serverlist.items():
            if status == None:
                l.append(serverelement)
            else:
                pass
        return l
    def get_command(self, serverele, cmd):
        if serverele in ["PMedia", "GMedia"]:
            cmd = "systemctl "+ cmd + " MediaServer"
        else:
            cmd = "service kodiakDG " + cmd
        return cmd
    
    def execute_status_cmd(self, serverele, cmd):
        status = self.server_status(serverele)
        if cmd == "stop" and status in ["Active", "Standby", "SM_START_COMPLETE"]:
            cmd = self.get_command(serverele, cmd)
            flag = self.execute_status_cmd(serverele, cmd)
            if flag == True:
                print("<Auto> Command Executed successfully")
                return True
        elif cmd == "restart" or cmd == "start" and status not in ["Active", "Standby", "SM_START_COMPLETE"]:
            cmd = self.get_command(serverele, cmd)
            flag = self.execute_status_cmd(serverele, cmd)
            if flag == True:
                print("<Auto> Command Executed successfully")
                return True
        else:
            print("<Auto> Error in execute_status_cmd func")
            return False
            
    
    def swo(self):
        Serverlist = {"PPOC":None, "PMedia":None, "SPOC":None, "GPOC":None, "GMedia":None}
        for serverelement in Serverlist:
            status, serverelement, ip = self.server_status(serverelement)
            
            if status in ["Active", "Standby", "SM_START_COMPLETE"]:
                Serverlist[serverelement]=status
        l = self.checkserversflag(Serverlist)
        if bool(l):
            print("Servers Status returned None for : ", l)
            
        flag = self.execute_status_cmd("SPOC", "stop")
        if flag == True:
            print("<Auto> SPOC stopped")
        else:
            print("<Auto> error in stopping server SPOC, Execution stopped")
            exit()
        
        
        
        
        
                
        
        
        
        

        