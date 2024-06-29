#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import datetime
from dumbbell import Dumbbell
import time
# from member_finder import MemberFinder

'''
Get (x1,y1), (x2, y2) of each dumbbell from an image of the full rack
https://www.mobilefish.com/services/record_mouse_coordinates/record_mouse_coordinates.php
'''
dumbbells = [Dumbbell(5, 226, 441, 243, 452)]
# dumbbells = [Dumbbell(5, 200, 423, 255, 481)]
# member_finder = MemberFinder()
video_path = '../resources/v.mp4'
cap = cv2.VideoCapture(video_path)
removed_dumbells = []


def set_dumbbells_empty_templates():
    empty_rack = cv2.imread('../resources/empty_rack.png', cv2.IMREAD_GRAYSCALE)
    for d in dumbbells:
        d.set_holder_template(empty_rack)


set_dumbbells_empty_templates()
init = False
while cap.isOpened():

    (success, frame) = cap.read()

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

    if not init:
        init=True
        for d in dumbbells:
            d.set_dumbbell_image(frame)

    # results = model.predict(source=frame, conf=0.3, iou=0.5)
    # print( member_finder.find_person_closest_to_point(frame,None))
        # cv2.rectangle(frame, (d.x1, d.y1), (d.x2, d.y2), (0, 0, 255), 2)

    for d in dumbbells:
        if d.check_removed(frame):
            print('removed')
            # cv2.imwrite('picked_up.png',frame)
            d.remove()
            removed_dumbells.append(d)
        elif d.check_put_back(frame):
            print('put_back')
            # d.put_back(frame) #TODO take frame later, otherwise hand is shown!
            if d in removed_dumbells:
                removed_dumbells.remove(d)

    for d in removed_dumbells:
        cv2.rectangle(frame, (d.x1, d.y1), (d.x2, d.y2), (0, 0, 255), 2)
        cv2.putText(frame, d.get_label(), (d.x1, d.y1), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('gym', frame)
    time.sleep(0.0625)
cap.release()
cv2.destroyAllWindows()
