class Navi_auto:
    def __init__(self):
        self.latitude = 1
        self.longitude = 0
        self.start_coordinate = [116.481028, 39.989643]
        self.desti_coordinate = [116.434446, 39.90816]
        self.res_url = ""
        self.res_data = []

    def get_coordinate(self, start_longitude, start_latitude, desti_longitude, desti_latitude):
        self.start_coordinate[self.longitude] = start_longitude
        self.start_coordinate[self.latitude] = start_latitude
        self.desti_coordinate[self.longitude] = desti_longitude
        self.desti_coordinate[self.latitude] = desti_latitude

    def get_url(self):
        start_pos = str(self.start_coordinate).strip('[').strip(']').replace(' ', '')
        desti_pos = str(self.desti_coordinate).strip('[').strip(']').replace(' ', '')
        self.res_url = f"https://restapi.amap.com/v3/direction/walking?key=1b1779b2176bc8d85a93f9aef22b8a53&origin={start_pos}&destination={desti_pos}"


if __name__ == '__main__':
    a = Navi_auto()
    a.get_url()
