import kivy
import os

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

#Turn screen backlight off
os.system("echo"+" "+"1"+" "+">"+"/sys/class/backlight/rpi_backlight/brightness")

Window.size = (800,480)

RootApp = None

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
    pass

class MainPanel(BoxLayout):
    pass
class MenuBar(ActionBar):
    pass
class ActionMenu(ActionPrevious):
    def toggle(self):
        RootApp.toggle_sidepanel()
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
    def keyboard(self):
        keyboard = Window.request_keyboard(
        self._keyboard_close, self)
        if keyboard.widget:
            vkeyboard = self._keyboard.widget
            vkeyboard.layout = 'numeric.json'

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
    menu = ObjectProperty()
    def build(self):
        self.menu = NavDrawer()
        return root_widget

if __name__ == '__main__':
    BikeApp().run()
