'''
Created on 18-May-2018

@author: kodiak
'''

import paramiko
import os

class ServerLogin():
    
    def __init__(self, Gateway, QCserverIP):
        self.GW = Gateway
        self.Server = QCserverIP
        
        
    def gw_login(self, GW):
        try:
            print("<Info> Trying to connecting to Gateway : ", GW)
            
            gwssh = paramiko.SSHClient()
            gwssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            gwssh.connect(hostname=GW, username="kodiak", password="kodiak")
            print("<Success> Gateway Connection Success ")
            return gwssh
            
        except Exception as err:
            print("<Failure> Gateway connection Failed.. Please check the connection \n", err)
            exit()
            
    def create_channel(self):
        
        Tserver = self.Server, 22
        Tgw = self.GW, 22
        gwssh = self.gw_login(GW=self.GW)
        
        try:
            print("<info> Creating transport Please wait...")
            gwtp = gwssh.get_transport()
            #print("ll : ", Tserver, Tgw)
            gwch = gwtp.open_channel("direct-tcpip", Tserver, Tgw)
            print("<Success> channel id {} created to establish connection to POC ".format(gwch.get_id()))
    
            #print("<info> Establishing connection to POC IP {}".format(Tserver))
            return gwch
        except Exception as err:
            print("<Failure> Channel creation Failed.. Please check the connection or Server may Down\n", err)
            exit()
            
    def Server_ssh(self):
        ch = self.create_channel()
        try:
            print("<info> Trying to connect POC/XDM server and IP is ", self.Server)
            Serverssh=paramiko.SSHClient()
            Serverssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            Serverssh.connect(hostname=self.Server, username="kodiak", password="kodiak", sock=ch)
            print("<Success> Connection is Successful")
            return Serverssh
        except Exception as err:
            print("<Failure> Connecting to Server Failed. \n", err)
            exit()
            