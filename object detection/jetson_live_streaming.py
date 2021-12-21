import socketio
import cv2
import time
import base64
sio = socketio.Client()
cap=cv2.VideoCapture('b.dav')
@sio.event
def connect():
    print('connection established')
    print('message sent')
    frame_rate = 10
    prev = 0
    while True:
        time_elapsed = time.time() - prev
        ret,frame=cap.read()
        if not ret:
            break
        frame=cv2.resize(frame,(400,400))
        print(frame.shape)
        if time_elapsed > 1./frame_rate:
            prev = time.time()
            frame = base64.b64encode(cv2.imencode('.jpg', frame,[cv2.IMWRITE_JPEG_QUALITY, 60])[1]).decode()

            sio.emit('my image',frame)
@sio.event
def disconnect():
    print('disconnected from server')
sio.connect('http://157.245.85.21:8000/')
sio.wait()
