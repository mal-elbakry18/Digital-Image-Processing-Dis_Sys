import cv2  # OpenCV for image processing
import numpy as np

def process_image(image_path, operation):
    # Load the image
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # Perform the specified operation
    if operation == 'edge_detection':
        result = cv2.Canny(img, 100, 200)
    elif operation == 'color_inversion':
        result = cv2.bitwise_not(img)
  
    else:
        print("Unknown operation")
        result = None

    return result
