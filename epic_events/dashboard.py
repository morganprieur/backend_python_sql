
from getpass import getpass 
from prompt_toolkit import PromptSession 
session = PromptSession() 


class Dashboard(): 
    print('hello dashboard') 

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
        '16 : Afficher tous les événements ', 

        '\n17 : Afficher un département ', 
        '18 : Afficher un utilisateur', 
        '19 : Afficher un client ', 
        '20 : Afficher un contrat ', 
        '21 : Afficher un événement ', 

        '\n22 : Afficher les événements sans contact support ', 
        '23 : Afficher les clients d\'un utilisateur commercial ', 
        '24 : Afficher les contrats d\'un utilisateur commercial ', 
        '25 : Afficher les contrats non fini de payer ', 
        '26 : Afficher les contrats non signés ', 
        '27 : Afficher les événements d\'un utilisateur support ', 
        '--------', 
        '\n\033[1m0 : Se déconnecter et fermer l\'application\033[0m ' 
    ] 



    def __init__(self): 
        pass 


    def display_welcome(self, user_name, user_dept): 
        # print(self.welcome) 
        print(f'\n* * * * * * * * * * * * * * * * * \
            \n\033[1mBonjour et bienvenue {user_name} (département {user_dept}) !\033[0m \
            \n\n\tCe programme vous permet de gérer vos clients. \
            \nLe fichier README.md contient les informations pour installer et utiliser l\'application.' 
            '\n' 
        ) 


    def display_menu(self, items: list): 
        """ Displays the menu for the user can chose which action to perform. 
            The menu's options depend on the role (= department) of the 
            connected user. 
        """ 
        print('\n* * * * * * * * * * * * * * * * *') 
        for item in items: 
            print(self.menu[item]) 
        # for r in self.rescue_menu: 
        #     print(r) 
        self.ask_for_action = session.prompt('\nChoisir une action : ') 
        print('') 
        return self.ask_for_action 

