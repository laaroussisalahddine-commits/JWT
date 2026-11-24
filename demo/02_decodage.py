"""Etape 2 : lire Header et Payload SANS verifier la signature."""
import base64
import json
from datetime import datetime, timedelta, timezone
import jwt

SECRET_KEY = "classroom-demo-key-not-for-production"

# Creer un JWT local pour que ce fichier fonctionne tout seul.
token = jwt.encode(
    {
        "sub": "student123",
        "role": "user",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
    },
    SECRET_KEY,
    algorithm="HS256",
)
header, body, signature = token.split(".")


def lire_base64url(partie):
    padding = "=" * (-len(partie) % 4)
    donnees = base64.urlsafe_b64decode(partie + padding)
    return json.loads(donnees)


print("=== ETAPE 2 : DECODAGE SANS VERIFICATION ===")
print("HEADER :", json.dumps(lire_base64url(header), indent=2))
print("PAYLOAD :", json.dumps(lire_base64url(body), indent=2))
print("\nATTENTION : decodage != verification de signature.")
print("Question : peut-on lire le Payload sans la cle secrete ?")
