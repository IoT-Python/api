import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from pymongo import MongoClient
import json
import os

load_dotenv()

MQTT_TOPIC=os.getenv('MQTT_TOPIC')
MQTT_USER=os.getenv('MQTT_USER')
MQTT_PASSWORD=os.getenv('MQTT_PASSWORD')
MQTT_HOST=os.getenv('MQTT_HOST')
MONGODB=os.getenv('MONGODB')

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_TOPIC)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    collection.insert_one(json.loads(msg.payload))

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
if (MQTT_USER):
    mqttc.username_pw_set(MQTT_USER, MQTT_PASSWORD)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

client = MongoClient(MONGODB)
database = client["projetIOT"]
collection = database["mesures"]

mqttc.connect(MQTT_HOST, 1883, 60)

mqttc.loop_forever()