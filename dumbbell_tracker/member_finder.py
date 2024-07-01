import cv2
from PIL import Image
from ultralytics import YOLO
import math
import sys 
import os
import numpy

class MemberFinder:
    def __init__(self):
        self.model = YOLO("../resources/members/dataset/yolov8n-members.pt")

    def __extractXY(self,b):
        xyxy=b.xyxy[0]
        return int(xyxy[0].item()),int(xyxy[1].item()),int(xyxy[2].item()),int(xyxy[3].item())

    def find_person_closest_to_point(self, frame:numpy.ndarray, q:list):
        resultsList = self.model.predict(source=frame, conf=0.7)  # Display preds. Accepts all YOLO predict arguments
        if(len(resultsList)<1):
            return None
        result=resultsList[0]
        return list(result.names.values())[0]
        print()
        persons=result.boxes
        if(len(persons)<1):
            return None
        coords=map(self.__extractXY, persons)
        
        if(len(coords)<1):
            return None
        
        print(coords)
        c=coords[0]
        # cv2.rectangle(frame, (235, 0), (302, 89), (0, 0,255), 2)
        # cv2.rectangle(frame, (435, 226), (461, 264), (0, 0,255), 2)
        cv2.rectangle(frame, (c[0],c[1]), (c[2],c[3]), (0, 0,255), 2)
        cv2.imwrite('coords.png', frame)


        # print(math.dist((235, 0), (302, 89)))
        # print(math.dist((435, 226), (461, 264)))
        # print(math.dist((390, 215), (414, 246)))
        minDistance=sys.maxsize
        xyxy=None
        for c in coords:
            x1=c[0]
            y1=c[1]
            d=math.dist([x1,y1], q)
            if minDistance>d:
                minDistance=d
                xyxy=c
                # print('ddddddddddddd')
                # print(xyxy)
        
        x1=xyxy[0]
        y1=xyxy[1]

        x2=xyxy[2]
        y2=xyxy[3]

        cropped = frame[y1:y2, x1:x2]
        return self.__identify__(cropped)