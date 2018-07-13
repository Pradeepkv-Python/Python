'''
Created on 30-Jul-2017

@author: pradeep
'''

Packages = {}
Packages["att"] = 'com.att.eptt'
Packages["vzw"] = 'com.verizon.pushtotalkplus'
Packages["sprint"] = "com.sprint.sdcplus"
Packages["bell"] = "com.bell.ptt"


appium = {}
appium["unlock"] = 'io.appium.unlock'
appium["ime"] = 'io.appium.android.ime'

input = {}
input["MDN"] = "Pradeep_012"
input["grp"] = "P1"
input["package"] = "att"
input["Path"] = "F:\DecryptEncryptDB\Android_08_003_00_38F-CDE_08_003_00_00_26K-UI_08_03_00_11W-1-att.apk"
input["remoteIP"] = "127.0.0.1"


Activation = {}

Activation["Accept"] = "//android.widget.Button[@content-desc='Accept']"
Activation["Allow"] = "com.android.packageinstaller:id/permission_allow_button"
Activation['BatteryYes'] = "//android.widget.Button[contains(@resource-id,'android:id/button1') or @text='Yes']"
Activation["Yes"]="//android.widget.Button[@content-desc='Yes']"
Activation["EnterCode"]="//android.view.View[@content-desc='Enter Code']"
Activation["EditText1"] = "//android.widget.EditText"
Activation["EditText"]="//android.widget.EditText[@text='Search']"
Activation["OK"]="//android.view.View[@content-desc='OK']"
Activation["SkipTutorial"]="//android.view.View[@content-desc='Skip Tutorial']"


CopyLog = {}

CopyLog["Menu"]="//android.widget.Button[@content-desc='Menu']"
CopyLog["ManualDial"]="//android.view.View[@content-desc='Manual Dial']"
CopyLog["PTTCall"]="//android.widget.Button[@content-desc='PTT Call']"
CopyLog["EneterNumber"]="//android.widget.EditText[@text='Enter Number']"
CopyLog["CopyPTTfiles"]="//android.view.View[@content-desc='Copy Files to Shared Memory']"
CopyLog["allow"]="com.android.packageinstaller:id/permission_allow_button"
CopyLog["Yes"]="//android.view.View[@content-desc='Yes']"
CopyLog["Back"]="//android.widget.Button[@content-desc='Back']"
CopyLog["Details"]="//android.widget.Button[@content-desc='Details']"

Presence = {}
Presence["Available"]="//android.view.View[@content-desc='My presence, Available']" #"//android.widget.EditText[@content-desc='My Presence, Available']" #text='Available' or 
Presence["DND"]= "//android.view.View[@content-desc='My Presence, do not disturb']"#"//android.widget.EditText[content-desc='My Presence, do not disturb']" #@text='Do Not Disturb' or 
Presence["setDND"]="//android.view.View[@content-desc='Do Not Disturb']" # This Available button for Drop Down list when changing presence
Presence["setAvailable"]="//android.view.View[@content-desc='Available']" # This Available button for Drop Down list when changing presence
Presence["NoConnection"]= "//android.view.View[@content-desc='My Presence, No Connection']"#"//android.widget.EditText[content-desc=''My Presence, No Connection']" #@text='No Connection' or 

Tab = {}
Tab["History"]="//android.view.View[@content-desc='History']"
Tab["Favorite"]="//android.view.View[@content-desc='Favorite']"
Tab["Contact"]="//android.view.View[@content-desc='Contact']"
Tab["Group"]="//android.view.View[@content-desc='groups tab']"
Tab["MapTab"]="//android.view.View[@content-desc='Location']"

Toast={}

Toast["ConnUNavailable"] = "//android.view.View[@content-desc='Connection is unavailable']"

Cat = {}
#Contacts
Cat["AddContact"]="//android.widget.Button[@content-desc='Add Contact']"
Cat["NewContact"]="//android.view.View[@content-desc='New Contact']"
Cat["EnterName"]="//android.widget.EditText[@content-desc='Enter Name']"
Cat["MDN"]="//android.widget.EditText[@content-desc='Enter Phone Number']"
Cat["AddGroup"]="//android.widget.Button[@content-desc='Add Group']"
Cat["Save"]="//android.widget.Button[@content-desc='Save']"
Cat["AddMember"]="//android.view.View[@content-desc='Add Members']"
Cat["Search"]="//android.widget.EditText[@content-desc='Search']" # serach when adding group member
Cat["SelectConatct"]="//android.view.View[@content-desc='checkbox unselected']"
Cat["DeleteGroup"]="//android.view.View[@content-desc='Delete Group']"
Cat["Delete"]="//android.view.View[@content-desc='Delete Contact']"
Cat["Cancel"]="//android.widget.Button[@content-desc='Cancel']"
Cat["Clear"] = "//android.widget.Button[@content-desc='Clear']"
Cat["delete"] = "//android.widget.Button[@content-desc='delete']"
Cat["Yes"]="//android.view.View[@content-desc='Yes']"
Cat["OK"]="//android.view.View[@content-desc='OK']"
Cat["Searchintab"]="//android.widget.EditText[@content-desc='Search']" 


Status = {}

Status["Confirm"] = "//android.widget.Button[@content-desc='Confirm']"
Status["Desc1"] = "//android.widget.Button[@content-desc='Connection to server is not available.']"
Status["UseWifi"] = "//android.view.View[@content-desc='Use Wi-Fi']"
Status["Reconnecting"] = "//android.view.View[@content-desc='Reconnecting, please wait...']"
Status["Contacting"] = "//android.view.View[@content-desc='Contacting Server']"
Status["Sync"] = "//android.view.View[@content-desc='Synchronization in progress, please wait...']"
Status["Information"] = "//android.view.View[@content-desc='Information']"
Status["Pleasewait"] = "//android.view.View[@content-desc='Please Wait']"
Status["Syncstarted"] = "//android.view.View[@content-desc='Sync started']"


Settings = {}

Settings["Settings"] = "//android.view.View[@content-desc='Settings' and [@index='1']"
Settings["Logout"] = "//android.view.View[@content-desc='Logout']"
Settings["Vibrate"] = "Vibrate Call"

PTX = {}

PTX["Sendtext"] = "//android.widget.Button[@content-desc='Send text']"
PTX["EnterText"] = "//android.widget.Button[@content-desc='Enter Text']"
PTX["SendPTXMessage"] = "//android.widget.Button[@content-desc='Send PTX Message']"
PTX["QuickTextMessage"] = "Quick Text Message"
PTX["Alert"] = "//android.widget.Button[@content-desc='Alert']"   #in PTX message window
# Alert Elements
PTX["SendAlert"] = "//android.widget.Button[@content-desc='Send alert']" # in Call screen window
PTX["Pleasewait"] = "Please wait"
PTX["Information"] = "Information"


# Location elements
PTX["MyLocation"] = "//android.widget.Button[@content-desc='My Location']" # in PTX window
PTX["share"] = "//android.widget.Image[@content-desc='share']"
PTX["SelfLocation"] = "Self Location"
PTX["Sendlocation"] = "//android.widget.Button[@content-desc='Send location']" # in Call window

# send image or video Elements
PTX["Sendimageorvideo"] = "//android.widget.Button[@content-desc='Send image or video']" #in PTX screen
PTX["Takephoto"] = "//android.view.View[@content-desc='Take a photo']"
PTX["VzwTakePhoto"] = "//android.view.View[@content-desc='Take Photo']"
PTX["RecordVideo"] = "//android.view.View[@content-desc='Record a Video']"
PTX["VzwRecordVideo"] = "//android.view.View[@content-desc='Record Video']"
PTX["ImageGallery"] = "//android.view.View[@content-desc='Image Gallery']"
PTX["VideoGallery"] = "//android.view.View[@content-desc='Video Gallery']"
PTX["photoShutter"] = "//android.widget.ImageView[@content-desc='Camera shutter']"
PTX["videoShutter"] = "//android.widget.ImageView[@content-desc='Video shutter']"
PTX["OK"] = "//android.widget.Button[contains(@resource-id,'com.lge.camera:id/btn_ok') or @text='OK']"
PTX["CamOK"] = "//android.view.View[@content-desc='OK']"
PTX["Startrecording"] = "//android.widget.ImageButton[@content-desc='Start recording']" #9.05
PTX["Stoprecording"] = "//android.widget.ImageView[@content-desc='stop']"
PTX["stoprecord"] = "//android.widget.ImageButton[@content-desc='Stop recording']"



# file Related Elements
PTX["File"] = "File"
PTX["Search"] = "Search" # /sdcard/PTT

#PTX['messagestatus'] = 


# record Elements
PTX["VOICEMESSAGE"] = "//android.widget.Button[@content-desc='VOICE MESSAGE']" #in PTX window
PTX["record"] = "//android.widget.Button[@content-desc='record']"
PTX["Sendingvoicemessage"] = "//android.widget.Button[@content-desc='Sending voice message']"
PTX["Sendvoicemessage"] = "//android.widget.Button[@content-desc='Send voice message']" # in call screen
PTX["recordOK"] = "//android.widget.Button[@content-desc='OK']"

Call = {}

Call["Call"] = "//android.widget.Button[@content-desc='Call']"
Call["CallEnd"] = "//android.widget.Button[@content-desc='call end']"
Call["addparticipent"] = "//android.widget.Button[@content-desc='add participant']"
Call["Information"] = "//android.widget.Button[@content-desc='Information']"
Call["OK"] = "//android.widget.Button[@content-desc='OK']"
Call["MissedCallAlert"] = "//android.view.View[@content-desc='Missed Call Alert']"
Call["Notnow"] = "//android.view.View[@content-desc='Not now']"
Call["Infopop"] = "//android.view.View[@content-desc='The contact you are trying to call is unavailable. Please try again later.']"

lcms = {}
lcms["importantmessage"] = "//android.view.View[@content-desc='Important message']" 
lcms["checkbox"] = "//android.view.View[@content-desc='Do not show again. CheckBox unchecked']"
lcms["Dismiss"] = "//android.widget.Button[@content-desc='Dismiss']"

PtxSecurity = {}

PtxSecurity['urlsearch'] = '''("//android.widget.EditText[contains(@resource-id,'com.android.chrome:id/url_bar')]")'''
PtxSecurity['moreoption'] = 'More options'
PtxSecurity['Newtab'] = 'New tab'
PtxSecurity["typeurl"]="//android.widget.EditText[@content-desc='Search or type URL']"
PtxSecurity["ERR_ADDRESS_UNREACHABLE"]="//android.view.View[@content-desc='ERR_ADDRESS_UNREACHABLE']"
PtxSecurity["ERR_CONNECTION_REFUSED"]="//android.view.View[@content-desc='ERR_CONNECTION_REFUSED']"

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
Network['Navigate']="//android.widget.ImageButton[@content-desc='Navigate up']"
Network['Connected'] = "//android.widget.TextView[@text='Connected']"
Network['Mobiledata'] = "//android.widget.TextView[@text='Mobile data']"
Network['checkbox'] = "//android.widget.CheckBox"

broadcast = {}
broadcast['group'] = "//android.view.View[contains(@text,'Group Type BroadCast')]"
broadcast['brdcall'] = "//android.view.View[@content-desc='Call']"



