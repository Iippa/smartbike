from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.garden.navigationdrawer import NavigationDrawer
from kivy.lang import Builder
from kivy.base import runTouchApp
from kivy.garden.navigationdrawer import NavigationDrawer
from kivy.uix.actionbar import ActionBar, ActionPrevious


class On_Hold_Screen(Screen):
    pass

class General_Info_Screen(Screen):
    pass

class Log_in_Screen(Screen):
    pass

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

class NavDrawer(NavigationDrawer):
    def __init__(self, **kwargs):
        super(NavDrawer, self).__init__( **kwargs)
        self.anim_type = 'slide_above_anim'
    def close_sidepanel(self, animate=True):
        if self.state == 'open':
            if animate:
                self.anim_to_state('closed')
            else:
                self.state = 'closed'

root_widget = Builder.load_file('Test.kv')

class TestApp(App):
    def build(self):
        return root_widget
TestApp().run()
