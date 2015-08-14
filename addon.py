import os
import xbmcaddon, xbmcgui, xbmc
import time
import socket



__addon__     = xbmcaddon.Addon()
__addonpath__ = __addon__.getAddonInfo('path').decode("utf-8")
__settings__ = xbmcaddon.Addon(id='script.program.tdasettings')


#global used to tell the worker thread the status of the window

#capture a couple of actions to close the window
ACTION_PREVIOUS_MENU = 10
ACTION_BACK = 92

def CarpcController_SendCommand(command):
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5005

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cmd = command + "\0"
    # Send request to server
    tmp = sock.sendto(cmd, (UDP_IP, UDP_PORT))

    sock.close()
    
#control
BACK_BUTTON			= 1501
TITLE_LABEL			= 1502
BUTTON_BASS_UP		= 1503
BUTTON_BASS_DOWN	= 1504
BUTTON_TREBLE_UP	= 1505
BUTTON_TREBLE_DOWN	= 1506
BUTTON_FADE_FRONT	= 1507
BUTTON_FADE_REAR	= 1508
BUTTON_BAL_LEFT		= 1509
BUTTON_BAL_RIGHT	= 1510

LABEL_BASS			= 1511
LABEL_TREBLE		= 1512
LABEL_FADE			= 1513
LABEL_BALANCE		= 1514

BUTTON_VOL_UP       = 1515
BUTTON_VOL_DOWN     = 1516
LABEL_VOLUME        = 1517

title="TDA7318 Settings"



def log(logline):
    print "TDASETTINGS: " + logline

def set_kodi_prop(property, value):
    log ("Setting: '{}', '{}'".format(property, value))
    strvalue=str(value)
    xbmcgui.Window(10000).setProperty(property, strvalue)

def get_kodi_prop(property):
    value=xbmcgui.Window(10000).getProperty(property)
    log("Loading: '" + property + "', '" + value + "'")
    return value




def updateVolume():
    if get_kodi_prop("Volume.Changed"):
        #__addon__.setSetting("volume",get_kodi_prop("Volume.Value"))
        set_kodi_prop("Volume.Changed","False")

    time.sleep(1)
    tdasettings.label_volume.setLabel("-" + __addon__.getSetting("volume"))

class tdasettings(xbmcgui.WindowXMLDialog):
    
    



    button_back=None
    title_label=None
    button_bass_up=None
    button_bass_down=None
    button_treble_up=None
    button_treble_down=None
    button_fade_front=None
    button_fade_rear=None
    button_balance_left=None
    button_balance_right=None

    def onInit(self):

        #print __settings__.getAddonInfo()

        if not __settings__.getSetting('volume'):
            __settings__.setSetting('volume',str(30))
        if not __settings__.getSetting('bass'):
            __settings__.setSetting('bass', str(7))
        if not __settings__.getSetting('treble'):
            __settings__.setSetting('treble', str(7))
        if not __settings__.getSetting('fade'):
            __settings__.setSetting('fade', str(0))
        if not __settings__.getSetting('balance'):
            __settings__.setSetting('balance', str(0))

        tdasettings.button_back=self.getControl(BACK_BUTTON)
        tdasettings.title_label=self.getControl(TITLE_LABEL)
        tdasettings.title_label.setLabel(title)
        
        tdasettings.button_volume_up=self.getControl(BUTTON_VOL_UP)
        tdasettings.button_volume_down=self.getControl(BUTTON_VOL_DOWN)
        tdasettings.button_bass_up=self.getControl(BUTTON_BASS_UP)
        tdasettings.button_bass_down=self.getControl(BUTTON_BASS_DOWN)
        tdasettings.button_treble_up=self.getControl(BUTTON_TREBLE_UP)
        tdasettings.button_treble_down=self.getControl(BUTTON_TREBLE_DOWN)
        tdasettings.button_fade_front=self.getControl(BUTTON_FADE_FRONT)
        tdasettings.button_fade_rear=self.getControl(BUTTON_FADE_REAR)
        tdasettings.button_balance_left=self.getControl(BUTTON_BAL_LEFT)
        tdasettings.button_balance_right=self.getControl(BUTTON_BAL_RIGHT)
		
		
        tdasettings.label_volume=self.getControl(LABEL_VOLUME)
        tdasettings.label_bass=self.getControl(LABEL_BASS)
        tdasettings.label_treble=self.getControl(LABEL_TREBLE)
        tdasettings.label_fade=self.getControl(LABEL_FADE)
        tdasettings.label_balance=self.getControl(LABEL_BALANCE)
        
        bass_int = int(__addon__.getSetting("bass")) - 7 
        tdasettings.label_bass.setLabel(str(bass_int))
        treble_int = int(__addon__.getSetting("treble")) - 7
        tdasettings.label_treble.setLabel(str(treble_int))
        tdasettings.label_fade.setLabel(__addon__.getSetting("fade"))
        tdasettings.label_balance.setLabel(__addon__.getSetting("balance"))
        updateVolume();

    def onAction(self, action):
        if action == ACTION_PREVIOUS_MENU:
            self.close()
        if action == ACTION_BACK:
            self.close()

    def onClick(self, controlID):
      
        if controlID == BACK_BUTTON:
            self.close()
        if controlID == BUTTON_BASS_UP:
            CarpcController_SendCommand("tda_bass_up")
            if int(__addon__.getSetting("bass")) < 14:
                __addon__.setSetting("bass",str(int(__addon__.getSetting("bass"))+1))
                bass_int = int(__addon__.getSetting("bass")) - 7 
                tdasettings.label_bass.setLabel(str(bass_int))

        if controlID == BUTTON_BASS_DOWN:
            CarpcController_SendCommand("tda_bass_down")
            if int(__addon__.getSetting("bass")) > 0:
                __addon__.setSetting("bass",str(int(__addon__.getSetting("bass"))-1))
                bass_int = int(__addon__.getSetting("bass")) - 7 
                tdasettings.label_bass.setLabel(str(bass_int))

        if controlID == BUTTON_TREBLE_UP:
            CarpcController_SendCommand("tda_treble_up")
            if int(__addon__.getSetting("treble")) < 14:
                __addon__.setSetting("treble",str(int(__addon__.getSetting("treble"))+1))
                treble_int = int(__addon__.getSetting("treble")) - 7 
                tdasettings.label_treble.setLabel(str(treble_int))

        if controlID == BUTTON_TREBLE_DOWN:
            CarpcController_SendCommand("tda_treble_down")
            if int(__addon__.getSetting("treble")) > 0:
                __addon__.setSetting("treble",str(int(__addon__.getSetting("treble"))-1))
                treble_int = int(__addon__.getSetting("treble")) - 7 
                tdasettings.label_treble.setLabel(str(treble_int))

        if controlID == BUTTON_FADE_FRONT:
            CarpcController_SendCommand("tda_fade_front")
            if int(__addon__.getSetting("fade")) < 31:
                __addon__.setSetting("fade",str(int(__addon__.getSetting("fade"))+1))
                treble_int = int(__addon__.getSetting("fade")) 
                tdasettings.label_fade.setLabel(__addon__.getSetting("fade"))

        if controlID == BUTTON_FADE_REAR:
            CarpcController_SendCommand("tda_fade_rear")
            if int(__addon__.getSetting("fade")) > -31:
                __addon__.setSetting("fade",str(int(__addon__.getSetting("fade"))-1))
                tdasettings.label_fade.setLabel(__addon__.getSetting("fade"))

        if controlID == BUTTON_BAL_LEFT:
            CarpcController_SendCommand("tda_balance_left")
            if int(__addon__.getSetting("bass")) < 31:
                __addon__.setSetting("balance",str(int(__addon__.getSetting("balance"))-1))
                tdasettings.label_balance.setLabel(__addon__.getSetting("balance"))

        if controlID == BUTTON_BAL_RIGHT:
            CarpcController_SendCommand("tda_balance_right")
            if int(__addon__.getSetting("bass")) > -31:
                __addon__.setSetting("balance",str(int(__addon__.getSetting("balance"))+1))
                tdasettings.label_balance.setLabel(__addon__.getSetting("balance"))

        if controlID == BUTTON_VOL_UP:
            CarpcController_SendCommand("tda_volume_up")
            #__addon__.setSetting("volume",str(int(__addon__.getSetting("volume"))+1))
            updateVolume()
            
        if controlID == BUTTON_VOL_DOWN:
            CarpcController_SendCommand("tda_volume_down")
            #__addon__.setSetting("volume",str(int(__addon__.getSetting("volume"))-1))
            updateVolume()


    def onFocus(self, controlID):
        pass
    
    def onControl(self, controlID):
        pass
 
tdadialog = tdasettings("tdasettings.xml", __addonpath__, 'default', '16x9')
tdadialog.doModal()
del tdadialog



    




