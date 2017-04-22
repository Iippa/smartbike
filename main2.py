#!/usr/bin/kivy
import os
import sys
sys.path.append("/home/pi/working/libs/kivy")

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.garden.navigationdrawer import NavigationDrawer

import binascii
import sys
import Adafruit_PN532 as PN532


# Set to fullscreen mode
#Window.size = (800,480)
#Window.fullscreen = True

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
    # Start Kivy in "In_use" screen
    sm.current = 'in_use'
    if __name__ == "__main__":
        os.system("echo"+" "+"0"+" "+">"+"/sys/class/backlight/rpi_backlight/bl_power")
        BikeApp().run()

class Welcome(Screen):
    # Define users name so that Kivy knows how to handle it
    user = StringProperty(get_name())
    pass

class Register(Screen):
    pass

class In_use(Screen):
    pass

Builder.load_file('/home/pi/working/smartbike/bike2.kv')

# Create the screen manager
sm = ScreenManager()

# Add screens
sm.add_widget(Register(name='register'))
sm.add_widget(Welcome(name='welcome'))
sm.add_widget(In_use(name='in_use'))


class BikeApp(App):
    def build(self):
        return sm

####################################    MAIN BODY   ####################################

while(1):
    read_mifare()

    if succes_read():
        if get_data():
            #Lauch in use mode
            in_use()
    else:
        continue
