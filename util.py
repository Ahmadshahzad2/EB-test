import cv2
import time
import base64
# from ultralytics import YOLO

# model = YOLO("yolov8n.pt")  # pretrained YOLOv8n model


def allowed_file(filename, allowed_extensions={'mp4', 'avi', 'mov'}):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def process_video_async(socketio, video_path):
    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    delay = 1 / frame_rate

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        processed_frame = process_frame(frame)
        socketio.emit('new_frame', {'data': processed_frame}, namespace='/video')
        time.sleep(delay)  # Control the frame rate

    cap.release()
    socketio.emit('video_complete', {'status': 'done'}, namespace='/video')

# def process_frame(frame):
#     results = model(frame, device='mps')
#     fina_frame=results[0].plot()

#     # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     _, encoded_image = cv2.imencode('.jpg', fina_frame)
#     return encoded_image.tobytes()

def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # results = model(frame, device='mps')
    # final_frame = results[0].plot()

    _, encoded_image = cv2.imencode('.jpg', gray)
    base64_image = base64.b64encode(encoded_image).decode('utf-8')  # encode as base64 string
    return base64_image