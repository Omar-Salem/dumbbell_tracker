import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image

# PREPARE:
# Get (x1,y1), (x2, y2) of each dumbell manually 
# from https://www.mobilefish.com/services/record_mouse_coordinates/record_mouse_coordinates.php

# for each coordinate, get cropped of present and missing, get size of present

# TRACK
# Taken-> for each coordinate, check if dumbell 'missing' exists in 
# 		  corresponding (x1,y1), (x2, y2), i.e: crop and cv2.matchTemplate
# Putback->for each missing coordinate, check if size is the same
image = cv2.imread('image.png')
x1=202
y1=426
x2=249
y2=482
cv2.rectangle(image, (x1,y1), (x2, y2), (0,0,255), 5)

cv2.imwrite('result.png', image)


# Get (x1,y1), (x2, y2) of each dumbell after removed
im = Image.open('after.png').convert('L')
im = im.crop((x1, y1, x2, y2))
im.save('_0.png')


# same one return->in step 1, check size of ??? 