
# P12 - Epic Events 

Projet d'apprentissage. 
Développer une application (CLI) de gestion de clientèle (CRM), avec Python et SQL.  


## Environnemnet virtuel Pipenv 
[Doc de Pipenv](https://post-it.pycolore.fr/post-it/python/pipenv) 

*  Créer un projet : `pipenv --python 3.11` -> crée le Pipfile 
*  Installer les dépendances du projet : `pipenv install` (ajouter des dépndances, comme "dev" par exemple : `--dev`) 
*  Activer l'environnement virtuel : `pipenv shell` 
    --> Le message "Launching subshell in virtual environment..." est afifché dans la console  
    --> le nom du termianl devient "pipenv" 
*  Lancer des commandes à l'intérieur de l'env virtuel : `pipenv run <command>` 
*  Lancer le programme : `pipenv run python chemin/du/projet.py`    


## Container Docker pour la BDD 
* Créer un fichier `.env` pour stocker les données sensibles : 
    - POSTGRES_DB = <le nom de la BDD> 
    - POSTGRES_USER = <le nom de l'utilisateur admin> 
    - POSTGRES_PASSWORD = <le mot de passe de l'admin> 
    - DB_PORT = <le port où servir la BDD> 
    - ADMINER_PORT = <le port où servir Adminer> 
    Docker utilise ces données pour créer la BDD dans le container. 
* Configurer le fichier compose.yaml en fonction de vos préférences (nom de container, par exemple). 


## Installation 

1. Télécharger le dossier .zip 
2. Extraire les fichiers dans un dossier local dédié au projet 
3. installer et lancer l'environnement virtuel (voir ci-dessus) 
4. Créer et lancer le container Docker : 
    taper dans un terminal `docker compose up --build` 
    * Après chaque modification du fichier compose.yaml : penser à : 
    - supprimer les volumes dans l'outil de gestion de Docker 
    - "re-builder" le container (`docker compose up --build`) 
    * Pour relancer le container sans avoir modifié le compose.yaml : `docker compose up` 
    * Fermer le container : `ctrl+c`, 
        ou depuis un autre terminal : `compose down` 
5. Vérifier qu'Adminer peut se connecter à la BDD : 
    - visiter l'adresse http://localhost:${ADMINER_PORT} 
    - sélectionner "Postgresql" dans le menu déroulant 
    + taper les informations suivantes dans le formulaire : 
        - host : <le_nom_du_service> 
        - utilisateur : POSTGRES_USER 
        - mot de passe : POSTGRES_PASSWORD 
        - nom de base de données : POSTGRES_DB 
    - envoyer le formulaire 
    --> Adminer affiche la bdd. 

6. Données 
    + Super utilisateur : 
        - Créer un fichier `data.json` dans le même dossier 
        - coller ces données dedans : 
        `{"users": [`
            `{`
                `"id": 1,`
                `"name": "super_admin",` 
                `"email": "admin@mail.org",` 
                `"phone": "06 12 34 56 78",` 
                `"department_id": 1` 
            `}`
        `]}` 
        Le super utilisateur pourra créer les autres départements et les autres utilisateurs. Il fait lui-même partie du département "gestion". 
    + Données secrètes : 
        - Dans le fichier `.env`, ajouter une entrée `USER_1_PW` avec pour valeur le mot de passe de votre choix pour le super utilisateur. 
        - Vérifier que le fichier `.env` est bien ajouté au fichier `.gitignore`. 

7. Configuration d'utilisation 
    Pour utiliser l'application en mode dev : 
    commenter la ligne `main('pub')` dans `project.py` et décommenter la ligne `main('dev')`. 
    Elle utilisera les données de connexion du super utilisateur du fichier json au lieu d'avoir à les taper. 
    **Attention :** ce mode n'est pas sécurisé, décommenter la ligne `main('pub')` et commenter la ligne `main('dev')` pour une utilisation publique.  


**Compléter** 

## Démarrer l'application : 

1. Activer Pipenv :     
    - `pipenv install` 
    - `pipenv shell` 
2. Se placer dans le dossier du projet : `cd epic_events` 
3. Lancer l'application : `pipenv run python projet.py` 



