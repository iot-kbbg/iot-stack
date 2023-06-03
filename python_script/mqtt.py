import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK Returned code=",rc)
        client.connected_flag=True
    else:
        print("Bad connection Returned code=",rc)


def on_log(client, userdata, level, buf):
	with open("mqtt_log.txt", "w") as f:
		f.write("log: ", buf, "\n")
	#print("log: ", buf)


def connect(client_name, broker, port=1883):
    print(f"Connecting to MQTT broker {broker} as {client_name}")
    client = mqtt.Client(client_name)
    client.connect(host=broker, port=port)
    client.connected_flag = False
    client.on_connect = on_connect
    client.on_log = on_log
    client.loop_start()
    while not client.connected_flag:
        time.sleep(1)
    return client
