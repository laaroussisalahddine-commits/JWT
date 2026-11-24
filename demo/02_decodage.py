"""Etape 2 : lire Header et Payload SANS verifier la signature."""

import base64
import json
from datetime import datetime, timedelta, timezone
import jwt

SECRET_KEY = "classroom-demo-key-not-for-production"

# Creer un JWT local pour que ce fichier fonctionne tout seul.
token = jwt.encode(
    {
        "sub": "salaheddine123", # -----> identifiant de student;
        "role": "user", #----> role d'identifiant
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5), #--->time exper
    },
    SECRET_KEY,
    algorithm="HS256",
)
header, body, signature = token.split(".")


def lire_base64url(partie):
    padding = "=" * (-len(partie) % 4)
    donnees = base64.urlsafe_b64decode(partie + padding)
    return json.loads(donnees)


print("\n=== ETAPE 2 : DECODAGE SANS VERIFICATION ===\n")
print("\nHEADER :", json.dumps(lire_base64url(header), indent=2))
print("\nPAYLOAD :", json.dumps(lire_base64url(body), indent=2))
print("\nATTENTION : decodage != verification de signature.\n")
