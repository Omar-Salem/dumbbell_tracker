#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import datetime

from dumbbell import Dumbbell
from imageService import ImageService
from memberFinder import MemberFinder


def find_person_closest_to_point(current_frame, r):
    holder = memberFinder.findPersonClosestToPoint(current_frame, [r.x1, r.y1])
    if holder is not None and r in removedDumbellsNeedingMemberIdentification:
        removedDumbellsNeedingMemberIdentification.remove(r)
        r.holder = holder
        return True
    return False

dumbbells = [Dumbbell(5, 226, 441, 243, 452)]
memberFinder = MemberFinder()
video_path = 'v.mp4'
cap = cv2.VideoCapture(video_path)
removedDumbellsNeedingMemberIdentification = []
removedDumbells = []
imageComparer = ImageService()


def crop(image, d):
    return image[d.y1:d.y2, d.x1:d.x2]


def prepare_dumbbells():
    '''
    Get (x1,y1), (x2, y2) of each dumbbell holder from an image of the empty rack, as small as possible
    https://www.mobilefish.com/services/record_mouse_coordinates/record_mouse_coordinates.php
    '''
    image = cv2.imread('frames/frame175.png', cv2.IMREAD_GRAYSCALE)
    for d in dumbbells:
        cropped_image = crop(image, d)
        cv2.imwrite(d.get_empty_template_file_path(), cropped_image)
        d.set_cv2_empty_template_image(cv2.imread(d.get_empty_template_file_path()))


prepare_dumbbells()

while cap.isOpened():

    (success, frame) = cap.read()

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

    for d in removedDumbells:
        cv2.rectangle(frame, (d.x1, d.y1), (d.x2, d.y2), (0, 0, 255), 2)
        cv2.putText(frame, '{} {}'.format(d.holder, d.weight), (d.x1, d.y1), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('gym', frame)

    for r in removedDumbellsNeedingMemberIdentification:
        find_person_closest_to_point(frame, r)

    for d in dumbbells:
        template = d.get_cv2_empty_template_image()
        searchArea = crop(frame, d)  # restrict search area

        removed = imageComparer.check_images_similar(template, searchArea)

        if not removed and d.removed:
            # print('put back!!')
            secondsPassedSinceRemoval = (datetime.datetime.now() - d.removedOn).total_seconds()
            if secondsPassedSinceRemoval > 1:
                d.removed = False
                d.holder = None
                d.removedOn = None
                removedDumbells.remove(d)
        if removed and not d.removed:
            # print('removed#####')
            d.removed = True
            d.removedOn = datetime.datetime.now()
            cv2.imwrite('removed.png', frame)
            # if not findPersonClosestToPoint(frame,d):
            # 	removedDumbellsNeedingMemberIdentification.append(d)
            removedDumbells.append(d)

cap.release()
cv2.destroyAllWindows()
