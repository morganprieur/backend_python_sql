
# Backend Python SQL 

CLI backend CRM application. Developped with Python (without framework) and PostgreSQL. 
It allows to manage users, authorizations with tokens, read, create and update clients, contracts and events, depending of the authorizations. "Admin" users are allowed to manage the other users. 

The PostgreSQL database is developped into a Docker container. 

## Outils pour l'installation 

### Container Docker pour la BDD 
* Créer un fichier `<projet>/.env` pour stocker les données sensibles : 
    - POSTGRES_DB = <le_nom_de_la_BDD> 
    - POSTGRES_USER = <le_nom_de_l_utilisateur_admin> 
    - POSTGRES_PASSWORD = <le_mot_de_passe_de_l_admin> 
    - DB_PORT = <le_port_où_servir_la_BDD> 
    - ADMINER_PORT = <le_port_où_servir_Adminer> 
    Docker utilise ces données pour créer la BDD dans le container et donner l'accès à l'utilisateur. 
* Configurer le fichier compose.yaml en fonction de vos préférences (nom de container, par exemple). 


### Environnement virtuel Pipenv 
[Doc de Pipenv](https://post-it.pycolore.fr/post-it/python/pipenv) 

*  Installer les dépendances du projet : `pipenv install` (ajouter des dépendances, comme "environnement de dev" par exemple : `--dev`) 
*  Activer l'environnement virtuel : `pipenv shell` 
    --> Le message "Launching subshell in virtual environment..." est afifché dans la console  
    --> le nom du terminal devient "pipenv" 
*  Lancer des commandes à l'intérieur de l'env virtuel :    
    - Vérifier que le nom du terminal est bien `pipenv`    
    - Taper la commande directement 
*  Lancer le programme :    
    - Se placer dans le dossier du projet : `cd epic_events` 
    - Taper `python projet.py <mode de saisie> <role de l'utilisateur>`    


## Installation 

1. Télécharger le dossier .zip 
2. Extraire les fichiers dans un dossier local dédié au projet 
    Ils contiennt les fichiers pour gérer le container Docker (BDD), .gitignore, les fichiers de Pipenv, le fichier d'installation et le dossier `epic_events` qui contient le projet. 
3. Créer et lancer le container Docker : 
    au niveau du fichier `compose.yaml`, taper dans un terminal `docker compose up --build` 
    * Après chaque modification du fichier compose.yaml, penser à : 
        - supprimer le container et le volume dans l'outil de gestion de Docker 
        - "re-builder" le container (`docker compose up --build`) 
    * Pour relancer le container sans avoir modifié compose.yaml :    
        `docker compose up` 
    * Pour fermer le container : `ctrl+c`, 
        ou depuis un autre terminal : `docker compose down` 
4. installer et lancer l'environnement virtuel (voir ci-dessus) 
5. Vérifier qu'Adminer peut se connecter à la BDD : 
    - visiter l'adresse `http://localhost:<ADMINER_PORT>` 
    - sélectionner "Postgresql" dans le menu déroulant 
    + taper les informations suivantes dans le formulaire : 
        - host : <le_nom_du_service> 
        - utilisateur : POSTGRES_USER 
        - mot de passe : POSTGRES_PASSWORD 
        - nom de base de données : POSTGRES_DB 
    - envoyer le formulaire 
    --> Adminer affiche la bdd. 

6. Données 
    + Données secrètes : 
        + Dans le fichier `.env` :    
            - ajouter une entrée `USER_1_PW` avec pour valeur le mot de passe de votre choix pour le super utilisateur. 
            - et une entrée `JWT_SECRET` avec la valeur de votre choix pour la phrase secrète à utiliser par JWT. 

            - SENTRY = <l'url reçue par mail> 

            - FILE_PATH = 'data.json' 
            - TOKEN_PATH = '<nom_du_fichier_contenant_les_tokens_chiffrés>.csv' 
            - JWT_KEY_PATH = '<nom_du_fichier_contenant_la_clé_JWT>.key' 

            Les chemins à importer : 
            - ROOTPATH='C:/Users/<chemin/vers/le/dossier/projet>'
            - PYTHONPATH='${ROOTPATH};${ROOTPATH}/epic_events;${ROOTPATH}/epic_events/controller;${ROOTPATH}/utils'

        - **Vérifier que le fichier `.env` sont bien ajoutés au fichier `.gitignore`.** 

7. Création et peuplement des tables    
    - lancer le script setup.py depuis le dossier `epic_events` : `python setup.py` 
        Opérations du fichier : 
            - installe les tables dans la BDD 
            - crée le département "gestion" 
            - crée un utilisateur du département "gestion". 
    - vérifier que les données sont bien enregistrées dans la BDD (depuis Adminer). 

8. Tokens     
    Les tokens sont créés à la connexion d'un utilisateur, si son mail et son mot de passe sont vérifiés. 

    Quand un utilisateur veut accéder à l'application, il entre d'abord son mail. S'il est enregistré et qu'un token est enregistré (chiffré) dans le fichier `<nom_du_fichier_contenant_les_tokens_chiffrés>.csv`, le token est vérifié : 
        - le token lui-même, contenant le mail et le département, 
        - la date de validité. 
    S'il est bon et valide, l'utilisateur est connecté avec l'autorisation correspondant à son département. 
    S'il n'est pas bon, un message est affiché et l'application est fermée. 
    S'il est bon mais périmé, un message est affiché, et l'utilisateur doit taper son mot de passe. 
        Le mot de passe est vérifié. S'il est bon, un nouveau token est créé et enregistré. L'utilisateur est conncté et obtient les autorisations liées à son département. 
        Si le mot de passe n'est pas bon, un message est affiché et l'application est fermée. 

9. Utilisation de l'application 
    A partir du dossier `epic_events`, taper la commande :     
    `python project.py <mode> <role>` 
    `mode` : le mode de saisie (dev|pub) 
    `role` : le rôle de l'utilisateur si besoin (admin|sales|support). Le rôle n'est utile que pour le mode "dev".  

    Pour utiliser l'application en mode démo : 
    `python project.py dev <role>` 
    Vous utiliserez alors les données de connexion de l'utilisateur choisi (`role`). 
    **Attention :** ce mode n'est pas sécurisé, il n'est pas adapté à une utilisation réelle.  


## sentry 
Sentry est un service de surveillance d'applications à distance. Il reçoit les erreurs ou événement configurés, et peut envoyer des notifications par mail aux utilisateurs enregistrés. 
Vous pourrez nous dire qui doit recevoir quelles notifications, pour qu'on les ajoute aux utilisateurs de Sentry. 

La clé privée d'accès à l'API vous sera envoyée par mail à la livraison de l'application. 
**Conservez-la en sécurité** : 
- Supprimez le mail du serveur de votre mailer 
- collez la clé dans votre fichier `.env` 
- vérifiez que le fichier `.env` est bien ajouté au fichier `.gitignore` 
- ne partagez pas ce fichier avec des personnes qui n'ont pas de raison de le consulter. 

