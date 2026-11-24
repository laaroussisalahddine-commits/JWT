"""Educational JWT demo (local only): generation, decoding, tampering, expiry."""
import base64
import json
from datetime import datetime, timedelta, timezone

import jwt

# For classroom demonstration only. Never hardcode secrets in production.
SECRET_KEY = "classroom-demo-key-not-for-production"
ALGORITHM = "HS256"


def decode_part(encoded: str) -> dict:
    padding = "=" * (-len(encoded) % 4)
    return json.loads(base64.urlsafe_b64decode(encoded + padding))


def encode_part(data: dict) -> str:
    raw = json.dumps(data, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def line() -> None:
    print("\n" + "#" * 55 + "\n")


def main() -> None:
    payload = {
        "sub": "student123",
        "role": "user",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    header, body, signature = token.split(".")

    print("=== ETAPE 1 : CREATION ===")
    print("JWT :", token)
    print("HEADER :", header)
    print("PAYLOAD :", body)
    print("SIGNATURE :", signature)
    line()

    print("=== ETAPE 2 : DECODAGE SANS VERIFICATION ===")
    decoded_header = decode_part(header)
    decoded_payload = decode_part(body)
    print("HEADER :", json.dumps(decoded_header, indent=2))
    print("PAYLOAD :", json.dumps(decoded_payload, indent=2))
    print("Attention : lire un payload ne prouve PAS sa validite.")
    line()

    print("=== ETAPE 3 : SIGNATURE ===")
    try:
        verified = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Token original : ACCEPTE | role :", verified["role"])
    except jwt.InvalidTokenError as exc:
        print("Token original : REFUSE |", type(exc).__name__)

    tampered_payload = decoded_payload.copy()
    tampered_payload["role"] = "admin"
    tampered_token = f"{header}.{encode_part(tampered_payload)}.{signature}"
    print("Payload modifie : role=user -> role=admin")
    try:
        jwt.decode(tampered_token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Token modifie : ACCEPTE (inattendu)")
    except jwt.InvalidSignatureError:
        print("Token modifie : REFUSE (signature invalide)")
    except jwt.InvalidTokenError as exc:
        print("Token modifie : REFUSE |", type(exc).__name__)
    line()

    print("=== ETAPE 4 : EXPIRATION ===")
    expired = jwt.encode(
        {
            "sub": "student123",
            "role": "user",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=5),
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    try:
        jwt.decode(expired, SECRET_KEY, algorithms=[ALGORITHM])
        print("Token expire : ACCEPTE (inattendu)")
    except jwt.ExpiredSignatureError:
        print("Token expire : REFUSE (expiration depassee)")
    except jwt.InvalidTokenError as exc:
        print("Token expire : REFUSE |", type(exc).__name__)

    print("\nCONCLUSION : verifier signature, algorithme, expiration et claims attendus.")


if __name__ == "__main__":
    main()
