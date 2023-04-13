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

sys_android_windows = 1
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
        # 创建layouts以及存储搜索结果的字典
        self.dict_all_places = {}
        self.popup_slct_boxlayout = BoxLayout(orientation='vertical', size_hint_x=None, width=280, size_hint_y=None,
                                              height=360)
        self.popup_mode_boxlayout = BoxLayout(orientation='horizontal', size_hint_y=None, height=100)
        self.popup_exit_boxlayout = BoxLayout(orientation='horizontal', size_hint_y=None, height=120)
        # 最后一层的确认和取消按钮
        self.popup_exit_boxlayout.cols = 2
        self.button_GO = Button(text='GO!', size_hint=(0.3, None), height=60)
        self.button_cancel = Button(text='Cancel', size_hint=(0.3, None), height=60)
        self.popup_exit_boxlayout.add_widget(self.button_GO)
        self.popup_exit_boxlayout.add_widget(self.button_cancel)
        # 倒数第二层的出行方式按钮
        self.popup_mode_boxlayout.cols = 3
        self.out_mode = 0  # 0 walk,1 bike,2 drive
        self.button_walk = ToggleButton(text='Walk', size_hint=(0.3, None), height=60)
        self.button_bike = ToggleButton(text='Bike', size_hint=(0.3, None), height=60)
        self.button_drive = ToggleButton(text='Drive', size_hint=(0.3, None), height=60)
        self.popup_mode_boxlayout.add_widget(self.button_walk)
        self.popup_mode_boxlayout.add_widget(self.button_bike)
        self.popup_mode_boxlayout.add_widget(self.button_drive)
        # 第一层的下拉框
        self.popup_slct_boxlayout.cols = 1
        self.spinner = MySpinner(size_hint=(1, None), height=40)
        self.spinner.font_name = 'SimSun'
        # 占位控件和标签
        self.tips = Label(text='select your destination')
        self.tips_2 = Label(text='select your way')
        self.place_holder = Widget(size_hint=(0.95, None), height=80)
        self.place_holder_2 = Widget(size_hint=(0.95, None), height=20)
        self.place_holder_3 = Widget(size_hint=(0.95, None), height=20)
        # 布局
        self.popup_slct_boxlayout.add_widget(self.place_holder)
        self.popup_slct_boxlayout.add_widget(self.tips)
        self.popup_slct_boxlayout.add_widget(self.place_holder_2)
        self.popup_slct_boxlayout.add_widget(self.spinner)
        self.popup_slct_boxlayout.add_widget(self.place_holder_3)
        self.popup_slct_boxlayout.add_widget(self.tips_2)
        self.popup_slct_boxlayout.add_widget(self.popup_mode_boxlayout)
        self.popup_slct_boxlayout.add_widget(self.popup_exit_boxlayout)
        # 生成popup
        self.setting_popup = Popup(title='Setting', content=self.popup_slct_boxlayout, auto_dismiss=False,
                                   size_hint_x=None,
                                   width=300, size_hint_y=None, height=380)
        # popup中各个按钮的函数绑定
        # 第三层的确认和取消按钮
        self.button_GO.bind(on_release=self.make_route)
        self.button_cancel.bind(on_release=self.setting_popup.dismiss)
        # 第二层的出行方式
        self.button_walk.bind(on_release=self.walk_route)
        self.button_bike.bind(on_release=self.bike_route)
        self.button_drive.bind(on_release=self.drive_route)

        # layouts
        self.box_layout = BoxLayout(orientation='vertical')
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

        self.box_layout.add_widget(canvas)
        self.box_layout.add_widget(swpage_layout)
        self.box_layout.add_widget(toolbar_layout)

        self.add_widget(self.box_layout)

    # 弹窗界面函数
    def walk_route(self, *args):
        self.out_mode = 0
        self.button_bike.state = 'normal'
        self.button_drive.state = 'normal'

    def bike_route(self, *args):
        self.out_mode = 1
        self.button_walk.state = 'normal'
        self.button_drive.state = 'normal'

    def drive_route(self, *args):
        self.out_mode = 2
        self.button_bike.state = 'normal'
        self.button_walk.state = 'normal'

    def make_route(self, *args):
        self.setting_popup.dismiss()
        NAVI_GaoDe.get_coordinate(start_latitude=32.20593, start_longitude=118.711273,
                                  desti_latitude=float(self.dict_all_places[self.spinner.text].split(',')[1]),
                                  desti_longitude=float(self.dict_all_places[self.spinner.text].split(',')[0]))
        if self.out_mode == 0:
            NAVI_GaoDe.get_walking_url()
        elif self.out_mode == 1:
            NAVI_GaoDe.get_bike_url()
        elif self.out_mode == 2:
            NAVI_GaoDe.get_drive_url()
        else:
            NAVI_GaoDe.get_walking_url()
        NAVI_GaoDe.make_navi_data()
        x = show_route.all_x
        y = show_route.all_y
        self.ax.clear()
        self.ax.axis('off')
        self.ax.plot(x, y)
        self.fig.canvas.draw()

    # 主界面函数
    def reset_navi(self, *args):
        self.ax.clear()
        self.ax.axis('off')
        self.ax.text(0.5, 0.5, 'Go and Explore!', ha='center', va='center')
        self.fig.canvas.draw()

    def choose_desti_way(self, *args):
        if self.input_dest.text:
            try:
                self.dict_all_places = NAVI_GaoDe.get_destination(destination=self.input_dest.text)
                self.spinner.values = self.dict_all_places.keys()
                self.spinner.text = self.spinner.values[0]
                self.setting_popup.open()
            except Exception as e:
                print(e)
                self.warning_popup.open()
        else:
            self.warning_popup.open()

    # gps_on_android
    def on_location(self, **kwargs):
        print(str(kwargs['lat']), str(kwargs['lon']))

    # 切换页面
    def go_to_second_screen(self, instance):
        myapp.screen_manager.current = 'second_screen'


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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = ScreenManager()

    def build(self):
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
