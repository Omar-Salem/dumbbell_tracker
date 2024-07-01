import pathlib
import cv2
import numpy as np
from pathlib import Path
import unittest

from dumbbell_tracker.image_comparer import ImageComparer

target=ImageComparer()
empty = cv2.imread('resources/empty.png')

class ImageComparerTest(unittest.TestCase):
	def member_identified(self):
          for x in range(127):
            d='resources/frames/frame{}.png'.format(x)
            print(d)
            test = cv2.imread(d)[441:452, 226:243]
            b=target.calculate_images_similarity_score(empty, test)
            self.assertTrue(b<0.5)

if __name__ == "__main__":
	unittest.main()


# full rack
for x in range(127):
    d='frames/frame{}.png'.format(x)
    print(d)
    test = cv2.imread(d)[441:452, 226:243]
    b=target.calculate_images_similarity_score(empty, test)
    if b>0.5:
        cv2.imwrite('negative matching failure_1.png', test)
        raise('negative matching 1 failed')
    
# empty
for x in range(151,244):
    d='frames/frame{}.png'.format(x)
    print(d)
    test = cv2.imread(d)[441:452, 226:243]
    b=target.calculate_images_similarity_score(empty, test)
    if not b:
        cv2.imwrite('positive matching failure.png', test)
        raise('positive matching failed')

# put back
for x in range(245,322):
    d='frames/frame{}.png'.format(x)
    print(d)
    test = cv2.imread(d)[441:452, 226:243]
    b=target.calculate_images_similarity_score(empty, test)
    if b:
        cv2.imwrite('negative matching failure_2.png', test)
        raise('negative matching 2 failed')