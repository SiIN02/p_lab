import paho.mqtt.client as mqtt
import sys
import time
from pymata4 import pymata4

prev_data = "5"

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
    global prev_data
    data = str(msg.payload.decode("utf-8"))

    if((data!='5') and (prev_data != data)):
        print(data, "has detected")
        board.set_pin_mode_servo(5)
        board.servo_write(5, 120)
        time.sleep(1)
        board.servo_write(5, 0)
        time.sleep(1)
    elif (data=="5"):
        print("non human")
    else:
        print("duplicated")
    prev_data = data


board = pymata4.Pymata4()

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe
client.on_message = on_message  
client.connect('192.168.0.83', 1883)
client.subscribe('facenum', 1)
client.loop_forever()