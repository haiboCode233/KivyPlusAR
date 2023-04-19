import serial
import time


class hardware:
    def __init__(self):
        self.baud_rate = 9600
        self.port = ''
        self.interface = ''
        self.Data = ''
        self.sta = 0

    def create_interface(self):
        self.port = 'COM7'
        self.baud_rate = 9600
        while True:
            try:
                self.interface = serial.Serial(self.port, self.baud_rate, timeout=0.1)
                break
            except Exception as e:
                print(e)
        time.sleep(2)
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
        self.Data = self.interface.read(20).decode()
        print(self.Data)
        return self.Data


if __name__ == '__main__':
    a = hardware()
    a.create_interface()
