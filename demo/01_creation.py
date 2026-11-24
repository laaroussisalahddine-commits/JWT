"""Etape 1 : creer et afficher les trois parties d un JWT signe."""

from datetime import datetime, timedelta, timezone
import jwt

SECRET_KEY = "classroom-demo-key-not-for-production"  # ---> Cle uniquement pour ce TP local (jamais en production).

payload = {
    "sub": "student123",
    "role": "user",
    "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
}
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
header, body, signature = token.split(".")

print("\n=== ETAPE 1 : CREATION ===\n")
print("\nJWT :", token)
print("\nHEADER :", header)
print("\nPAYLOAD :", body)
print("\nSIGNATURE :", signature)
