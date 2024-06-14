import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image

class Dumbell:
	def __init__(self,weight, x1,y1,x2, y2):
		self.weight = weight
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.emptyTemplateImage=None

	def getCV2EmptyTemplateImage(self):
		return self.emptyTemplateImage

	def setCV2EmptyTemplateImage(self, cv2Image):
		self.emptyTemplateImage=cv2Image

	def getEmptyTemplateFilePath(self):
		return '{}Ks_{}.png'.format(self.weight,self.x1)

# PREPARE:
# https://ezgif.com/video-to-jpg
# Get (x1,y1), (x2, y2) of each dumbell manually 
# from https://www.mobilefish.com/services/record_mouse_coordinates/record_mouse_coordinates.php

dumbells = [
Dumbell(5,202,426,249,482)
]

# fullRack = cv2.imread('full.png')
for d in dumbells:
  # Get image of each dumbell after removed from rack
	im = Image.open('empty.png').convert('L')
	im = im.crop(( d.x1,  d.y1,  d.x2, d.y2))
	im.save(d.getEmptyTemplateFilePath())
	d.setCV2EmptyTemplateImage(cv2.imread(d.getEmptyTemplateFilePath()))

video_path = "v.mp4"
matchTemplateThreshole=0.9
cap = cv2.VideoCapture(video_path)
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()
    if not success:
        break
    for d in dumbells:
    	template=d.getCV2EmptyTemplateImage()
    	w, h = template.shape[:-1] 
    	searchArea = frame[d.y1:d.y2,d.x1:d.x2] # restrict search area
    	res = cv2.matchTemplate(searchArea, template, cv2.TM_CCOEFF_NORMED)

    	loc = np.where(res >= matchTemplateThreshole)
    	for pt in zip(*loc[::-1]):  # Switch columns and rows
    		cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
		cv2.imwrite('result.png', frame)



# for each coordinate, get cropped of present and missing, get size of present

# TRACK
# Taken-> for each coordinate, check if dumbell 'missing' exists in 
# 		  corresponding (x1,y1), (x2, y2), i.e: crop and cv2.matchTemplate
# Putback->for each missing coordinate, check if size is the same

# x1=202
# y1=426
# x2=249
# y2=482
# cv2.rectangle(image, (x1,y1), (x2, y2), (0,0,255), 5)

# cv2.imwrite('result.png', image)





# same one return->in step 1, check size of ??? 