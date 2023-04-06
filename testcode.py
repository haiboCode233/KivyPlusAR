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
            start = "116.481028,39.989643"
            end = "116.434446,39.90816"
            url = f"https://restapi.amap.com/v3/direction/walking?key=1b1779b2176bc8d85a93f9aef22b8a53&origin=116.481028,39.989643&destination=116.434446,39.90816"
            response = requests.get(url)
            data = response.json()

            # 解析路径数据
            paths = data["route"]["paths"]
            polyline = paths[0]['steps']  # list
            i = 0
            try:
                while True:
                    print(type(polyline[i]['polyline'].split(';')))
                    points.extend(polyline[i]['polyline'].split(';'))
                    i = i + 1
            except Exception as e:
                print(e)
            show_route.gps_lon_lat.clear()
            for i in range(0, len(points)):
                x, y = map(float, points[i].split(","))
                show_route.gps_lon_lat.append(y)
                show_route.gps_lon_lat.append(x)
            show_route.create_pic_data()
            self.draw_route(show_route.all_x, show_route.all_y)
            return True
        return super(MapWidget, self).on_touch_down(touch)


class MapApp(App):
    def build(self):
        return MapWidget()


if __name__ == "__main__":
    MapApp().run()
