'''
Created on 13-Feb-2018

@author: pradeep
'''
import sqlite3
import os
import time

Audit = os.environ["Audit"]
Operation = os.environ["Operation"]
Values = os.environ["Values"]
#valuessim = "'12345', 'airtel', 'pradeep', 'patil'"
#valuesmob = "'Device3', 'samsung', '1234', '567', 'android', 'pradeep', 'patil'"
TransferredFrom = os.environ["TransferredFrom"]
TransferredTo = os.environ["TransferredTo"]
Device = os.environ["Device"]
SimNumber = os.environ["SimNumber"]
date = time.asctime()
'''Audit = "Mobile"
Operation = "UPDATE"
Values = "'Device3', 'samsung', '1234', '567', 'android', 'pradeep', 'patil'"
#valuessim = "'12345', 'airtel', 'pradeep', 'patil'"
#valuesmob = "'Device3', 'samsung', '1234', '567', 'android', 'pradeep', 'patil'"
TransferredFrom = "Patil"
TransferredTo = "Syed"
Device = "Device3"
SimNumber = "12345"'''


def sql(command):
    #conn = sqlite3.connect("E:\\PTT\\test.db")
    try:
        conn = sqlite3.connect("F:\\AutomationData\\WBInventory.db")
    except Exception as err:
        print(err)
        exit()
    db = conn.cursor()
    try:
        db.execute(command)
    except Exception as err:
        print(err)
        exit()
    
    formattermob = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s"
    formattersim = "%s\t%s\t%s\t%s\t%s"
    res = db.fetchall()
    #print(res)
    if Audit == "Mobile":
        print(formattermob % ('Device', 'Manufacturer', 'IMEI', 'RFID', 'OS', 'TransferredFrom', 'TransferredTo', 'ModifiedDate'))
        print("-"*120)
    elif Audit == "SIM":
        print(formattersim % ('SIMNumber', 'Operator', 'TransferredFrom', 'TransferredTo', 'ModifiedDate'))
        print("-"*80)
    #print(formatter)
    for i in res:
        #print(i)
        if Audit == "Mobile":
            #print(" in ")
            #print(formattermob % ('Device', 'Manufacturer', 'IMEI', 'RFID', 'OS', 'TransferredFrom', 'TransferredTo', 'ModifiedDate'))
            print(formattermob % i)
        elif Audit == "SIM":
            #print(formattersim % ('SIMNumber', 'Operator', 'TransferredFrom', 'TransferredTo', 'ModifiedDate'))
            print(formattersim % i)
    #print(res)
    conn.commit()
    conn.close()
    
    

#sql statements
cratetablesim = "create table SIM (SIMNumber, Operator, TransferredFrom, TransferredTo, ModifiedDate);"
cratetablemobile = "create table MobileDevices (Device, Manufacturer, IMEI, RFID, OS, TransferredFrom, TransferredTo, ModifiedDate);"
addnewdevice = "insert into MobileDevices values ({0}, '{1}');".format(Values, date)
#print(addnewdevice)
addnewsim = "insert into SIM values ({0}, '{1}');".format(Values, date)
deletedevice = "delete from MobileDevices where Device='{0}';".format(Device)
deletesim = "delete from SIM where SIMNumber='{0}';".format(SimNumber)
updatemobile = "update MobileDevices set TransferredFrom='{0}', TransferredTo='{1}', 'ModifiedDate'='{2}' where Device='{3}';".format(TransferredTo,TransferredFrom,time.asctime(), Device)
updatesim = "update SIM set TransferredFrom='{0}', TransferredTo='{1}', 'ModifiedDate'='{2}' where SIMNumber='{3}';".format(TransferredTo,TransferredFrom, time.asctime(), SimNumber)
selectdevice = "select * from MobileDevices;"
selectsim = "select * from SIM;"
fetchlist = "select {0} from MobileDevices;".format("Device")
#sql(cratetablemobile)
#sql(cratetablesim)
#print(sql(fetchlist))
#exit()
if Audit == "Mobile":
    if Operation == "VIEW_ALL":
        sql(selectdevice)
    elif Operation == "ADD":
        sql(addnewdevice)
        sql(selectdevice)
    elif Operation == "DELETE":
        sql(deletedevice)
        sql(selectdevice)
    elif Operation == "UPDATE":
        sql(updatemobile)
        sql(selectdevice)
        
if Audit == "SIM":
    if Operation == "VIEW_ALL":
        sql(selectsim)
    elif Operation == "ADD":
        sql(addnewsim)
        sql(selectsim)
    elif Operation == "DELETE":
        sql(deletesim)
        sql(selectsim)
    elif Operation == "UPDATE":
        sql(updatesim)
        sql(selectsim)
