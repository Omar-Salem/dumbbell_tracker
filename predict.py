# import cv2
# from PIL import Image
# from ultralytics import YOLO

# kwargs={"conf":.5}
# model = YOLO("yolov8n.pt")
# # accepts all formats - image/dir/Path/URL/video/PIL/ndarray. 0 for webcam
# results = model.predict(source="us.jpg", show=True, **kwargs)  # Display preds. Accepts all YOLO predict arguments
# results[0].save(filename=f"results.jpg")


# boxes=results[0].boxes.xyxy
# print(results[0].boxes.id)
# for xyxy in boxes:
#     print(xyxy[0])
#     print(xyxy[1])

from deepface import DeepFace
f1 = "test.jpg"
f2 = "source.jpg"
# backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']
# result = DeepFace.verify(img1_path=f1, img2_path=f2, detector_backend=backends[2])
dfs = DeepFace.find(img_path = f1, db_path = "db")
print(result)