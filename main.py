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
from kivy.clock import Clock
import GPSAPI
import show_route
import threading
import time
import queue
import device

NAVI_GaoDe = GPSAPI.Navi_auto()
GPS_Device = GPSAPI.device()
My_kit = device.hardware()
sys_android_windows = 0
Window.size = (360, 640)
LabelBase.register(name='SimSun', fn_regular='SimSun.ttf')
update_pos_stop = 0


class MySpinner(Spinner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.values = ['Option 1', 'Option 2', 'Option 3']
        self.text = self.values[0]


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

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
        # matplotlib
        self.fig, self.ax = plt.subplots()
        x = np.linspace(0, 2 * np.pi, 100)
        y = np.sin(x)
        self.ax.plot(x, y)
        # self.ax.axis('off')
        self.user_position_plot = ''
        self.event_queue = queue.Queue()
        self.update_pos = threading.Thread(target=self.update_user_position)
        self.update_pos.start()  # 发射事件
        self.update_flg = 0
        self.update_thread_flg = 1
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
        now_location = GPS_Device.get_location()
        # 118.71125,32.205848
        NAVI_GaoDe.get_coordinate(  # start_latitude=now_location[0],
            # start_longitude=now_location[1],
            start_latitude=32.205848,
            start_longitude=118.71125,
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
        My_kit.send_route(x_data=x, y_data=y)  # 发送路径
        self.ax.clear()
        # self.ax.axis('off')
        now_location = show_route.convert_now_location(now_location)
        print("now location: ", now_location)
        self.ax.plot(x, y)
        self.user_position_plot, = self.ax.plot(show_route.DegreeConvert(show_route.gps_read_point(0)[0]),
                                                show_route.DegreeConvert(show_route.gps_read_point(0)[1]), 'ro')
        self.update_flg = 1
        self.fig.canvas.draw()
        if self.update_thread_flg:
            Clock.schedule_interval(self.update_plot, 1)
            self.update_thread_flg = 0

    # 发射事件（发射用户位置）
    def update_user_position(self):
        global update_pos_stop
        test_mode = 1
        while True:
            time.sleep(1)
            if self.update_flg:
                if test_mode:
                    self.event_queue.put([2, 2])
                else:
                    now_location = GPS_Device.get_location()
                    x = now_location[0]
                    y = now_location[1]
                    self.event_queue.put([x, y])
            else:
                pass
            if update_pos_stop == 1:
                break

    def update_plot(self, *args):
        event = self.event_queue.get()
        if len(event) == 2:
            self.user_position_plot.set_data(2, 2)  # 更新红点的坐标
            self.fig.canvas.draw()  # 重新绘制图像
            # print("pass")
        else:
            pass
        pass

    # 主界面函数
    def reset_navi(self, *args):
        self.ax.clear()
        # self.ax.axis('off')
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

    # 切换页面
    def go_to_second_screen(self, instance):
        myapp.screen_manager.current = 'second_screen'


class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)

        self.box_layout = BoxLayout(orientation='vertical', size_hint=(1, 1), padding=[50, 0, 50, 0])
        # widgets
        self.button_connect = ToggleButton(text='Connect Device', size_hint=(1, None), height=60)
        self.button_connect.bind(on_release=self.on_connect_device)
        self.connect_sta_lb = Label(text="Unconnected", size_hint=(1, None), height=60)

        self.button_powerquery = Button(text='Update Power', font_size=20, size_hint=(1, None), height=60)
        self.button_powerquery.bind(on_release=self.on_query_power)
        self.power_sta_lb = Label(text="70%", size_hint=(1, None), height=60)

        self.place_holder = Widget(size_hint=(1, None), height=280)

        self.backbutton = Button(text='Go back to Main Screen', font_size=20, size_hint=(1, None), height=60)
        self.backbutton.bind(on_press=self.go_to_main_screen)

        self.box_layout.add_widget(self.button_connect)
        self.box_layout.add_widget(self.connect_sta_lb)
        self.box_layout.add_widget(self.button_powerquery)
        self.box_layout.add_widget(self.power_sta_lb)
        self.box_layout.add_widget(self.place_holder)
        self.box_layout.add_widget(self.backbutton)

        self.add_widget(self.box_layout)

    def on_connect_device(self, *args):
        My_kit.create_interface()
        if My_kit.sta == 1:
            self.connect_sta_lb.text = "Connected"
            return
        else:
            self.button_connect.state = 'normal'
            self.connect_sta_lb.text = "Unconnected"

    def on_query_power(self, *args):
        power_value = My_kit.query_power()
        self.power_sta_lb.text = power_value

    def go_to_main_screen(self, instance):
        myapp.screen_manager.current = 'main_screen'


class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = ScreenManager()
        self.main_screen = MainScreen()

    def build(self):
        screen = Screen(name='main_screen')
        screen.add_widget(self.main_screen)
        self.screen_manager.add_widget(screen)

        second_screen = SecondScreen()
        screen = Screen(name='second_screen')
        screen.add_widget(second_screen)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

    def on_stop(self):
        global update_pos_stop
        update_pos_stop = 1
        pass


if __name__ == '__main__':
    myapp = MyApp()
    myapp.run()
