import paho.mqtt.client as mqtt
from gtts import gTTS
import pygame, time

data = '5'
pre = '1'
path = "/home/pi/Desktop/animals.ogg" #junghoon 0
path1 = "/home/pi/Desktop/animals1.ogg" # jaeseon 1
path2 = "/home/pi/Desktop/animals2.ogg" # sunghoon 2
path3 = "/home/pi/Desktop/animals3.ogg" # woosung 3
path4 = "/home/pi/Desktop/animals4.ogg" # myenghoon 4
speaker_volume = 1

#tts


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))


def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    global data
    print(str(msg.payload.decode("utf-8")))    
    data = msg.payload.decode("utf-8")
         
while True:
    client = mqtt.Client()
    client.on_message = on_message
    client.connect('localhost', 1883)
    client.loop_start()
    client.subscribe('facenum', 1)
    client.loop_stop()

    if pre != data and 0 == int(data):                              
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.set_volume(speaker_volume)
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        time.sleep(2)         
    elif pre != data and 1 == int(data):                             
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.set_volume(speaker_volume)
        pygame.mixer.music.load(path1)
        pygame.mixer.music.play()
        time.sleep(2)    
    elif pre != data and 2 == int(data):           
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.set_volume(speaker_volume)
        pygame.mixer.music.load(path2)
        pygame.mixer.music.play()
        time.sleep(2)                   
    elif pre != data and 3 == int(data):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.set_volume(speaker_volume)
        pygame.mixer.music.load(path3)
        pygame.mixer.music.play()
        time.sleep(2)        
    elif pre != data and 4 == int(data):        
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.set_volume(speaker_volume)
        pygame.mixer.music.load(path4)
        pygame.mixer.music.play()
        time.sleep(2)      
    print(data)

    pre = data