# Dumbell Tracker
## Tracking gym member who don't put back their weights!

### Required packages
```sh
pip3 install dlib
pip3 install tf-keras
pip3 install deepface
pip3 install ultralytics
pip3 install opencv-python
pip3 install scikit-image
```

### Run demo
```sh
git clone git@github.com:Omar-Salem/dumbbell_tracker.git
cd dumbbell_tracker
```

### Key elements
##### dumbbell_weights.pt
Obtained by [training yolo](https://docs.ultralytics.com/usage/cli/#__tabbed_1_2), here the dataset of interest was obtained from https://universe.roboflow.com/cgm/dumbbell_2.5, but it can be any other set.
```sh
yolo train data=dataset.yaml model=yolov8n.pt epochs=3 lr0=0.01
```
##### db
A folder containing the person's photos, each file should have 1 person in it, file name is the person's name.