import requests
from dotenv import load_dotenv
import os
load_dotenv()

DISCORD=os.getenv('DISCORD')
url = DISCORD

data = {
    "content" : "message content",
    "username" : "Lorène"
}

data["embeds"] = [
    {
        "description" : "text in embed",
        "title" : "embed title"
    }
]

result = requests.post(url, json = data)

try:
    result.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
else:
    print(f"Payload delivered successfully, code {result.status_code}.")