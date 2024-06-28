#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import datetime
from dumbbell import Dumbbell
from imageService import ImageService
from memberFinder import MemberFinder


def find_person_closest_to_point(current_frame, r):
    holder = memberFinder.findPersonClosestToPoint(current_frame, [r.x1, r.y1])
    if holder is not None and r in removed_dumbells_needing_member_identification:
        removed_dumbells_needing_member_identification.remove(r)
        r.holder = holder
        return True
    return False

dumbbells = [Dumbbell(5, 226, 441, 243, 452)]
memberFinder = MemberFinder()
video_path = 'v.mp4'
cap = cv2.VideoCapture(video_path)
removed_dumbells_needing_member_identification = []
removed_dumbells = []
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

    for d in removed_dumbells:
        cv2.rectangle(frame, (d.x1, d.y1), (d.x2, d.y2), (0, 0, 255), 2)
        cv2.putText(frame, '{} {}'.format(d.holder, d.weight), (d.x1, d.y1), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('gym', frame)

    for r in removed_dumbells_needing_member_identification:
        find_person_closest_to_point(frame, r)

    for d in dumbbells:
        empty_holder_template = d.get_cv2_empty_template_image()
        search_area = crop(frame, d)  # restrict search area

        empty_holder_visible = imageComparer.check_images_similar(empty_holder_template, search_area)

        if not empty_holder_visible and d.removed:
            d.put_back()
            # print('put back!!')
            # if seconds_passed_since_removal > 1:
            removed_dumbells.remove(d)
        if empty_holder_visible and not d.removed:
            d.pick_up()
            cv2.imwrite('removed.png', frame)
            # if not findPersonClosestToPoint(frame,d):
            # 	removedDumbellsNeedingMemberIdentification.append(d)
            removed_dumbells.append(d)

cap.release()
cv2.destroyAllWindows()
