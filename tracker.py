import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO("weights.pt")

# Open the video file
video_path = "/Users/omar.salem/Desktop/v.mov"
# video_path = "/Users/omar.salem/Downloads/stepper.mp4"
cap = cv2.VideoCapture(video_path)
kwargs={"conf":.1}

initiated=False
# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if not success:
        break
    # Run YOLOv8 tracking on the frame, persisting tracks between frames
    results = model.track(frame, persist=True, **kwargs)
    # print('results:', end='')
    # print(results[0].boxes)
    boxes=results[0].boxes
    for b in boxes:
        if b is None:
            continue
        if b.cls.item() == 1:
            continue
        print('id:', end='')
        print(b.id.item(), end='')
        print(',class:', end='')
        print(b.cls.item(), end='')
        print(', x:', end='')
        print(b.xyxy[0][0].item(), end='')
        print(', y:', end='')
        print(b.xyxy[0][1].item())
        # for xyxy in b.xyxy[0]:
        #     print(xyxy.item())
        # x=coords[0]
        # y=coords[1]
    # if not initiated:
    #     initiated=True
        # print('id:')
        # print(b.id)
        # print('xyxy:')
        # print(b.xyxy)

    # if not detected:
    #     # start timer
    # else:
    #     # reset timer


    
   

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

class Dumbell:
  def __init__(self, x, y):
    self.x = x
    self.y = y