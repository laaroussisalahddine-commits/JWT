"""Etape 4 : signer un JWT deja expire puis montrer son rejet."""
from datetime import datetime, timedelta, timezone
import jwt

SECRET_KEY = "classroom-demo-key-not-for-production"
ALGORITHM = "HS256"

payload_expire = {
    "sub": "student123",
    "role": "user",
    "exp": datetime.now(timezone.utc) - timedelta(minutes=5),
}
token_expire = jwt.encode(payload_expire, SECRET_KEY, algorithm=ALGORITHM)

print("=== ETAPE 4 : EXPIRATION ===")
print("Token cree et signe avec une date d'expiration passee.")
try:
    jwt.decode(token_expire, SECRET_KEY, algorithms=[ALGORITHM])
    print("Token expire : ACCEPTE (inattendu)")
except jwt.ExpiredSignatureError:
    print("Token expire : REFUSE (expiration depassee)")
except jwt.InvalidTokenError as exc:
    print("Token expire : REFUSE |", type(exc).__name__)

print("Question : une signature valide suffit-elle pour accepter un JWT ?")
