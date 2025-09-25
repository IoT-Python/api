from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pymongo import MongoClient
from dotenv import load_dotenv
import os

from starlette.requests import Request

load_dotenv()
# connexion à la base de donnée
MONGODB = os.getenv('MONGODB')
client = MongoClient(MONGODB)
database = client["projetIOT"]
collection = database["mesures"]
app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def redirect_typer():
    return RedirectResponse("/mesures")

@app.get("/mesures")
def affichage_info(request: Request):

   # récupération des données
    docs = list(collection.find({"end_device_ids.device_id": "bridge-chaumont"}, {"_id":0}))

    # boucle pour afficher toutes les données
    for doc in docs:
        print(doc.get("received_at"), doc.get('end_device_ids').get('device_id'),
              doc.get('uplink_message').get('decoded_payload'))

    # passer les infos au templates
    return templates.TemplateResponse(request=request, name="index.html", context={"liste": docs})