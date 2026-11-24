"""Etape 3 : modifier role=user en role=admin puis verifier la signature."""
import base64
import json
from datetime import datetime, timedelta, timezone
import jwt

SECRET_KEY = "classroom-demo-key-not-for-production"
ALGORITHM = "HS256"

payload = {
    "sub": "student123",
    "role": "user",
    "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
}
token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
header, body, signature = token.split(".")

print("=== ETAPE 3 : SIGNATURE ===")
try:
    original = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print("Token original : ACCEPTE | role =", original["role"])
except jwt.InvalidTokenError as exc:
    print("Token original : REFUSE |", type(exc).__name__)

# Ici on simule une modification locale non autorisee du payload.
payload_modifie = payload.copy()
payload_modifie["role"] = "admin"
# datetime n'est pas serialisable par json : convertir exp en timestamp.
payload_modifie["exp"] = int(payload_modifie["exp"].timestamp())
json_modifie = json.dumps(payload_modifie, separators=(",", ":")).encode("utf-8")
body_modifie = base64.urlsafe_b64encode(json_modifie).rstrip(b"=").decode("ascii")
# On conserve volontairement la signature de l'ancien token.
token_modifie = f"{header}.{body_modifie}.{signature}"
print("Role modifie : user -> admin (signature originale conservee)")

try:
    jwt.decode(token_modifie, SECRET_KEY, algorithms=[ALGORITHM])
    print("Token modifie : ACCEPTE (inattendu)")
except jwt.InvalidSignatureError:
    print("Token modifie : REFUSE (signature invalide)")
except jwt.InvalidTokenError as exc:
    print("Token modifie : REFUSE |", type(exc).__name__)

print("Question : pourquoi ne peut-on pas signer cette modification sans la cle ?")
