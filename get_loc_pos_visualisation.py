import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pioneer_sdk import Pioneer
import keyboard

# Инициализация дрона
mini = Pioneer()

# Списки для хранения округленных координат
x_coordinates = []
y_coordinates = []
z_coordinates = []

# Количество точек для сглаживания (подберите оптимальное значение)
smoothing_points = 5

# Создание трехмерного графика
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Обработчик событий для закрытия соединения по нажатию клавиши ESC
def close_connection_on_escape(e):
    if keyboard.is_pressed('esc'):
        print("Программа завершена по запросу пользователя.")
        mini.close_connection()
        plt.close()

# Привязываем обработчик событий
keyboard.hook(close_connection_on_escape)

try:
    while True:
        # Получение локальных координат дрона
        array_of_coordinates = mini.get_local_position_lps()

        if array_of_coordinates:
            x_coordinates.append(array_of_coordinates[0])
            y_coordinates.append(array_of_coordinates[1])
            z_coordinates.append(array_of_coordinates[2])

            # Применение скользящего среднего для сглаживания
            if len(x_coordinates) >= smoothing_points:
                x_smoothed = round(sum(x_coordinates[-smoothing_points:]) / smoothing_points, 2)
                y_smoothed = round(sum(y_coordinates[-smoothing_points:]) / smoothing_points, 2)
                z_smoothed = round(sum(z_coordinates[-smoothing_points:]) / smoothing_points, 2)

                ax.plot([x_smoothed], [y_smoothed], [z_smoothed], marker='o', color='blue')

            plt.draw()
            plt.pause(0.1)  # Пауза для обновления графика

        time.sleep(0.1)  # Уменьшил период ожидания

except KeyboardInterrupt:
    print("Программа завершена по запросу пользователя.")
finally:
    # Подписываем оси на графике
    ax.set_xlabel('X ')
    ax.set_ylabel('Y ')
    ax.set_zlabel('Z ')

    # Нанесение стартовой точки зеленым цветом
    ax.scatter(x_coordinates[0], y_coordinates[0], z_coordinates[0], color='green', label='Start')

    # Нанесение конечной точки красным цветом
    ax.scatter(x_coordinates[-1], y_coordinates[-1], z_coordinates[-1], color='red', label='End')

    # Сохранение графика в файл при завершении программы
    filename = 'drone_trajectory.png'
    fig.savefig(filename, format='png', dpi=300, bbox_inches='tight')
    print(f"График сохранен в файл: {filename}")

    # Закрытие соединения с дроном (если не было закрыто по нажатию ESC)
    mini.close_connection()

# Отображение окна с графиком и оставление его открытым после завершения программы
plt.show()
