Link ThingsBoard Dashboard https://demo.thingsboard.io/dashboard/98325830-6ecd-11ec-9a90-af0223be0666?publicId=b1256de0-75ea-11ec-9c90-dfa5d40d8afd

print("Xin chào ThingsBoard")
import paho.mqtt.client as mqttclient
import time
import json

BROKER_ADDRESS = "demo.thingsboard.io"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "Pn8pZiPKNDrFhvr3iFrV"


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    temp_data = {'value': True}
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj['method'] == "setValue":
            temp_data['value'] = jsonobj['params']
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
    except:
        pass


def connected(client, usedata, flags, rc):
    if rc == 0:
        print("Thingsboard connected successfully!!")
        client.subscribe("v1/devices/me/rpc/request/+")
    else:
        print("Connection is failed")


client = mqttclient.Client("Gateway_Thingsboard")
client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message

temp = 20
humi = 50
light_intensity = 100
longitude = 106.65499877929688
latitude = 10.779999732971191
counter = 0
while True:
    collect_data = {'temperature': temp, 'humidity': humi, 'light':light_intensity,
                    'longitude':longitude, 'latitude': latitude}
    temp += 1
    humi += 1
    light_intensity += 1
    client.publish('v1/devices/me/telemetry', json.dumps(collect_data), 1)
    time.sleep(10)
