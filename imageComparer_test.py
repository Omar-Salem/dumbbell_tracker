import pathlib
import cv2
import numpy as np
from pathlib import Path

from imageComparer import ImageComparer

imageComparer=ImageComparer()
template = cv2.imread('dumbells/empty/5Ks_226.png')


# original
for x in range(126):
    d='frames/frame{}.png'.format(x)
    print(d)
    test = cv2.imread(d)[441:452, 226:243]
    b=imageComparer.checkImagesSimilar(template,test)
    if b:
        cv2.imwrite('XXXXXXXXXXXXXXXXXXXXXXXX.png', test)
        raise('negative matching failed')
    
# picked up
for x in range(131,242):
    d='frames/frame{}.png'.format(x)
    print(d)
    test = cv2.imread(d)[441:452, 226:243]
    b=imageComparer.checkImagesSimilar(template,test)
    if not b:
        cv2.imwrite('YYYYYYYYYYYYYYYYYY.png', test)
        raise('positive matching failed')

# put back
for x in range(243,322):
    d='frames/frame{}.png'.format(x)
    print(d)
    test = cv2.imread(d)[441:452, 226:243]
    b=imageComparer.checkImagesSimilar(template,test)
    if b:
        raise('negative matching failed')