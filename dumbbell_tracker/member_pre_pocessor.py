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
val_ratio = 0.10
face_prediction_conf=0.6

def get_set_dir():
    p=random.randrange(0,2)
    is_train=p<=train_ratio
    is_valid=p>train_ratio and p<=train_ratio+val_ratio
    is_test=p>train_ratio+val_ratio
    if(is_train):
        return train_dir
    if(is_valid):
        return valid_dir
    if(is_test):
        return test_dir

def write_image(dir,frame,frame_count):
    images_dir = os.path.join(dir, 'images')
    image_file_path=os.path.join(images_dir, str(frame_count)+'.png')
    cv2.imwrite(image_file_path, frame)

def write_label(dir,coords,frame_count):  
        labels_dir = os.path.join(dir, 'labels')
        label_file_path=os.path.join(labels_dir, str(frame_count)+'.txt')
        f = open(label_file_path, "w")
        f.write("{} {} {} {} {}".format(clazz,coords.x,coords.y,coords.w,coords.h))
        f.close()

def build_dataset():
    cap = cv2.VideoCapture(video_path)
    face_detection_model = YOLO("../resources/yolov8n-face.pt")
    frame_count=-1
    while cap.isOpened():

        (success, frame) = cap.read()

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

        if frame is None:
            break

        frame_count+=1

        results = face_detection_model.predict(source=frame, conf=face_prediction_conf)
        if(len(results)<1):
            continue
            # raise Exception("prediction failed")
        faces=results[0].boxes
        if(len(faces)!=1):
            continue
            # raise Exception("exactly 1 face needed")
        
        dir=get_set_dir()
        write_image(dir,frame,frame_count)
        
        coords=__extract_coords(faces[0])
        write_label(dir,coords,frame_count)

def train():
    # Load a model
    # model = YOLO("yolov8n.yaml")  # build a new model from YAML
    # model = YOLO(os.path.join(dataset_dir, 'weights.pt'))  # load a pretrained model (recommended for training)
    # model = YOLO("yolov8n.yaml").load("yolov8n.pt")  # build from YAML and transfer weights
    model = YOLO("yolov8n.pt")
    # Train the model
    dataset_yaml_path=Path(os.path.join(dataset_dir, 'data.yaml')).absolute()
    results = model.train(data=dataset_yaml_path, epochs=3)

    im2 = cv2.imread("test.jpg")
    results = model.predict(source=im2, save=True, save_txt=True)

build_dataset()
train()