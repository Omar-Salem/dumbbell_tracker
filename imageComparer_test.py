import pathlib
import cv2
import numpy as np
from pathlib import Path

from imageService import ImageService

imageComparer=ImageService()
template = cv2.imread('dumbbells/empty/5Ks_226.png')
# template = cv2.imread('average.png')


# full rack
for x in range(126):
    d='frames/frame{}.png'.format(x)
    print(d)
    test = cv2.imread(d)[441:452, 226:243]
    b=imageComparer.check_images_similar(template, test)
    if b:
        cv2.imwrite('negative matching failure_1.png', test)
        raise('negative matching failed')
    
# empty
for x in range(151,242):
    d='frames/frame{}.png'.format(x)
    print(d)
    test = cv2.imread(d)[441:452, 226:243]
    b=imageComparer.check_images_similar(template, test)
    if not b:
        cv2.imwrite('positive matching failure.png', test)
        raise('positive matching failed')

# put back
# for x in range(243,322):
#     d='frames/frame{}.png'.format(x)
#     print(d)
#     test = cv2.imread(d)[441:452, 226:243]
#     b=imageComparer.check_images_similar(template, test)
#     if b:
#         cv2.imwrite('negative matching failure_2.png', test)
#         raise('negative matching failed')