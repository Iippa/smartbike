
import binascii
import sys
import Adafruit_PN532 as PN532
import kivy

from kivy.app import App
from kivy.uix.label import Label

kivy.require('1.9.1') # replace with your current kivy version !

from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.button import Label
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage
import os


from connected import Connected

class Login(Screen):
    def do_login(self, loginText, passwordText):
        app = App.get_running_app()

        app.username = loginText
        app.password = passwordText

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'connected'

        app.config.read(app.get_application_config())
        app.config.write()

    def resetForm(self):
        self.ids['login'].text = ""
        self.ids['password'].text = ""

class LoginApp(App):
    username = StringProperty(None)
    password = StringProperty(None)

    def build(self):
        manager = ScreenManager()

        manager.add_widget(Login(name='login'))
        manager.add_widget(Connected(name='connected'))

        return manager

    def get_application_config(self):
        if(not self.username):
            return super(LoginApp, self).get_application_config()

        conf_directory = self.user_data_dir + '/' + self.username

        if(not os.path.exists(conf_directory)):
            os.makedirs(conf_directory)

        return super(LoginApp, self).get_application_config(
            '%s/config.cfg' % (conf_directory)
        )
class Welcome(App):
    global name
    # This returns the content we want in the window
    def build(self):
        # Return a label widget with Hello Kivy
        return Label(text="Welcome!")

class CarouselApp(App):
    def build(self):
        carousel = Carousel(direction='right')
        for i in range(10):
            src = "http://placehold.it/480x270.png&text=slide-%d&.png" % i
            image = AsyncImage(source=src, allow_stretch=True)
            carousel.add_widget(image)
        return carousel

class Exit(App):
    # This returns the content we want in the window
    def build(self):

        # Return a label widget with Hello Kivy
        exit()


##-------------------------------------------------------------##


#Create toggle switch to represent succesfull opening of lock
Key=False

'''
Listing of users and their information: name, current balance, and their identified tag

Balance: updated based on the amount of use
Tag: On the first time of registration read phone NFC or RFID card
Name: Fill based on the registration info

'''

codes = {
    1: {'info' : {'name':'Iippa', 'balance':10.00, 'tag':'1234'}},
    2: {'info' : {'name':'nelson', 'balance':25.15, 'tag':'4457'}},
    3: {'info' : {'name':'Joni', 'balance':1.00, 'tag':'4334'}},
    4: {'info' : {'name':'Mikki', 'balance':14.00, 'tag':1254}},
    5: {'info' : {'name':'Kari', 'balance':7.15, 'tag':7778}}
    }


# Setup how the PN532 is connected to the Raspbery Pi/BeagleBone Black.
# It is recommended to use a software SPI connection with 4 digital GPIO pins.

# Configuration for a Raspberry Pi:
CS   = 18
MOSI = 23
MISO = 24
SCLK = 25

# Configuration for a BeagleBone Black:
# CS   = 'P8_7'
# MOSI = 'P8_8'
# MISO = 'P8_9'
# SCLK = 'P8_10'

# Create an instance of the PN532 class.
pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
# Call begin to initialize communication with the PN532.  Must be done before
# any other calls to the PN532!
pn532.begin()
# Configure PN532 to communicate with MiFare cards.
pn532.SAM_configuration()

#Create toggle switch to represent succesfull opening of lock

key = False

# Kivy App
class MyApp(App):
        def build(self):
            return Label(text='Tervetuloa %s' %name)
def scan_database(uid):
    #Search through all know tags and print result
    for code in codes:
        if uid == codes[code]['info']['tag']:
            return True

def valid_login():
        #Read value from NFC/RFID reader
        scan = '0x{0}'.format(binascii.hexlify(uid))
        if scan_database(scan):
            return True
        else:
            return False

print ('Waiting for Mifare card...')
while(1):
        uid = pn532.read_passive_target()
        print 0x{0}'.format(binascii.hexlify(uid)))
        if uid is None:
                continue
        if valid_login():
            CarouselApp().run()
        else:
            LoginApp().run()
        print ('Found card with UID: 0x{0}'.format(binascii.hexlify(uid)))
        break
