import paho.mqtt.client as mqtt

import serial

mes = 5

def on_connect(client, userdata, flags, rc):

    if rc == 0:

        print("connected OK")

    else:

        print("Bad connection Returned code=", rc)

#def on_disconnect(client, userdata, flags, rc=0):

#     print(str(rc))

#     #ser.close()

#def on_subscribe(client, userdata, mid, granted_qos):

#     print("subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):

    global mes

    print(str(msg.payload.decode("utf-8")))

    ser.write(msg.payload)

    mes = str(msg.payload.decode("utf-8"))

ser = serial.Serial('/dev/ttyUSB1', 9600, parity=serial.PARITY_NONE)

ser.close()

ser.open()

client = mqtt.Client()

client1 = mqtt.Client()

# 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_subscribe(topic 구독),

# on_message(발행된 메세지가 들어왔을 때)

client.on_connect = on_connect

#client.on_disconnect = on_disconnect

#client.on_subscribe = on_subscribe

client.on_message = on_message

# address : localhost, port: 1883 에 연결

client.connect('localhost', 1883)

client1.connect('192.168.0.114', 1883)

while True:

    client.loop_start()

    client.subscribe('facenum', 1)

    client1.publish('facenum', mes)

    

    client.loop_stop()

ser.close().
