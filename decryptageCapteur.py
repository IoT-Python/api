import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from pymongo import MongoClient
import json
import os
import base64
import struct

load_dotenv()

MQTT_TOPIC = os.getenv('MQTT_TOPIC')
MQTT_USER = os.getenv('MQTT_USER')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')
MQTT_HOST = os.getenv('MQTT_HOST')
MONGODB = os.getenv('MONGODB')

# Connexion à MongoDB
client = MongoClient(MONGODB)
database = client["projetIOT"]
collection = database["mesures"]

# Décodage VS133
# def decode_vs133(msg_b64):
#     donnees = base64.b64decode(msg_b64)
#     valeurs = struct.unpack('<BBIBBIBBI', donnees)
#     return {
#         "entrees": valeurs[2],
#         "sorties": valeurs[5],
#         "periode": valeurs[8],
#     }


def decode_vs133(msg_b64):
    donnees = base64.b64decode(msg_b64)
    print("Payload brut (hex):", donnees.hex(), "Taille:", len(donnees))

    if len(donnees) != 18:
        # On ne plante pas, on stocke brut pour analyse
        return {"raw_payload": donnees.hex(), "taille": len(donnees)}

    valeurs = struct.unpack('<BBIBBIBBI', donnees)
    return {
        "entrees": valeurs[2],
        "sorties": valeurs[5],
        "periode": valeurs[8]
    }

# Callback quand on se connecte au broker
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connecté avec code {reason_code}")
    client.subscribe(MQTT_TOPIC)

# Callback quand un message arrive
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())

        uplink = data.get("uplink_message", {})

        # Si VS133
        if "frm_payload" in uplink:
            decoded = decode_vs133(uplink["frm_payload"])
            data["uplink_message"]["decoded_payload"] = decoded

        # On enregistre tout tel quel
        collection.insert_one(data)
        print("Message enregistré :", data)

    except Exception as e:
        print("Erreur :", e)

# Client MQTT
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
if MQTT_USER:
    mqttc.username_pw_set(MQTT_USER, MQTT_PASSWORD)

mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect(MQTT_HOST, 1883, 60)
print("En attente de messages MQTT...")
mqttc.loop_forever()