import requests
import show_route


class Navi_auto:
    def __init__(self):
        self.latitude = 1
        self.longitude = 0
        self.start_coordinate = [116.481028, 39.989643]
        self.desti_coordinate = [116.434446, 39.90816]
        self.res_url = ""

    def get_coordinate(self, start_longitude, start_latitude, desti_longitude, desti_latitude):
        self.start_coordinate[self.longitude] = start_longitude
        self.start_coordinate[self.latitude] = start_latitude
        self.desti_coordinate[self.longitude] = desti_longitude
        self.desti_coordinate[self.latitude] = desti_latitude

    def get_url(self):
        start_pos = str(self.start_coordinate).strip('[').strip(']').replace(' ', '')
        desti_pos = str(self.desti_coordinate).strip('[').strip(']').replace(' ', '')
        self.res_url = f"https://restapi.amap.com/v3/direction/walking?key=1b1779b2176bc8d85a93f9aef22b8a53&origin={start_pos}&destination={desti_pos}"

    def make_navi_data(self):
        points = []
        data = requests.get(self.res_url).json()
        paths = data["route"]["paths"]
        polyline = paths[0]['steps']  # list
        for i in range(0, len(polyline)):
            points.extend(polyline[i]['polyline'].split(';'))
        show_route.gps_lon_lat.clear()
        for i in range(0, len(points)):
            x, y = map(float, points[i].split(","))
            show_route.gps_lon_lat.append(y)
            show_route.gps_lon_lat.append(x)
        show_route.create_pic_data()


if __name__ == '__main__':
    a = Navi_auto()
    a.get_url()
    a.make_navi_data()
