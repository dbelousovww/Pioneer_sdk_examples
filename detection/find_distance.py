import cv2
import numpy as np
from pioneer_sdk import Camera

# Загрузка коэффициентов калибровки камеры из файла
def load_camera_calibration_coefficients(file_path):
    cv_file = cv2.FileStorage(file_path, cv2.FILE_STORAGE_READ)
    camera_matrix = cv_file.getNode("mtx").mat()
    dist_coeffs = cv_file.getNode("dist").mat()
    cv_file.release()
    return camera_matrix, dist_coeffs

# Калибровка камеры
camera_matrix, dist_coeffs = load_camera_calibration_coefficients("data.yml")

# Размер объекта в метрах
size_of_object_real = 0.2  # Реальный размер объекта в метрах
camera = Camera()

while True:
    frame = camera.get_cv_frame()

    # Фильтрация красного цвета
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 100, 110])
    upper_red = np.array([10, 255, 255])
    red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)
    red_objects = cv2.bitwise_and(frame, frame, mask=red_mask)

    # Поиск контура красного объекта
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # Находим контур с максимальной площадью
        max_contour = max(contours, key=cv2.contourArea)

        # Измеряем площадь контура
        contour_area = cv2.contourArea(max_contour)

        # Рассчитываем расстояние до объекта
        radius = np.sqrt(contour_area / np.pi)
        distance_to_object = (camera_matrix[0, 0] * size_of_object_real) / (2 * radius)

        print(f"Расстояние до объекта: {distance_to_object:.2f} метров")

        # Отрисовываем контур и выводим расстояние на экран
        cv2.drawContours(red_objects, [max_contour], -1, (0, 255, 0), 2)
        cv2.putText(red_objects, f"Distance: {distance_to_object:.2f} m", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow("video", red_objects)

    if cv2.waitKey(1) == 27:  # Выход при нажатии клавиши ESC
        break

cv2.destroyAllWindows()
