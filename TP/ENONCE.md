# TP Étudiant — JWT : lecture, intégrité et expiration

**Durée :** 20–30 minutes | **Niveau :** débutant | **Matériel :** Python 3 + PyJWT

## Situation
Votre service émet un JWT signé pour `student01` avec `role=user`. Votre mission : comprendre pourquoi un client ne doit jamais être considéré admin simplement parce qu'il affiche un tel rôle dans un Payload modifié.

## Consignes
Travaillez **uniquement sur les tokens que vous créez localement**. Complétez `starter.py` sans consulter `demo/jwt_demo.py`.

1. **Créer :** générer un JWT `sub=student01`, `role=user`, exp dans 2 minutes, signé en HS256. Afficher ses 3 segments.
2. **Observer :** décoder Header et Payload *sans vérification de signature*. Répondre : pourquoi le Payload n'est-il pas confidentiel ?
3. **Modifier :** remplacer `user` par `admin` dans le Payload encodé, **conserver l'ancienne signature**. Faire vérifier le token modifié avec la clé et `algorithms=["HS256"]`.
4. **Expirer :** créer un JWT correctement signé dont `exp` est dans le passé. Faire vérifier ce token et observer l'exception.
5. **Conclure :** expliquer en 3 phrases la différence entre lecture, vérification de signature et expiration.

## Livrables
- `starter.py` complété et exécutable.
- Capture terminal des trois résultats : original accepté, modifié rejeté, expiré rejeté.
- Réponses aux 3 questions ci-dessous.

## Questions
1. Un client change `role=user` en `admin` : pourquoi le serveur sûr rejette-t-il le token ?
2. Pourquoi n'est-il pas recommandé de mettre un mot de passe dans le Payload ?
3. Si un token est bien signé mais expiré, faut-il l'accepter ? Pourquoi ?

## Critères de réussite
- JWT généré et découpé en 3 parties
- Payload décodé sans clé et principe expliqué
- Token modifié refusé pour signature invalide
- Token expiré refusé pour expiration
- Conclusion claire et personnelle

**Bonus :** Expliquer pourquoi `algorithms=["HS256"]` est fixé par le serveur et non copié depuis le Header non fiable.
