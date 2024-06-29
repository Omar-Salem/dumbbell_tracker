from skimage.metrics import structural_similarity
import cv2
import numpy as np
        
class ImageComparer(object):
    
    def __init__(self):
        self.minimum_commutative_image_diff = 1

    def check_images_similar(self, image1, image2):
        image_1=cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        image_2=cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

        # Compute SSIM between two images
        (score, diff) = structural_similarity(image_1, image_2, full=True)
        # print(score)
        return score>0.8