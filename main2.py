from pymongo import MongoClient
import dotenv, os

dotenv.load_dotenv()

MONGODB  = os.getenv('MONGODB')

mongoc = MongoClient(MONGODB)
database = mongoc["projetIOT"]
collection = database["mesures"]

docs = collection.find({"end_device_ids.device_id":"bridge-chaumont"})
for doc in docs:
    print(doc.get("received_at"), doc.get('end_device_ids').get('device_id'), doc.get('uplink_message').get('decoded_payload').get('haut'))