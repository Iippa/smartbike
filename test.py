#!/usr/bin/env python
# -*- coding: utf-8 -*-#

#--------------------------------------------------------------------------
'''dictionary that contains the correspondance between items descriptions
and methods that actually implement the specific function and panels to be
shown instead of the first main_panel
'''
SidePanel_AppMenu = {'Tervetuloa':['on_uno',None],
                     'Rekisteroidy':['on_due',None],
                     'Kaytossa':['on_tre',None],
                     }
id_AppMenu_METHOD = 0
id_AppMenu_PANEL = 1


#--------------------------------------------------------------------------
import os
import kivy
kivy.require('1.8.0')


from kivy.app import App
from kivy.garden.navigationdrawer import NavigationDrawer
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.actionbar import ActionBar, ActionButton, ActionPrevious
from kivy.properties import  ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label

RootApp = None


import binascii
import Adafruit_PN532 as PN532
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
servoPin = 17
GPIO.setup(servoPin,GPIO.OUT)
pwm=GPIO.PWM(servoPin,50)
pwm.start(7)

#Initialize RFID reader
# Setup how the PN532 is connected to the Raspbery Pi/BeagleBone Black.
# It is recommended to use a software SPI connection with 4 digital GPIO pins.

# Configuration for a Raspberry Pi:
CS   = 18
MOSI = 23
MISO = 24
SCLK = 25

# Create an instance of the PN532 class.
pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
# Call begin to initialize communication with the PN532.  Must be done before
# any other calls to the PN532!
pn532.begin()
# Configure PN532 to communicate with MiFare cards.
pn532.SAM_configuration()

#Create toggle switch to represent succesfull opening of lock
key = False

#Turn screen backlight off
os.system("echo"+" "+"1"+" "+">"+"/sys/class/backlight/rpi_backlight/bl_power")

# Get the name of the user from database
def get_data():
    return True

def get_name():
    name = 'Iiro'
    return name

def read_mifare():
    while(1):
        uid = pn532.read_passive_target()
        if uid != None:
            #Read value from NFC/RFID reader
            scan = '0x{0}'.format(binascii.hexlify(uid))
            return scan

def succes_read():
    return True

def in_use():
    togle_servo(1)
    if __name__ == "__main__":
        os.system("echo"+" "+"0"+" "+">"+"/sys/class/backlight/rpi_backlight/bl_power")
        TestApp().run()

class Bike(Button):
    def logout(self):
        print "Logout"
        togle_servo(3)
        #Turn screen backlight off
        os.system("echo"+" "+"1"+" "+">"+"/sys/class/backlight/rpi_backlight/bl_power")
        RootApp.stop()


def togle_servo(time):
    desiredPosition = 0
    DC=1./18.*(desiredPosition)+2
    pwm.ChangeDutyCycle(DC)
    sleep(time)
    desiredPosition = 80
    DC=1./18.*(desiredPosition)+2
    pwm.ChangeDutyCycle(DC)

class SidePanel(BoxLayout):
    pass

class MenuItem(Button):
    def __init__(self, **kwargs):
        super(MenuItem, self).__init__( **kwargs)
        self.bind(on_press=self.menuitem_selected)

    def menuitem_selected(self, *args):
        print self.text, SidePanel_AppMenu[self.text], SidePanel_AppMenu[self.text][id_AppMenu_METHOD]
        try:
            function_to_call = SidePanel_AppMenu[self.text][id_AppMenu_METHOD]
        except:
            print 'errore di configurazione dizionario voci menu'
            return
        getattr(RootApp, function_to_call)()

#

class AppActionBar(ActionBar):
    pass

class ActionMenu(ActionPrevious):
    def menu(self):
        print 'ActionMenu'
        RootApp.toggle_sidepanel()

class ActionQuit(ActionButton):
    pass
    def menu(self):
        print 'App quit'
        RootApp.stop()


class MainPanel(BoxLayout):
    pass

class AppArea(FloatLayout):
    pass

class PaginaUno(FloatLayout):
    pass

class PaginaDue(FloatLayout):
    pass

class PaginaTre(FloatLayout):
    pass

class AppButton(Button):
    nome_bottone = ObjectProperty(None)
    def app_pushed(self):
        print self.text, 'button', self.nome_bottone.state


class NavDrawer(NavigationDrawer):
    def __init__(self, **kwargs):
        super(NavDrawer, self).__init__( **kwargs)

    def close_sidepanel(self, animate=True):
        if self.state == 'open':
            if animate:
                self.anim_to_state('closed')
            else:
                self.state = 'closed'


class TestApp(App):

    def build(self):

        # Set to fullscreen mode
        Window.size = (800,480)

        global RootApp
        RootApp = self

        # NavigationDrawer
        self.navigationdrawer = NavDrawer()

        # SidePanel
        side_panel = SidePanel()
        self.navigationdrawer.add_widget(side_panel)

        # MainPanel
        self.main_panel = MainPanel()

        self.navigationdrawer.anim_type = 'slide_above_anim'
        self.navigationdrawer.add_widget(self.main_panel)

        return self.navigationdrawer

    def toggle_sidepanel(self):
        self.navigationdrawer.toggle_state()

    def on_uno(self):
        print 'UNO... exec'
        self._switch_main_page('Tervetuloa', PaginaUno)

    def on_due(self):
        print 'DUE... exec'
        self._switch_main_page('Rekisteroidy', PaginaDue)
    def on_tre(self):
        print 'TRE... exec'
        self._switch_main_page('Kaytossa',  PaginaTre)

    def _switch_main_page(self, key,  panel):
        self.navigationdrawer.close_sidepanel()
        if not SidePanel_AppMenu[key][id_AppMenu_PANEL]:
            SidePanel_AppMenu[key][id_AppMenu_PANEL] = panel()
        main_panel = SidePanel_AppMenu[key][id_AppMenu_PANEL]
        self.navigationdrawer.remove_widget(self.main_panel)    # FACCIO REMOVE ED ADD perchè la set_main_panel
        self.navigationdrawer.add_widget(main_panel)            # dà un'eccezione e non ho capito perchè
        self.main_panel = main_panel

####################################    MAIN BODY   ####################################

while(1):
    read_mifare()

    if succes_read():
        if get_data():
            #Lauch in use mode
            in_use()
    else:
        continue
