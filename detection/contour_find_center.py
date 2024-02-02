import cv2
import numpy as np
from pioneer_sdk import Camera

# Подключение к камере дрона
camera = Camera()

def filter_red_color(frame):
    # Преобразование кадра в цветовое пространство HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Определение диапазона красного цвета в HSV
    lower_red = np.array([0, 100, 110])
    upper_red = np.array([10, 255, 255])

    # Создание маски для красного цвета
    red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)

    # Применение маски к исходному кадру
    red_objects = cv2.bitwise_and(frame, frame, mask=red_mask)

    return red_objects, red_mask

def find_object_center(mask):
    # Поиск контуров на маске
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Поиск контура с максимальной площадью
        max_contour = max(contours, key=cv2.contourArea)

        # Вычисление центра масс контура
        M = cv2.moments(max_contour)
        if M["m00"] != 0:
            center_x = int(M["m10"] / M["m00"])
            center_y = int(M["m01"] / M["m00"])
            return center_x, center_y
    return None

if __name__ == "__main__":
    while True:
        frame = camera.get_cv_frame()  # Получение кадра (в данном случае уже декодированного)
        
        if frame is not None:
            # Изменение размера кадра до определенной ширины и высоты
            new_width = 640  # указать новую ширину
            new_height = 480  # указать новую высоту
            frame = cv2.resize(frame, (new_width, new_height))
    
            # Фильтрация красного цвета
            red_objects, red_mask = filter_red_color(frame)
    
            # Поиск центра красного объекта
            red_center = find_object_center(red_mask)
    
            if red_center:
                # Нарисовать круг в центре красного объекта
                cv2.circle(red_objects, red_center, 5, (0, 0, 255), -1)
    
            cv2.imshow("video", red_objects)  # Показать кадр с красным объектом и центром на экране
    
            if cv2.waitKey(1) == 27:  # Выход при нажатии клавиши ESC
                break

    cv2.destroyAllWindows()  # Закрыть все открытые окна OpenCV
