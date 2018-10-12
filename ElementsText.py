'''
Created on 30-Jul-2017

@author: pradeep
'''

Log = {}
Log["folderpath"] = "F:\Logs"
Login = ['======== New Session', ">: SIP Response ", "<ALA_SIGNAL>: SIP Request INVITE", "<ALA_SIGNAL>: SIP Request REGISTER", "<ALA_SIGNAL>: SIP Request SUBSCRIBE", "<ALA_SIGNAL>: SIP Request PUBLISH", "<ALA_SIGNAL>: SIP Request NOTIFY", "<ALA_SIGNAL>: SIP Request OPTIONS", 'Presence icon type', '<KN_OPTYPE_ALL_REG_SUCCESS>']

Packages = {}
Packages["att"] = 'com.att.eptt'
Packages["vzw"] = 'com.verizon.pushtotalkplus'
Packages["sprint"] = "com.sprint.sdcplus"

appium = {}
appium["unlock"] = 'io.appium.unlock'
appium["ime"] = 'io.appium.android.ime'

input = {}
input["MDN"] = "WB_Auto_Android"
input["grp"] = "Pradeep"
input["package"] = "att"
input["Path"] = "D:\Software-WB\programs\Android_08_003_00_34G-CDE_08_003_00_00_25Y-UI_08_03_00_11D-1-verizon.apk"
input["remoteIP"] = "127.0.0.1"
input["bearer"] = "3g" #wifi, 3g, both

NWsim = {}
NWsim["UPtime"] = 5
NWsim["DOWNtime"] = 2
NWsim["count"] = 500



Activation = {}

Activation["Accept"] = "//android.widget.Button[@text='Accept']"
Activation["Allow"] = "com.android.packageinstaller:id/permission_allow_button"
Activation['BatteryYes'] = "//android.widget.Button[@text='Yes']"
Activation["Yes"]="//android.view.View[@text='Yes']"
Activation["EnterCode"]="//android.view.View[@text='Enter Code']"
Activation["EditText1"] = "//android.widget.EditText"
Activation["EditText"]="//android.widget.EditText[@text='Search']"
Activation["OK"]="//android.view.View[@text='OK']"
Activation["SkipTutorial"]="//android.view.View[@text='Skip Tutorial']"
Activation["Error"]="//android.view.View[@text='Error']"
Activation["Exit"]="//android.view.View[@text='Exit']"
Activation["grpsearch"]="//android.view.View[contains(@resource-id,'ext-uxsearchfield')]"

lcms = {}
lcms["importantmessage"] = "//android.view.View[@text='Important message']" 
lcms["checkbox"] = "//android.view.View[@text='Do not show again. CheckBox unchecked']"
lcms["Dismiss"] = "//android.widget.Button[@text='Dismiss']"

CopyLog = {}

CopyLog["Menu"]="//android.widget.Button[@text='Menu']"
CopyLog["ManualDial"]="//android.widget.Button[@text='Manual Dial']"
CopyLog["PTTCall"]="//android.widget.Button[@text='PTT Call']"
CopyLog["EneterNumber"]="//*[@class='android.widget.EditText']"#[@text='Enter number']" # or @text='Enter Number'
CopyLog["CopyPTTfiles"]="//android.view.View[@text='Copy Files to Shared Memory']"
CopyLog["allow"]="com.android.packageinstaller:id/permission_allow_button"
CopyLog["Yes"]="//android.view.View[@text='Yes']"
CopyLog["Back"]="//android.widget.Button[@text='Back']"
CopyLog["Details"]="//android.widget.Button[@text='Details']"
CopyLog["Settings"]="//android.widget.Button[@text='Settings' and @index='1']"

Presence = {}
Presence["Available"]="//android.widget.EditText[@text='Available']"#"//android.view.View[@text='My presence, Available']"
Presence["DND"]= "//android.widget.EditText[@text='Do not disturb']"#"//android.view.View[@text='My Presence, do not disturb']"
Presence["setDND"]="//android.view.View[@text='Do not disturb']" # This Available button for Drop Down list when changing presence
Presence["setAvailable"]="//android.view.View[@text='Available']" # This Available button for Drop Down list when changing presence
Presence["NoConnection"]= "//android.widget.EditText[@text='No Connection']" #"//android.view.View[@text=''My Presence, No Connection']"

Tab = {}
Tab["History"]="//android.view.View[@text='History']"
Tab["Favorite"]="//android.view.View[@text='Favorite']"
Tab["Contact"]="//android.view.View[@text='Contact']"
Tab["Group"]="//android.view.View[contain(@text,'groups ')]"
Tab["MapTab"]="//android.view.View[@text='Location']"

Cat = {}
#Contacts
Cat["AddContact"]="//android.widget.Button[@text='Add Contact']"
Cat["NewContact"]="//android.view.View[@text='New Contact']"
Cat["EnterName"]="//android.widget.EditText[@text='Enter name' or @text='Enter Name']"
Cat["MDN"]="//android.widget.EditText[@text='Enter Phone Number']"
Cat["AddGroup"]="//android.widget.Button[@text='Add Group']"
Cat["Save"]="//android.widget.Button[@text='Save']"
Cat["AddMember"]="//android.view.View[@text='Add Members']"
Cat["AddMembers"]="//android.view.View[@text='Add Member(s)']"
Cat["Search"]="//android.widget.EditText"# serach when adding group member [@text='Search']
Cat["Searchintab"]="//android.widget.EditText[@text='Search']" 
Cat["SelectConatct"]="//android.view.View[@text='checkbox unselected']"
Cat["DeleteGroup"]="//android.view.View[@text='Delete group']"
Cat["Delete"]="//android.view.View[@text='Delete contact' or @text='Delete Contact']"
Cat["Cancel"]="//android.widget.Button[@text='Cancel']"
Cat["Clear"] = "//android.widget.Button[@text='Clear']"
Cat["delete"] = "//android.widget.Button[@text='delete']"
Cat["Yes"]="//android.view.View[@text='Yes']"
Cat["OK"]="//android.view.View[@text='OK']"


Status = {}

Status["Confirm"] = "//android.view.View[@text='Confirm']"
Status["Desc1"] = "//android.widget.Button[@text='Connection to server is not available.']"
Status["UseWifi"] = "//android.view.View[contains(@text,'Use wifi. . CheckBox ')]"
Status["Reconnecting"] = "//android.view.View[@text='Reconnecting, please wait...']"
Status["Contacting"] = "//android.view.View[@text='Contacting Server']"
Status["Sync"] = "//android.view.View[@text='Synchronization in progress, please wait...']"
Status["Information"] = "//android.view.View[@text='Information']"
Status["Yes"]="//android.view.View[@text='Yes']"
Status["Pleasewait"] = "//android.view.View[@text='Please Wait']"
Status["Syncstarted"] = "//android.view.View[@text='Sync started']"
Status["EmergencyAlert"]="//android.view.View[@text='Emergency Alert']"
Toast={}

Toast["ConnUNavailable"] = "//android.view.View[@text='Connection is unavailable']"

Settings = {}

Settings["Settings"] = "//android.view.View[@text='Settings' and @index=1 and @enabled='true' and @clickable='false']"

Settings["Logout"] = "//android.view.View[@text='Logout' and @index='0']"
PTXstatus = {}
#PTXstatus["text"] = 

PTX = {}

PTX["Sendtext"] = "//android.view.View[@text='Send text']"
PTX["EnterText"] = "//*[@class='android.widget.EditText']"#"//android.widget.Button[@text='Enter text']"
PTX["SendPTXMessage"] = "//android.view.View[@text='Send PTX Message']"
PTX["QuickTextMessage"] = "Quick Text Message"
PTX["Alert"] = "//android.widget.Button[@text='Alert']"   #in PTX message window
# Alert Elements
PTX["SendAlert"] = "//android.widget.Button[@text='Send alert']" # in Call screen window
PTX["Pleasewait"] = "Please wait"
PTX["Information"] = "Information"


# Location elements
PTX["MyLocation"] = "//android.view.View[@text='My Location']" # in PTX window
PTX["share"] = "//android.widget.Image[@text='share']"
PTX["SelfLocation"] = "Self Location"
PTX["Sendlocation"] = "//android.view.View[@text='Send location']" # in Call window

# send image or video Elements
PTX["Sendimageorvideo"] = "//android.view.View[@text='Send image or video']" #in PTX screen
PTX["Takephoto"] = "//android.view.View[@text='Take a photo']"
PTX["VzwTakePhoto"] = "//android.view.View[@text='Take photo']"
PTX["RecordVideo"] = "//android.view.View[@text='Record a Video']"
PTX["VzwRecordVideo"] = "//android.view.View[@text='Record video']"
PTX["ImageGallery"] = "//android.view.View[@text='Image Gallery']"
PTX["VideoGallery"] = "//android.view.View[@text='Video Gallery']"
PTX["photoShutter"] = "//android.widget.ImageView[@text='Camera shutter']"
PTX["videoShutter"] = "//android.widget.ImageView[@text='Video shutter']"
PTX["OK"] = "//android.widget.Button[contains(@resource-id,'com.lge.camera:id/btn_ok') or @text='OK']"
PTX["CamOK"] = "//android.view.View[@text='OK']"
PTX["Startrecording"] = "//android.widget.ImageButton[@text='Start recording']" #9.05
PTX["Stoprecording"] = "//android.widget.ImageView[@text='stop']"
PTX["stoprecord"] = "//android.widget.ImageButton[@text='Stop recording']"



# file Related Elements
PTX["File"] = "File"
PTX["Search"] = "Search" # /sdcard/PTT


# record Elements
PTX["VOICEMESSAGE"] = "//android.view.View[@text='VOICE MESSAGE']" #in PTX window
PTX["record"] = "//android.widget.Button[@text='record']"
PTX["Sendingvoicemessage"] = "//android.widget.Button[@text='Sending voice message']"
PTX["Sendvoicemessage"] = "//android.view.View[@text='Send voice message' and @clickable='true']" # in call screen
PTX["recordOK"] = "//android.widget.Button[@text='OK']"

Call = {}

Call["Call"] = "//android.widget.Button[@text='Call']"
Call["CallEnd"] = "//android.widget.Button[@text='call end']"
Call["addparticipent"] = "//android.widget.Button[@text='add participant']"
Call["Information"] = "//android.widget.Button[@text='Information']"
Call["OK"] = "//android.widget.Button[@text='OK']"
Call["MissedCallAlert"] = "//android.view.View[@text='Missed call alert']"
Call["Notnow"] = "//android.view.View[@text='Not now']"
Call["Infopop"] = "//android.view.View[@text='The contact you are trying to call is unavailable. Please try again later.']"


PtxSecurity = {}

PtxSecurity['urlsearch'] = '''("//android.widget.EditText[contains(@resource-id,'com.android.chrome:id/url_bar')]")'''
PtxSecurity['moreoption'] = 'More options'
PtxSecurity['Newtab'] = 'New tab'
PtxSecurity["typeurl"]="//android.widget.EditText[@text='Search or type URL']"
PtxSecurity["ERR_ADDRESS_UNREACHABLE"]="//android.view.View[@text='ERR_ADDRESS_UNREACHABLE']"
PtxSecurity["ERR_CONNECTION_REFUSED"]="//android.view.View[@text='ERR_CONNECTION_REFUSED']"

Secretcode = {}
Secretcode["vzw"] = "899788"
Secretcode["att"] = "563788"
Secretcode["sprint"] = "732788"

chrome = {}
chrome['advanced'] = "//android.widget.Button[@text='ADVANCED']"


Network = {}
Network['ON'] = "//android.widget.Switch[contains(@resource-id,'com.android.settings:id/switch_widget') or @text='ON']"
Network['DataON'] = "//android.widget.Switch[@text='ON']"
Network['OFF'] = "//android.widget.Switch[contains(@resource-id,'com.android.settings:id/switch_widget') or @text='OFF']"
Network['DataOFF'] = "//android.widget.Switch[@text='OFF']"
Network['OK'] = "//android.widget.Button[@text='OK']"
Network['Navigate']="//android.widget.ImageButton[@text='Navigate up']"
Network['Connected'] = "//android.widget.TextView[@text='Connected']"
Network['Mobiledata'] = "//android.widget.TextView[@text='Mobile data']"
Network['checkbox'] = "//android.widget.CheckBox"

TGSC = {}
TGSC['TGSCon'] = "//android.widget.Button[@text='talk group select. on']"
TGSC['TGSCoff'] = "//android.widget.Button[@text='talk group select. off']"
TGSC["Information"] = "//android.view.View[@text='Scan list empty. Scan mode cannot be turned on.']"
TGSC["Scanlist"] = "//android.view.View[@text='Scan list']"
TGSC["Priority1"] = "//android.view.View[@text='Set priority 1']"
TGSC["Priority2"] = "//android.view.View[@text='Set priority 2']"
TGSC["Priority3"] = "//android.view.View[@text='Set priority 3']"
TGSC["Nopriority"] = "//android.view.View[@text='No priority']"
TGSC["calltopri1"] = "//android.view.View[@text='Scan_Pri_1_Group_Common']"
TGSC["calltopri2"] = "//android.view.View[@text='Scan_Pri_2_Group_Common']"
TGSC["calltopri3"] = "//android.view.View[@text='Scan_Pri_3_Group_Common']"

broadcast = {}
broadcast['group'] = "//android.view.View[contains(@text,'Group Type BroadCast')]"
broadcast['brdcall'] = "//android.view.View[@text='Call']"

emergency = {}
emergency["declare"] = "//android.widget.Button[@text='Declare Emergency']"


NWsimu = ['======== New Session', '=======>REGISTER', 'Expires: ', 'Kpoc: 1;', 'Presence icon type', '<KN_OPTYPE_ALL_REG_SUCCESS>']

