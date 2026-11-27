# Démonstration locale de la sécurité des JWT

## Démo automatique pour la dernière diapositive

```bash
cd "/home/laaroussidin/Desktop/EST/JWT/srv"
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python jwt_demo.py demo
```

Les deux commandes d’installation sont à faire une seule fois. La commande `demo` démarre une API locale, obtient les JWT via `POST /login`, affiche les trois segments du JWT, décode le header et le payload, puis envoie de vraies requêtes HTTP. Le serveur s’arrête à la fin.

| Requête | Jeton | Réponse attendue |
| --- | --- | --- |
| `GET /profile` | Utilisateur valide | `200 OK` |
| `GET /admin` | Utilisateur valide | `403 Forbidden` |
| `GET /admin` | Administrateur valide | `200 OK` |
| `GET /profile` | Signé avec une autre clé | `401 Unauthorized` · `invalid_signature` |
| `GET /profile` | Signé par l’API et expiré | `401 Unauthorized` · `expired_token` |
| `GET /profile` | Absent | `401 Unauthorized` · `missing_token` |

**À dire à l’oral.** « Le header et le payload sont lisibles après décodage. L’API vérifie la signature, l’émetteur, le public visé et l’expiration avant de lire le rôle pour autoriser l’accès à `/admin`. Un jeton rejeté donne un 401. Un utilisateur authentifié qui n’a pas le rôle requis reçoit un 403. »

Le test de signature utilise un jeton de test signé avec une autre clé. Les droits d’accès sont illustrés avec deux comptes de démonstration.

## Démo dans le navigateur

```bash
.venv/bin/python jwt_demo.py serve
```

Ouvrir [Démo JWT](http://127.0.0.1:8000/). Cliquer sur **Connexion Alice**, puis sur **GET /profile** et **GET /admin** pour voir les réponses `200` et `403`. Cliquer sur **Connexion Admin**, puis sur **GET /admin** pour voir `200`. **Effacer le jeton** permet de montrer un `401` sur la prochaine requête protégée. Le bouton **Copier le JWT pour Postman** copie le jeton actif.

## Collection Postman

`GET /users` renvoie les noms et rôles des comptes de démonstration. Envoyer le jeton de l’administrateur dans **Authorization → Bearer Token** pour obtenir `200 OK`. Le jeton d’Alice donne `403 Forbidden`. Sans jeton, l’API répond `401 Unauthorized`.

Pour les étapes 5 à 7 de la dernière diapositive, ouvrir la section correspondante sur la page de démo. L’étape 5 montre le changement de rôle dans le JSON décodé. Pour les étapes 6 et 7 dans Postman, envoyer `GET http://127.0.0.1:8000/demo/samples` et utiliser les valeurs renvoyées comme **Bearer Token**.

| Étape | Requête | Jeton de test | Réponse |
| --- | --- | --- | --- |
| 6 | `GET /admin` | `invalid_signature`, signé avec une autre clé | `401` · `invalid_signature` |
| 7 | `GET /profile` | `expired_token`, signé par l’API et déjà expiré | `401` · `expired_token` |

En gardant le serveur actif, ouvrir Postman Desktop et choisir **Import**, puis sélectionner `jwt_demo.postman_collection.json`. Ouvrir la collection **Démo JWT locale** et lancer **Run collection** en mode local. On peut aussi envoyer les requêtes une par une dans l’ordre affiché. Les requêtes de connexion enregistrent leurs jetons dans les variables de la collection.

`POST /login` attend exactement les champs texte `username` et `password`. La requête **Connexion avec champ inattendu · 400** ajoute `sadsad` et vérifie la réponse `400 Bad Request` avec `invalid_login_request`.

Pour tester l’expiration avec le navigateur ou Postman, se connecter, laisser le jeton expirer, puis envoyer de nouveau `GET /profile` avec ce même jeton. Le serveur démarre avec une durée de validité de cinq minutes. L’option `serve --ttl 10` permet de refaire cette partie en 11 secondes.

### Requêtes manuelles dans Postman

1. Envoyer `POST http://127.0.0.1:8000/login`. Dans **Body → raw → JSON**, saisir `{"username":"alice","password":"alice-demo"}`. Copier la valeur `access_token` de la réponse.
2. Envoyer `GET http://127.0.0.1:8000/profile`. Dans **Authorization → Bearer Token**, coller le jeton. La réponse est `200` avec `"role": "user"`.
3. Envoyer `GET http://127.0.0.1:8000/admin` avec le même jeton. La réponse est `403`.
4. Refaire la connexion avec `{"username":"admin","password":"admin-demo"}` et tester `/admin` avec le nouveau jeton. La réponse est `200`.
5. Pour voir l’expiration en direct, redémarrer avec `.venv/bin/python jwt_demo.py serve --ttl 10`, se reconnecter et utiliser le nouveau jeton sur `/profile` après 11 secondes. La réponse est `401` avec `expired_token`.

Le serveur écoute uniquement sur `127.0.0.1`. Chaque démarrage génère une nouvelle clé de signature. Les comptes et leurs mots de passe sont des exemples pour la démonstration.

[Documentation PyJWT sur la vérification des jetons](https://pyjwt.readthedocs.io/en/stable/api.html)



`How to run`: cd ~/Desktop/EST/JWT/srv
.venv/bin/python jwt_demo.py serve


`how to run in windows` : cd .\srv
py -m venv .venv-win
.\.venv-win\Scripts\python.exe -m pip install -r requirements.txt
.\.venv-win\Scripts\python.exe jwt_demo.py serve