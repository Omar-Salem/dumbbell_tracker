# Dumbell Tracker
## Tracking gym member who don't put back their weights!

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
##### members
A folder containing the members's photos, each file should have 1 person in it, file name is the person's name.