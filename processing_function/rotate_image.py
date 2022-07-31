import numpy as np
import math
import cv2

try:
    import read_character as re
except:
    import processing_function.read_character as re

# ROTATE AN IMAGE BY ANGLE
def rotateByAngle(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rotation_matrix = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rotation_matrix, image.shape[1::-1])
    return result

# AUTO DETECT PLATE EDGES AND ROTATE
def rotateImage(image):
    edges_image = cv2.Canny(image,  threshold1 = 100,  threshold2 = 200, apertureSize = 3, L2gradient = True)
    lines = cv2.HoughLinesP(edges_image, 1, math.pi/180, threshold=40, minLineLength=image.shape[1]/2.6, maxLineGap=image.shape[1]/25)

    if lines is not None:
        list_angle = []
        for [[x1, y1, x2, y2]] in lines:
            a, b = re.linearEquation([x1, y1], [x2, y2])
            if a > 0:
                angle = math.atan(a) / math.pi * 180
            else:
                angle = -math.atan(-a) / math.pi * 180
            if abs(angle) <= 45:
                list_angle.append(angle)

        if not list_angle:
            return image
        
        angle = sum(list_angle) / len(list_angle)
        image = rotateByAngle(image, angle)

    return image