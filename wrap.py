import cv2, os
import numpy as np
import pyzbar.pyzbar as pyzbar
from matplotlib import pyplot as plt
import random
from readQR import *


img = cv2.imread('qr_Colour.png')
#img = cv2.imread('qr.png')
MAG = 30.0
PERIOD = 1.0
img = cv2.copyMakeBorder(
                 img, 
                 50, 
                 50, 
                 50, 
                 50, 
                 cv2.BORDER_CONSTANT, 
                 value=(255,255,255)
              )
rows, cols, depth = img.shape

#####################
# Concave effect

img_output = np.zeros(img.shape, dtype=img.dtype)

for i in range(rows):
    for j in range(cols):
        offset_x = int(MAG * math.sin(2 * 3.14 * i / (2*cols)))
        offset_y = 0
        if j+offset_x < cols:
            img_output[i,j] = img[i,(j+offset_x)%cols]
        else:
            img_output[i,j] = (255,255,255)

img_output = cv2.rotate(img_output, cv2.cv2.ROTATE_90_CLOCKWISE)  
#cv2.imshow('Concave', img_output)

img = cv2.imread('test3.png')
obj = decodeColourQR(img)
print(obj)
cv2.waitKey()

# #####################
# # Vertical wave

# img_output = 255-np.zeros(img.shape, dtype=img.dtype)

# for i in range(rows):
    # for j in range(cols):
        # offset_x = int(MAG * math.sin(PERIOD * 3.14 * i / 720))
        # offset_y = 0
        # if j+offset_x < rows:
            # img_output[i,j] = img[i,(j+offset_x)%cols]
        # else:
            # img_output[i,j] = (255,255,255)

# cv2.imshow('Input', img)
# cv2.imshow('Vertical wave', img_output)

# #####################
# # Horizontal wave

# img_output = np.zeros(img.shape, dtype=img.dtype)

# for i in range(rows):
    # for j in range(cols):
        # offset_x = 0
        # offset_y = int(MAG * math.sin(PERIOD * 3.14 * j / 720))
        # if i+offset_y < rows:
            # img_output[i,j] = img[(i+offset_y)%rows,j]
        # else:
            # img_output[i,j] = (255,255,255)

# cv2.imshow('Horizontal wave', img_output)

# #####################
# # Both horizontal and vertical 

# img_output = np.zeros(img.shape, dtype=img.dtype)

# for i in range(rows):
    # for j in range(cols):
        # offset_x = int(MAG * math.sin(2 * 3.14 * i / 180))
        # offset_y = int(MAG * math.cos(2 * 3.14 * j / 180))
        # if i+offset_y < rows and j+offset_x < cols:
            # img_output[i,j] = img[(i+offset_y)%rows,(j+offset_x)%cols]
        # else:
            # img_output[i,j] = (255,255,255)

# cv2.imshow('Multidirectional wave', img_output)

