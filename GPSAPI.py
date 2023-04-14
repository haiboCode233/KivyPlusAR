import requests
import show_route
import serial


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

    def get_bike_url(self):
        start_pos = str(self.start_coordinate).strip('[').strip(']').replace(' ', '')
        desti_pos = str(self.desti_coordinate).strip('[').strip(']').replace(' ', '')
        self.res_url = f"https://restapi.amap.com/v4/direction/bicycling?key={self.key}&origin={start_pos}&destination={desti_pos}"

    def get_drive_url(self):
        start_pos = str(self.start_coordinate).strip('[').strip(']').replace(' ', '')
        desti_pos = str(self.desti_coordinate).strip('[').strip(']').replace(' ', '')
        self.res_url = f"https://restapi.amap.com/v3/direction/driving?origin={start_pos}&destination={desti_pos}&key={self.key}"

    def make_navi_data(self):
        points = []
        data = requests.get(self.res_url).json()
        try:
            paths = data["route"]["paths"]
            polyline = paths[0]['steps']  # list
        except Exception as e:
            paths = data["data"]["paths"]
            polyline = paths[0]['steps']  # list
        for i in range(0, len(polyline)):
            points.extend(polyline[i]['polyline'].split(';'))
        show_route.gps_lon_lat.clear()
        for i in range(0, len(points)):
            x, y = map(float, points[i].split(","))
            show_route.gps_lon_lat.append(y)
            show_route.gps_lon_lat.append(x)
        show_route.create_pic_data()


class device:
    def __init__(self):
        self.location = []
        self.baud_rate = 115200
        self.port = ''
        self.interface = ''
        self.GPS_Data = ''
        self.create_interface()

    def create_interface(self):
        for i in range(0, 100):
            self.port = 'COM'
            self.port = self.port + str(i)
            try:
                self.interface = serial.Serial(self.port, self.baud_rate, timeout=1)
                self.GPS_Data = self.interface.readline().decode('utf-8')
                if len(self.GPS_Data) >= 8:
                    print(self.GPS_Data)
                    print("Successfully find the device!")
                    print("Port:{}".format(self.port))
                    break
                else:
                    print(self.GPS_Data)
                    print("Connected to {},but it is not the device".format(self.port))
            except Exception as e:
                print("{} is not the device".format(self.port))
                print("error msg:{}".format(e))

    def get_location(self):
        while True:
            self.GPS_Data = self.interface.readline().decode('utf-8')
            if self.GPS_Data.startswith('$GNRMC'):
                fields = self.GPS_Data.split(',')
                self.location = []
                self.location.append(show_route.DegreeConvert(float(fields[3])))
                self.location.append(show_route.DegreeConvert(float(fields[5])))
                print(self.location)
                return


if __name__ == '__main__':
    a = device()
    a.get_location()
