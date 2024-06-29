import pathlib
import cv2
import numpy as np
from pathlib import Path

from src.image_comparer import ImageComparer

imageComparer=ImageComparer()
template = cv2.imread('dumbbells/empty/5Ks_226.png')


# full rack
for x in range(127):
    d='frames/frame{}.png'.format(x)
    print(d)
    test = cv2.imread(d)[441:452, 226:243]
    b=imageComparer.check_images_similar(template, test)
    if b:
        cv2.imwrite('negative matching failure_1.png', test)
        raise('negative matching failed')
    
# empty
for x in range(151,244):
    d='frames/frame{}.png'.format(x)
    print(d)
    test = cv2.imread(d)[441:452, 226:243]
    b=imageComparer.check_images_similar(template, test)
    if not b:
        cv2.imwrite('positive matching failure.png', test)
        raise('positive matching failed')

# put back
for x in range(245,322):
    d='frames/frame{}.png'.format(x)
    print(d)
    test = cv2.imread(d)[441:452, 226:243]
    b=imageComparer.check_images_similar(template, test)
    if b:
        cv2.imwrite('negative matching failure_2.png', test)
        raise('negative matching 2 failed')