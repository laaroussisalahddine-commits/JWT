"""Etape 1 : creer et afficher les trois parties d un JWT signe."""
from datetime import datetime, timedelta, timezone
import jwt

# Cle uniquement pour ce TP local (jamais en production).
SECRET_KEY = "classroom-demo-key-not-for-production"

payload = {
    "sub": "student123",
    "role": "user",
    "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
}
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
header, body, signature = token.split(".")

print("=== ETAPE 1 : CREATION ===")
print("JWT :", token)
print("HEADER :", header)
print("PAYLOAD :", body)
print("SIGNATURE :", signature)
print("\nQuestion : combien de parties contient le JWT signe ?")
