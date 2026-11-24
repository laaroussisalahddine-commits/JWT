# Sécurité des JWT — Démonstration + TP étudiant

Mini-projet pédagogique pour un exposé Web Application Security (20 min).

## Objectifs
- Comprendre Header, Payload, Signature d'un JWT signé (JWS).
- Distinguer encodage Base64URL, chiffrement et signature.
- Montrer que la lecture du Payload **ne vérifie pas** sa signature.
- Refuser un Payload modifié et un JWT expiré.

## Préparation (Python 3)
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```
Sur 1337, si le Nexus configuré ne fournit pas PyJWT et si la politique réseau le permet :
```bash
python -m pip install --index-url https://pypi.org/simple -r requirements.txt
```

## Démonstration professeur / présentateur

### Scripts indépendants : une expérience à la fois
```bash
python demo/01_creation.py
python demo/02_decodage.py
python demo/03_signature.py
python demo/04_expiration.py
```
Chaque fichier crée son propre JWT et peut être lancé directement, sans dépendre du script précédent.

### Script global : les quatre expériences réunies
```bash
python demo/jwt_demo.py
```
Les JWT non expirés durent 5 minutes ; chaque lancement en génère de nouveaux.

**Conseil de présentation :** expliquer chaque fichier séparé au tableau, poser la question associée, puis lancer `jwt_demo.py` pour récapituler. Les questions et réponses d'animation figurent dans `docs/QUESTIONS_INTERACTIVES.md`.


## Activité étudiant
Lire `tp/ENONCE.md` et compléter `tp/starter.py`. Ne pas consulter `demo/` avant d'avoir tenté le TP.

## Documents
- `docs/PLAN_PRESENTATION.md` : plan collectif + timing.
- `docs/QUESTIONS_INTERACTIVES.md` : une question orale après chaque étape.
- `tp/ENONCE.md` : consignes et critères de réussite.
- `docs/CTF_BONUS.md` : challenge web officiel (optionnel).

## Sécurité et périmètre
Ce dépôt est **uniquement éducatif**. La clé en clair sert à la démonstration et ne doit pas être reprise en production. Le TP modifie des tokens créés localement, sans attaquer de services tiers. En production : secret fort hors du code, algorithmes autorisés fixés côté serveur, HTTPS, validation de `exp`, `iss`, `aud` lorsque pertinents, autorisations côté serveur et stockage adapté.

## Ressources
- [PyJWT : Usage Examples](https://pyjwt.readthedocs.io/en/stable/usage.html)
- [PortSwigger : JWT attacks](https://portswigger.net/web-security/jwt)
