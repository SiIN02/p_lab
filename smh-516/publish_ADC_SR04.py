import paho.mqtt.client as mqtt
import json
import random,time
import sys
from pymata4 import pymata4

DISTANCE_CM = 2
TRIGGER_PIN = 13
ECHO_PIN = 12
ANALOG_PIN = 2  # arduino pin number
POLL_TIME = 0.1  # number of seconds between polls

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))


def on_publish(client, userdata, mid):
    print("In on_pub callback mid= ", mid)

def the_callback(data):
    #print(f'Distance in cm: {data[DISTANCE_CM]}')
    pass

def sonar(my_board, trigger_pin, echo_pin, callback):
    my_board.set_pin_mode_sonar(trigger_pin, echo_pin, callback)

board = pymata4.Pymata4()
board.set_pin_mode_analog_input(ANALOG_PIN)


client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish

client.connect('192.168.0.83', 1883)
client.loop_start()
sonar(board, TRIGGER_PIN, ECHO_PIN, the_callback)
while(1):
    value = board.analog_read(ANALOG_PIN)[0]
    client.publish('register', value, 1)
    centimeter = board.sonar_read(TRIGGER_PIN)[0]
    client.publish('distance',centimeter , 1)
    time.sleep(1)
