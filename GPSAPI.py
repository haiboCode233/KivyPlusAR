import requests
import show_route


class Navi_auto:
    def __init__(self):
        self.key = '1b1779b2176bc8d85a93f9aef22b8a53'
        self.latitude = 1
        self.longitude = 0
        self.start_coordinate = [116.481028, 39.989643]
        self.desti_coordinate = [116.434446, 39.90816]
        self.res_url = ""

    def get_destination(self, destination, region='320111'):
        url = f"https://restapi.amap.com/v5/place/text?key={self.key}&keywords={destination}&region={region}&city_limit=true&show_fields=children"
        data_dict = requests.get(url).json()
        pos_dict = {}
        for poi in data_dict["pois"]:
            pos_dict[poi['name']] = poi['location']
        return pos_dict

    def get_coordinate(self, start_longitude, start_latitude, desti_longitude, desti_latitude):
        self.start_coordinate[self.longitude] = start_longitude
        self.start_coordinate[self.latitude] = start_latitude
        self.desti_coordinate[self.longitude] = desti_longitude
        self.desti_coordinate[self.latitude] = desti_latitude

    def get_walking_url(self):
        start_pos = str(self.start_coordinate).strip('[').strip(']').replace(' ', '')
        desti_pos = str(self.desti_coordinate).strip('[').strip(']').replace(' ', '')
        self.res_url = f"https://restapi.amap.com/v3/direction/walking?key={self.key}&origin={start_pos}&destination={desti_pos}"

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
    a.get_destination("南京信息工程大学附属中学")
