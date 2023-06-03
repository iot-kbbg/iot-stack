import mqtt
import time
from queue import Queue
import json
import os, time
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

queue = Queue()

CLIENT_NAME = "pi4desk"
BROKER_IP = "192.168.220.1"

TOPIC_PUBLISH = f"{CLIENT_NAME}/status"
TOPIC_SUBSCRIBE = "#"

INFLUXDB_TOKEN = "YeHoMaIxzigO5lXntu12R0fR2qSaem_8ejO1AndNGGsd2al4pw2_REwylMVffOg2uWvcqDPKSwBmCW14tF6dbA=="
org = "iot-kbbg"
url = "http://192.168.220.1:8086"
bucket = "iot"


def on_message(client, userdata, message):
	#print("message received ", str(message.payload.decode("utf-8")))
	#print("message topic=", message.topic)
	#print("message qos=", message.qos)
	#print("message retain flag=", message.retain)
	queue.put(message)


client = mqtt.connect(CLIENT_NAME, BROKER_IP)
client.on_message = on_message
print("Publishing to topic ", TOPIC_PUBLISH)
client.publish(TOPIC_PUBLISH, "connected")
print("Subscribing to topic ", TOPIC_SUBSCRIBE)
client.subscribe(TOPIC_SUBSCRIBE)

write_client = influxdb_client.InfluxDBClient(url=url, token=INFLUXDB_TOKEN, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)

while client.connected_flag:
	while not queue.empty():
		message = queue.get()
		if message is None:
			continue
		if message.topic == "sensors/Karen":
			#print("Received message: ", str(message.payload.decode("utf-8")))
			try:
				jsonmessage = json.loads(str(message.payload.decode("utf-8")))
				temp = float(jsonmessage["temperature"])
			except ValueError:
				print("no valid json found. not parsing message")
			except TypeError:
				print("no valid json found. not parsing message")

			point = (Point("sensor_karen").field("temperature", temp))
			write_api.write(bucket=bucket, org=org, record=point)
        
		if message.topic == "sensors/bas_esp":
			#print("Received message: ", str(message.payload.decode("utf-8")))
			try:
				jsonmessage = json.loads(str(message.payload.decode("utf-8")))
				temp = float(jsonmessage["temperature"])
			except ValueError:
				print("no valid json found. not parsing message")
			except TypeError:
				print("no valid json found. not parsing message")

			point = (Point("sensor_bas").field("temperature", temp))
			write_api.write(bucket=bucket, org=org, record=point) 