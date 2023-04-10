import requests
from kivy.app import App
from matplotlib.figure import Figure
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

import show_route

Window.size = (360, 640)


class MapWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MapWidget, self).__init__(**kwargs)
        self.fig = Figure()
        self.ax = self.fig.add_subplot()

        self.key = '1b1779b2176bc8d85a93f9aef22b8a53'
        self.dest = '南京信息工程大学附属中学'
        self.region = '320111'

    def draw_route(self, x, y):

        self.ax.plot(x, y)
        self.ax.axis('off')
        canvas = FigureCanvasKivyAgg(self.fig)
        self.add_widget(canvas)
        self.canvas.ask_update()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # 获取路径规划结果
            points = []

            url = f"https://restapi.amap.com/v5/place/text?key=1b1779b2176bc8d85a93f9aef22b8a53&keywords=南京信息工程大学附属中学&region=320111&city_limit=true&show_fields=children"
            data_dict = requests.get(url).json()
            for poi in data_dict["pois"]:
                print(poi['name']+"  "+poi['location'])



class MapApp(App):
    def build(self):
        return MapWidget()


if __name__ == "__main__":
    MapApp().run()
