import cv2
from PIL import Image
from ultralytics import YOLO

model = YOLO("weights.pt")
# accepts all formats - image/dir/Path/URL/video/PIL/ndarray. 0 for webcam
results = model.predict(source="d.jpg", show=True)  # Display preds. Accepts all YOLO predict arguments
results[0].save(filename=f"results.jpg")


boxes=results[0].boxes.xyxy
print(results[0].boxes.id)
for xyxy in boxes:
    print(xyxy[0])
    print(xyxy[1])