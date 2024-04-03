
from getpass import getpass 
from prompt_toolkit import PromptSession 
session = PromptSession() 


class Dashboard(): 
    print('hello dashboard') 

    welcome = '\n* * * * * * * * * * * * * * * * * \
        \n\033[1mBonjour et bienvenue !\033[0m \
        \n\n\tCe programme vous permet de gérer vos clients. \
        \nLe fichier README.md contient les informations pour installer et utiliser l\'application. \
        \n\n\tDans le menu, vous pouvez à tout moment utiliser les Commandes interface : \
        \n\033[1m* pour revenir au menu principal \n0 pour sortir\033[0m' 

    # gestion_menu = { 
    #     '1': 'Créer un département', 
    #     '2': 'Créer un utilisateur', 
    #     '3': 'Créer un contrat', 
    #     '4': 'Afficher tous les départements', 
    #     '5': 'Afficher tous les utilisateurs', 
    #     '6': 'Afficher tous les clients', 
    #     '7': 'Afficher tous les contrats', 
    #     '8': 'Afficher tous les événements', 
    #     '9': 'Afficher les sans contact support', 
    #     '10': 'Modifier un département', 
    #     '11': 'Modifier un utilisateur', 
    #     '12': 'Modifier un événement', 
    # } 



    menu = [ 
        '\n', 
        '1 : Enregistrer un département', 
        '2 : Enregistrer un utilisateur', 
        '3 : Enregistrer un client', 
        '4 : Enregistrer un contrat', 
        '5 : Enregistrer un événement', 

        '\n6 : Modifier un département', 
        '7 : Modifier un utilisateur', 
        '8 : Modifier un client', 
        '9 : Modifier un contrat', 
        '10 : Modifier un événement', 

        '\n11 : Supprimer un utilisateur', 

        '\n12 : Afficher tous les départements ', 
        '13 : Afficher tous les utilisateurs ', 
        '14 : Afficher tous les client ', 
        '15 : Afficher tous les contrats ', 
        '16 : Afficher tous les événeùents ', 

        '\n17 : Afficher un département ', 
        '18 : Afficher un utilisateur ', 
        '19 : Afficher un client ', 
        '20 : Afficher un contrat ', 
        '21 : Afficher un événement ', 

        '\n22 : Afficher les événements sans contact support ', 
        '23 : Afficher les clients d\'un utilisateur commercial ', 
        '24 : Afficher les contrats d\'un utilisateur commercial ', 
        '25 : Afficher les contrats non finis de payer ', 
        '26 : Afficher les contrats non signés ', 
        '27 : Afficher les événements d\'un utilisateur support ' 
    ] 

    display_rescue = [ 
        '--------', 
        '\033[1mCommandes interface :\033[0m ', 
        '* pour revenir au menu principal ', 
        '0 pour sortir et fermer l\'application ' 
    ] 


    def __init__(self): 
        pass 


    def display_welcome(self): 
        print(self.welcome) 


    def display_menu(self, items: list): 
        """ Display the menu for chosing which action the user wants to do. 
        """ 

        print('\n* * * * * * * * * * * * * * * * *') 
        for item in items: 
            print(self.menu[item]) 
        for r in self.display_rescue: 
            print(r) 
        self.ask_for_action = session.prompt('\nChoisir une action : ') 
        print('') 
        return self.ask_for_action 

