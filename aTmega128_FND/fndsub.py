import paho.mqtt.client as mqtt
import serial


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))
    ser.close()

def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    print(str(msg.payload.decode("utf-8")))
    ser.write(b'str(msg.payload.decode("utf-8"))')
    


ser = serial.Serial(port='/dev/ttyAMA0', // 시리얼통신에 사용할 포트
            baudrate=9600,                // 통신속도 지정
            parity=serial.PARITY_NONE,       // 패리티 비트 설정방식
            stopbits=serial.STOPBITS_ONE,     // 스톱비트 지정
            bytesize=serial.EIGHTBITS)       // 데이터 비트수 지정
         //'/dev/ttyS0' 'ls /dev/serial*' 
# 새로운 클라이언트 생성
client = mqtt.Client()
# 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_subscribe(topic 구독),
# on_message(발행된 메세지가 들어왔을 때)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe
client.on_message = on_message
# address : localhost, port: 1883 에 연결
client.connect('192.168.0.83', 1883)
# common topic 으로 메세지 발행
client.subscribe('common', 1)
client.loop_forever()
