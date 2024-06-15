#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import cv2
from memberFinder import MemberFinder
import threading
import datetime


def findPersonClosestToPoint(frame,r):
	holder=memberFinder.findPersonClosestToPoint(frame,[r.x1,r.y1])
	if holder is not None and r in removedDumbellsNeedingMemberIdentification:
		removedDumbellsNeedingMemberIdentification.remove(r)
		r.holder=holder
		return True
	return False

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
		self.removedOn = None
		self.holder = None

	def getCV2EmptyTemplateImage(self):
		return self.emptyTemplateImage

	def setCV2EmptyTemplateImage(self, cv2Image):
		self.emptyTemplateImage = cv2Image

	def getEmptyTemplateFilePath(self):
		return 'dumbells/empty/{}Ks_{}.png'.format(self.weight, self.x1)



dumbells = [Dumbell(5, 226, 441, 243, 452)]

memberFinder=MemberFinder()
video_path = 'v.mp4'
matchTemplateThreshold = 0.6
cap = cv2.VideoCapture(video_path)
removedDumbellsNeedingMemberIdentification=[]
removedDumbells=[]


# Prepare offline:
# https://ezgif.com/video-to-jpg
# Get (x1,y1), (x2, y2) of each dumbell holder after removed from rack, as small as possible
# from https://www.mobilefish.com/services/record_mouse_coordinates/record_mouse_coordinates.php


#bonus, get image of each dumbell on full rack to track individual weights
# fullRack = cv2.imread('full_rack.png')


for d in dumbells:
	image = cv2.imread('empty_rack.png')
	# Grayscale 
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
	image = image[d.y1:d.y2,d.x1:d.x2]
	cv2.imwrite(d.getEmptyTemplateFilePath(), image)
	d.setCV2EmptyTemplateImage(cv2.imread(d.getEmptyTemplateFilePath()))


while cap.isOpened():

	(success, frame) = cap.read()

	if cv2.waitKey(10) & 0xFF == ord('q'):
		break

	for d in removedDumbells:
		cv2.rectangle(frame, (d.x1,d.y1), (d.x2,d.y2), (0, 0,255), 2)
		cv2.putText(frame, '{} {}'.format(d.holder,d.weight), (d.x1,d.y1), cv2.FONT_HERSHEY_SIMPLEX ,  
				   1, (255, 255, 255) , 2, cv2.LINE_AA) 
	
	cv2.imshow('gym', frame)

	for r in removedDumbellsNeedingMemberIdentification:
		findPersonClosestToPoint(frame,r)

	for d in dumbells:
		template = d.getCV2EmptyTemplateImage()
		(w, h) = template.shape[:-1]
		searchArea = frame[d.y1:d.y2, d.x1:d.x2]  # restrict search area
		# searchArea = cv2.cvtColor(searchArea, cv2.COLOR_BGR2GRAY) 
		res = cv2.matchTemplate(searchArea, template,
								cv2.TM_CCOEFF_NORMED)
		# print(res)
		removed = res >= matchTemplateThreshold

		if not removed and d.removed:
			secondsPassedSinceRemoval=(datetime.datetime.now()-d.removedOn).total_seconds()
			if secondsPassedSinceRemoval>1:
				d.removed=False
				d.holder=None
				d.removedOn=None
				removedDumbells.remove(d)
		if removed and not d.removed:
			print('removed')
			d.removed=True
			d.removedOn=datetime.datetime.now()
			cv2.imwrite('result.png', frame)
			if not findPersonClosestToPoint(frame,d):
				removedDumbellsNeedingMemberIdentification.append(d)
			removedDumbells.append(d)

cap.release()
cv2.destroyAllWindows()
