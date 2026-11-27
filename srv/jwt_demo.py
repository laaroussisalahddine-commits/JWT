import argparse
import base64
import json
import secrets
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import jwt


HOST = "127.0.0.1"
ISSUER = "jwt-demo"
AUDIENCE = "jwt-demo-api"
ALGORITHM = "HS256"
PAGE = Path(__file__).with_name("index.html")
ACCOUNTS = {
    "alice": ("alice-demo", "user"),
    "admin": ("admin-demo", "admin"),
}


def issue_token(username, signing_key, lifetime, *, issued_at=None):
    issued_at = issued_at or datetime.now(timezone.utc)
    return jwt.encode(
        {
            "sub": username,
            "role": ACCOUNTS[username][1],
            "iss": ISSUER,
            "aud": AUDIENCE,
            "iat": issued_at,
            "exp": issued_at + timedelta(seconds=lifetime),
        },
        signing_key,
        algorithm=ALGORITHM,
    )


class DemoServer(ThreadingHTTPServer):
    def __init__(self, port, lifetime, *, quiet=False):
        super().__init__((HOST, port), DemoHandler)
        self.signing_key = secrets.token_bytes(32)
        self.lifetime = lifetime
        self.quiet = quiet

    def sample_tokens(self):
        return {
            "invalid_signature": issue_token("alice", secrets.token_bytes(32), 300),
            "expired_token": issue_token(
                "alice",
                self.signing_key,
                300,
                issued_at=datetime.now(timezone.utc) - timedelta(minutes=10),
            ),
        }


class DemoHandler(BaseHTTPRequestHandler):
    def log_message(self, message, *args):
        if not self.server.quiet:
            super().log_message(message, *args)

    def respond(self, status, body, *, bearer_challenge=None):
        self.send_body(
            status,
            json.dumps(body).encode("utf-8"),
            "application/json",
            bearer_challenge=bearer_challenge,
        )

    def send_body(self, status, data, content_type, *, bearer_challenge=None):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        if bearer_challenge:
            self.send_header("WWW-Authenticate", bearer_challenge)
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        if self.path != "/login":
            self.respond(404, {"error": "not_found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 4096:
                raise ValueError
            body = json.loads(self.rfile.read(length))
            if not isinstance(body, dict) or body.keys() != {"username", "password"}:
                raise ValueError
            username = body["username"]
            password = body["password"]
            if not isinstance(username, str) or not isinstance(password, str):
                raise ValueError
        except ValueError:
            self.respond(400, {"error": "invalid_login_request"})
            return

        account = ACCOUNTS.get(username)
        if account is None or password != account[0]:
            self.respond(401, {"error": "invalid_credentials"})
            return
        token = issue_token(username, self.server.signing_key, self.server.lifetime)
        self.respond(200, {"access_token": token, "token_type": "Bearer"})

    def do_GET(self):
        if self.path == "/":
            self.send_body(200, PAGE.read_bytes(), "text/html; charset=utf-8")
            return
        if self.path == "/demo/samples":
            self.respond(200, self.server.sample_tokens())
            return
        if self.path not in ("/profile", "/admin", "/users"):
            self.respond(404, {"error": "not_found"})
            return
        authorization = self.headers.get("Authorization", "").split()
        if len(authorization) != 2 or authorization[0].lower() != "bearer":
            self.respond(401, {"error": "missing_token"}, bearer_challenge="Bearer")
            return

        try:
            claims = jwt.decode(
                authorization[1],
                self.server.signing_key,
                algorithms=[ALGORITHM],
                issuer=ISSUER,
                audience=AUDIENCE,
                options={"require": ["sub", "role", "iss", "aud", "iat", "exp"]},
            )
        except jwt.InvalidTokenError as error:
            reason = "invalid_token"
            if isinstance(error, jwt.ExpiredSignatureError):
                reason = "expired_token"
            elif isinstance(error, jwt.InvalidSignatureError):
                reason = "invalid_signature"
            self.respond(
                401, {"error": reason}, bearer_challenge='Bearer error="invalid_token"'
            )
            return

        if self.path in ("/admin", "/users") and claims["role"] != "admin":
            self.respond(403, {"error": "admin_required"})
            return
        if self.path == "/users":
            users = [
                {"username": username, "role": role}
                for username, (_, role) in ACCOUNTS.items()
            ]
            self.respond(200, {"users": users})
            return
        self.respond(200, {"sub": claims["sub"], "role": claims["role"]})


def call_api(base_url, path, *, token=None, body=None):
    headers = {"Content-Type": "application/json"} if body is not None else {}
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    request = Request(base_url + path, data=data, headers=headers)
    try:
        response = urlopen(request, timeout=3)
    except HTTPError as error:
        response = error
    with response:
        return response.status, json.load(response)


def login(base_url, username):
    status, body = call_api(
        base_url, "/login", body={"username": username, "password": ACCOUNTS[username][0]}
    )
    if status != 200:
        raise RuntimeError(f"POST /login pour {username} → HTTP {status}: {body}")
    return body["access_token"]


def show_token(token):
    for label, segment in zip(("Header", "Payload", "Signature"), token.split(".")):
        print(f"{label} (Base64url) = {segment}")
        if label != "Signature":
            decoded = base64.urlsafe_b64decode(segment + "=" * (-len(segment) % 4))
            print(json.dumps(json.loads(decoded), ensure_ascii=False, indent=2))
    print("Le décodage affiche le contenu. L’API vérifie ensuite la signature et les claims.")


def run_demo():
    with DemoServer(0, 300, quiet=True) as server:
        worker = Thread(target=server.serve_forever)
        worker.start()
        try:
            base_url = f"http://{HOST}:{server.server_port}"
            user_token = login(base_url, "alice")
            admin_token = login(base_url, "admin")
            print(f"API locale : {base_url}")
            print("POST /login (alice) → HTTP 200. JWT signé par le serveur.\n")
            show_token(user_token)

            samples = server.sample_tokens()
            cases = [
                (
                    "JWT utilisateur valide", "/profile", user_token,
                    200, {"sub": "alice", "role": "user"},
                ),
                (
                    "JWT utilisateur valide", "/admin", user_token,
                    403, {"error": "admin_required"},
                ),
                (
                    "JWT administrateur valide", "/admin", admin_token,
                    200, {"sub": "admin", "role": "admin"},
                ),
                (
                    "Signature avec une autre clé", "/profile", samples["invalid_signature"],
                    401, {"error": "invalid_signature"},
                ),
                (
                    "JWT signé mais expiré", "/profile", samples["expired_token"],
                    401, {"error": "expired_token"},
                ),
                ("Jeton absent", "/profile", None, 401, {"error": "missing_token"}),
            ]
            print()
            for label, path, token, expected_status, expected_body in cases:
                status, body = call_api(base_url, path, token=token)
                print(f"GET {path} · {label} → HTTP {status} {json.dumps(body)}")
                if (status, body) != (expected_status, expected_body):
                    raise RuntimeError(f"Réponse attendue : HTTP {expected_status} {expected_body}")
            print(f"\n{len(cases)} scénarios vérifiés.")
        finally:
            server.shutdown()
            worker.join()


def main():
    parser = argparse.ArgumentParser(description="Démonstration locale de la validation des JWT")
    parser.add_argument("mode", choices=("demo", "serve"))
    parser.add_argument("--port", type=int, default=8000, help="Port du mode serve")
    parser.add_argument("--ttl", type=int, default=300, help="Durée de validité en secondes")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535 or args.ttl < 1:
        parser.error("Le port doit être entre 1 et 65535 et le TTL doit être positif.")
    if args.mode == "demo":
        run_demo()
        return

    try:
        with DemoServer(args.port, args.ttl) as server:
            print(f"API JWT sur http://{HOST}:{server.server_port}", flush=True)
            server.serve_forever()
    except KeyboardInterrupt:
        pass
    except OSError as error:
        parser.exit(1, f"Impossible de démarrer le serveur ({error}).\n")


if __name__ == "__main__":
    main()
