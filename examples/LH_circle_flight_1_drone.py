from pioneer_sdk import Pioneer
import math

r = 0.5  # radius
a = 2 * math.pi / 20  # 20 points on a circle 
# coordinates of the center of the circle
x_c = 0
y_c = 2
z_c = -1

mini = Pioneer()
while not mini.connected():
    pass
try:
    mini.arm()
    mini.takeoff()
    mini.go_to_local_point(x=0, y=0, z=z_c, yaw=0)
    k = 0
    while True:
        x = x_c + r * math.cos(a * k)
        y = y_c + r * math.sin(a * k)
        mini.go_to_local_point(x=x, y=y, z=z_c, yaw=0)
        while not mini.point_reached():
            pass
        k += 1
finally:
    mini.land()
