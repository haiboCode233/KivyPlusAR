import math
import numpy as np

all_x = []
all_y = []
rot_theta = (0 / 180) * math.pi
rot = np.array([[math.cos(rot_theta), -math.sin(rot_theta)], [math.sin(rot_theta), math.cos(rot_theta)]])
gps_lon_lat = []  # 这里放所有的GPS点
__IterativeTimes = 10  # 反向转换程序中的迭代次数
__IterativeValue = 0  # 反向转换程序中的迭代初始值
__A = 6378.137  # 椭球体长轴,千米
__B = 6356.752314  # 椭球体短轴,千米
__B0 = 0  # 标准纬度,弧度
__L0 = 0  # 原点经度,弧度


# 角度到弧度的转换
def DegreeToRad(degree):
    return math.pi * degree / 180


# 弧度到角度的转换
def RadToDegree(rad):
    return (180 * rad) / math.pi


# 设定__A与__B
def SetAB(a, b):
    global __A
    global __B
    if a <= 0 or b <= 0:
        return
    __A = a
    __B = b


# 设定__B0
def SetLB0(pmtL0, pmtB0):
    global __L0
    global __B0
    l0 = DegreeToRad(pmtL0)
    if l0 < -math.pi or l0 > math.pi:
        return
    __L0 = l0

    b0 = DegreeToRad(pmtB0)
    if b0 < -math.pi / 2 or b0 > math.pi / 2:
        return
    __B0 = b0


# 经纬度转XY坐标
# pmtLB0: 参考点经纬度
# pmtLB1: 要转换的经纬度
# 返回值: 直角坐标，单位：公里
def LBToXY(pmtLB0_lat, pmtLB0_lon, pmtLB1_lat, pmtLB1_lon):
    global __B0
    global rot
    SetLB0(pmtLB0_lon, pmtLB0_lat)
    B = DegreeToRad(pmtLB1_lat)
    L = DegreeToRad(pmtLB1_lon)

    xy = [0, 0]
    K = 0
    E = math.exp(1)
    if L < -math.pi or L > math.pi or B < (-math.pi / 2) or B > (math.pi / 2):
        return xy
    if __A <= 0 or __B <= 0:
        return xy
    f = (__A - __B) / __A  # 扁率
    dtemp = 1 - (__B / __A) * (__B / __A)
    if dtemp < 0:
        return xy
    e = math.sqrt(dtemp)  # 第一偏心率
    dtemp = (__A / __B) * (__A / __B) - 1
    if dtemp < 0:
        return xy
    e_ = math.sqrt(dtemp)  # 第二偏心率

    NB0 = ((__A * __A) / __B) / math.sqrt(1 + e_ * e_ * math.cos(__B0) * math.cos(__B0))  # 卯酉圈曲率半径
    K = NB0 * math.cos(__B0)
    xy[0] = K * (L - __L0)
    xy[1] = K * math.log(
        math.tan(math.pi / 4 + (B) / 2) * math.pow((1 - e * math.sin(B)) / (1 + e * math.sin(B)), e / 2))
    y0 = K * math.log(
        math.tan(math.pi / 4 + (__B0) / 2) * math.pow((1 - e * math.sin(__B0)) / (1 + e * math.sin(__B0)), e / 2))
    xy[1] = xy[1] - y0
    xy[1] = -xy[1]  # 正常的Y坐标系（向上）转程序的Y坐标系（向下）
    xy[0] = xy[0] * 1000
    xy[1] = xy[1] * 1000

    xy_rot = np.array([xy[0], xy[1]])
    xy_rot = np.dot(xy_rot, rot)
    xy[0] = xy_rot[0]
    xy[1] = xy_rot[1]
    return xy


def gps_read_point(point_index):
    global gps_lon_lat
    return_value = [0, 0]
    return_value[0] = gps_lon_lat[point_index * 2]
    return_value[1] = gps_lon_lat[point_index * 2 + 1]
    return return_value


# 度分转度度
def DegreeConvert(sDegree):
    if sDegree == 0:
        return 0
    integer = int(sDegree)
    decimal = sDegree - int(sDegree)
    min = integer % 100
    hour = int(integer / 100)
    dDegree = float(hour) + float(min / 60) + float(decimal / 60)
    return dDegree


# 度度转度分
def DD2DFConvert(dDegree):
    if dDegree == 0:
        return 0
    integer = int(dDegree)
    decimal = dDegree - integer
    integer = integer * 100
    decimal = decimal * 60
    return integer + decimal


def create_pic_data():
    global gps_lon_lat, all_x, all_y
    for i in range(0, int(len(gps_lon_lat) / 2)):
        all_x.append(LBToXY(DegreeConvert(gps_read_point(0)[0]), DegreeConvert(gps_read_point(0)[1]),
                            DegreeConvert(gps_read_point(i)[0]), DegreeConvert(gps_read_point(i)[1]))[0])
        all_y.append(LBToXY(DegreeConvert(gps_read_point(0)[0]), DegreeConvert(gps_read_point(0)[1]),
                            DegreeConvert(gps_read_point(i)[0]), DegreeConvert(gps_read_point(i)[1]))[1])


