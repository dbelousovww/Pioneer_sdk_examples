from pioneer_sdk import Pioneer

# Создаем экземпляр класса Pioneer
mini = Pioneer()

# Задаем массив точек задачи
task_points_array = [[0, 1, 1],
                    [0, 0, 1]]

# Функция для перемещения дрона в начальную точку
def go_to_start_point():
    mini.arm()                                      # Включаем моторы дрона
    mini.takeoff()                                  # Дрон взлетает
    mini.go_to_local_point(x=0, y=0, z=1, yaw=0)    # Дрон перемещается в начальную точку
    while not mini.point_reached():                 # Ожидаем достижения точки
        pass

# Функция для получения локальных координат и управления светодиодом
def get_local_coords():
    r = g = b = 0
    local_coords_arr = mini.get_local_position_lps() # Получаем массив локальных координат
    if local_coords_arr:
        if 0 < local_coords_arr[1] < 0.5:
            r = g = 0
            b = 0.1
        elif 0.5 < local_coords_arr[1] < 1:
            r = b = 0
            g = 0.1
        else:
            b = g = 0
            r = 0.1
        mini.led_control(led_id=255, r=r, g=g, b=b)  # Управление светодиодом

# Функция для выполнения задачи по перемещению между точками
def do_the_task():
    k = 0
    while k < len(task_points_array):
        mini.go_to_local_point(x=task_points_array[k][0], y=task_points_array[k][1], z=task_points_array[k][2], yaw=0)
        while not mini.point_reached():     # Ожидаем достижения точки
            get_local_coords()              # Получаем и обрабатываем локальные координаты
        k += 1

# Основная часть программы
if __name__ == '__main__':
    try:
        go_to_start_point()  # Выполняем функцию для начального перемещения
        do_the_task()        # Выполняем задачу перемещения между точками
    except KeyboardInterrupt:
        mini.land()          # При прерывании программы выполняем посадку дрона
    finally:
        mini.land()          # После выполнения кода в блоке try выполняем посадку
        del mini             # Освобождаем ресурсы
