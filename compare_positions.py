#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image
from memberFinder import MemberFinder


class Dumbell:

	def __init__(
		self,
		weight,
		x1,
		y1,
		x2,
		y2,
		):

		self.weight = weight
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.emptyTemplateImage = None
		self.removed = False
		self.holder = None

	def getCV2EmptyTemplateImage(self):
		return self.emptyTemplateImage

	def setCV2EmptyTemplateImage(self, cv2Image):
		self.emptyTemplateImage = cv2Image

	def getEmptyTemplateFilePath(self):
		return '{}Ks_{}.png'.format(self.weight, self.x1)


# PREPARE:
# https://ezgif.com/video-to-jpg
# Get (x1,y1), (x2, y2) of each dumbell manually
# from https://www.mobilefish.com/services/record_mouse_coordinates/record_mouse_coordinates.php

dumbells = [Dumbell(5, 202, 426, 249, 482)]

memberFinder=MemberFinder()
# fullRack = cv2.imread('full.png')


# Get image of each dumbell after removed from rack
for d in dumbells:

	im = Image.open('empty.png').convert('L')
	im = im.crop((d.x1, d.y1, d.x2, d.y2))
	im.save(d.getEmptyTemplateFilePath())
	d.setCV2EmptyTemplateImage(cv2.imread(d.getEmptyTemplateFilePath()))

video_path = 'v.mp4'
matchTemplateThreshold = 0.9
cap = cv2.VideoCapture(video_path)
while cap.isOpened():

	# Read a frame from the video

	(success, frame) = cap.read()

	if cv2.waitKey(10) & 0xFF == ord('q'):
		break

	if not success:
		continue

	cv2.imshow('window-name', frame)

	for d in dumbells:
		template = d.getCV2EmptyTemplateImage()
		(w, h) = template.shape[:-1]
		searchArea = frame[d.y1:d.y2, d.x1:d.x2]  # restrict search area
		res = cv2.matchTemplate(searchArea, template,
								cv2.TM_CCOEFF_NORMED)
		removed = res >= matchTemplateThreshold

		if not removed and d.removed:
			print('put back!')
			d.removed=False
			d.holder=None
		if removed and not d.removed:
			d.removed=True
			holder=memberFinder.findPersonClosestToPoint(frame,[d.x1,d.y1])
			if holder is not None:
				d.holder=holder
				print('{} removed {}',format(d.holder,str(d.weight)))
			cv2.rectangle(frame, (d.x1,d.y1), (d.x2,d.y2), (0, 0,255), 2)
			cv2.imwrite('result.png', frame)

cap.release()
cv2.destroyAllWindows()
