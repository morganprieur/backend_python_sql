
from dashboard import Dashboard 
from manager import Manager 
from models import Base, Client, Contract, Department, Event, User  
from views import Views 

from datetime import datetime, timedelta 
import json 
import os 
import re 
import time 

from sentry_sdk import capture_message 
# capture_message('Something went wrong') 


class Controller(): 
    print(f'hello controller') 
    def __init__(self, role): 
        self.dashboard = Dashboard() 
        self.views = Views() 
        self.manager = Manager() 
        self.manager.connect() 
        self.manager.create_session() 

        self.user_session = None 
        self.role = role 
        with open(os.environ.get('FILE_PATH'), 'r') as users_file: 
            self.registered = json.load(users_file) 


    def start(self, mode): 
        """ This method starts the application. 
            Pre-required: 
                The setup.py script has to be called to install the tables and the 
                first data, for allowing to use the app. 
            Args: 
                mode (str): The mode to enter the user credentials
                    'dev': the data are getting from the data.json file, 
                    'pub': the data has to be entered by the user. 
        """ 
        if mode is None: 
            print('Vous devez indiquer un mode de récupération des informations de connexion : "python project.py <dev/pub>.') 

        if self.user_session is None: 
            if self.role is not None: 
                self.connect_user(mode) 
            else: 
                self.connect_user(mode, None) 


        # ======== M E N U ======== # 

        # Displays only the useful menus, depending on the connected user  
        if self.user_session in ['GESTION', 'COMMERCE', 'SUPPORT']: 
            self.display_roles_menus() 
        else: 
            print('DEBUG self.user_session CL56 :',self.user_session) 
            print('Ce mail n\'est pas enregistré, veuillez contacter un administrateur.') 
            self.close_the_app() 
            return False 

        # ======== M E N U  C H O I C E S ======== # 
        # ==== Registers one dept ==== # 
        if self.dashboard.ask_for_action == '1': 
            self.dashboard.ask_for_action = None 

            self.register_dept() 

            self.views.enter_to_continue() 
            self.start(mode) 

        # ==== Registers one user ==== # 
        if self.dashboard.ask_for_action == '2': 
            self.dashboard.ask_for_action = None 

            self.register_user(mode) 
            # from sentry_sdk import capture_message 
            capture_message('Un utilisateur a été créé. ') 

            self.views.enter_to_continue() 
            self.start(mode) 

        # ==== Registers one client ==== # 
        if self.dashboard.ask_for_action == '3': 
            self.dashboard.ask_for_action = None 

            self.register_client(mode) 

            self.views.enter_to_continue() 
            self.start(mode) 

        # ==== Registers one contract ==== # 
        if self.dashboard.ask_for_action == '4': 
            self.dashboard.ask_for_action = None 

            self.register_contract(mode) 

            self.views.enter_to_continue() 
            self.start(mode) 

        # ==== Registers one event ==== # 
        if self.dashboard.ask_for_action == '5': 
            self.dashboard.ask_for_action = None 

            self.register_event(mode) 

            self.views.enter_to_continue() 
            self.start(mode) 

        # ==== Modifies one department ==== # 
        if self.dashboard.ask_for_action == '6': 
            self.dashboard.ask_for_action = None 

            self.modify_dept() 

            self.views.enter_to_continue() 
            self.start(mode) 

        # ==== Modifies one user ==== # 
        if self.dashboard.ask_for_action == '7': 
            self.dashboard.ask_for_action = None 

            self.modify_user() 
            # from sentry_sdk import capture_message 
            capture_message('Un utilisateur a été modifié. ') 

            self.views.enter_to_continue() 
            self.start(mode) 

        # ==== Modifies one client ==== # 
        if self.dashboard.ask_for_action == '8': 
            self.dashboard.ask_for_action = None 

            self.modify_client() 

            self.views.enter_to_continue() 
            self.start(mode) 

        # ==== Modifies one contract ==== # 
        if self.dashboard.ask_for_action == '9': 
            self.dashboard.ask_for_action = None 

            self.modify_contract() 
            # from sentry_sdk import capture_message 
            capture_message('Un contrat a été modifié. ') 

            self.views.enter_to_continue() 
            self.start(mode) 

        # ==== Modifies one event ==== # 
        if self.dashboard.ask_for_action == '10': 
            self.dashboard.ask_for_action = None 

            self.modify_event() 

            self.views.enter_to_continue() 
            self.start(mode) 

        # ==== Deletes one user ==== # 
        if self.dashboard.ask_for_action == '11': 
            self.dashboard.ask_for_action = None 

            self.delete_user() 

            self.views.enter_to_continue() 
            self.start(mode) 

        # ==== Displays all departments ==== # 
        if self.dashboard.ask_for_action == '12': 
            self.dashboard.ask_for_action = None 

            self.show_all_depts() 

            self.views.enter_to_continue() 
            self.start(mode) 

        # ==== Displays all users ==== # 
        if self.dashboard.ask_for_action == '13': 
            self.dashboard.ask_for_action = None 

            self.show_all_users() 

            self.views.enter_to_continue() 
            self.start(mode) 

        # ==== Displays all clients ==== # 
        if self.dashboard.ask_for_action == '14': 
            self.dashboard.ask_for_action = None 

            self.show_all_clients() 

            self.views.enter_to_continue() 
            self.start(mode) 

        # ==== Displays all contracts ==== # 
        if self.dashboard.ask_for_action == '15': 
            self.dashboard.ask_for_action = None 

            self.show_all_contracts() 

            self.views.enter_to_continue() 
            self.start(mode) 

        # ==== Displays all events ==== # 
        if self.dashboard.ask_for_action == '16': 
            self.dashboard.ask_for_action = None 

            self.show_all_events() 

            self.views.enter_to_continue() 
            self.start(mode) 

        # ==== Displays one department ==== # 
        if self.dashboard.ask_for_action == '17': 
            self.dashboard.ask_for_action = None 

            self.show_one_dept() 

            self.views.enter_to_continue() 
            self.start(mode) 

        # ==== Displays one user ==== # 
        if self.dashboard.ask_for_action == '18': 
            self.dashboard.ask_for_action = None 

            self.show_one_user() 

            self.views.enter_to_continue() 
            self.start(mode) 

        # ==== Displays one client ==== # 
        if self.dashboard.ask_for_action == '19': 
            self.dashboard.ask_for_action = None 

            self.show_one_client() 

            self.views.enter_to_continue() 
            self.start(mode) 

        # ==== Displays one contract ==== # 
        if self.dashboard.ask_for_action == '20': 
            self.dashboard.ask_for_action = None 

            self.show_one_contract() 

            self.views.enter_to_continue() 
            self.start(mode) 

        # ==== Displays one event ==== # 
        if self.dashboard.ask_for_action == '21': 
            self.dashboard.ask_for_action = None 

            self.show_one_event() 

            self.views.enter_to_continue() 
            self.start(mode) 

        # ==== Displays events that don't have 'support' contact ==== # 
        if self.dashboard.ask_for_action == '22': 
            self.dashboard.ask_for_action = None 

            self.show_events_without_support() 

            self.views.enter_to_continue() 
            self.start(mode) 

        # ==== Displays clients of one 'commerce' user ==== # 
        if self.dashboard.ask_for_action == '23': 
            self.dashboard.ask_for_action = None 

            show_clients_of_commerce_user() 

            self.views.enter_to_continue() 
            self.start(mode) 

        # ==== Displays contracts of one 'commerce' user ==== # 
        if self.dashboard.ask_for_action == '24': 
            self.dashboard.ask_for_action = None 

            self.show_contracts_of_commerce_user() 

            self.views.enter_to_continue() 
            self.start(mode) 

        # ==== Displays not paid contracts ==== # 
        if self.dashboard.ask_for_action == '25': 
            self.dashboard.ask_for_action = None 

            self.show_not_paid_contracts() 

            self.views.enter_to_continue() 
            self.start(mode) 

        # ==== Displays not signed contracts ==== # 
        if self.dashboard.ask_for_action == '26': 
            self.dashboard.ask_for_action = None 

            self.show_not_signed_contracts() 

            self.views.enter_to_continue() 
            self.start(mode) 

        # ==== Displays events of one 'support' user ==== # 
        if self.dashboard.ask_for_action == '27': 
            self.dashboard.ask_for_action = None 

            self.show_events_support_user() 

            self.views.enter_to_continue() 
            self.start(mode) 

        # ==== QUIT THE APP ==== #  
        if self.dashboard.ask_for_action == '0': 
            self.dashboard.ask_for_action = None 
            self.close_the_app() 


    def connect_user(self, mode): 
        """ Connects a user to the application. 
            Process: 
                - Compare the email with the registered email 
                If email does not exist: 
                    message
                    quit the app. 
                else: 
                    - Check if the token exists 
                    if token does not exist: 
                        ask for password 
                        if pw ok: 
                            get token 
                            register token 
                            return permission = dept.upper() 
                        if pw NOT ok: 
                            message
                            quit the app. 
                    if token exists: 
                        If token is not ok: 
                            message 
                            quit the app. 
                        If token ok and NOT expired: 
                            return permission = dept.upper() 
                        If token ok and expired: 
                            return 'past' 
            Args: 
                mode (str): The mothod to send the user credentials 
                    'dev': getting the data from the data.json file. 
                    'pub': the user has to enter the data with the keyboard. 
            Returns: 
                User instance: the connected user. 
        """ 
        print('DEBUG connect_user mode de saisie (dev / pub) : ', mode) 
        print('DEBUG connect_user role user (admin / sales / support) : ', self.role) 
        userConnect = {} 
        if mode == 'pub': 
            # Type the required credentials: 
            userConnect['email'] = self.views.input_user_connection_email() 
            # Check the format of the email 
            print(f"|{userConnect['email']}|") 
            reg = '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,6}' 
            if re.match(reg, userConnect['email']): 
                print('Ce mail est valide. ') 
            else: 
                print('Ce mail n\'est pas valide. ') 
                return False 
        elif mode == 'dev': 
            # file deepcode ignore PT: local project 
            # with open(os.environ.get('FILE_PATH'), 'r') as jsonfile: 
            #     self.registered = json.load(jsonfile) 
                userConnect = {} 
                if self.role == 'admin': 
                    userConnect = self.registered['users'][0] 
                    userConnect['pass'] = os.environ.get('USER_1_PW') 
                elif self.role == 'sales': 
                    userConnect = self.registered['users'][1] 
                    userConnect['pass'] = os.environ.get('USER_2_PW') 
                elif self.role == 'support': 
                    userConnect = self.registered['users'][2] 
                    userConnect['pass'] = os.environ.get('U_3_PW') 
                else: 
                    print(f'Cet argument n\'est pas reconnu ({self.role}). Veuillez contacter un administrateur. ') 
        else: 
            print(f'Cet argument n\'est pas reconnu ({mode}). Vous devez utiliser "dev" ou "pub".') 

        # Check the email with the registered emails into the DB 
        # print('DEBUG userEmail CL363 :', userConnect['email']) 
        self.logged_user = self.manager.select_one_user( 
            'email', 
            userConnect['email'] 
        ) 
        if self.logged_user: 
            # Check if the token exists 
            row = self.manager.verify_if_token_exists( 
                self.logged_user.email) 
            if row is not None: 
                # Check token for connected user + department 
                token_check = self.manager.verify_token( 
                    self.logged_user.email, 
                    self.logged_user.department.name, 
                    row 
                ) 

                if token_check == 'past': 
                    userPass = '' 
                    if mode == 'dev': 
                        userPass = userConnect['pass'] 
                    elif mode == 'pub': 
                        userPass = self.views.input_user_connection_pass() 
                    print(f'input pass CL397 : |{userPass}|') 
                    pw_check = self.check_pw(mode, userPass) 
                    if pw_check: 
                        token = self.manager.get_token(60, { 
                            'email': self.logged_user.email, 
                            'dept': self.logged_user.department.name 
                        }) 
                        self.manager.register_token( 
                            self.logged_user.email, 
                            token 
                        ) 

                        row = self.manager.verify_if_token_exists( 
                            self.logged_user.email 
                        ) 
                        self.user_session = self.manager.verify_token( 
                            self.logged_user.email, 
                            self.logged_user.department.name, 
                            row 
                        ) 

                        print('Un token a été enregistré. ') 
                        self.dashboard.display_welcome( 
                            self.logged_user.name, 
                            self.logged_user.department.name 
                        ) 
                        self.views.enter_to_continue() 

                elif token_check in ['GESTION', 'COMMERCE', 'SUPPORT']: 
                    print('Un token est enregistré. ') 
                    # print('self.user_session :', self.user_session) 
                    self.user_session = token_check 
                    print('DEBUG self.user_session :', self.user_session) 
                    self.dashboard.display_welcome( 
                        self.logged_user.name, 
                        self.logged_user.department.name 
                    ) 
                    self.views.enter_to_continue() 

            else: 
                userPass = '' 
                if mode == 'dev': 
                    userPass = userConnect['pass'] 
                elif mode == 'pub': 
                    userPass = self.views.input_user_connection_pass() 
                print(f'input pass CL456 : |{userPass}|') 
                if self.check_pw( 
                    mode, 
                    userPass 
                ): 
                    token = self.manager.get_token(60, { 
                        'email': self.logged_user.email, 
                        'dept': self.logged_user.department.name 
                    }) 
                    self.manager.register_token( 
                        self.logged_user.email, token) 

                    row = self.manager.verify_if_token_exists( 
                        self.logged_user.email 
                    ) 
                    token_check = self.manager.verify_token( 
                        self.logged_user.email, 
                        self.logged_user.department.name, 
                        row 
                    ) 

                    if token_check in ['GESTION', 'COMMERCE', 'SUPPORT']: 
                        print('Un token a été enregistré. ') 
                        # print('self.user_session CL479 :', self.user_session) 
                        self.user_session = token_check 
                        print('self.user_session CL481 :', self.user_session) 
                        self.dashboard.display_welcome( 
                            self.logged_user.name, 
                            self.logged_user.department.name 
                        ) 
                        self.views.enter_to_continue() 

                else: 
                    print('Les informations saisies ne sont pas bonnes, veuillez contacter un administrateur.')                 
                    self.close_the_app() 
        else: 
            return False 


    # ==== register methods ==== # 
    def register_dept(self): 
        """ Registers one department with the data entered into the terminal. 
            Only Gestion users are allowed to do this. 
            Returns: 
                Department object: The just created department instance. 
        """ 
        if self.user_session == 'GESTION': 
            print('\nEnregistrer un département') 
            fields = self.views.input_create_dept() 

            if fields['name'] == '*': 
                print('Vous avez tapé *, vous allez être redirigé vers le menu.') 
            else: 
                self.register_confirmation_process('dept', fields) 

        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 

    def register_user(self, mode): 
        """ Registers one user with the data entered into the terminal. 
            Only the gestion users are allowed to do this. 
            The password is hashed, the token is registered into the encrypted file. 
            Returns: 
                User object: The just created user instance. 
        """ 
        if self.user_session == 'GESTION': 
            print('\nEnregistrer un utilisateur') 
            fields = {} 
            if mode == 'dev': 
                user_role = self.views.input_user_role() 
                users = self.registered['users'] 
                if user_role == '*': 
                    print('Vous avez tapé *, vous allez être redirigé vers le menu.') 
                elif user_role == 'sales': 
                    fields = users['users'][1] 
                    fields['entered_password'] = os.environ.get('USER_2_PW') 
                elif user_role == 'support': 
                    fields = users['users'][2] 
                    fields['entered_password'] = os.environ.get('U_3_PW') 
                else: 
                    print('Cet utilisateur n\'existe pas. ') 
                    return False 
            elif mode == 'pub': 
                fields = self.views.input_create_user() 
                if fields['name'] == '*': 
                    print('Vous avez tapé *, vous allez être redirigé vers le menu.') 
            else: 
                print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
                return False 
            self.register_confirmation_process('user', fields) 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 

    def register_client(self, mode): 
        """ Registers one client with the data entered into the terminal. 
            Only the 'commerce' users are allowed to do this. 
            Returns: 
                Client object: The just created client instance. 
        """ 
        if self.user_session == 'COMMERCE': 
            print('\nEnregistrer un client') 
            if mode == 'dev': 
                clients = self.registered['clients'] 
                fields = clients[0] 
            elif mode == 'pub': 
                fields = self.views.input_create_client() 
                if fields['name'] == '*': 
                    print('Vous avez tapé *, vous allez être redirigé vers le menu.') 
                    return false 
            else: 
                print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
                return False 
            fields['sales_contact_id'] = self.logged_user.id 
            self.register_confirmation_process('client', fields) 

        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 

    def register_contract(self, mode): 
        """ Registers one contract with the data entered into the terminal. 
            Only the 'gestion' users are allowed to do this. 
            Returns: 
                Contract object: The just created contract instance. 
        """ 
        if self.user_session == 'GESTION': 
            print('\nEnregistrer un contrat') 
            if mode == 'dev': 
                contracts = self.registered['contracts'] 
                fields = contracts[0] 
            elif mode == 'pub': 
                fields = self.views.input_create_contract() 
                if fields['client_name'] == '*': 
                    print('Vous avez tapé *, vous allez être redirigé vers le menu.') 
                    return False 
            else: 
                print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
                return False 
            self.register_confirmation_process('contract', fields) 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 

    def register_event(self, mode): 
        """ Registers one event with the data entered into the terminal. 
            Only the 'commerce' users are allowed to do this. 
            Returns: 
                Event object: The just created event instance. 
        """ 
        if self.user_session == 'COMMERCE': 
            print('\nEnregistrer un événement') 

            print('\nSélectionner un contract : ') 
            fields = self.views.input_select_entity('contract') 
            contract = self.manager.select_one_contract( 
                fields['field_to_select'], 
                fields['value_to_select'] 
            ) 
            if not contract.is_signed: 
                print(f"Le contrat {contract.id} n\'est pas signé, vous ne pouvez pas créer d\'événement.") 
            else: 
                if mode == 'dev': 
                    events = self.registered['events'] 
                    event = events[0] 
                    event['contract_id'] = fields['value_to_select']
                elif mode == 'pub': 
                    fields = self.views.input_create_event() 
                    fields['contract_id'] = fields['value_to_select']

                    if fields['name'] == '*': 
                        print('Vous avez tapé *, vous allez être redirigé vers le menu.') 
                else: 
                    print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
                    return False 
                self.register_confirmation_process('event', fields) 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    # ==== modify methods ==== # 
    def modify_dept(self): 
        """ Modifies one department, entering the field and the new value to register. 
            Only the 'gestion' users are allowed to do this. 
            Returns: 
                Department object: The modified department instance. 
        """ 
        if self.user_session == 'GESTION': 
            print('\nModifier un département') 
            dept_to_select = self.views.input_select_entity('dept') 

            if dept_to_select['field_to_select'] == '*': 
                print('Vous avez tapé *, vous allez être redirigé vers le menu.') 
                return False 
            else: 
                dept_to_modify = self.manager.select_one_dept( 
                    dept_to_select['field_to_select'], 
                    dept_to_select['value_to_select'] 
                ) 
                fields = self.views.input_modify_dept(dept_to_modify) 

                # Confirmation : 
                confirmation = self.views.ask_for_confirmation( 
                    'modifier', 
                    'dept' 
                ) 
                if (confirmation == 'y') | (confirmation == 'Y'): 
                    modified_item = self.manager.update_dept( 
                        dept_to_modify, 
                        dept_to_select['value_to_select'], 
                        fields['new_name'] 
                    ) 
                    print(f"Le nom du département {modified_item.id} a bien été modifié : {modified_item}. ") 
                    return modified_item 
                else: 
                    print('Vous avez annulé la modification, le département n\'a pas été modifié.') 
                    return False 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 

    def modify_user(self): 
        """ Modifies a User instance, entering the field to modify and the new value to register. 
            A User instance needs to get the password hashed, and a token, depending of his/her 
            department, created. The controller does it, in order to send the manager, only the data to register. 
            All operations have already been done. 
            Returns: 
                User object: The modified User instance. 
        """ 
        if self.user_session == 'GESTION': 
            print('\nModifier un utilisateur') 
            user_to_select = self.views.input_select_entity('user') 

            if user_to_select['field_to_select'] == '*': 
                print('Vous avez tapé *, vous allez être redirigé vers le menu.') 
                return False 
            else: 
                user_to_modify = self.manager.select_one_user( 
                    user_to_select['field_to_select'], 
                    user_to_select['value_to select'] 
                ) 

                fields = self.views.input_modify_entity( 
                    'user', 
                    user_to_modify 
                ) 

                if fields['field_to_modify'] == 'password': 
                    hash_new_pw = self.manager.hash_pw(fields['new_value']) 
                    fields['new_value'] = hash_new_pw 

                fields[fields['field_to_modify']] = fields['new_value'] 

                self.modify_confirmation_process( 
                    user_to_modify, 
                    fields['field_to_modify'], 
                    fields 
                ) 

        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 

    def modify_client(self): 
        """ Modifies one client, entering the field and the new value to register. 
            Only the 'commerce' users are allowed to do this. 
            Returns: 
                Client object: The modified client instance. 
        """ 
        if self.user_session == 'COMMERCE': 
            print('\nModifier un client') 
            client_to_select = self.views.input_select_entity('client') 

            if client_to_select['field_to_select'] == '*': 
                print('Vous avez tapé *, vous allez être redirigé vers le menu.') 
                return False 
            else: 
                client_to_modify = self.manager.select_one_client( 
                    client_to_select['field_to_select'], 
                    client_to_select['value_to_select'] 
                ) 
                fields = self.views.input_modify_entity( 
                    'client', 
                    client_to_modify 
                ) 

                fields[fields['field_to_modify']] = fields['new_value'] 

                self.modify_confirmation_process( 
                    client_to_modify, 
                    fields['field_to_modify'], 
                    fields 
                ) 

        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 

    def modify_contract(self): 
        """ Modifies one contract, entering the field and the new value to register. 
            Only the 'commerce' and 'gestion' users are allowed to do this. 
            Returns: 
                Contract object: The modified contract instance. 
        """ 
        if (self.user_session == 'GESTION') | (self.user_session == 'COMMERCE'): 
            print('\nModifier un contrat') 
            contract_to_select = self.views.input_select_entity('contract') 

            if contract_to_select['field_to_select'] == '*': 
                print('Vous avez tapé *, vous allez être redirigé vers le menu.') 
                return False 
            else: 
                contract_to_modify = self.manager.select_one_contract( 
                    contract_to_select['field_to_select'], 
                    contract_to_select['value_to_select'] 
                ) 

                fields = self.views.input_modify_entity( 
                    'contract', 
                    contract_to_modify 
                ) 
                # fields = self.views.input_modify_contract( 
                #     contract_to_modify 
                # ) 
                fields['new_value'] = bool(fields['new_value']) 


                self.modify_confirmation_process( 
                    'contract', 
                    contract_to_modify, 
                    fields['field_to_modify'], 
                    fields 
                ) 

        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 

    def modify_event(self): 
        """ Modifies one event, entering the field and the new value to register. 
            Only the 'gestion' and 'support' users are allowed to do this. 
            Returns: 
                Event object: The modified event instance. 
        """ 
        if (self.user_session == 'GESTION') | (self.user_session == 'SUPPORT'): 
            print('\nModifier un événement') 
            event_to_select = self.views.input_select_entity('event') 

            if event_to_select['field_to_select'] == '*': 
                print('Vous avez tapé *, vous allez être redirigé vers le menu.') 
                return False 
            else: 
                event_to_modify = self.manager.select_one_event( 
                    event_to_select['field_to_select'], 
                    event_to_select['value_to_select'] 
                ) 

                if self.user_session == 'GESTION': 
                    fields = self.views.input_modify_entity( 
                        'event', 
                        event_to_modify, 
                        gestion=True 
                    ) 

                    fields[fields['field_to_modify']] = fields['new_value'] 

                    self.modify_confirmation_process( 
                        'event', 
                        event_to_modify, 
                        fields['field_to_modify'], 
                        fields 
                    ) 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    # ==== delete method ==== # 
    def delete_user(self): 
        """ Deletes one user from the DB. Only a user who does not have any client can be deleted. 
            Only the 'gestion' users are allowed to do this. 
            Returns: 
                bool: True if it has been deleted, False instead. 
        """ 
        if self.user_session == 'GESTION': 
            print('\nSupprimer un utilisateur') 
            user_to_select = self.views.input_select_entity('user') 

            if user_to_select['field_to_select'] == '*': 
                print('Vous avez tapé *, vous allez être redirigé vers le menu.') 
            else: 
                self.confirmation_process(fields, 'supprimer', 'user') 

        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    # ==== show all methods ==== # 
    def show_all_depts(self): 
        """ Displays all departments. 
            Only 'gestion' users are allowed to do this. 
            Returns: 
                list: The registered department instances. 
        """ 
        print('\nAfficher tous les départements ') 
        if self.user_session == 'GESTION': 
            depts = self.manager.select_all_entities('depts') 
            if depts != []: 
                print(f'Il y a {len(depts)} départements : ') 
                self.views.display_entity(depts) 
                return depts 
            else: 
                print('Il n\'y a aucun département à afficher. ') 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 

    def show_all_users(self): 
        """ Displays all users. 
            Only 'gestion' users are allowed to do this. 
            Returns: 
                list: The registered user instances. 
        """ 
        print('\nAfficher tous les utilisateurs ') 
        if self.user_session == 'GESTION': 
            users = self.manager.select_all_entities('users') 
            if users != []: 
                print(f'Il y a {len(users)} utilisateurs : ') 
                self.views.display_entity(users) 
                return users 
            else: 
                print('Il n\'y a aucun utilisateur à afficher. ') 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 

    def show_all_clients(self): 
        """ Displays all clients. 
            All the connected users are allowed to do this. 
            Returns: 
                list: The registered client instances. 
        """ 
        print('\nAfficher tous les clients ') 
        if self.user_session in ['GESTION', 'COMMERCE', 'SUPPORT']: 
            clients = self.manager.select_all_entities('clients') 
            if clients != []: 
                print(f'Il y a {len(clients)} clients : ') 
                self.views.display_entity(clients) 
                return clients 
            else: 
                print('Il n\'y a aucun client à afficher. ') 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 

    def show_all_contracts(self): 
        """ Displays all contracts. 
            All the connected users are allowed to do this. 
            Returns: 
                list: The registered contract instances. 
        """ 
        print('\nAfficher tous les contrats ') 
        if self.user_session in ['GESTION', 'COMMERCE', 'SUPPORT']:  
            contracts = self.manager.select_all_entities('contracts') 
            if contracts != []: 
                print(f'Il y a {len(contracts)} contrats : ') 
                self.views.display_entity(contracts) 
                return contracts 
            else: 
                print('Il n\'y a aucun contrat à afficher. ') 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 

    def show_all_events(self): 
        """ Displays all events. 
            All the connected users are allowed to do this. 
            Returns: 
                list: The registered events instances. 
        """ 
        print('\nAfficher tous les événementss ') 
        if self.user_session in ['GESTION', 'COMMERCE', 'SUPPORT']:  
            events = self.manager.select_all_entities('events') 
            if events != []: 
                print(f'Il y a {len(events)} événements : ') 
                self.views.display_entity(events) 
                return events 
            else: 
                print('Il n\'y a aucun événement à afficher. ') 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    # ==== show one methods ==== # 
    def show_one_dept(self): 
        """ Displays one department. 
            Only 'gestion' users are allowed to do this. 
            Returns: 
                Department object: The registered department instance. 
        """ 
        if self.user_session in ['GESTION', 'COMMERCE', 'SUPPORT']: 
            print('\nAfficher un département') 
            dept_to_select = self.views.input_select_entity('dept') 

            if dept_to_select['field_to_select'] == '*': 
                print('Vous avez tapé *, vous allez être redirigé vers le menu.') 
            else: 
                # print(dept_to_select) 
                dept = self.manager.select_one_dept( 
                    dept_to_select['field_to_select'], 
                    dept_to_select['value_to_select'] 
                ) 
                if dept is not None: 
                    self.views.display_entity([dept]) 
                    return dept 
                else: 
                    print('Il n\'y a aucun département avec ces informations.') 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 

    def show_one_user(self): 
        """ Displays one user. 
            Only 'gestion' users are allowed to do this. 
            Returns: 
                User object: The registered user instance. 
        """ 
        if self.user_session == 'GESTION' : 
            print('\nAfficher un utilisateur') 
            user_to_select = self.views.input_select_entity('user') 

            if user_to_select['field_to_select'] == '*': 
                print('Vous avez tapé *, vous allez être redirigé vers le menu.') 
            else: 
                user = self.manager.select_one_user( 
                    user_to_select['field_to_select'], 
                    user_to_select['value_to_select'] 
                ) 
                if user is not None: 
                    self.views.display_entity([user]) 
                    return user 
                else: 
                    print('Il n\'y a aucun utilisateur avec ces informations.') 

        elif self.user_session in ['COMMERCE', 'SUPPORT']:  
            user_to_select = self.views.input_select_entity('user') 

            if user_to_select['field_to_select'] == '*': 
                print('Vous avez tapé *, vous allez être redirigé vers le menu.') 
            else: 
                user = self.manager.select_one_user( 
                    user_to_select['field_to_select'], 
                    user_to_select['value_to_select'] 
                ) 
                if user is not None: 
                    self.views.display_user_minimum(user) 
                    return user 
                else: 
                    print('Il n\'y a aucun utilisateur avec ces informations.') 
                return user 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 

    def show_one_client(self): 
        """ Displays one client. 
            Only 'gestion' and 'commerce' users are allowed to do this. 
            Returns: 
                Client object: The registered client instance. 
        """ 
        if self.user_session in ['GESTION', 'COMMERCE', 'SUPPORT']:  
            print('\nAfficher un client') 
            client_to_select = self.views.input_select_entity('client') 

            if client_to_select['field_to_select'] == '*': 
                print('Vous avez tapé *, vous allez être redirigé vers le menu.') 
            else: 
                client = self.manager.select_one_client( 
                    client_to_select['field_to_select'], 
                    client_to_select['value_to_select'] 
                ) 
                if client is not None: 
                    self.views.display_entity([client]) 
                    return client 
                else: 
                    print('Il n\'y a aucun utilisateur avec ces informations.') 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 

    def show_one_contract(self): 
        if self.user_session in ['GESTION', 'COMMERCE', 'SUPPORT']:  
            print('\nAfficher un contrat') 
            contract_to_select = self.views.input_select_entity('contract') 

            if contract_to_select['field_to_select'] == '*': 
                print('Vous avez tapé *, vous allez être redirigé vers le menu.') 
            else: 
                contract = self.manager.select_one_contract( 
                    contract_to_select['field_to_select'], 
                    contract_to_select['value_to_select'] 
                ) 
                if contract is not None: 
                    self.views.display_entity([contract]) 
                    return contract 
                else: 
                    print('Il n\'y a aucun utilisateur avec ces informations.') 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 

    def show_one_event(self): 
        if self.user_session in ['GESTION', 'COMMERCE', 'SUPPORT']:  
            print('\nAfficher un événement') 
            event_to_select = self.views.input_select_entity('event') 

            if event_to_select['field_to_select'] == '*': 
                print('Vous avez tapé *, vous allez être redirigé vers le menu.') 
            else: 
                event = self.manager.select_one_event( 
                    event_to_select['field_to_select'], 
                    event_to_select['value_to_select'] 
                ) 
                if event is not None: 
                    self.views.display_entity([event]) 
                    return event 
                else: 
                    print('Il n\'y a aucun événement avec ces informations.') 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    # ==== show with criteria methods ==== # 
    def show_events_without_support(self): 
        """ Selects the events those don't have a support_contact_id. 
            Only "gestion" users are allowed to do this. 
            Returns: 
                List of Event instances: The list of the events, 
                or False if the user does not have the authorization to perform this. 
        """ 
        if self.user_session == 'GESTION': 
            print('\nAfficher les événements sans contact support') 
            events = self.manager.select_entities_with_criteria( 
                'events', 
                'without support', 
                self.logged_user.id 
            ) 
            self.views.display_entity([events]) 
            return events 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 

    def show_clients_of_commerce_user(self): 
        """ Selects the clients who are attached to the user. 
            Only "commerce" users are allowed to do this. 
            Returns: 
                Client instance: The list of the clients, 
                or False if the user does not have the authorization to perform this. 
        """ 
        if self.user_session == 'COMMERCE': 
            print('\nAfficher les clients d\'un utilisateur commercial') 
            clients = self.manager.select_entities_with_criteria( 
                'clients', 
                'sales contact', 
                self.logged_user.id 
            ) 
            self.views.display_entity([clients]) 
            return clients 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 

    def show_contracts_of_commerce_user(self): 
        """ Selects the contracts those are attached to the user's clients. 
            Only "commerce" users are allowed to do this. 
            Returns: 
                List of Contract instances: The list of the contracts, 
                or False if the user does not have the authorization to perform this. 
        """ 
        if self.user_session == 'COMMERCE': 
            print('\nAfficher les contrats d\'un utilisateur commercial ') 
            clients = self.manager.select_entities_with_criteria( 
                'clients', 
                'sales contact', 
                self.logged_user.id 
            ) 
            contracts = [] 
            for client in clients: 
                contract = self.manager.select_entities_with_criteria( 
                    'contracts', 
                    'client', 
                    self.logged_user.id 
                ) 
                contracts.append(contract) 
            self.views.display_entity([contracts]) 
            return contracts 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 

    def show_not_paid_contracts(self): 
        """ Selects the contracts those aren't entirely paid. 
            Only "commerce" users are allowed to do this. 
            Returns: 
                List of Contract instances: The list of the contracts, 
                or False if the user does not have the authorization to perform this. 
        """ 
        if self.user_session == 'COMMERCE': 
            print('\nAfficher les contrats non fini de payer ') 
            contracts = self.manager.select_entities_with_criteria( 
                'contracts', 
                'not paid', 
                self.logged_user.id 
            ) 
            self.views.display_entity([contracts]) 
            return contracts 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 

    def show_not_signed_contracts(self): 
        """ Selects the contracts those aren't signed. 
            Only "commerce" users are allowed to do this. 
            Returns: 
                List of Contract instances: The list of the contracts, 
                or False if the user does not have the authorization to perform this. 
        """ 
        if self.user_session == 'COMMERCE': 
            print('\nAfficher les contrats non signés ') 
            contracts = self.manager.select_entities_with_criteria( 
                'contracts', 
                'not signed', 
                self.logged_user.id 
            ) 
            self.views.display_entity([contracts]) 
            return contracts 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 

    def show_events_support_user(self): 
        """ Selects the events those are attached to the 'support' user. 
            Only "support" users are allowed to do this. 
            Returns: 
                List of Event instances: The list of the events, 
                or False if the user does not have the authorization to perform this. 
        """ 
        if self.user_session == 'SUPPORT': 
            print('\nAfficher les événements d\'un utilisateur support ') 
            events = self.manager.select_entities_with_criteria( 
                'events', 
                'support contact', 
                self.logged_user.id 
            ) 
            self.views.display_entity([events]) 
            return events 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 
    # ==== show with criteria methods ==== # 


    # ======== Utils ======== # 
    def set_session(self, dept_name): 
        """ Set the session name depending on the department of the user. 
            Args:
                dept_name (str): The department returned by the verify_token manager's method. 
        """ 
        if dept_name == 'gestion': 
            self.user_session = 'GESTION' 
        if dept_name == 'commerce': 
            self.user_session = 'COMMERCE' 
        if dept_name == 'support': 
            self.user_session = 'SUPPORT' 
        print('DEBUG : ', self.user_session) 


    def check_pw(self, mode, userPass): 
        """ Recursive method that checks the password of the user, if the token is past. 
            Args: 
                mode (str): The mode (dev or pub) wich the app has ben runned. 
                pass_counter (int): It counts the attempts to enter the password of the user. 
                self.logged_user (User instance): The user selected with his email. 
            Returns: 
                bool: True if the self.user_session has been filled, if all was alright. 
                        False instead. 
        """ 
        pass_counter = 0 
        if self.manager.check_pw( 
            self.logged_user.email, 
            userPass 
        ): 
            return True 
        else: 
            pass_counter += 1 
            if pass_counter < 3: 
                if mode == 'pub': 
                    print(f'Les informations saisies ne sont pas bonnes, merci de réessayer. \
                        Il vous reste {3-pass_counter} essais. ') 
                    userPass = self.views.input_user_connection_pass() 
                    self.check_pw(mode, pass_counter, userPass) 
                elif mode == 'dev': 
                    print('Il y a un problème avec le pw.')                 
                    self.close_the_app() 
                else: 
                    return False 


    def display_roles_menus(self): 
        gestion_menu = [1, 2, 4, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 29] 
        sales_menu = [3, 5, 8, 9, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 29] 
        support_menu = [10, 14, 15, 16, 17, 18, 19, 20, 21, 27, 29] 
        if self.user_session == 'GESTION': 
            self.dashboard.display_menu(gestion_menu) 
        elif self.user_session == 'COMMERCE': 
            self.dashboard.display_menu(sales_menu) 
        if self.user_session == 'SUPPORT': 
            self.dashboard.display_menu(support_menu) 


    def register_confirmation_process(self, entity_name, fields): 
        """ Asks for confirmation of recording an entity and receives the answer. 
            Proceeds to the action or discards the data if not confirmed. 
            If user created: a message is sent to Sentry. 
            Args: 
                fields (dict): The data to register int othe DB. 
                entity_name (str): The name of the entity in 'dept', 'user', 'client', 'contract', 'event'. 
        """ 
        entity_dict = { 
            'dept': 'Le département', 
            'user': 'L\'utilisateur', 
            'client': 'Le client', 
            'contract': 'Le contrat', 
            'event': 'L\'événement', 
        } 
        print(f'\nVoici les données à enregistrer : ') 
        self.views.display_dict(entity_name, fields) 
        confirmation = self.views.ask_for_confirmation( 
            'enregistrer', 
            entity_name 
        ) 
        if (confirmation == 'Y') | (confirmation == 'y'): 
            print(confirmation) 
            # print('entity_name CL1231 :', entity_name) 
            # print('fields CL1236 :', fields) 
            new_item = self.manager.add_entity(entity_name, fields) 
            if entity_name == 'user': 
                # # Sentry notification 
                # capture_message(f'L\'utilisateur {new_item.name} (ID {new_item.id}) a été créé. ') 
                print(f"{entity_dict[entity_name]} \"{new_item.name}\" (ID : {new_item.id}) a bien été créé. ") 
            elif entity_name == 'contract': 
                print(f"{entity_dict[entity_name]} ID {new_item.id} a bien été créé. ") 
            else: 
                print(f"{entity_dict[entity_name]} \"{new_item.name}\" (ID : {new_item.id}) a bien été créé. ") 
        else: 
            print(confirmation) 
            print('Vous avez annulé l\'opération, vous allez être redirigé vers le menu. ') 


    def modify_confirmation_process(self, entity_name, entity_to_modify, select, fields): 
        """ Asks for confirmation of modifying an entity and receives the answer. 
            Proceeds to the action or discards the data if not confirmed. 
            Not for departments. 
            Args: 
                entity (str): The name of the entity in 'dept', 'user', 'client', 'contract', 'event'. 
                entity_to_modify (obj): The entity to modify. 
                select (dict): The data to retrieve into the DB, for modifying them. 
                fiels (dict): The data to replace into the DB. 
        """ 
        # print('fields CL1333 :', fields) 
        entity_dict = { 
            'user': 'L\'utilisateur', 
            'client': 'Le client', 
            'contract': 'Le contrat', 
            'event': 'L\'événement', 
        } 
        print(f'Voici les données à modifier : ') 
        self.views.display_dict(None, fields) 
        confirmation = self.views.ask_for_confirmation( 
            'modifier', 
            entity_name 
        ) 
        if (confirmation == 'Y') | (confirmation == 'y'): 
            print(confirmation) 

            if entity_name == 'user': 
                modified_item = self.manager.update_user( 
                    entity_to_modify, 
                    fields['field_to_modify'], 
                    fields['new_value'] 
                ) 
                print(f"{entity_dict[entity_name]} {modified_item.id} a bien été modifié : \"{modified_item}\". ") 
                return modified_item 
            elif entity_name == 'client': 
                modified_item = self.manager.update_client( 
                    entity_to_modify, 
                    fields['field_to_modify'], 
                    fields['new_value'] 
                ) 
                print(f"{entity_dict[entity_name]} {modified_item.id} a bien été modifié : \"{modified_item}\". ") 
                return modified_item 
            elif entity_name == 'contract': 
                modified_item = self.manager.update_contract( 
                    entity_to_modify, 
                    fields['field_to_modify'], 
                    fields['new_value'] 
                ) 
                print(f"{entity_dict[entity_name]} ID {modified_item.id} a bien été modifié : \"{modified_item}\". ") 
                # if (fields['field_to_modify'] == 'signed') & (modified_item.is_signed is True): 
                #     # from sentry_sdk import capture_message 
                #     capture_message(f'Le contrat ID {new_item.id} a été signé.') 
                return modified_item 
            elif entity_name == 'event': 
                modified_item = self.manager.update_event( 
                    entity_to_modify, 
                    fields['field_to_modify'], 
                    fields['new_value'] 
                ) 
                print(f"{entity_dict[entity_name]} {modified_item.id} a bien été modifié : \"{modified_item}\". ") 
                return modified_item 
            else: 
                print('Il y a eu un problème, merci de contacter un administrateur. ') 
                return False 
        else: 
            print(confirmation) 
            print('Vous avez annulé l\'opération, vous allez être redirigé vers le menu. ') 



    """ Command to quit the application """ 
    @staticmethod 
    def close_the_app(): 
        print('\nFermeture de l\'application. Bonne fin de journée !') 

    # ======== /Utils ======== # 

