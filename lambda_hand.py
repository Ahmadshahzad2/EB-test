import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # pretrained YOLOv8n model


def lambda_handler(frame):
    results = model(frame, device='mps')
    fina_frame=results[0].plot()

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, encoded_image = cv2.imencode('.jpg', fina_frame)
    return encoded_image.tobytes()