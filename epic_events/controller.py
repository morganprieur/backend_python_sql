
from dashboard import Dashboard 
from manager import Manager 
from models import Base, Client, Contract, Department, Event, User  
from views import Views 

from datetime import datetime, timedelta 
import json 
import os 
import time 

from prompt_toolkit import PromptSession 
session = PromptSession() 


class Controller(): 
    print(f'hello controller') 
    def __init__(self): 
        self.dashboard = Dashboard() 
        self.views = Views() 
        self.manager = Manager() 
        self.manager.connect() 
        self.manager.create_session() 

        self.user_session = None 


    def start(self, mode): 

        if self.user_session == None: 
            self.connect_user(mode) 


        # ======== M E N U ======== # 

        # Displays only the useful menus, regarding the connected user  
        if self.user_session == 'GESTION': 
            self.dashboard.display_menu([1, 2, 4, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]) 
        elif self.user_session == 'COMMERCE': 
            self.dashboard.display_menu([3, 5, 8, 9, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26]) 
        elif self.user_session == 'SUPPORT': 
            self.dashboard.display_menu([10, 14, 15, 16, 17, 18, 19, 20, 21, 27]) 
        else: 
            print('Vous devez vous connecter pour pouvoir accéder aux fonctionnalités de l\'application. ') 


        # ==== Registers one dept ==== # 
        if self.dashboard.ask_for_action == '1': 
            self.dashboard.ask_for_action = None 

            self.register_dept() 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Registers one user ==== # 
        if self.dashboard.ask_for_action == '2': 
            self.dashboard.ask_for_action = None 

            self.register_user() 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Registers one client ==== # 
        if self.dashboard.ask_for_action == '3': 
            self.dashboard.ask_for_action = None 

            self.register_client() 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Registers one contract ==== # 
        if self.dashboard.ask_for_action == '4': 
            self.dashboard.ask_for_action = None 

            self.register_contract() 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Registers one event ==== # 
        if self.dashboard.ask_for_action == '5': 
            self.dashboard.ask_for_action = None 

            self.register_event() 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Modifies a department ==== # 
        if self.dashboard.ask_for_action == '6': 
            self.dashboard.ask_for_action = None 

            self.modify_dept() 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Modifies one user ==== # 
        if self.dashboard.ask_for_action == '7': 
            self.dashboard.ask_for_action = None 

            self.modify_user() 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Modifies one client ==== # 
        if self.dashboard.ask_for_action == '8': 
            self.dashboard.ask_for_action = None 

            self.modify_client() 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Modifies one contract ==== # 
        if self.dashboard.ask_for_action == '9': 
            self.dashboard.ask_for_action = None 

            self.modify_contract() 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Modifies one event ==== # 
        if self.dashboard.ask_for_action == '10': 
            self.dashboard.ask_for_action = None 

            self.modify_event() 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Deletes one user ==== # 
        if self.dashboard.ask_for_action == '11': 
            self.dashboard.ask_for_action = None 

            self.delete_user() 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Displays all departments ==== # 
        if self.dashboard.ask_for_action == '12': 
            self.dashboard.ask_for_action = None 

            self.show_all_depts() 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Displays all users ==== # 
        if self.dashboard.ask_for_action == '13': 
            self.dashboard.ask_for_action = None 

            self.show_all_users() 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Displays all clients ==== # 
        if self.dashboard.ask_for_action == '14': 
            self.dashboard.ask_for_action = None 


            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Displays all contracts ==== # 
        if self.dashboard.ask_for_action == '15': 
            self.dashboard.ask_for_action = None 

            self.show_all_contracts() 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Displays all events ==== # 
        if self.dashboard.ask_for_action == '16': 
            self.dashboard.ask_for_action = None 

            self.show_all_events() 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Displays a department ==== # 
        if self.dashboard.ask_for_action == '17': 
            self.dashboard.ask_for_action = None 

            self.show_one_dept() 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Displays a user ==== # 
        if self.dashboard.ask_for_action == '18': 
            self.dashboard.ask_for_action = None 

            self.show_one_user() 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Displays a client ==== # 
        if self.dashboard.ask_for_action == '19': 
            self.dashboard.ask_for_action = None 

            self.show_one_client() 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Displays a contract ==== # 
        if self.dashboard.ask_for_action == '20': 
            self.dashboard.ask_for_action = None 

            self.show_one_contract() 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Displays an event ==== # 
        if self.dashboard.ask_for_action == '21': 
            self.dashboard.ask_for_action = None 

            self.show_one_event() 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Displays events that don't have 'support' contact ==== # 
        if self.dashboard.ask_for_action == '22': 
            self.dashboard.ask_for_action = None 

            self.show_events_without_support() 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Displays clients of one 'commerce' user ==== # 
        if self.dashboard.ask_for_action == '23': 
            self.dashboard.ask_for_action = None 

            show_clients_of_commerce_user() 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Displays contracts of one 'commerce' user ==== # 
        if self.dashboard.ask_for_action == '24': 
            self.dashboard.ask_for_action = None 

            self.show_contracts_of_commerce_user() 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Displays not paid contracts ==== # 
        if self.dashboard.ask_for_action == '25': 
            self.dashboard.ask_for_action = None 

            self.show_not_paid_contracts() 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Displays not signed contracts ==== # 
        if self.dashboard.ask_for_action == '26': 
            self.dashboard.ask_for_action = None 

            self.show_not_signed_contracts() 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Displays events of one 'support' user ==== # 
        if self.dashboard.ask_for_action == '27': 
            self.dashboard.ask_for_action = None 

            self.show_events_support_user() 

            self.press_enter_to_continue() 
            self.start(mode) 



        """ Command to quit the application """ 
        if self.dashboard.ask_for_action == '0': 
            self.dashboard.ask_for_action = None 
            self.close_the_app() 




    # ======== actions ======== # 
    # TODO: if not checked, back to form + counter (3x max) 
    def connect_user(self, mode): 
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
                # print(self.registered) 
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
            # new_session = False 

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
                if logged_user.department.name == 'gestion': 
                    self.user_session = 'GESTION' 
                if logged_user.department.name == 'commerce': 
                    self.user_session = 'COMMERCE' 
                if logged_user.department.name == 'support': 
                    self.user_session = 'SUPPORT' 
                print(self.user_session) 
            else: 
                print(self.user_session) 
            self.dashboard.display_welcome() 


    # ==== register ==== # 
    def register_dept(self): 
        if self.user_session == 'GESTION': 
            print('\nEnregistrer un département') 
            fields = self.views.input_create_dept() 
            new_item = self.manager.add_entity('dept', fields) 
            print(f"Le département {new_item.id} {new_item.name} a bien été créé. ") 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    def register_user(self): 
        if self.user_session == 'GESTION': 
            print('\nEnregistrer un utilisateur') 
            fields = self.views.input_create_user() 

            # Hash password: 
            fields['password'] = self.manager.hash_pw(fields['entered_password'], 12) 
            fields.pop('entered_password') 

            # get token: use method into the manager 
            fields['department_id'] = self.manager.select_one_dept('name', fields['department_name']).id 
            fields.pop('department_name') 
            # print(fields) 

            new_item = self.manager.add_entity('user', fields) 
            print(f"L\'utilisateur {new_item.id} {new_item.name} a bien été créé. ") 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    def register_client(self): 
        if self.user_session == 'COMMERCE': 
            print('\nEnregistrer un client') 
            fields = self.views.input_create_client() 
            fields['sales_contact_id'] = logged_user.id 

            new_item = self.manager.add_entity('client', fields) 
            print(f"Le client {new_item.name} (ID : {new_item.id}) du contact {new_item.User.name} a bien été créé. ") 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    def register_contract(self): 
        if self.user_session == 'GESTION': 
            print('\nEnregistrer un contrat') 
            fields = self.views.input_create_contract() 
            fields['client_id'] = self.manager.select_one_client('name', fields['client_name']) 
            fields.pop('client_name') 

            new_item = self.manager.add_entity('contract', fields) 
            print(f"Le contrat {new_item.id} du client {new_item.client.name} a bien été créé. ") 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    def register_event(self): 
        if self.user_session == 'COMMERCE': 
            print('\nEnregistrer un événement') 

            contract = self.views.input_select_entity('contract') 
            contract = self.manager.select_one_contract('id', contract.id) 
            if contract.signed: 
                fields = self.views.input_create_event() 

                new_item = self.manager.add_entity('event', fields) 
                print(f"L'événement a bien été créé : {new_item} ") 
            else: 
                print(f"Le contrat {contract.id} n\'est pas signé, vous ne pouvez pas créer l\'événement.") 

        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    # ==== modify ==== # 
    def modify_dept(self): 
        if self.user_session == 'GESTION': 
            print('\nModifier un département') 
            dept_to_select = self.views.input_select_entity('dept') 
            dept_to_modify = self.manager.select_one_dept( 
                dept_to_select['chosen_field'], 
                dept_to_select['value_to_select'] 
            ) 
            fields = self.views.input_modify_dept(dept_to_modify) 

            # Confirmation : 
            confirmation = self.views.ask_for_confirmation('modifier', 'dept') 

            if (confirmation == 'y') | (confirmation == 'Y'): 
                modified_item = self.manager.update_dept( 
                    dept_to_modify, 
                    dept_to_select['value_to_select'], 
                    fields['new_name'] 
                ) 
                print(f"Le nom du département {modified_item.id} a bien été modifié : {modified_item}. ") 
            else: 
                print('Vous avez annulé la modification, le département n\'a pas été modifié.') 
                return False 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    def modify_user(self): 
        if self.user_session == 'GESTION': 
            print('\nModifier un utilisateur') 
            user_to_select = self.views.input_select_entity('user') 
            user_to_modify = self.manager.select_one_user( 
                user_to_select['field_to_select'], 
                user_to_select['value_to select'] 
            ) 

            # fields = self.views.input_modify_user(user_to_modify) 
            # if self.user_session == 'GESTION': 
            #     gestion = True 
            fields = self.views.input_modify_entity( 
                'user', 
                user_to_modify 
            ) 
            print('fields : ', fields) 

            # TODO: verif 
            if fields['field_to_modify'] == 'password': 
                hash_new_pw = self.manager.hash_pw(fields['new_value'], 12) 
                fields['new_value'] = hash_new_pw 
            elif fields['field_to_modify'] == 'token': 
                data = { 
                    'email': user_to_modify.email, 
                    'pass': user_to_modify.password, 
                    'dept': user_to_modify.departments.name 
                } 
                new_token = self.manager.get_token(2, data) 
                fields['new_value'] = new_token 
            
            # print('fields avant changemt (controller 7) : ', fields) 
            fields[fields['field_to_modify']] = fields['new_value'] 

            # Confirmation : 
            confirmation = self.views.ask_for_confirmation('modifier', 'user') 
            if (confirmation == 'y') | (confirmation == 'Y'): 
                modified_item = self.manager.update_user( 
                    user_to_modify, 
                    fields['field_to_modify'], 
                    fields['new_value'] 
                ) 
                print(f"L'utilisateur {modified_item.id} a bien été modifié : \"{modified_item}\". ") 
            else: 
                print('Vous avez annulé la modification, l\'utilisateur n\'a pas été modifié.') 
                return False 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    def modify_client(self): 
        if self.user_session == 'COMMERCE': 
            print('\nModifier un client') 
            client_to_select = self.views.input_select_entity('client') 
            client_to_modify = self.manager.select_one_client( 
                client_to_select['field_to_select'], 
                client_to_select['value_to_select'] 
            ) 

            # fields = self.views.input_modify_client(client_to_modify) 
            # if self.user_session == 'GESTION': 
            #     gestion = True 
            fields = self.views.input_modify_entity( 
                'client', 
                client_to_modify 
            ) 

            # print('fields avant changemt (controller 8) : ', fields) 
            fields[fields['field_to_modify']] = fields['new_value'] 
            # print('fields après changemt (controller 8) : ', fields) 

            # Confirmation : 
            confirmation = self.views.ask_for_confirmation('modifier', 'client') 
            if (confirmation == 'y') | (confirmation == 'Y'): 
                modified_item = self.manager.update_client( 
                    client_to_modify, 
                    fields['field_to_modify'], 
                    fields['new_value'] 
                ) 
                print(f"Le client a bien été modifié : \"{modified_item}\". ") 
            else: 
                print('Vous avez annulé la modification, le client n\'a pas été modifié.') 
                return False 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    def modify_contract(self): 
        if self.user_session == 'COMMERCE': 
            print('\nModifier un contrat') 
            contract_to_select = self.views.input_select_entity('contract') 
            contract_to_modify = self.manager.select_one_contract( 
                contract_to_select['field_to_select'], 
                contract_to_select['value_to_select'] 
            ) 

            fields = self.views.input_modify_contract(contract_to_modify) 
            # if self.user_session == 'GESTION': 
            #     gestion = True 
            fields = self.views.input_modify_entity( 
                'contract', 
                contract_to_modify 
            ) 

            # print('fields avant changemt (controller 9) : ', fields) 
            fields[fields['field_to_modify']] = fields['new_value'] 
            # print('fields après changemt (controller 9) : ', fields) 

            # Confirmation : 
            confirmation = self.views.ask_for_confirmation('modifier', 'contract') 
            if (confirmation == 'y') | (confirmation == 'Y'): 
                modified_item = self.manager.update_contract( 
                    contract_to_modify, 
                    fields['field_to_modify'], 
                    fields['new_value'] 
                ) 
                print(f"Le contrat a bien été modifié : \"{modified_item}\". ") 
            else: 
                print('Vous avez annulé la modification, le contrat n\'a pas été modifié.') 
                return False 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    def modify_event(self): 
        if (self.user_session != 'GESTION') & (self.user_session != 'SUPPORT'): 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 
        else: 
            print('\nModifier un événement') 
            event_to_select = self.views.input_select_entity('event') 
            event_to_modify = self.manager.select_one_event( 
                event_to_select['field_to_select'], 
                event_to_select['value_to_select'] 
            ) 

            if self.user_session == 'GESTION': 
                gestion = True 
            fields = self.views.input_modify_entity( 
                'event', 
                event_to_modify, 
                gestion=gestion 
            ) 
            print('fields : ', fields) 

            # print('fields avant changemt (controller 10) : ', fields) 
            fields[fields['field_to_modify']] = fields['new_value'] 
            # print('fields après changemt (controller 10) : ', fields) 

            # Confirmation : 
            confirmation = self.views.ask_for_confirmation('modifier', 'event') 
            if (confirmation == 'y') | (confirmation == 'Y'): 
                modified_item = self.manager.update_event( 
                    event_to_modify, 
                    fields['field_to_modify'], 
                    fields['new_value'] 
                ) 
                print(f"L'événement {modified_item.id} a bien été modifié : \"{modified_item}\". ") 
            else: 
                print('Vous avez annulé la modification, l\'événement n\'a pas été modifié.') 
                return False 


    # ==== delete ==== # 
    def delete_user(self): 
        if self.user_session == 'GESTION': 
            print('\nSupprimer un utilisateur') 
            user_to_select = self.views.input_select_entity('user') 

            # Confirmation : 
            confirmation = self.views.ask_for_confirmation('supprimer', 'user') 
            if (confirmation == 'y') | (confirmation == 'Y'): 
                user_to_delete = self.manager.delete_user( 
                    user_to_select['chosen_field'], 
                    user_to_select['old_value'] 
                ) 
                print(f"L'utilisateur {user_to_select['old_value']} a bien été supprimé. ") 
            else: 
                print('Vous avez annulé la suppression, l\'utilisateur n\'a pas été supprimé.') 
                return False 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    # ==== show all ==== # 
    def show_all_depts(self): 
        if self.user_session == 'GESTION': 
            depts = self.manager.select_all_entities('depts') 
            self.display_all_entities(depts) 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    def show_all_users(self): 
        if self.user_session == 'GESTION': 
            users = self.manager.select_all_entities('users') 
            self.display_all_entities(users) 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    def show_all_clients(self): 
        if (self.user_session == 'GESTION') | (self.user_session == 'COMMERCE') | (self.user_session == 'SUPPORT'): 
            clients = self.manager.select_all_entities('clients') 
            self.display_all_entities(clients) 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    def show_all_contracts(self): 
        if (self.user_session == 'GESTION') | (self.user_session == 'COMMERCE') | (self.user_session == 'SUPPORT'): 
            contracts = self.manager.select_all_entities('contracts') 
            self.display_all_entities(contracts) 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    def show_all_events(self): 
        if (self.user_session == 'GESTION') | (self.user_session == 'COMMERCE') | (self.user_session == 'SUPPORT'): 
            events = self.manager.select_all_entities('events') 
            self.display_all_entities(events) 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    # ==== show one ==== # 
    def show_one_dept(self): 
        if (self.user_session == 'GESTION') | (self.user_session == 'COMMERCE') | (self.user_session == 'SUPPORT'): 
            print('\nAfficher un département') 
            dept_to_select = self.views.input_select_entity('dept') 
            dept = self.manager.select_one_dept(dept_to_select['chosen_field'], dept_to_select['old_value']) 
            self.views.display_entity([dept]) 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    def show_one_user(self): 
        if (self.user_session == 'GESTION') : 
            print('\nAfficher un utilisateur') 
            user_to_select = self.views.input_select_entity('user') 
            user = self.manager.select_one_user( 
                user_to_select['chosen_field'], 
                user_to_select['old_value'] 
            ) 
            self.views.display_entity([user]) 
        if (self.user_session == 'COMMERCE') | (self.user_session == 'SUPPORT') : 
            user_to_select = self.views.input_select_entity('user') 
            user = self.manager.select_one_user( 
                user_to_select['chosen_field'], 
                user_to_select['old_value'] 
            ) 
            self.views.display_user_minimum(user) 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    def show_one_client(self): 
        if (self.user_session == 'GESTION')  | (self.user_session == 'COMMERCE') | (self.user_session == 'SUPPORT'): 
            print('\nAfficher un client') 
            client_to_select = self.views.input_select_entity('client') 
            client = self.manager.select_one_client( 
                client_to_select['chosen_field'], 
                client_to_select['old_value'] 
            ) 
            self.views.display_entity([client]) 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    def show_one_contract(self): 
        if (self.user_session == 'GESTION')  | (self.user_session == 'COMMERCE') | (self.user_session == 'SUPPORT'): 
            print('\nAfficher un contrat') 
            contract_to_select = self.views.input_select_entity('contract') 
            contract = self.manager.select_one_contract( 
                contract_to_select['chosen_field'], 
                contract_to_select['old_value'] 
            ) 
            self.views.display_entity([contract]) 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    def show_one_event(self): 
        if (self.user_session == 'GESTION')  | (self.user_session == 'COMMERCE') | (self.user_session == 'SUPPORT'): 
            print('\nAfficher un événement') 
            event_to_select = self.views.input_select_entity('event') 
            event = self.manager.select_one_event( 
                event_to_select['chosen_field'], 
                event_to_select['old_value'] 
            ) 
            self.views.display_entity([event]) 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    # ==== show with criteria ==== # 
    def show_events_without_support(self): 
        if (self.user_session == 'GESTION'): 
            print('\nAfficher les événements sans contact support') 
            events = self.manager.select_entities_with_criteria( 
                'events', 
                'without support', 
                logged_user.id 
            ) 
            self.views.display_entity([event]) 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    def show_clients_of_commerce_user(self): 
        if (self.user_session == 'COMMERCE'): 
            print('\nAfficher les clients d\'un utilisateur commercial') 
            clients = self.manager.select_entities_with_criteria( 
                'clients', 
                'sales contact', 
                logged_user.id 
            ) 
            self.views.display_entity([clients]) 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    def show_contracts_of_commerce_user(self): 
        if (self.user_session == 'COMMERCE'): 
            print('\nAfficher les contrats d\'un utilisateur commercial ') 
            contracts = self.manager.select_entities_with_criteria( 
                'contracts', 
                'sales contact', 
                logged_user.id 
            ) 
            self.views.display_entity([contracts]) 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    def show_not_paid_contracts(self): 
        if (self.user_session == 'COMMERCE'): 
            print('\nAfficher les contrats non fini de payer ') 
            contracts = self.manager.select_entities_with_criteria( 
                'contracts', 
                'not paid', 
                logged_user.id 
            ) 
            self.views.display_entity([contracts]) 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    def show_not_signed_contracts(self): 
        if (self.user_session == 'COMMERCE'): 
            print('\nAfficher les contrats non signés ') 
            contracts = self.manager.select_entities_with_criteria( 
                'contracts', 
                'not signed', 
                logged_user.id 
            ) 
            self.views.display_entity([contracts]) 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 


    def show_events_support_user(self): 
        if (self.user_session == 'SUPPORT'): 
            print('\nAfficher les événements d\'un utilisateur support ') 
            events = self.manager.select_entities_with_criteria( 
                'events', 
                'support contact', 
                logged_user.id 
            ) 
            self.views.display_entity([events]) 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 



    @staticmethod 
    def press_enter_to_continue(): 
        session.prompt('Appuyez sur entrée pour continuer ') 

    """ Command to quit the application """ 
    @staticmethod 
    def close_the_app(): 
        print('\nFermeture de l\'application. Bonne fin de journée !') 

    # ======== /actions ======== # 

