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

Window.size = (360, 640)


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

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

        # widgets for toolbar_layout
        self.input_dest = TextInput(multiline=False, hint_text="Enter your destination", size_hint_x=None, width=240,
                                    size_hint_y=None, height=60)
        self.go = Button(text='GO!', font_size=32, size_hint_x=None, width=120, size_hint_y=None, height=60)
        self.go.bind(on_press=self.change_pic)

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

    def change_pic(self, *args):
        self.ax.clear()
        self.ax.axis('off')
        x = [1, 2, 3]
        y = [4, 5, 6]
        self.ax.plot(x, y)
        self.fig.canvas.draw()


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
