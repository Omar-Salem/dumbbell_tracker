import cv2
from ultralytics import YOLO
import os
import shutil
import random
from pathlib import Path

class Coords:
    def __init__(
            self,
            x,
            y,
            w,
            h,
    ):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

def __extract_coords(box):
    xywhn=box.xywhn[0]
    return Coords(float(xywhn[0].item()),float(xywhn[1].item()),float(xywhn[2].item()),float(xywhn[3].item()))


# TODO:get dynamically
video_path = '../resources/members/Omar Salem.mov'
member_name='Omar Salem'
clazz=0

dataset_dir = '../resources/members/dataset'
test_dir = os.path.join(dataset_dir, 'test')
train_dir = os.path.join(dataset_dir, 'train')
valid_dir = os.path.join(dataset_dir, 'valid')

random.seed(42)
train_ratio = 0.80
# val_ratio = 0.10
# test_ratio = 0.10

cap = cv2.VideoCapture(video_path)
model = YOLO("../resources/yolov8n-face.pt")
face_prediction_conf=0.6
frame_count=-1
while cap.isOpened():

    (success, frame) = cap.read()

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

    if frame is None:
        break

    frame_count+=1

    results = model.predict(source=frame, conf=face_prediction_conf)
    if(len(results)<1):
        continue
        # raise Exception("prediction failed")
    faces=results[0].boxes
    if(len(faces)!=1):
        continue
        # raise Exception("exactly 1 face needed")
    
    coords=__extract_coords(faces[0])
    p=random.randrange(0,2)
    is_train=p<=train_ratio
    is_valid=p>train_ratio and p<=0.90
    is_test=p>0.90 and p<=1.0
    dir=''
    if(is_train):
        dir=train_dir
    elif(is_valid):
        dir=valid_dir
    elif(is_test):
        dir=test_dir
    
    images_dir = os.path.join(dir, 'images')
    image_file_path=os.path.join(images_dir, str(frame_count)+'.png')
    cv2.imwrite(image_file_path, frame)

    labels_dir = os.path.join(dir, 'labels')
    label_file_path=os.path.join(labels_dir, str(frame_count)+'.txt')
    f = open(label_file_path, "w")
    f.write("{} {} {} {} {}".format(clazz,coords.x,coords.y,coords.w,coords.h))
    f.close()

# Load a model
# model = YOLO("yolov8n.yaml")  # build a new model from YAML
model = YOLO(os.path.join(dataset_dir, 'weights.pt'))  # load a pretrained model (recommended for training)
# model = YOLO("yolov8n.yaml").load("yolov8n.pt")  # build from YAML and transfer weights

# Train the model
results = model.train(data=os.path.join(dataset_dir, 'data.yaml'), epochs=3)
