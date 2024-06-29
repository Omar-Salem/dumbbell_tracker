#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import datetime
from dumbbell import Dumbbell
from member_finder import MemberFinder
from ultralytics import YOLO




'''
Get (x1,y1), (x2, y2) of each dumbbell holder from an image of the empty rack, as small as possible
https://www.mobilefish.com/services/record_mouse_coordinates/record_mouse_coordinates.php
'''
dumbbells = [Dumbbell(5, 226, 441, 243, 452)]
member_finder = MemberFinder()
video_path = 'v.mp4'
cap = cv2.VideoCapture(video_path)
removed_dumbells = []


def crop(image, d):
    return image[d.y1:d.y2, d.x1:d.x2]


def prepare_dumbbells():
    image = cv2.imread('frames/frame175.png', cv2.IMREAD_GRAYSCALE)
    for d in dumbbells:
        cropped_image = crop(image, d)
        cv2.imwrite(d.get_empty_template_file_path(), cropped_image)
        d.set_cv2_empty_template_image(cv2.imread(d.get_empty_template_file_path()))


prepare_dumbbells()
model = YOLO("yolov8n-face.pt")
while cap.isOpened():

    (success, frame) = cap.read()

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

    # results = model.predict(source=frame, conf=0.3, iou=0.5)
    # print( member_finder.find_person_closest_to_point(frame,None))
        # cv2.rectangle(frame, (d.x1, d.y1), (d.x2, d.y2), (0, 0, 255), 2)
    for d in removed_dumbells:
        cv2.rectangle(frame, (d.x1, d.y1), (d.x2, d.y2), (0, 0, 255), 2)
        cv2.putText(frame, d.get_label(), (d.x1, d.y1), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('gym', frame)

    for d in dumbbells:
        if d.check_put_back(frame):
            d.put_back()
            removed_dumbells.remove(d)
        elif d.check_picked_up(frame):
            d.pick_up()
            removed_dumbells.append(d)

cap.release()
cv2.destroyAllWindows()
