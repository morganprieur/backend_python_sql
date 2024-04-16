
# P12 - Epic Events 

Application (utilisable avec CLI) de gestion de clientèle (CRM), en Python, avec PostgreSQL.  
Pas de framework Python. 
Base de données dans un container Docker 


## Outils pour l'installation 

### Container Docker pour la BDD 
* Créer un fichier `<projet>/.env` pour stocker les données sensibles : 
    - POSTGRES_DB = <le_nom_de_la_BDD> 
    - POSTGRES_USER = <le_nom_de_l_utilisateur_admin> 
    - POSTGRES_PASSWORD = <le_mot_de_passe_de_l_admin> 
    - DB_PORT = <le_port_où_servir_la_BDD> 
    - ADMINER_PORT = <le_port_où_servir_Adminer> 
    Docker utilise ces données pour créer la BDD dans le container et l'exposer à l'utilisateur. 
* Configurer le fichier compose.yaml en fonction de vos préférences (nom de container, par exemple). 


### Environnement virtuel Pipenv 
[Doc de Pipenv](https://post-it.pycolore.fr/post-it/python/pipenv) 

*  Créer un projet : `pipenv --python 3.11` -> crée le Pipfile 
*  Installer les dépendances du projet : `pipenv install` (ajouter des dépndances, comme "dev" par exemple : `--dev`) 
*  Activer l'environnement virtuel : `pipenv shell` 
    --> Le message "Launching subshell in virtual environment..." est afifché dans la console  
    --> le nom du termianl devient "pipenv" 
*  Lancer des commandes à l'intérieur de l'env virtuel :    
    - Vérifier que le nom du terminal est bien `pipenv`    
    - Taper `pipenv run <command>` 
*  Lancer le programme :    
    - Se placer dans le dossier du projet : `cd epic_events` 
    - Taper `python projet.py`    


## Installation 

1. Télécharger le dossier .zip 
2. Extraire les fichiers dans un dossier local dédié au projet 
    Ils contiennt les fichiers pour gérer le container Docker (BDD), .gitignore, les fichiers de Pipenv, le fichier d'installation et de peuplement de la BDD et le dossier `epic_events` qui contient le projet. 
3. installer et lancer l'environnement virtuel (voir ci-dessus) 
4. Créer et lancer le container Docker : 
    taper dans un terminal `docker compose up --build` 
    * Après chaque modification du fichier compose.yaml, penser à : 
        - supprimer le container et le volume dans l'outil de gestion de Docker 
        - "re-builder" le container (`docker compose up --build`) 
    * Pour relancer le container sans avoir modifié le compose.yaml :    
        `docker compose up` 
    * Pour fermer le container : `ctrl+c`, 
        ou depuis un autre terminal : `compose down` 
5. Vérifier qu'Adminer peut se connecter à la BDD : 
    - visiter l'adresse `http://localhost:${ADMINER_PORT}` 
    - sélectionner "Postgresql" dans le menu déroulant 
    + taper les informations suivantes dans le formulaire : 
        - host : <le_nom_du_service> 
        - utilisateur : POSTGRES_USER 
        - mot de passe : POSTGRES_PASSWORD 
        - nom de base de données : POSTGRES_DB 
    - envoyer le formulaire 
    --> Adminer affiche la bdd. 

6. Données 
    - Créer un fichier `epic_events/data.json`  
    - coller ces données dedans : 
        `{"users": [` 
            `{`
                `"name": "super_admin",` 
                `"email": "admin@mail.org",` 
                `"phone": "06 12 34 56 78",` 
                `"department_id": 1` 
            `}`
        `],`
        `"departments": [`
            `{`
                `"name": "gestion"`
            `},`
            `{`
                `"name": "commerce"`
            `},`
            `{`
                `"name": "support"`
            `}`
        `]}` 
        Le super utilisateur pourra créer les autres utilisateurs et gérer les départements. Il fait lui-même partie du département "gestion". 

    + Données secrètes : 
        + Dans le fichier `.env` :    
            - ajouter une entrée `USER_1_PW` avec pour valeur le mot de passe de votre choix pour le super utilisateur. 
            - et une entrée `JWT_SECRET` avec la valeur de votre choix pour la phrase secrète à utiliser par JWT. 

            - 'SENTRY' = <l'url reçue par mail> 

            - 'FILE_PATH' = 'data.json' 
            - 'TOKEN_PATH' = '<nom_du_fichier_contenant_les_tokens_chiffrés>.csv' 
            - 'JWT_KEY_PATH' = '<nom_du_fichier_contenant_la_clé_JWT>.key' 

            Les chemins à importer : 
            - 'ROOTPATH'='C:/Users/<chemin/vers/le/dossier/projet>'
            - 'PYTHONPATH'='${ROOTPATH};${ROOTPATH}/epic_events;${ROOTPATH}/epic_events/controller;${ROOTPATH}/utils'

        - **Vérifier que les fichiers `data.json` et `.env` sont bien ajoutés au fichier `.gitignore`.** 

        + Tokens 
            Les tokens créés lors de l'installation sont enregistrés chiffrés dans un fichier. La clé utilisée est enregistrée dans un fichier pour être accessible quand on en a besoin (chiffrer / déchiffrer les données). 
            + A l'installation (fichier setup.py) : 
                - la clé est générée une seule fois pour toute l'application (à renouveler si elle est corrompue). 
                - elle est enregistrée dans un fichier : `<nom_du_fichier_contenant_la_clé_JWT>.key`. 
                - récupérée pour pouvoir l'utiliser. 
                - les données d'origine sont chiffrées et enregistrées dans le fichier : `<nom_du_fichier_contenant_les_tokens_chiffrés>.csv`. 
            + Pour mettre à jour ou ajouter un token : manager.register_token 
                - Récupère la clé. 
                - Déchiffre les données du fichier chiffré. 
                - Parcourt les données déchiffrées pour chercher le mail. 
                - SI trouvé : remplace le token enregistré par le nouveau, 
                    SINON : ajoute le binome mail/token à la liste des données. 
                - chiffre les données màj. 
                - enregistre les données màj chiffrées dans le fichier :  `<nom_du_fichier_contenant_les_tokens_chiffrés>.csv`. 
            + Pour vérifier un token (**prérequis : le mail et le mot de passe sont bons**) : manager.verify_token 
                - Récupère la clé. 
                - Déchiffre les données du fichier chiffré. 
                - parcourt les données déchiffrées pour chercher le mail. 
                    SI trouvé : vérifie le token 
                        SI ok : vérifie la date du token 
                            SI PAS PASSE : accepte la connexion de 
                                l'utilisateur 
                            SINON : appele manager.get_token() pour 
                                rafraichir le token et l'enregistrer dans le fichier chiffré 
                        SINON : message "Token non conforme" 
                    SINON : None. 


    + Création et peuplement des tables    
        - lancer le script setup.py depuis le dossier parent :     
            `cd ..`    
            `python setup.py` 
            Opérations du fichier : 
                - installe les tables dans la BDD 
                - crée le département "gestion" 
                - crée un utilisateur du département "gestion". 
        - vérifier que les données sont bien enregistrées dans la BDD (depuis Adminer, avec les données de connexion indiquées dans ### Container Docker pour la BDD). 

7. Configuration pour l'utilisation 
    Pour utiliser l'application en mode dev : 
    commenter la ligne `main()` dans `epic_events/project.py` et décommenter la ligne `main('dev')`. 
    Elle utilisera les données de connexion du super utilisateur du fichier json au lieu d'avoir à les taper. 
    **Attention :** ce mode n'est pas sécurisé, décommenter la ligne `main()` et commenter la ligne `main('dev')` pour une utilisation publique.  


## sentry 
Sentry est un service de surveillance d'applications à distance. Il reçoit les erreurs ou événement configurés, et peut envoyer des notifications aux utilisateurs enregistrés. 
Vous pourrez nous dire qui doit recevoir quelles notifications, pour qu'on les ajoute aux utilisateurs de Sentry. 

La clé privée d'accès à l'API vous sera envoyée par mail à la livraison de l'application. 
**Conservez-la en sécurité** : 
- Supprimez le mail du serveur de votre mailer 
- collez la clé dans votre fichier `.env` 
- vérifiez que le fichier `.env` est bien ajouté au fichier `.gitignore` 
- ne partagez pas ce fichier avec des personnes qui n'ont pas de raison de le consulter. 


