import cv2
from ultralytics import YOLO


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
    print(box)
    xywhn=box.xywhn[0]
    return Coords(int(xywhn[0].item()),int(xywhn[1].item()),int(xywhn[2].item()),int(xywhn[3].item()))


video_path = '../resources/members/Omar Salem.mov'
member_name='Omar Salem'
cap = cv2.VideoCapture(video_path)
model = YOLO("../resources/yolov8n-face.pt")
while cap.isOpened():

    (success, frame) = cap.read()

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

    if frame is None:
        break

    results = model.predict(source=frame, conf=0.7)
    if(len(results)<1):
        raise Exception("prediction failed")
    faces=results[0].boxes
    if(len(faces)!=1):
        raise Exception("exactly 1 face needed")
    
    coords=__extract_coords(faces[0])
    print(coords)
    # top_x=coords.x
    # top_y
    # bottom_x
    # bottom_y=
    # cv2.rectangle(frame, (top_x,top_y), (bottom_x,bottom_y), (0, 0,255), 2)
    # cv2.imwrite('coords.png', frame)
    raise Exception("zzzzz")