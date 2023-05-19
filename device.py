import serial
import time
import math


class hardware:
    def __init__(self):
        self.baud_rate = 9600
        self.port = ''
        self.interface = ''
        self.Data = ''
        self.sta = 0

    def create_interface(self):
        self.port = 'COM3'
        self.baud_rate = 9600
        while True:
            try:
                self.interface = serial.Serial(self.port, self.baud_rate, timeout=0.1)
                break
            except Exception as e:
                print(e)
        time.sleep(1)
        self.interface.write(b'a')
        self.Data = self.interface.read(20)
        print("test:   ", self.Data)
        if self.Data == b'cba':
            self.sta = 1
        else:
            self.sta = 0

    def query_power(self):
        print("start query...")
        self.interface.write(b'p')
        try:
            self.Data = self.interface.read(20).decode()
            print(self.Data)
            return self.Data
        except Exception as e:
            return False

    def data_select(self, data):
        if self.sta != 1 or len(data) <= 100:
            return data
        new_data = []
        select_step = math.ceil(len(data)/100)  # 最多发送100组数据
        select_idx = 0  # 索引
        while select_idx < len(data) - 1:
            new_data.append(data[select_idx])
            select_idx = select_idx + select_step
        return new_data

    def data_process(self, data):
        if self.sta != 1:
            return
        for i in range(0, len(data)):
            data[i] = round(data[i], 1)
        return data

    def send_location(self, x_data, y_data):
        if self.sta == 1:
            self.interface.write(str(x_data).encode())
            self.interface.write(b',')
            self.interface.write(str(y_data).encode())
            self.interface.write(b'x')

    def send_route(self, x_data, y_data):
        x_data = self.data_select(x_data)
        y_data = self.data_select(y_data)
        x_data = self.data_process(x_data)
        y_data = self.data_process(y_data)
        print(len(x_data))
        print(len(y_data))
        if self.sta == 1:
            self.interface.write(b's')  # 开始发送坐标
            for i in range(0, len(x_data)):
                self.interface.write(str(x_data[i]).encode())
                self.interface.write(b',')
                self.interface.write(str(y_data[i]).encode())
                self.interface.write(b'x')  # 一小组结束
            self.interface.write(b'e')  # 发送结束标志
        else:
            print("not connected to the device!")

    def send_cmd_L(self):
        self.interface.write(b'l')  # 开始发送横坐标

    def send_cmd_M(self):
        self.interface.write(b'm')  # 开始发送横坐标

    def send_cmd_R(self):
        self.interface.write(b'r')  # 开始发送横坐标


if __name__ == '__main__':
    a = hardware()
    a.create_interface()
