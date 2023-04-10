import numpy as np
import matplotlib.pyplot as plt
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.text import LabelBase
from kivy.uix.spinner import Spinner
import GPSAPI
import show_route

NAVI_GaoDe = GPSAPI.Navi_auto()
from plyer import gps

sys_android_windows = 0
Window.size = (360, 640)
LabelBase.register(name='SimSun', fn_regular='SimSun.ttf')


class MySpinner(Spinner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.values = ['Option 1', 'Option 2', 'Option 3']
        self.text = self.values[0]


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        # gps_on_android
        if sys_android_windows:
            self.gps = gps
            self.gps.configure(on_location=self.on_location)
            self.gps.start()
        # popup warning
        self.warning_empty = Label(text='Empty Input!')
        self.warning_popup = Popup(title='Warning', content=self.warning_empty, auto_dismiss=True, size_hint=(0.5, 0.2))

        # popup setting

        self.dict_all_places = {}
        self.popup_slct_boxlayout = BoxLayout(orientation='vertical', size_hint_x=None, width=280, size_hint_y=None,
                                              height=360)
        self.popup_mode_boxlayout = BoxLayout(orientation='horizontal', size_hint_y=None, height=100)
        self.popup_exit_boxlayout = BoxLayout(orientation='horizontal', size_hint_y=None, height=120)

        self.popup_exit_boxlayout.cols = 2
        self.button_GO = Button(text='GO!', size_hint=(0.3, None), height=60)
        self.button_cancel = Button(text='Cancel', size_hint=(0.3, None), height=60)
        self.popup_exit_boxlayout.add_widget(self.button_GO)
        self.popup_exit_boxlayout.add_widget(self.button_cancel)

        self.popup_mode_boxlayout.cols = 3
        self.button_walk = ToggleButton(text='Walk', size_hint=(0.3, None), height=60)
        self.button_bike = ToggleButton(text='Bike', size_hint=(0.3, None), height=60)
        self.button_drive = ToggleButton(text='Drive', size_hint=(0.3, None), height=60)
        self.popup_mode_boxlayout.add_widget(self.button_walk)
        self.popup_mode_boxlayout.add_widget(self.button_bike)
        self.popup_mode_boxlayout.add_widget(self.button_drive)

        self.popup_slct_boxlayout.cols = 1
        self.spinner = MySpinner(size_hint=(1, None), height=40)
        self.spinner.font_name = 'SimSun'

        self.tips = Label(text='select your destination')
        self.tips_2 = Label(text='select your way')
        self.place_holder = Widget(size_hint=(0.95, None), height=80)
        self.place_holder_2 = Widget(size_hint=(0.95, None), height=20)
        self.place_holder_3 = Widget(size_hint=(0.95, None), height=20)

        self.popup_slct_boxlayout.add_widget(self.place_holder)
        self.popup_slct_boxlayout.add_widget(self.tips)
        self.popup_slct_boxlayout.add_widget(self.place_holder_2)
        self.popup_slct_boxlayout.add_widget(self.spinner)
        self.popup_slct_boxlayout.add_widget(self.place_holder_3)
        self.popup_slct_boxlayout.add_widget(self.tips_2)
        self.popup_slct_boxlayout.add_widget(self.popup_mode_boxlayout)
        self.popup_slct_boxlayout.add_widget(self.popup_exit_boxlayout)

        self.setting_popup = Popup(title='Setting', content=self.popup_slct_boxlayout, auto_dismiss=False,
                                   size_hint_x=None,
                                   width=300, size_hint_y=None, height=380)

        # layouts
        box_layout = BoxLayout(orientation='vertical')
        toolbar_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60)
        toolbar_layout.cols = 2
        swpage_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60)
        swpage_layout.cols = 2

        # widgets for box_layout
        self.fig, self.ax = plt.subplots()
        x = np.linspace(0, 2 * np.pi, 100)
        y = np.sin(x)
        self.ax.plot(x, y)
        self.ax.axis('off')
        canvas = FigureCanvasKivyAgg(self.fig)

        # widgets for swpage_layout
        self.device_button = Button(text='Device Page', font_size=32, size_hint_x=None, width=240,
                                    size_hint_y=None, height=60)
        self.device_button.bind(on_press=self.go_to_second_screen)
        self.reset_button = Button(text='Reset', font_size=32, size_hint_x=None, width=120,
                                   size_hint_y=None, height=60)
        self.reset_button.bind(on_press=self.reset_navi)

        # widgets for toolbar_layout
        self.input_dest = TextInput(multiline=False, hint_text="Enter your destination", size_hint_x=None, width=240,
                                    size_hint_y=None, height=60)
        self.input_text = ""
        self.input_last_text = ""
        self.input_dest.font_name = './SimSun.ttf'
        self.go = Button(text='Search', font_size=32, size_hint_x=None, width=120, size_hint_y=None, height=60)
        self.go.bind(on_press=self.choose_desti_way)

        # layouts
        swpage_layout.add_widget(self.device_button)
        swpage_layout.add_widget(self.reset_button)

        toolbar_layout.add_widget(self.input_dest)
        toolbar_layout.add_widget(self.go)

        box_layout.add_widget(canvas)
        box_layout.add_widget(swpage_layout)
        box_layout.add_widget(toolbar_layout)

        self.add_widget(box_layout)

    def go_to_second_screen(self, instance):
        myapp.screen_manager.current = 'second_screen'

    def reset_navi(self, *args):
        self.ax.clear()
        self.ax.axis('off')
        self.ax.text(0.5, 0.5, 'Go and Explore!', ha='center', va='center')
        self.fig.canvas.draw()

    def choose_desti_way(self, *args):
        if self.input_dest.text:
            self.dict_all_places = NAVI_GaoDe.get_destination(destination=self.input_dest.text)
            self.spinner.values = self.dict_all_places.keys()
            self.spinner.text = self.spinner.values[0]
            self.setting_popup.open()
        else:
            self.warning_popup.open()

    def make_route(self, *args):
        self.ax.clear()
        self.ax.axis('off')
        self.input_text = self.input_dest.text
        if self.input_text == "" or self.input_text == self.input_last_text:
            return
        self.input_last_text = self.input_text
        NAVI_GaoDe.get_walking_url()
        NAVI_GaoDe.make_navi_data()
        x = show_route.all_x
        y = show_route.all_y
        self.ax.plot(x, y)
        self.fig.canvas.draw()

    # gps_on_android
    def on_location(self, **kwargs):
        print(str(kwargs['lat']), str(kwargs['lon']))


class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)

        self.orientation = 'vertical'

        label = Label(text='Welcome to Second Screen', font_size=30)
        self.add_widget(label)

        button = Button(text='Go back to Main Screen', font_size=20)
        button.bind(on_press=self.go_to_main_screen)
        self.add_widget(button)

    def go_to_main_screen(self, instance):
        myapp.screen_manager.current = 'main_screen'


class MyApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        main_screen = MainScreen()
        screen = Screen(name='main_screen')
        screen.add_widget(main_screen)
        self.screen_manager.add_widget(screen)

        second_screen = SecondScreen()
        screen = Screen(name='second_screen')
        screen.add_widget(second_screen)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == '__main__':
    myapp = MyApp()
    myapp.run()
