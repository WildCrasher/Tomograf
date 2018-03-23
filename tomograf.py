import numpy as np
import cv2
import math
import time

# interval - angle between detectors
# step - angle while model is moving on circle (alfa)

imgOriginal = cv2.imread("Foto/Kolo.jpg")
image_height, image_width, idontcare = imgOriginal.shape

def runParallelModel(N_detectors_and_emiters, interval, step):
    image = imgOriginal
    radius = calculateRadius() - 1
    offset = round(radius)
    alfa = 90  # 1
    interval_in_radians = math.pi / (180 / interval)
    detector_cords = []
    emiter_cords = []
    matrix = []
    #for i in range(4):
    #(int(360/step))
    for i in range(int(360/step)):
        alfa_in_radians = math.pi / (180 / alfa)
        count_emiters_and_detectors_position(emiter_cords, detector_cords, radius, interval_in_radians, alfa_in_radians, N_detectors_and_emiters, offset)
        change_image(image, emiter_cords, [120, 120, 120])
        change_image(image, detector_cords, [50, 100, 220])
        new_row_in_matrix(emiter_cords, detector_cords, matrix, image, N_detectors_and_emiters)
        detector_cords = []
        emiter_cords = []
        alfa = alfa + step
    normalize_each_element(matrix, N_detectors_and_emiters)

    cv2.imshow("changed", image)
    #cv2.waitKey(0)
    #cv2.imshow("sinogram", np.array(matrix))


def count_emiters_and_detectors_position(emiter_cords, detector_cords, radius, interval_in_radians, alfa_in_radians, N_detectors_and_emiters, offset):
    for i in range(N_detectors_and_emiters):
        xEmiter = round(radius * math.cos(alfa_in_radians + math.pi - interval_in_radians / 2 + i * (interval_in_radians / (N_detectors_and_emiters - 1)))) + offset
        yEmiter = round(radius * math.sin(alfa_in_radians + math.pi - interval_in_radians / 2 + i * (interval_in_radians / (N_detectors_and_emiters - 1)))) + offset
        xDetector = round(radius * math.cos(alfa_in_radians - interval_in_radians / 2 + i * (interval_in_radians / (N_detectors_and_emiters - 1)))) + offset
        yDetector = round(radius * math.sin(alfa_in_radians - interval_in_radians / 2 + i * (interval_in_radians / (N_detectors_and_emiters - 1)))) + offset
        emiter_cords.append([xEmiter, yEmiter])
        detector_cords.append([xDetector, yDetector])

def new_row_in_matrix(emiter_cords, detector_cords, matrix, image, N_detectors_and_emiters):
    row = []
    for i in range(N_detectors_and_emiters):
        row.append([0, 0, 0])

    for i in range(N_detectors_and_emiters):
        x1 = emiter_cords[i][0]
        x2 = detector_cords[N_detectors_and_emiters - 1 - i][0]
        y1 = emiter_cords[i][1]
        y2 = detector_cords[N_detectors_and_emiters - 1 - i][1]
        x_actual = x1
        y_actual = y1

        if (x1 < x2):
            x_direction = 1
            dx = x2 - x1
        else:
            x_direction = -1
            dx = x1 - x2
        if (y1 < y2):
            y_direction = 1
            dy = y2 - y1
        else:
            y_direction = -1
            dy = y1 - y2
        #image[y_actual, x_actual] = [200, 100, 50]
        row[i] = increment_value_in_row(row[i], image[y_actual, x_actual])
        if (dx > dy):
            a = (dy - dx) * 2
            b = dy * 2
            e = b - dx
            while( x_actual != x2):
                if (e >= 0):
                    x_actual += x_direction
                    y_actual += y_direction
                    e += a
                else:
                    e += b
                    x_actual += x_direction
                row[i] = increment_value_in_row(row[i], image[y_actual, x_actual])
                #image[y_actual, x_actual] = [200, 100, 50]

        else:
            a = (dx - dy) * 2
            b = dx * 2
            e = b - dy
            while y_actual != y2:
                if (e >= 0):
                    x_actual += x_direction
                    y_actual += y_direction
                    e += a
                else:
                    e += b
                    y_actual += y_direction
                row[i] = increment_value_in_row(row[i], image[y_actual, x_actual])
                #image[y_actual, x_actual] = [200, 100, 50]
    matrix.append(row)

#image cords in cv2 are swaped cv2image[y, x]
def change_image(image, emiter_cords, rgb):
    for cords in emiter_cords:
        image[cords[1]][cords[0]] = rgb

def calculateRadius():
    if image_height > image_width:
        return image_width / 2
    else:
        return round(image_height) / 2

def increment_value_in_row( row, value ):
    lists_of_lists = [row, value]
    result = [sum(x) for x in zip(*lists_of_lists)]
    return result

def normalize_each_element( matrix, N_detectors_and_emiters ):
    normalize_value = 255
    rgb = 3
    for x in range(len(matrix)):
        for y in range(N_detectors_and_emiters):
            for z in range(rgb):
                matrix[x][y][z] = int(round(matrix[x][y][z]/ normalize_value))
    return matrix



#N_detectors_and_emiters, interval, step
runParallelModel(5, 10, 2)

cv2.waitKey(0)
