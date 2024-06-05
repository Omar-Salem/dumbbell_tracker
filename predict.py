import cv2
from PIL import Image
from ultralytics import YOLO
import math
import sys 
from deepface import DeepFace
import os

def extractXY(b):
    xyxy=b.xyxy[0]
    return xyxy[0].item(),xyxy[1].item(),xyxy[2].item(),xyxy[3].item()

kwargs={"conf":.5}
model = YOLO("yolov8n.pt")
# accepts all formats - image/dir/Path/URL/video/PIL/ndarray. 0 for webcam
results = model.predict(source="us_.jpg", **kwargs)  # Display preds. Accepts all YOLO predict arguments


boxes=results[0].boxes
persons=[b for b in boxes if b.cls.item()==0]
coords=map(extractXY, persons)
minDistance=sys.maxsize
xyxy=None
q=[785.1337890625, 481.4678039550781] #TODO CHANGE THIS!
frame=Image.open('us_.jpg')           #TODO CHANGE THIS!
for c in coords:
    x1=c[0]
    y1=c[1]
    d=math.dist([x1,y1], q)
    if d<minDistance:
        minDistance=d
        xyxy=c
print(xyxy)
frame = frame.crop(xyxy)
frame.save('_0.png')
# frame = "test.jpg"
backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']
db_path="db"
result = DeepFace.find(img_path = '_0.png', db_path = db_path, detector_backend=backends[2])
for row in result:
    identity = row["identity"][0]
    fileNameWithExtensions=os.path.basename(identity)
    personName=os.path.splitext(fileNameWithExtensions)[0]
    print(personName)