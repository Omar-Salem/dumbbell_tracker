import pathlib
import cv2
import numpy as np
from pathlib import Path

idx=0
for x in range(131,242):
    idx+=1
    d='frames/frame{}.png'.format(x)
    print(d)
    img = cv2.imread(d)[441:452, 226:243]
    if idx == 1:
        first_img = img
        continue
    else:
        second_img = img
        second_weight = 1/(idx+1)
        first_weight = 1 - second_weight
        first_img = cv2.addWeighted(first_img, first_weight, second_img, second_weight, 0)

cv2.imwrite('average.png', first_img)