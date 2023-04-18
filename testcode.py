import matplotlib.pyplot as plt

# 模拟导航路径数据
path = [(0, 0), (1, 1), (2, 3), (3, 4), (4, 2)]

# 初始化绘图
fig, ax = plt.subplots()
ax.set_xlim(-1, 5)
ax.set_ylim(-1, 5)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Navigation Path')

# 绘制导航路径
x = [point[0] for point in path]
y = [point[1] for point in path]
ax.plot(x, y, 'b-')

# 初始化用户位置
user_position = (0, 0)
user_position_plot, = ax.plot(user_position[0], user_position[1], 'ro')  # 用户位置的红点


# 更新用户位置
def update_user_position(new_pos):
    user_position_plot.set_data(new_pos[0], new_pos[1])  # 更新红点的坐标
    plt.draw()  # 重新绘制图像


# 模拟用户位置的更新
import time

for i in range(1, len(path)):
    new_position = path[i]
    update_user_position(new_position)
    plt.pause(1)  # 暂停一秒
    time.sleep(1)  # 等待一秒
