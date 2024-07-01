import cv2
from PIL import Image
from ultralytics import YOLO
import math
import sys 
import os
import numpy

class MemberFinder:
    def __init__(self):
        self.model = YOLO("resources/members/dataset/yolov8n-members.pt")

    def identify_member(self, frame:numpy.ndarray):
        resultsList = self.model.predict(source=frame, conf=0.7)
        if(len(resultsList)<1):
            return None
        result=resultsList[0]
        return list(result.names.values())[0]