# Ce script écrit le fichier creds.json à partir d'une variable d'environnement
import os
import json

google_creds = os.getenv("GOOGLE_CREDS_JSON")

if google_creds:
    with open("creds.json", "w") as f:
        json.dump(json.loads(google_creds), f)
