import cv2
from ultralytics import YOLO
import math
from extractor import Extractor

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'{self.x}, {self.y}'

    def __repr__(self):
        return self.__str__()

    def moved(self,x,y):
        return math.dist([self.x,self.y], [x,y])>0.1



# Load the YOLOv8 model
model = YOLO("dumbell_weights.pt")

# Open the video file
video_path = "/Users/omar.salem/Desktop/v.mov"
# video_path = "/Users/omar.salem/Downloads/stepper.mp4"
cap = cv2.VideoCapture(video_path)
kwargs={"conf":.5}

initiated=False
dumbells={}
extractor=Extractor()
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()
    if not success:
        break
    # Run YOLOv8 tracking on the frame, persisting tracks between frames
    results = model.track(frame, persist=True, **kwargs)
    boxes=results[0].boxes
    discovered_dumbells=[b for b in boxes if b is not None and b.cls.item()==0]
    
    if not initiated:
        initiated=True
        for d in discovered_dumbells:
            id=d.id.item()
            xyxy=d.xyxy[0]
            x=xyxy[0].item()
            y=xyxy[1].item()
            dumbells[id]=Position(x,y)
    else:
        for d in discovered_dumbells:
            id=d.id.item()
            xyxy=d.xyxy[0]
            x=xyxy[0].item()
            y=xyxy[1].item()
            if id in dumbells and dumbells[id].moved(x,y):
                person=extractor.findPersonClosestToPoint(frame,[x,y])
                print(person)




    
   

    # Visualize the results on the frame
    annotated_frame = results[0].plot()

    # Display the annotated frame
    cv2.imshow("YOLOv8 Tracking", annotated_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()