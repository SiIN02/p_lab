import time
import cv2
import imutils
import platform
import numpy as np
from threading import Thread
from queue import Queue

from keras.models import load_model
import numpy as np

import paho.mqtt.client as mqtt

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)
model = load_model("keras_Model.h5", compile=False)


class Streamer :
    
    def __init__(self ):
        
        if cv2.ocl.haveOpenCL() :
            cv2.ocl.setUseOpenCL(True)
        print('[wandlab] ', 'OpenCL : ', cv2.ocl.haveOpenCL())
            
        np.set_printoptions(suppress=True)
        
        self.capture = None
        self.thread = None
        self.width = 640
        self.height = 360
        self.stat = False
        self.current_time = time.time()
        self.preview_time = time.time()
        self.sec = 0
        self.Q = Queue(maxsize=128)
        self.started = False
        self.client = mqtt.Client()
        
    def run(self, src = 0 ) :
        
        self.stop()
    
        self.capture = cv2.VideoCapture( src )
            
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        
        if self.thread is None :
            self.thread = Thread(target=self.update, args=())
            self.thread.daemon = False
            self.thread.start()
        
        self.started = True
    
    def stop(self):
        
        self.started = False
        
        if self.capture is not None :
            
            self.capture.release()
            self.clear()
            
    def update(self):
                    
        while True:

            if self.started :
                (grabbed, frame) = self.capture.read()
                
                if grabbed : 
                    self.Q.put(frame)

                image = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
                image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

                # Normalize the image array
                image = (image / 127.5) - 1

                # Predicts the model
                prediction = model.predict(image)
                index = np.argmax(prediction)
                class_name = index
                confidence_score = prediction[0][index]

                # Print prediction and confidence score
                print("Class:", class_name)
                print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

                self.client.connect('192.168.0.83', 1883)
                self.client.publish('facescore',str(np.round(confidence_score * 100))[:-2], 1)
                self.client.publish('facenum',str(class_name), 1)
                self.client.disconnect()

                
                          
    def clear(self):
        
        with self.Q.mutex:
            self.Q.queue.clear()
            
    def read(self):

        return self.Q.get()

    def blank(self):
        
        return np.ones(shape=[self.height, self.width, 3], dtype=np.uint8)
    
    def bytescode(self):
        
        if not self.capture.isOpened():
            
            frame = self.blank()

        else :
            
            frame = imutils.resize(self.read(), width=int(self.width) )
        
            if self.stat :  
                cv2.rectangle( frame, (0,0), (120,30), (0,0,0), -1)
                fps = 'FPS : ' + str(self.fps())
                cv2.putText  ( frame, fps, (10,20), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1, cv2.LINE_AA)
            
            
        return cv2.imencode('.jpg', frame )[1].tobytes()
    
    def fps(self):
        
        self.current_time = time.time()
        self.sec = self.current_time - self.preview_time
        self.preview_time = self.current_time
        
        if self.sec > 0 :
            fps = round(1/(self.sec),1)
            
        else :
            fps = 1
            
        return fps
                   
    def __exit__(self) :
        print( '* streamer class exit')
        self.capture.release()