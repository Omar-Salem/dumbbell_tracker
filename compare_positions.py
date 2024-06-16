#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import cv2
from memberFinder import MemberFinder
from imageComparer import ImageComparer
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
cap = cv2.VideoCapture(video_path)
removedDumbellsNeedingMemberIdentification=[]
removedDumbells=[]
imageComparer=ImageComparer()

# Prepare:
# Get (x1,y1), (x2, y2) of each dumbell holder after removed from rack, as small as possible
# from https://www.mobilefish.com/services/record_mouse_coordinates/record_mouse_coordinates.php

def crop(image, d):
	return image[d.y1:d.y2, d.x1:d.x2]

def prepareDumbells(image):
	for d in dumbells:
		croppedImage = crop(image,d)
		cv2.imwrite(d.getEmptyTemplateFilePath(), croppedImage)
		# d.setCV2EmptyTemplateImage(image)
		d.setCV2EmptyTemplateImage(cv2.imread(d.getEmptyTemplateFilePath()))


prepareDumbells(cv2.imread('empty_rack.png',cv2.IMREAD_GRAYSCALE))

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
		searchArea = crop(frame,d)  # restrict search area

		removed=imageComparer.checkImagesSimilar(template,searchArea)

		if not removed and d.removed:
			# print('put back!!')
			secondsPassedSinceRemoval=(datetime.datetime.now()-d.removedOn).total_seconds()
			if secondsPassedSinceRemoval>1:
				d.removed=False
				d.holder=None
				d.removedOn=None
				removedDumbells.remove(d)
		if removed and not d.removed:
			# print('removed#####')
			d.removed=True
			d.removedOn=datetime.datetime.now()
			cv2.imwrite('removed.png', frame)
			# if not findPersonClosestToPoint(frame,d):
			# 	removedDumbellsNeedingMemberIdentification.append(d)
			removedDumbells.append(d)

cap.release()
cv2.destroyAllWindows()
