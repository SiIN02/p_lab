import paho.mqtt.client as mqtt
import json
import time
#import Adafruit_DHT  #Adafruit_DHT , adafruit_dht both are needed
import adafruit_dht
from board import *

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))

count=0
def on_publish(client, userdata, mid):
    print("In on_pub callback mid= ", mid)

DHT_PIN = D17       # GPIO17
dht11 = adafruit_dht.DHT11(DHT_PIN, False)

while True:
    try:
        dht11.measure()
        temp = dht11.temperature
        humid = dht11.humidity

        if humid is not None and temp is not None:
            print(f"temp= {temp:.2f}°C")
            print(f"humid= {humid:.2f}")                        
            # 새로운 클라이언트 생성
            client = mqtt.Client()            
            # 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_publish(메세지 발행)
            client.on_connect = on_connect
            client.on_disconnect = on_disconnect
            client.on_publish = on_publish            
            # address : localhost, port: 1883 에 연결
            client.connect('192.168.0.83', 1883)        
            # common topic 으로 메세지 발행
            client.publish('temp',temp, 1)
            client.publish('wat',humid,1)    
        else:
            print("failed to get reading from the sensor.Try again!")
        
    except RuntimeError as error:
        print("runtime error: "+str(error.args[0]))
    time.sleep(1.0)


#client.loop_stop()
# 연결 종료
#client.disconnect()
    
