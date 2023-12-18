import cv2
import numpy as np
from pioneer_sdk import Camera

# Ширина и высота кадра
frameWidth = 480
frameHeight = 360
camera = Camera()

# Функция-заглушка для создания трекбаров
def empty(a):
    pass

# Создание окна HSV и трекбаров для настройки параметров
cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)
cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
cv2.createTrackbar("HUE Max", "HSV", 179, 179, empty)
cv2.createTrackbar("SAT Min", "HSV", 0, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 0, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)

# Имя файла для сохранения значений HSV
filename = "hsv_values.txt"

while True:
    # Получение кадра с камеры и изменение размера
    img = camera.get_cv_frame()
    img = cv2.resize(img, (frameWidth, frameHeight))
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Получение значений трекбаров
    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

    # Запись значений в текстовый файл
    with open(filename, 'w') as txt_file:
        txt_file.write(f"lower [{h_min}, {s_min}, {v_min}] \nupper [{h_max}, {s_max}, {v_max}]")

    # Определение нижней и верхней границ маски
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    # Создание маски и применение ее к изображению
    mask = cv2.inRange(imgHsv, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # Горизонтальное объединение изображения, маски и результата
    hStack = np.hstack([img, mask, result])
    cv2.imshow('Горизонтальное объединение', hStack)

    # Выход из цикла при нажатии клавиши 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
