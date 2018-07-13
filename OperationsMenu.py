'''
Created on 08-Jan-2018

@author: kodiak
'''
import Modules
from time import sleep

ptx = Modules.ModulesforPTT('4723', "127.0.0.1")

print('''1) Install Build 
2) Continue for feature testing''')

ch = int(input("Enter Your choice : "))
if ch == 1:
    ptx.uninstall_builds()
    ptx.install_build()
if ch >= 2:
    pass
driver = ptx.appium_driver()

while driver:
    if ptx.status_check(driver, ptx.InAppStatus) == False:
        ptx.adb_launch()

    print("""=======================Menu=======================\n
1) Activation and login                                             2) XDM Operation from device
3) XDM Operation from CAT [Unavailable]                             4) Calls
5) PTX Operation                                                    6) Network Operation
7) Logout, Re-login and ADB commands                                8) Background and Foreground
9) Presence change between Avalable to DND and viceversa           10) Copy PTT files                                                 
11) SWO [Unavailable]        12) Rehome [Unavailable]        13) Outage reduction [Unavailable]              14) exit\n
=================================================\n""")
    def choose():
        choice = int(input("Please choose your operation :"))
        return choice
    choice = choose()
    

    if choice == 1:
        while True:
            print("""=====Activation and login=====
1) Activation
2) Back
==================""")
            choice = choose()
            if choice == 1:
                
                print("<info> Clear the app data and activation")
                
                ptx.adb_launch(action="clear")
                ptx.adb_launch()
                ptx.activation(driver)
            
            elif choice == 2:
                break
                
    
#Contact Operation    
    elif choice == 2:
        while True:
            print("""=====Contact mgmt=====
1) Contact operation
2) Group operation
3) Delete Conatct
4) Back
==================""")
            choice = choose()
            if choice == 1:
                contactcount = int(input("How many contacts need to add? :"))
                if(ptx.moveto_contact(driver)):
                    ptx.add_contacts(driver, contactcount)
                
            
            elif choice == 2:
                groupcount = int(input("How many Groups need to add? :"))
                if(ptx.moveto_group(driver)):
                    ptx.add_group(driver, groupcount)
            
            elif choice == 3:
                contactcount = int(input("How many contacts need to delete?"))
                if(ptx.moveto_contact(driver)):
                    ptx.delete_contacts(driver, contactcount)
            
            elif choice == 4:
                break
    #XDM operation from CAT
    elif choice == 3:
        print("need to implement in Python")
        
    elif choice == 4:
        while True:
            print("""=====Calls=====
1) 1-1 call
2) Adhoc call
3) Group Call
4) Back
==================""")
            choice = choose()
            if choice == 1:
                print("\n Making 1-1 call")
                ptx.moveto_contact(driver)
                flag, Presence = ptx.search_mdn(driver)
                if Presence != 'Available':
                    print("<Warning> Can't complete call as contact is offline")
                    break
                ptx.call(driver)
            elif choice == 2:
                print("\n Making Adhoc call")
                ptx.moveto_contact(driver)
                flag, Presence = ptx.search_mdn(driver)
                if Presence != 'Available':
                    print("<Warning> Can't complete call as contact is offline")
                    break
                ptx.call_adhoc(driver)
                ptx.grp_addmembers(driver, 2)
                ptx.call(driver)
            elif choice == 3:
                print("\n Making Group call")
                ptx.moveto_group(driver)
                flag = ptx.search_group(driver)
                if flag == False:
                    print("Failed to search group, Going back")
                    break
                ptx.call(driver)
            elif choice == 4:
                break

    #PTX Operation
    if choice == 5:
        while True:
            print("""=====PTX menu=====
1) PTX in Contact tab
2) PTX in Group tab
3) Back
==================""")
            choice = choose()
            if choice == 1:
                ptx.moveto_contact(driver)
                
                while True:
                    print("""=====PTX menu=====
1) PTX In Call screen
2) PTX In second level screen with status
3) Back
==================""")
                    choice = choose()
                    if choice == 2:
                        print("""=====sending All PTX message type=====""")
                        flag = ptx.search_mdn(driver)
                     
                        if flag == False:
                            print("Failed to search MDN. Going back to menu")
                            break
                        ptx.ptx_sendText(driver)
                        ptx.ptxmsgStatus(driver, "text")
                        ptx.ptx_sendAlert(driver)
                        #ptx.ptxmsgStatus(driver, "alert2")
                        ptx.ptx_sendImage(driver)
                        ptx.ptxmsgStatus(driver, "image")
                        ptx.ptx_sendvideo(driver)
                        ptx.ptxmsgStatus(driver, "video")
                        ptx.ptx_sendLocation(driver)
                        ptx.ptxmsgStatus(driver, "location")
                        ptx.ptx_sendVoiceMessage(driver)
                        ptx.ptxmsgStatus(driver, "audio")
                        ptx.backbutton(driver, 2)
                    elif choice == 1:
                        print("""=====send All PTX message type=====""")
 
                        flag, presence = ptx.search_mdn(driver)
                        if flag == False:
                            print("Failed to search MDN. Going back to menu")
                            break
                        ptx.ptx_sendText(driver)
                        ptx.backbutton(driver, 1)
                        ptx.ptx_sendAlert(driver)
                        ptx.ptx_sendImage(driver)
                        ptx.ptx_sendvideo(driver)
                        ptx.ptx_sendLocation(driver)
                        ptx.ptx_sendVoiceMessage(driver)
                        ptx.backbutton(driver, 1)
                        
                    elif choice == 3:
                        break
            if choice == 2: 
                ptx.moveto_group(driver)
                
                while True:
                    print("""=====PTX menu=====
1) PTX In Call screen
2) PTX In second level screen with status
3) Back
==================""")
                    choice = choose()
                    if choice == 2:
                        print("""=====send All PTX message type=====""")
                        flag = ptx.search_group(driver)
                        if flag == False:
                            print("Failed to search group, Going back")
                            break
                        ptx.ptx_sendText(driver)
                        ptx.ptxmsgStatus(driver, "text")
                        ptx.ptx_sendImage(driver)
                        ptx.ptxmsgStatus(driver, "image")
                        ptx.ptx_sendvideo(driver)
                        ptx.ptxmsgStatus(driver, "video")
                        ptx.ptx_sendLocation(driver)
                        ptx.ptxmsgStatus(driver, "location")
                        ptx.ptx_sendVoiceMessage(driver)
                        ptx.ptxmsgStatus(driver, "audio")
                        ptx.backbutton(driver, 2)
                    elif choice == 1:
                        print("""=====send All PTX message type=====""")
                        flag = ptx.search_group(driver)
                        if flag == False:
                            print("Failed to search group, Going back")
                            break
                        ptx.ptx_sendText(driver)
                        ptx.ptx_sendImage(driver)
                        ptx.ptx_sendvideo(driver)
                        ptx.ptx_sendLocation(driver)
                        ptx.ptx_sendVoiceMessage(driver)
                        ptx.backbutton(driver, 1)
                        
                    elif choice == 3:
                        break          
            elif choice == 3:
                break    
            
    #Network Operation
    if choice == 6:
        while True:
            print("""=====Network menu=====
1) Switch DATA to WIFI and vice versa
2) Back
==================""")
            choice = choose()
            if choice == 1:
                ptx.network_switch(driver)
            elif choice == 2:
                break
            
    #Logout and login
    if choice == 7:
        while True:
            print("""=====Logout and login menu=====
1) Login
2) Logout
3) adb commands to clear, force-stop, start
4) Back
=======================""")
            choice = choose()
            if choice == 1:
                if ptx.adb_launch() == True:
                    print("<info> Client Launched successfully")
                    if ptx.status_check(driver, ptx.InAppStatus) == True:
                        print("<info> Relogin success")
                    else:
                        print("<info> Relogin Failed")
                else:
                    print("<info> Client Launch Failed")
            elif choice == 2:
                ptx.logout(driver)
                
            elif choice == 3:
                print('''================
1)clear data
2)force stop
3)start application''')
                choice = choose()
                if choice == 1:
                    ptx.adb_launch(action = "clear")
                if choice == 2:
                    ptx.adb_launch(action = "stop")
                if choice == 3:
                    ptx.adb_launch(action = "start")
                    
            elif choice == 4:
                break
        
    # Background and Foreground
    if choice == 8:
        while True:
            print("""=====BG and FG menu=====
1) switch FG to BG and viceversa
2) Back
=======================""")
            choice = choose()
            if choice == 1:
                ptx.switch_apptoBGandFG(driver)
            elif choice == 2:
                break
    
    #Presence change between Avalable to DND and viceversa
    if choice == 9:
        while True:
            print("""=====Presence change menu=====
1) Switch Presence
2) Back
=======================""")
            choice = choose()
            if choice == 1:
                ptx.mypresence_switch(driver)
            elif choice == 2:
                break
            
    #Copy PTT files
    if choice == 10:
        ptx.copy_Logs(driver)
    
        
    if choice == 14:
        driver.quit()
        print("**** Thank You ****")
        exit()