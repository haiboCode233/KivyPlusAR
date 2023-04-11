import numpy as np
import matplotlib.pyplot as plt
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg


class MyWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)

        # 创建 Figure 对象和 FigureCanvasKivyAgg 对象
        self.fig = plt.figure()
        canvas = FigureCanvasKivyAgg(self.fig)
        self.button = Button(text="plot", size_hint=(0.3, 0.3))
        self.button.bind(on_release=self.update_data)
        self.add_widget(self.button)
        self.add_widget(canvas)
        # 调用 Matplotlib 绘图方法绘制初始图形
        self.plot_data()

    def plot_data(self):
        # 清除 Figure 对象的现有图形
        self.fig.clf()

        # 生成随机数据
        x = np.random.rand(50)
        y = np.random.rand(50)

        # 绘制散点图
        plt.scatter(x, y)

        # 调用 FigureCanvasKivyAgg 对象的 draw() 方法将图形渲染到界面上
        self.canvas.draw()

    def update_data(self):
        # 调用 Matplotlib 绘图方法更新图形
        self.plot_data()


class MyApp(App):
    def build(self):
        return MyWidget()


if __name__ == '__main__':
    MyApp().run()
