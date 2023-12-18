import cv2
import numpy as np
from pioneer_sdk import Camera

# Connect to the drone camera
camera = Camera()

def filter_red_color(frame):
    # Convert the frame to the HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the red color in HSV
    lower_red = np.array([0, 110, 120])
    upper_red = np.array([10, 255, 255])

    # Create a mask for the red color
    red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)

    # Apply the mask to the original frame
    red_objects = cv2.bitwise_and(frame, frame, mask=red_mask)

    return red_objects

if __name__ == "__main__":
    while True:
        frame = camera.get_cv_frame()  # Get frame (in this case already decoded)

        # Resize the frame to a specific width and height
        new_width = 640  # specify the new width
        new_height = 480  # specify the new height
        frame = cv2.resize(frame, (new_width, new_height))

        # Filter red color
        red_objects = filter_red_color(frame)

        cv2.imshow("video", red_objects)  # Show the frame with red objects on the screen

        if cv2.waitKey(1) == 27:  # Exit if the ESC key is pressed
            break

    cv2.destroyAllWindows()  # Close all opened OpenCV windows
