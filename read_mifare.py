import binascii
import sys
import Adafruit_PN532 as PN532
import kivy
kivy.require('1.9.1') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label

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

'''
Listing of users and their information: name, current balance, and their identified tag

Balance: updated based on the amount of use
Tag: On the first time of registration read phone NFC or RFID card
Name: Fill based on the registration info

'''

codes = {
    1: {'info' : {'name':'Iippa', 'balance':10.00, 'tag':'0x80a1345b'}},
    2: {'info' : {'name':'nelson', 'balance':25.15, 'tag':'75110484217139'}},
    3: {'info' : {'name':'Joni', 'balance':1.00, 'tag':4334}},
    4: {'info' : {'name':'Mikki', 'balance':14.00, 'tag':1254}},
    5: {'info' : {'name':'Kari', 'balance':7.15, 'tag':7778}}
   }

#Create toggle switch to represent succesfull opening of lock

key = False

class MyApp(App):
        def build(self):
                if key == True:
                        return Label(text='Tervetuloa %s' %name)
                else:
                        return Label(text='Ei loytynyt. Rekisteroidy nyt?')
def scan_database():
        global key, uid, name
        #Read value from NFC/RFID reader
        scan = '0x{0}'.format(binascii.hexlify(uid))
        #Search through all know tags and print result
        for code in codes:
                if scan == codes[code]['info']['tag']:
                        print ('Tervetuloa %s' %codes[code]['info']['name'])
                        print ('Tamanhetkinen saldo: %s euroa' %codes[code]['info']['balance'])
                        key = True
                        name = codes[code]['info']['name']
                        break
print ('Waiting for Mifare card...')
while(1):
        uid = pn532.read_passive_target()
        if uid is None:
                continue
        scan_database()
        print ('Found card with UID: 0x{0}'.format(binascii.hexlify(uid)))
        if __name__ == '__main__':
                MyApp().run()
        break
