import os
import paho.mqtt.client as mqtt
import smtplib, ssl
import json
from dotenv import load_dotenv
from email.mime.text import MIMEText
from pymongo import MongoClient

load_dotenv()
# Récupération des variables d'environnement
email_address=os.getenv("EMAIL_ADDRESS")
email_password=os.getenv("EMAIL_APP_PASS")
MQTT_TOPIC=os.getenv('MQTT_TOPIC')

# Variable d'environnement MongoDB
MONGODB = os.getenv("MONGODB")

# Infos SMTP Gmail
smtp_address = "smtp.gmail.com"
smtp_port = 465

# Destinataire
email_receiver = "alertes.iot@gmail.com"

# Connexion à MongoDB
client= MongoClient(MONGODB)
database = client["projetIOT"]
collection = database["mesures"]

# Callback quand on se connecte au broker
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_TOPIC)

# Callback quand un message est reçu
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    collection.insert_one(json.loads(msg.payload))

# --- Récupération des alertes où 'haut' > 3 ---
alerts = list(collection.find({"haut": {"$gt": 3}}, {"_id": 0, "haut": 1, "device_id": 1, "received_at": 1}))

# --- Construction du corps du mail ---
if alerts:
    body = "⚠️ Alertes de hauteur détectées :\n\n"
    for a in alerts:
        body += f"- Appareil {a['device_id']} : hauteur = {a['haut']} | reçu à {a['received_at']}\n"
else:
    body = "✅ Aucune alerte de hauteur supérieure à 3."

# Création du message MIME
message = MIMEText(body, "plain")
message["From"] = email_address
message["To"] = "alertes.iot@gmail.com"
message["Subject"] = "Alertes depuis MongoDB"

# Envoi du mail
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(email_address, email_password)
    server.send_message(message)

print("✅ Mail envoyé !")