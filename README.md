# Dumbell Tracker
## Tracking gym member who don't put back their weights!

### Run demo
```sh
git clone git@github.com:Omar-Salem/dumbbell_tracker.git
cd dumbbell_tracker/dumbbell_tracker
python3 tracker.py
```

### Key elements
##### dumbbell_tracker/resources/dumbbells/empty_rack.png
An image of the rack with the dumbbells removed, coordinates of each 
placeholder (obtained manually) are used to generate each dumbbell empty placeholder, these images are then used to check when a dumbbell has been removed.

##### dumbbell_tracker/member_pre_pocessor.py
Fed a video of a member moving their head around, preferably using the same camera and in same lighting condition as detections, results are then stored in dumbbell_tracker/resources/members/dataset/yolov8n-members.pt for member identification.