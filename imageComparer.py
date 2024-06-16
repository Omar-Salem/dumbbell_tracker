import cv2
import numpy as np
        
class ImageComparer(object):
    
    def __init__(self):
        self.minimum_commutative_image_diff = 1
    
    def checkImagesSimilar(self,image1, image2):
        # hash0 = imagehash.average_hash(pilImg)
        # hash1 = imagehash.average_hash(Image.open('toBeCompared.jpeg'))
        # cutoff = 5  # Can be changed according to what works best for your images
        # diff=255 - cv2.absdiff(image1, image2)
        # print(diff)
        # return diff>1
        commutative_image_diff = self.get_contour_difference(image1 , image2 )
        print(commutative_image_diff)
        # if commutative_image_diff < self.minimum_commutative_image_diff:
        #     return True
        return commutative_image_diff<1
    
    @staticmethod
    def get_contour_difference(image_1, image_2):
        image_1=cv2.cvtColor(image_1, cv2.COLOR_BGR2GRAY)
        image_2=cv2.cvtColor(image_2, cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(image_1, 127, 255,0)
        ret, thresh2 = cv2.threshold(image_2, 127, 255,0)

        contours,hierarchy = cv2.findContours(thresh,2,1)
        cnt1 = contours[0]

        contours,hierarchy = cv2.findContours(thresh2,2,1)
        cnt2 = contours[0]
        
        return cv2.matchShapes(cnt1,cnt2,1,0.0)