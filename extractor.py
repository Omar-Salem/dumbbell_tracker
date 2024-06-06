import cv2
from PIL import Image
from ultralytics import YOLO
import math
import sys 
from deepface import DeepFace
import os
import numpy

class Extractor:
    def __init__(self):
        self.kwargs={"conf":.5}
        self.model = YOLO("yolov8n.pt")

        self.backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']
        self.db_path="db"

    def __extractXY__(self,b):
        xyxy=b.xyxy[0]
        return int(xyxy[0].item()),int(xyxy[1].item()),int(xyxy[2].item()),int(xyxy[3].item())
    
    def __identify__(self,frame):
        result = DeepFace.find(img_path = frame, db_path = self.db_path, detector_backend=self.backends[2])
        for row in result:
            identity = row["identity"][0]
            fileNameWithExtensions=os.path.basename(identity)
            personName=os.path.splitext(fileNameWithExtensions)[0]
            return

    def findPersonClosestToPoint(self, frame:numpy.ndarray, q:list):
        results = self.model.predict(source=frame, **self.kwargs)  # Display preds. Accepts all YOLO predict arguments
        boxes=results[0].boxes
        persons=[b for b in boxes if b.cls.item()==0]
        coords=map(self.__extractXY__, persons)
        minDistance=sys.maxsize
        xyxy=None
        for c in coords:
            x1=c[0]
            y1=c[1]
            d=math.dist([x1,y1], q)
            if minDistance>d:
                minDistance=d
                xyxy=c
        
        x1=xyxy[0]
        y1=xyxy[1]

        x2=xyxy[2]
        y2=xyxy[3]

        cropped = frame[y1:y2, x1:x2]
        return self.__identify__(cropped)