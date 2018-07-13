'''
Created on 08-May-2018

@author: kodiak
'''

#import jumpssh
import paramiko
from time import sleep
import os

MDN = os.environ["MDN"]
Server = os.environ["Server"]

serverdict = {"QC3Primary":('192.168.30.74', 22), "QC3Secondary":('192.168.30.80', 22), "QC9Secondary":('10.3.1.183', 22), 
              "QC9Primary":('10.3.1.177', 22), "QC2Primary":('10.3.2.86', 22), "QC2Secondary":('10.3.2.90', 22),
               "QC7Primary":('10.3.1.66', 22), "QC7Secondary":('10.3.1.70', 22)}
server = serverdict[Server]
GW = "10.0.24.64"
la = ("10.0.24.64", 22)
print("****Started Outage reduction Bit enabler****\n")
print("<info> Establishing Gateway connection..")
print("<info> Gateway IP : ", GW)
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=GW, username="kodiak", password="kodiak")
    print("<Success> Gateway Connection Success ")
except Exception as err:
    print("<Failure> Gateway connection Failed.. Please check the connection")
    exit()
# create Transport for gateway
try:
    
    gwtp = ssh.get_transport()
    # create channel
    ch = gwtp.open_channel("direct-tcpip", server, la)
    print("<info> channel id {} created to establish connection to POC ".format(ch.get_id()))
    
    print("<info> Establishing connection to POC IP {}".format(server))
except Exception as err:
    print("<Failure> Channel creation Failed.. Please check the connection or Server may Down\n", err)
    exit()
try:
    qc = paramiko.SSHClient()
    qc.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    qc.connect(hostname=server, username="kodiak", password="kodiak", sock=ch)
    print("<Success> POC Connection Success ")
except Exception as err:
    print("<Failure> POC connection Failed.. Please check the connection")
    exit()

print("Please wait Executing the Outage Reduction commands.. it will take around 20sec\n")
channel = qc.invoke_shell()
sleep(4)
channel.send("su")
channel.send("\n")
sleep(4)
channel.send("kodiak")
channel.send("\n")
sleep(2)
channel.send(". /etc/kodiakDG.conf")
channel.send("\n")
channel.send("!ttdir")
#channel.send('ttdir DG_$PTTSERVERID"_6"')
channel.send("\n")
sleep(2)
#channel.send("desc DG.POC_PREESTSESSIONINFO;")
#channel.send("\n")
#sleep(2)
sqlselectcmd="select RESTARTFLAG from DG.POC_PREESTSESSIONINFO where MDN=" + MDN + ";"
channel.send(sqlselectcmd)
channel.send("\n")
sleep(3)
sqlupdatecmd="update DG.POC_PREESTSESSIONINFO set RESTARTFLAG=1 where MDN=" + MDN + ";"
channel.send(sqlupdatecmd)
channel.send("\n")
sleep(3)
channel.send(sqlselectcmd)
channel.send("\n")
sleep(3)
channel.send("exit")
channel.send("\n")
sleep(3)

def check_console(console):
    if channel.recv_ready():
        print("****************Console Logs*****************")
        buf = ""
        #print(type(buf))
        buf = channel.recv(9999)
        buf = buf.decode(encoding='ascii')
        print(buf)
        print("****************End of Console Logs*****************")
    
buffer = check_console("0 rows found.")

channel.close()
