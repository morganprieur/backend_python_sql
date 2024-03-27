
from manager import Manager 
from models import Base, Client, Contract, Department, Event, User  
from views import Views 

from datetime import datetime, timedelta 
import json 
import os 
import time 

# from prompt_toolkit import PromptSession 
# session = PromptSession() 


class Controller(): 
    print(f'hello controller') 
    # test_fct() 
    def __init__(self):  # , view, manager 
        self.views = Views() 
        self.manager = Manager() 
        # self.helpers = Helpers() 
        self.manager.connect() 
        self.manager.create_session() 

        self.user_session = None 


    # def start(self, mode, user_session=None): 
    def start(self, mode): 
        # self.user_session = None 

        # Mode de saisie des infos utilisateur 
        print('mode de saisie ML41 : ', mode) 
        userConnect = {} 
        if mode == 'pub': 
            # Type the required credentials: 
            userConnect = self.views.input_user_connection() 
        else:  
            # file deepcode ignore PT: local project 
            with open(os.environ.get('FILE_PATH'), 'r') as jsonfile: 
                self.registered = json.load(jsonfile) 
                print(self.registered) 
                userConnect = self.registered['users'][0] 

        # Verify password 
        userConnect['password'] = os.environ.get('USER_1_PW') 
        checked = self.manager.check_pw( 
            userConnect['email'], 
            userConnect['password'] 
        ) 
        if not checked: 
            # TODO: retour formulaire + compteur (3 fois max) 
            print('Les informations saisies ne sont pas bonnes, merci de réessayer.') 
        else: 
            logged_user = self.manager.select_one_user( 
                'email', userConnect['email']) 

            # Verify JWT 
            # Check token pour utilisateur connecté + département 
            self.user_session = self.manager.verify_token( 
                logged_user.email, 
                logged_user.password, 
                logged_user.department.name 
            ) 
            print('self.user_session CL65 : ', self.user_session) 
            # # TODO: sortie propre après l'échec du token 
            if self.user_session == 'past': 
                print('self.user_session CL68 : ', self.user_session) 
                print(logged_user.token) 
                delta = 8*3600 
                new_token = self.manager.get_token(delta, { 
                    'email': logged_user.email, 
                    'pass': logged_user.password, 
                    'dept': logged_user.department.name 
                }) 
                updated_logged_user = self.manager.update_user(logged_user.id, 'token', new_token) 
                updated_user_db = self.manager.select_one_user('email', logged_user.email) 
                print(updated_user_db.token) 
                print(self.user_session) 
            else: 
                print(self.user_session) 
            # return logged_user 

            if(logged_user) & (session.prompt('\nCreate user ? ')=='y'): 
                self.create_user() 
            else: 
                if(logged_user) & (session.prompt('\nCreate client ? ')=='y'): 
                    self.create_client() 
                else: 
                    if(logged_user) & (session.prompt('\nCreate contract ? ')=='y'): 
                        self.create_contract() 
                    else: 
                        if(logged_user) & (session.prompt('\nCreate event ? ')=='y'): 
                            self.create_event() 


    # ======== Create ======== # 
    # TODO: prompt data + retour dans l'application if False. 
    def create_user(self): 
        """ Creates a new user, following the prompted data. 
            Permission: GESTION 
            Returns: 
                object User: The just created User instance, 
                    or false if the user does not have the permission to create it. 
        """ 
        if user_session == 'GESTION': 
            print('self.registered CL90 create_user : ', self.registered) 
            user_3 = self.registered['users'][2] 
            new_user = self.manager.add_user( 
                user_3['name'], 
                user_3['email'], 
                user_3['phone'], 
                user_3['department_name']  
            ) 
            new_user_db = self.manager.select_one_user('name', fields[0]) 
            return new_user 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 

    # TODO: prompt data + retour dans l'application if False. 
    def create_client(self): 
        """ Creates a new client, following the prompted data. 
            Permission: COMMERCE 
            Returns: 
                object Client: The just created Client instance, 
                    or false if the user does not have the permission to create it. 
        """ 
        if user_session == 'COMMERCE': 
            print('self.registered CL106 create_client : ', self.registered) 
            client_1 = self.registered['clients'][0] 
            new_client = self.manager.add_client( 
                client_1['name'], 
                client_1['email'], 
                client_1['phone'], 
                client_1['corporation_name'], 
                logged_user.id 
            ) 
            new_client_db = self.manager.select_one_client('name', client_1['name']) 
            print(f'Le client {new_client_db.name} (id : {new_client_db.id}) a bien été créé.') 
            return new_client_db 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 

    # TODO: prompt data + retour dans l'application if False. 
    def create_contract(self): 
        """ Calls the manager.add_contract, sending the prompted data. 
            Permission: GESTION 
            Returns: 
                object Contract: The just created Contract instance, 
                    or false if the user does not have the permission to create it. 
        """ 
        if user_session == 'GESTION': 
            print('self.registered["contracts] CL149 create_contract : ', self.registered['contracts']) 
            contract_1 = self.registered['contracts'][0] 
            new_contract = self.manager.add_contract( 
                contract_1['client_name'], 
                contract_1['amount'], 
                contract_1['paid_amount'], 
                contract_1['is_signed'] 
            ) 
            new_contract_db = self.manager.select_one_contract('id', 1) 
            # new_client_db = self.manager.select_one_client('name', 'client 1') 
            print(f'Le contrat {new_contract_db.id} (du client {new_contract_db.client_name}) a bien été créé.') 
            return new_contract_db 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 

    # TODO: prompt data + retour dans l'application if False. 
    def create_event(self): 
        """ Calls the manager.add_event, sending the prompted data. The 'support_contact_id' is let empty. 
            A Gestion user will fill it. 
            Permission: COMMERCE 
            Returns: 
                object Event: The just created Event instance, 
                    or false if the user does not have the permission to create it. 
        """ 
        if user_session == 'COMMERCE': 
            contract_db = self.manager.select_one_contract('id', 1) 
            if contract_db.is_signed == 1: 
                print('self.registered["events"] CL171 create_event : ', self.registered['events']) 
                event_1 = self.registered['events'][0] 
                new_event = self.manager.add_event( 
                    event_1= ['name'], 
                    event_1= ['contract_id'], 
                    event_1= ['start_datetime'], 
                    event_1= ['end_datetime'], 
                    # event_1= ['support_contact_name'], 
                    event_1= ['location'], 
                    event_1= ['Attendees'], 
                    event_1= ['notes'] 
                ) 
                new_event_db = self.manager.select_one_event('id', 1) 
                # new_client_db = self.manager.select_one_client('name', 'client 1') 
                print(f'L\'événement {new_event_db.name} (id : {new_event_db.id}) a bien été créé.') 
                return new_event_db 
            else: 
                print(f'Le contrat numéro {contract_db.id} n\'est pas signé, recontactez le client avant de créer l\'événement.') 
                return False 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    # ======== Modify ======== # 
    # TODO: prompt data + retour dans l'application if False. 
    def modify_user(self, id, field, new_value): 
        """ Modifies a user, following the prompted data. 
            Permission: GESTION 
            paparms: 
                id (int): The id of the user to modify. 
                field (str): The name of the field to modify. 
                new_value (str): The new value to register. 
            Returns: 
                object User: The just modified User instance, 
                    or false if the user does not have the permission to create it. 
        """ 
        if user_session == 'GESTION': 
            # TODO: to put into the menu 
            user_to_modify = self.manager.select_one_user('name', 'support_user 1') 
            confirmation = session.prompt(f'\nVoulez-vous modifier l\'utilisateur {user_to_modify.name} (id : {user_to_modify.id}) ? (y/n) ') 
            modified_user = self.manager.update_user(user_to_modify.id, 'email', 'support_user_1@mail.org') 
            if confirmation: 
                modified_user_db = self.manager.select_one_user('id', user_to_modify.id) 
                print(f'L\'utilisateur {modified_user_db.id} été supprimé.') 
                return modified_user_db 
            else: 
                print('Vous avez annulé la suppression, l\'utilisateur n\'a pas été supprimé.') 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    # TODO: prompt data + retour dans l'application if False. 
    def modify_client(self, id, field, new_value): 
        """ Modifies a client, following the prompted data. 
            Permission: COMMERCE, who is referenced as the client's contact. 
            paparms: 
                id (int): The id of the client to modify. 
                field (str): The name of the field to modify. 
                new_value (str): The new value to register. 
            Returns: 
                object Client: The just modified Client instance, 
                    or false if the user does not have the permission to create it. 
        """ 
        if user_session == 'COMMERCE': 
            client_to_modify = self.manager.select_one_client('id', 1) 
            if client_to_modify.sales_contact_id == logged_user.id: 
                # TODO: to put into the menu 
                # user_name = session.prompt('\nQuel est le nom complet de l\'utilisateur à modifier ? ') 
                # user_to_modify = self.manager.select_one_user('name', user_name) 
                modified_client = self.manager.update_client(id, 'email', 'client_1@mail.com') 
                modified_client_db = self.manager.select_one_client('id', client_to_modify.id) 
                return modified_client_db 
            else: 
                print('Vous n\'avez pas l\'autorisation d\'effectuer cette action (département Commerce).') 
                return False 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action (Commercial responsable du client).') 
            return False 


    # TODO: prompt data + retour dans l'application if False. 
    def modify_contract(self, id, field, new_value): 
        """ Modifies a contract, following the prompted data. 
            Permission: COMMERCE, who is referenced as the client's contact. 
            paparms: 
                id (int): The id of the contract to modify. 
                field (str): The name of the field to modify. 
                new_value (str): The new value to register. 
            Returns: 
                object Contract: The just modified Contract instance, 
                    or false if the user does not have the permission to create it. 
        """ 
        if user_session == 'COMMERCE': 
            contract_to_modify = self.manager.select_one_contract('id', 1) 
            contract_to_modify_sales_contact = contract_to_modify.client_id.sales_contact_id 
            if contract_to_modify_sales_contact == logged_user.id: 
                # TODO: to put into the menu 
                modified_contract = self.manager.update_contract(contract_to_modify.id, 'paid_amount', 700) 
                modified_contract_db = self.manager.select_one_contract('id', contract_to_modify.id) 
                return modified_contract_db 
            else: 
                print('Vous n\'avez pas l\'autorisation d\'effectuer cette action (département Commerce).') 
                return False 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action (Commercial responsable du client).') 
            return False 


    # TODO: prompt data + retour dans l'application if False. 
    def modify_event(self, id, field, new_value):  # TODO 
        """ Modifies a event, following the prompted data. 
            Permission: GESTION. 
            paparms: 
                id (int): The id of the event to modify. 
                field (str): The name of the field to modify. 
                new_value (str): The new value to register. 
            Returns: 
                object Contract: The just modified Event instance, 
                    or false if the user does not have the permission to create it. 
        """ 
        if user_session == 'GESTION': 
            event_to_modify = self.manager.select_one_event('id', 1) 
            # TODO: to put into the menu 
            support_contact_id = self.manager.select_one_user('name', 'support_user 1') 
            modified_event = self.manager.update_event(event_to_modify.id, 'support_contact_id', support_contact_id) 
            modified_event_db = self.manager.select_one_event('id', event_to_modify.id) 
            return modified_event_db 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action (département Gestion).') 
            return False 





    # # ==== Utiliser ça ou pas ? ==== # 
    # # Essai décorateur verify jwt (à faire, sur méthodes d'actions conditionnelles) 
    # def check_permission(self): 
    #     tokened = self.manager.verify_token( 
    #         userConnect['email'], 
    #         password, 
    #         logged_user.department.name 
    #     ) 
    #     # TODO: sortie propre après l'échec du token 
    #     if not tokened: 
    #         print('Vous n\'avez pas de rôle défini, contactez le service info.') 
    #         return False 
    #     else: 
    #         self.user_session = 'GESTION' 
    #         print('autorisation gestion ok') 
    #         return True 
    # # ==== /Utiliser ça ou pas ? ==== # 

# ==== Pour aide navigation et menus ==== # 
def copy_start(self, new_session=False): 
        """ Displays the menus and manages the logic of the application.  
            Args:
                new_session (boolean), default=False. 
                    If True -> displays the menu and the welcome message, 
                                and authorizes to create players and tournament, and reports. 
                    else -> displays only the menu, 
                            and authorizes to register scores, close a round 
                            and a tournament, and reports. 
        """ 

        # Check if a tournament isn't closed yet, 
        # then set the new_session to False, 
        # else set it to True. 
        last_tournament = helpers.select_one_tournament('last') 

        if last_tournament: 
            if last_tournament.end_date == '': 
                new_session = False 
            else: 
                new_session = True 
        else: 
            new_session = True 
            last_tournament = None 

        if new_session: 
            self.board.display_welcome() 
        self.board.display_first_menu() 


        # ======== "R E G I S T E R"  M E N U S ======== # 

        # ==== menu "enregistrer" ==== # 
        if self.board.ask_for_menu_action == '1': 
            self.board.ask_for_menu_action = None 

            # Displays only the useful menus 
            if new_session: 
                self.board.display_register([0, 1, 2, 3]) 
            else: 
                items = [] 
                items.append(0) 
                for i in range(4, 7): 
                    items.append(i) 
                self.board.display_register(items) 


            # ==== Registers one player ==== # 
            if self.board.ask_for_register == '1': 
                self.board.ask_for_register = None 

                print('\nEnregistrer un joueur') 
                self.register_controller.enter_new_player() 
                # serializes player 

                self.press_enter_to_continue() 
                self.start() 
# ==== /Pour aide navigation et menus ==== # 

