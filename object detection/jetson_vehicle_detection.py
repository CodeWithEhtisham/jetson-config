import cv2
from datetime import datetime
import time
import socketio
import cv2
import base64
sio = socketio.Client()
print("client activated")
net=cv2.dnn_DetectionModel(r"D:\gil\demo\yolov4\yolov4.cfg",r"D:\gil\demo\yolov4\yolov4.weights")
net.setInputSize(608,608)
net.setInputScale(1.0/255)
net.setInputSwapRB(True)

with open(r'D:\gil\demo\yolov4\obj.names','rt') as f:
    names=f.read().rstrip('\n').split('\n')
fpsLimit = 1 # throttle limit
startTime = time.time()
cap = cv2.VideoCapture('b.dav')
print("cap s")
@sio.event
def connect():
    while True:
        print("frames")
        ret,frame = cap.read()
        frame = frame[:, 280:]
        nowTime = time.time()
        if (int(nowTime - startTime)) > fpsLimit:
            classes,confidances,boxes=net.detect(frame,confThreshold=0.1,nmsThreshold=0.4)
            if type(classes)==type((1,1)):
                continue
            results=[]
            print(results)
            time.sleep(5)
            for classId,confidance,box in zip(classes.flatten(),confidances.flatten(),boxes):
                label='%.2f' % confidance
                label = '%s: %s' % (names[classId],label)
                # print(label)
                labelSize,baseLine= cv2.getTextSize(label,cv2.FONT_HERSHEY_SIMPLEX,0.5,1)
                left,top,wedth,height=box
                top=max(top,labelSize[1])
                results.append({
                    "label":str(names[classId]),
                    "prob":str('%.2f' % confidance),
                    "x":str(left),
                    "y":str(top),
                    "w":str(wedth),
                    "h":str(height)
                })
            frame = base64.b64encode(cv2.imencode('.jpg', frame,[cv2.IMWRITE_JPEG_QUALITY, 60])[1]).decode()

            dic={
                "cartotal":0,
                "bustotal":0,
                "trucktotal":0,
                "rickshawtotal":0,
                "biketotal":0,
                "vantotal":0,
                "total":0

            }
            for i in results:
                # print(i["label"])
                if i["label"] =='Motorcycle' or i["label"]=="Bicycle":
                    dic['biketotal']+=1
                    dic['total']+=1
                elif i['label']=='Auto_rikshaw':
                    dic['rickshawtotal']+=1
                    dic['total']+=1
                elif i['label']=='Bus':
                    dic['bustotal']+=1
                    dic['total']+=1
                elif i['label']=='Truck':
                    dic['trucktotal']+=1
                    dic['total']+=1
                elif i['label']=='Van':
                    dic['vantotal']+=1
                    dic['total']+=1
                else:
                    dic['cartotal']+=1
                    dic['total']+=1
            # print(frame)
            obj={
                "image":frame,
                "image_path":datetime.strftime(datetime.now(), "%Y-%m-%d:%H:%M:%S")+'_uob.jpg',
                # "tag":tag,
                "datetime":datetime.strftime(datetime.now(), "%Y-%m-%d:%H:%M:%S"),
                "camera_id":"12345",
                "camera_loc":"UOB",
                "results":results,
                "counts":dic
            }
            sio.emit('main page socket',obj)

cv2.destroyAllWindows()
@sio.event
def disconnect():
    print('disconnected from server')
print("connecting........")
sio.connect('http://165.227.84.39/')
sio.wait()