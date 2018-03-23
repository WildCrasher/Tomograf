import numpy as np
import cv2
import math
import time

# interval - angle between detectors
# step - angle while model is moving on circle (alfa)

def runConeModel( N_detectors_and_emiters, interval, step, image):
    radius = calculateRadius(image)
    offset = round( radius ) - 1
    alfa = 90 #1
    interval_in_radians = math.pi / (180 / interval)
    detector_cords = []
	emiter_cords = []
    matrix = []

   # for i in range(int(360/step)):
    for i in range(10):
        alfa_in_radians = math.pi / (180 / alfa)
        xE = round(radius * math.cos(alfa_in_radians)) + offset
        yE = round(radius * math.sin(alfa_in_radians)) + offset
        for j in range(N_detectors_and_emiters):
            xD = round(radius * math.cos(alfa_in_radians + math.pi - interval_in_radians/2 + j*( interval_in_radians/(N_detectors_and_emiters-1))) ) + offset
            yD = round(radius * math.sin(alfa_in_radians + math.pi - interval_in_radians/2 + j*( interval_in_radians/(N_detectors_and_emiters-1))) ) + offset
            detector_cords.append( [ xD, yD] )
            image[xD][yD] = [50,80,200]

        image[xE][yE] = [120,120,120]
        new_row_in_matrix(xE, yE, detector_cords, matrix, image)

        detector_cords = []
        alfa = alfa + step

    cv2.imshow("changed", image)

def count_emiters_position():
	

def new_row_in_matrix(xE, yE, detector_cords, matrix, image):
    row = []
    for i in range(len(detector_cords)):
        row.append(0)
    #for i in range(100):
       # image[10][i] = [200,100,50]
    for i in range(len(detector_cords)):

        middle_point_between_two_points = [ ( xE + detector_cords[i][0] ) / 2, ( yE + detector_cords[i][1] ) / 2 ]
        print(abs(middle_point_between_two_points[1] / middle_point_between_two_points[0]))
        if abs(middle_point_between_two_points[1] / middle_point_between_two_points[0]) > 0.5:
            x1 = xE
            y1 = yE
            x2 = detector_cords[i][0]
            y2 = detector_cords[i][1]
            dx = x2 - x1
            dy = y2 - y1
            e = dx/2
            print("if")
            for j in range(dx):
                print("2if")
                row[i] = row[i] + 1#image[x1][y1]
                x1 = x1 + 1
                e = e - dy
                if e < 0:
                    y1 = y1 + 1
                    e = e + dx
                image[x1][y1] = [200,100,50]
    matrix.append(row)

def calculateRadius(image):
    height, width, idontcare = image.shape
    if height > width:
        return width / 2
    else:
        return height / 2



imgOriginal = cv2.imread("Foto/Kolo.jpg")
#cv2.imshow("First image",imgOriginal)
runConeModel(5, 10, 20, imgOriginal)

cv2.waitKey(0)
