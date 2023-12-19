from pioneer_sdk import Pioneer

# IP-адреса дронов
mini_ip = ["192.168.137.222", "192.168.137.18"]

# Словари для хранения объектов Pioneer и флагов достижения точек для каждого дрона
mini = {}
point_reached = {}

# Координаты точек маршрута
coords = [[0, 1, 1],
          [0, 0, 1],
          [0, 1, 1]]

# Функция ожидания соединения со всеми дронами
def wait_connection():
    while True:
        ret = True
        for ip in mini_ip:
            if not mini[ip].connected():
                ret = False
        if ret:
            return

# Функция для перемещения дронов в начальную точку
def go_to_start_point():
    for ip in mini_ip:
        input(ip + " ARM?")  # Запрос на включение моторов дрона
        mini[ip].arm()
        mini[ip].takeoff()
        mini[ip].go_to_local_point(x=0, y=0, z=1, yaw=0)
        while not mini[ip].point_reached():
            pass

# Функция для выполнения полетного задания по заданным точкам
def run_mission_flight():
    k = 0
    while k < len(coords):
        print("k = " + str(k))
        for ip in mini_ip:
            mini[ip].go_to_local_point(x=coords[k][0], y=coords[k][1], z=coords[k][2], yaw=0)
            point_reached[ip] = False
        while True:
            points_reached = True
            for ip in mini_ip:
                if not point_reached[ip]:
                    point_reached[ip] = mini[ip].point_reached()
                if not point_reached[ip]:
                    points_reached = False
            if points_reached:
                break
        k += 1

# Функция для посадки всех дронов
def all_land():
    for ip in mini_ip:
        mini[ip].land()
    return

if __name__ == '__main__':
    # Инициализация объектов Pioneer для каждого дрона
    for ip in mini_ip:
        mini[ip] = Pioneer(ip=ip, name=ip, logger=False)
    wait_connection()  # Ожидание соединения со всеми дронами
    try:
        go_to_start_point()
        run_mission_flight()  # Замена названия функции
    finally:
        all_land()
