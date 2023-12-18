import cv2
import numpy as np
from pioneer_sdk import Camera

# Connect to the drone camera
camera = Camera()

def filter_red_color(frame):
    # Convert the frame to the HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the red color in HSV
    lower_red = np.array([0, 100, 110])
    upper_red = np.array([10, 255, 255])

    # Create a mask for the red color
    red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)

    # Apply the mask to the original frame
    red_objects = cv2.bitwise_and(frame, frame, mask=red_mask)

    return red_objects, red_mask

def find_object_center(mask):
    # Find contours on the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the contour with the maximum area
        max_contour = max(contours, key=cv2.contourArea)

        # Calculate the center of mass of the contour
        M = cv2.moments(max_contour)
        if M["m00"] != 0:
            center_x = int(M["m10"] / M["m00"])
            center_y = int(M["m01"] / M["m00"])
            return center_x, center_y
    return None

if __name__ == "__main__":
    while True:
        frame = camera.get_cv_frame()  # Get frame (in this case already decoded)

        # Resize the frame to a specific width and height
        new_width = 640  # specify the new width
        new_height = 480  # specify the new height
        frame = cv2.resize(frame, (new_width, new_height))

        # Filter red color
        red_objects, red_mask = filter_red_color(frame)

        # Find the center of the red object
        red_center = find_object_center(red_mask)

        if red_center:
            # Draw a circle at the center of the red object
            cv2.circle(red_objects, red_center, 5, (0, 0, 255), -1)

        cv2.imshow("video", red_objects)  # Show the frame with red object and center on the screen

        if cv2.waitKey(1) == 27:  # Exit if the ESC key is pressed
            break

    cv2.destroyAllWindows()  # Close all opened OpenCV windows
