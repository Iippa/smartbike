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

#Create toggle switch to represent succesfull opening of lock

key = False

# Kivy App
class MyApp(App):
        def build(self):
            return Label(text='Tervetuloa %s' %name)

def valid_login():
        #Read value from NFC/RFID reader
        scan = '0x{0}'.format(binascii.hexlify(uid))
        #mysql
        MYSQL_DATABASE_HOST = os.getenv('IP', '0.0.0.0')
        MYSQL_DATABASE_USER = 'iippa'
        MYSQL_DATABASE_PASSWORD = ''
        MYSQL_DATABASE_DB = 'my_flask_app'
        conn = pymysql.connect(
            host=MYSQL_DATABASE_HOST,
            user=MYSQL_DATABASE_USER,
            passwd=MYSQL_DATABASE_PASSWORD,
            db=MYSQL_DATABASE_DB)
            cursor = conn.cursor()
            cursor.execute("SELECT * from user where username='%s' and password='%s'" %
                        (username, password))
                        data = cursor.fetchone()
        if data:
            return True
        else:
            return False

print ('Waiting for Mifare card...')
while(1):
        uid = pn532.read_passive_target()
        if uid is None:
                continue
        if valid_login():
            if __name__ == '__main__':
                MyApp().run()
        else:
            continue
        print ('Found card with UID: 0x{0}'.format(binascii.hexlify(uid)))
        break
