
import os
import threading
#kivy shit
import kivy
from kivy.app import App
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.garden.navigationdrawer import NavigationDrawer
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.actionbar import ActionBar, ActionButton, ActionPrevious
from kivy.core.window import Window
from kivy.uix.screenmanager import SlideTransition
from kivy.animation import Animation

#raspi shit
from MCP3008 import Reader
from time import sleep
import RPi.GPIO as GPIO

# set window size for kivy
Window.size = (800,480)


# Intitialize raspberry
GPIO.setmode(GPIO.BCM)

# Pins for lock
SERVOPIN = 17
LOCK_HALL = 8

GPIO.setup(SERVOPIN, GPIO.OUT)
GPIO.setup(LOCK_HALL, GPIO.IN)

# Set pins for MCP3008 chip

# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25



# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# Battery connected to pin 0
potentiometer_adc = 0
pwm=GPIO.PWM(SERVOPIN,50)   # Intitialize pulsewithmodule communicatio with servo
lock_state = 'open' # Always assume lock to ne open
DEBUG = False

def system_run():
    print 'system run'
    '''Run to set ecerything up when starting system'''
    global pwm
    global DEBUG
    os.system("echo"+" "+"255"+" "+">"+"/sys/class/backlight/rpi_backlight/brightness") #Turn screen backlight off

    read_values_thread = threading.Thread(target=read_values) # Create thread for reading values
    read_values_thread.start()

    if GPIO.input(LOCK_HALL):
        print 'servo open'
        pwm.start(3.5)  # Set servo to open position
    else:
        print 'servo close'
        pwm.start(2.5)  # Set servo to locked position

    servo_thread = threading.Thread(target=toggle_servo) # Create thread toggling servo
    servo_thread.start()

def read_values():
    '''Read values from MCP3008 chip eg. battery voltage and GPS coordinates'''
    global DEBUG
    global lock_state
    last_read = 0       # this keeps track of the last potentiometer value
    tolerance = 5       # to keep from being jittery we'll only change
                        # volume when the pot has moved more than 5 'counts'

    current_user = None
    while True:
        if lock_state == 'open':
            # we'll assume that the pot didn't move
            trim_pot_changed = False
            # read the analog pin
            trim_pot = Reader.readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
            # how much has it changed since the last read?
            pot_adjust = abs(trim_pot - last_read)

            if (pot_adjust > tolerance):
                trim_pot_changed = True

            if DEBUG:
                print "trim_pot_changed", trim_pot_changed

            if ( trim_pot_changed ):
                battery_charge = trim_pot / 10.24 - 6.92           # convert 10bit adc0 (0-1024) trim pot read into 0-100 volume level
                battery_charge = round(battery_charge)          # round out decimal value
                battery_charge = int(battery_charge)            # cast charge level as integer
                print 'Battery charge is %s percent' %(battery_charge)
                if DEBUG:
                    print "battery_charge", battery_charge
                    print "tri_pot_changed", battery_charge
            # save the potentiometer reading for the next loop
            last_read = trim_pot
            sleep(5)
        elif lock_state == 'closed':
            # we'll assume that the pot didn't move
            trim_pot_changed = False
            # read the analog pin
            trim_pot = Reader.readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
            # how much has it changed since the last read?
            pot_adjust = abs(trim_pot - last_read)

            if (pot_adjust > tolerance):
                trim_pot_changed = True

            if DEBUG:
                print "trim_pot_changed", trim_pot_changed

            if ( trim_pot_changed ):
                battery_charge = trim_pot / 10.24 - 6.92           # convert 10bit adc0 (0-1024) trim pot read into 0-100 volume level
                battery_charge = round(battery_charge)          # round out decimal value
                battery_charge = int(battery_charge)            # cast charge level as integer

                print 'Battery charge is %s percent' %(battery_charge)
                if DEBUG:
                    print "battery_charge", battery_charge
                    print "tri_pot_changed", battery_charge
                    # save the potentiometer reading for the next loop
            last_read = trim_pot
            sleep(15)
            var = raw_input('stop this?')
            if var == 'y':
                break
            else:
                continue

def toggle_servo():

    global pwm
    global lock_state
    hall_input = GPIO.input(LOCK_HALL)
    api_reference = True
    lock_open_tries = 0
    alive = True
    while alive == True:
        print 'Amount of currently runing threads ',threading.active_count()
        print 'going to toggle servo'
        print 'lock state now is ', lock_state
        if lock_state == 'closed':
            print 'lock state closed'
            desiredPosition = 30
            DC=1./18.*(desiredPosition)+2
            pwm.ChangeDutyCycle(DC)
            while True:
                if GPIO.input(LOCK_HALL) == True:
                    desiredPosition = 5
                    DC=1./18.*(desiredPosition)+2
                    pwm.ChangeDutyCycle(DC)
                    print 'servo should be now back to locked'
                    print 'setting lock state to open'
                    lock_state = 'open'
                    lock_open_tries = 0
                    root_widget.current = 'in_use'
                    alive = False
                    break
                else:
                    lock_open_tries += 1
                    sleep(1)
                    if lock_open_tries == 5:
                        print 'Lock broken'
                        alive = False
                        break
        elif lock_state == 'open':
            print 'lock state open'
            print 'hall input is', hall_input
            hall_input = GPIO.input(LOCK_HALL)
            if hall_input == False: # Hall sensor is grounding this pin meaning lock is locked
                lock_state = 'closed'
                root_widget.current = 'unlock'
                print 'setting lock state to locked'
                print lock_state
                alive = False
            else:
                desiredPosition = 30
                DC=1./18.*(desiredPosition)+2
                pwm.ChangeDutyCycle(DC)
                while hall_input == True:
                    hall_input = GPIO.input(LOCK_HALL)
                    if hall_input == False:
                        desiredPosition = 5
                        DC=1./18.*(desiredPosition)+2
                        pwm.ChangeDutyCycle(DC)
                        sleep(1)
class Unlock_Screen(Screen):
    def open(self):
        servo_thread = threading.Thread(target=toggle_servo) # Create thread toggling servo
        servo_thread.start()
    def current_threads(self):
        print 'Amount of currently runing threads ',threading.active_count()
class NavDrawer(NavigationDrawer):
    def __init__(self, **kwargs):
        super(NavDrawer, self).__init__( **kwargs)
        print 'luodaan'
    def state_toggle(self, animate=True):
        if self.state == 'open':
            if animate:
                print 'lets try'
                self.anim_to_state('closed')
            else:
                self.state = 'closed'

    def print_self_state(self):
        print self.state
class SidePanel(BoxLayout):
    def change_current(self, screen):
        root_widget.current = screen
        root_widget.ids.navdrawer.toggle_state()
    def lock_bike(self):
        toggle_servo()
    def thread_count(self):
        print threading.active_count()
    pass
class MainPanel(BoxLayout):
    pass
class MenuBar(ActionBar):
    pass
class ActionMenu(ActionPrevious):
    def toggle(self):
        print 'toggle'
class On_Hold_Screen(Screen):

    def wake_up(self):
        #Turn screen backlight on
        os.system("echo"+" "+"255"+" "+">"+"/sys/class/backlight/rpi_backlight/brightness")

        root_widget.current = 'gen_info'

class General_Info_Screen(Screen):

    #Set location for images
    general_info_images = [ 'images/general_info/screen1.png',
                            'images/general_info/screen2.png',
                            'images/general_info/screen3.png',
                            'images/general_info/screen4.png',
                            'images/general_info/screen5.png'
                            ]

    #Set text
    text_button1 = 'Previous'
    text_button1_2 = 'Login'
    text_button2 = 'Next'
    text_button2_2 = 'Continue'

    #Set image and text in the beginning
    level = 0
    # Get the current path and add project project location to it
    image_source = StringProperty(str(os.path.dirname(os.path.abspath(__file__))+'/images/general_info/screen1.png'))
    button2_text = StringProperty(text_button2)
    button1_text = StringProperty(text_button1_2)

    def update_up(self):
        '''Change button text and image source to right one when going 1->5'''
        while True:
            if self.level == 0:
                self.level += 1
                self.image_source = str(os.path.dirname(os.path.abspath(__file__))) + '/' + str(self.select_image(self.level))
                self.button1_text = self.text_button1
                self.button2_text = self.text_button2
                break
            if self.level == 4:
                self.level = 1
                self.image_source = str(os.path.dirname(os.path.abspath(__file__))) + '/' + str(self.select_image(self.level))
                self.button1_text = self.text_button1_2
                self.button2_text = self.text_button2
                root_widget.current = 'in_use'
                print ('Do something')
                break
            if self.level == 3:
                self.level += 1
                self.image_source = str(self.select_image(self.level))
                self.button1_text = self.text_button1
                self.button2_text = self.text_button2_2
                break
            if self.level == 1 or self.level == 2:
                self.level += 1
                self.image_source = str(self.select_image(self.level))
                self.button1_text = self.text_button1
                self.button2_text = self.text_button2
                break

    def update_down(self):
        '''Change button text and image source to right one when going 5->1'''
        while True:
            if self.level == 0:
                #Do something
                root_widget.transition = SlideTransition(direction='left')
                root_widget.current = 'log_in'
                break
            if self.level == 4:
                self.level -= 1
                self.image_source = str(self.select_image(self.level))
                self.button1_text = self.text_button1
                self.button2_text = self.text_button2
                break
            if self.level == 1:
                self.level -= 1
                self.image_source = str(self.select_image(self.level))
                self.button1_text = self.text_button1_2
                self.button2_text = self.text_button2
                break
            if self.level == 2 or self.level == 3:
                self.level -= 1
                self.image_source = str(self.select_image(self.level))
                self.button1_text = self.text_button1
                self.button2_text = self.text_button2
                break

    def select_image(self, level):
        '''Select right image from the list general_info_images'''
        print (level)
        return self.general_info_images[level]

class Log_in_Screen(Screen):
    icon_source = str(os.path.dirname(os.path.abspath(__file__))+'/images/icons/loginicon.png')
    backspace_source = str(os.path.dirname(os.path.abspath(__file__))+'/images/icons/backicon.png')
    def login_check(self, email, password):
        print (email)
        print (password)
        self.emaildisplay.text = ''
        self.passdisplay.text = ''
        root_widget.current = 'in_use'

class Feedback_Screen(Screen):
    pass

class In_Use_Screen(Screen):
    pass

class History_Screen(Screen):
    pass

class Navigation_Screen(Screen):
    pass

class MyScreenManager(ScreenManager):
    pass


root_widget = Builder.load_file('Bike.kv')
class BikeApp(App):
    icon = 'app_icon'
    def build(self):
        root_widget.current = 'unlock'
        return root_widget

if __name__ == '__main__':
    system_run()
    BikeApp().run()
