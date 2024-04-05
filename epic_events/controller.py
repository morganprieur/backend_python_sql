
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
    # test_fct() 
    def __init__(self):  # , view, manager 
        self.dashboard = Dashboard() 
        self.views = Views() 
        self.manager = Manager() 
        self.manager.connect() 
        self.manager.create_session() 

        self.user_session = None 


    # def start(self, mode, user_session=None): 
    # def start(self, mode, new_session=True): 
    def start(self, mode): 
        # self.user_session = None 

        if self.user_session == None: 
            self.connect_user(mode) 


        # if new_session: 
        #     self.dashboard.display_welcome() 
        # self.dashboard.display_menu() 


        # ======== M E N U ======== # 

        # Displays only the useful menus 
        if self.user_session == 'GESTION': 
            self.dashboard.display_menu([1, 2, 4, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]) 
        elif self.user_session == 'COMMERCE': 
            self.dashboard.display_menu([3, 5, 8, 9, 14, 15, 16, 18, 19, 20, 21, 23, 24, 25, 26]) 
        elif self.user_session == 'SUPPORT': 
            self.dashboard.display_menu([10, 14, 15, 16, 18, 19, 20, 21, 27]) 
        else: 
            print('Vous devez vous connecter pour pouvoir accéder aux fonctionnalités de l\'application. ') 
            # self.board.display_menu(items) 


        # ==== Registers one dept ==== # 
        if self.dashboard.ask_for_action == '1': 
            self.dashboard.ask_for_action = None 

            if self.user_session == 'GESTION': 
                print('\nEnregistrer un département') 
                fields = self.views.input_create_dept() 
                new_item = self.manager.add_entity('dept', fields) 
                print(f"Le département {new_item.id} {new_item.name} a bien été créé. ") 
            else: 
                print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
                return False 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Registers one user ==== # 
        if self.dashboard.ask_for_action == '2': 
            self.dashboard.ask_for_action = None 

            if self.user_session == 'GESTION': 
                print('\nEnregistrer un utilisateur') 
                fields = self.views.input_create_user() 
                # Hash password: 
                fields['password'] = self.manager.hash_pw(fields['entered_password'], 12) 
                fields.pop('entered_password') 
                # get token: into the manager 
                fields['department_id'] = self.manager.select_one_dept('name', fields['department_name']).id 
                fields.pop('department_name') 
                # print(fields) 

                new_item = self.manager.add_entity('user', fields) 
                print(f"L\'utilisateur {new_item.id} {new_item.name} a bien été créé. ") 
            else: 
                print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
                return False 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Registers one client ==== # 
        if self.dashboard.ask_for_action == '3': 
            self.dashboard.ask_for_action = None 

            if self.user_session == 'COMMERCE': 
                print('\nEnregistrer un client') 
                fields = self.views.input_create_client() 
                fields['sales_contact_id'] = logged_user.id 

                new_item = self.manager.add_entity('client', fields) 
                print(f"Le client {new_item.name} (ID : {new_item.id}) du contact {new_item.User.name} a bien été créé. ") 
            else: 
                print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
                return False 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Registers one contract ==== # 
        if self.dashboard.ask_for_action == '4': 
            self.dashboard.ask_for_action = None 

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

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Registers one event ==== # 
        if self.dashboard.ask_for_action == '5': 
            self.dashboard.ask_for_action = None 

            if self.user_session == 'COMMERCE': 
                print('\nEnregistrer un événement') 
                fields = self.views.input_create_event() 

                new_item = self.manager.add_entity('event', fields) 
                print(f"L'événement a bien été créé. ") 
            else: 
                print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
                return False 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Modifies a department ==== # 
        if self.dashboard.ask_for_action == '6': 
            self.dashboard.ask_for_action = None 

            if self.user_session == 'GESTION': 
                print('\nModifier un département') 
                dept_to_select = self.views.input_select_entity('dept') 
                dept_to_modify = self.manager.select_one_dept( 
                    'name', 
                    dept_to_select['old_value'] 
                ) 
                fields = self.views.input_modify_dept(dept_to_modify) 

                # Confirmation : 
                confirmation = self.views.ask_for_confirmation('modifier', 'dept') 

                if (confirmation == 'y') | (confirmation == 'Y'): 
                    modified_item = self.manager.update_dept( 
                        # fields['name_to_replace'], 
                        dept_to_select['old_value'], 
                        fields['new_name'] 
                    ) 
                    print(f"Le nom du département {modified_item.id} a bien été modifié : {modified_item}. ") 
                else: 
                    print('Vous avez annulé la modification, le département n\'a pas été modifié.') 
                    return False 
            else: 
                print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
                return False 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Modifies one user ==== # 
        if self.dashboard.ask_for_action == '7': 
            self.dashboard.ask_for_action = None 

            if self.user_session == 'GESTION': 
                print('\nModifier un utilisateur') 
                user_to_select = self.views.input_select_entity('user') 
                user_to_modify = self.manager.select_one_user( 
                    user_to_select['chosen_field'], 
                    user_to_select['old_value'] 
                ) 

                fields = self.views.input_modify_user(user_to_modify) 
                # print('fields avant changemt (controller 7) : ', fields) 
                fields[fields['field_to_modify']] = fields['new_value'] 
                # print('fields après changemt (controller 7) : ', fields) 

                # Confirmation : 
                confirmation = self.views.ask_for_confirmation('modifier', 'user') 
                if (confirmation == 'y') | (confirmation == 'Y'): 
                    modified_item = self.manager.update_user( 
                        user_to_modify.id, 
                        fields['field_to_modify'], 
                        fields['new_value'] 
                    ) 
                    print(f"L'utilisateur {modified_item.id} a bien été modifié : \"{modified_item}\". ") 
                else: 
                    print('Vous avez annulé la modification, le département n\'a pas été modifié.') 
                    return False 
            else: 
                print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
                return False 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Modifies one client ==== # 
        if self.dashboard.ask_for_action == '8': 
            self.dashboard.ask_for_action = None 

            if self.user_session == 'COMMERCE': 
                print('\nModifier un client') 
                client_to_select = self.views.input_select_entity('client') 
                client_to_modify = self.manager.select_one_client( 
                    client_to_select['chosen_field'], 
                    client_to_select['old_value'] 
                ) 

                fields = self.views.input_modify_client(client_to_modify) 
                # print('fields avant changemt (controller 8) : ', fields) 
                fields[fields['field_to_modify']] = fields['new_value'] 
                # print('fields après changemt (controller 8) : ', fields) 

                # Confirmation : 
                confirmation = self.views.ask_for_confirmation('modifier', 'client') 
                if (confirmation == 'y') | (confirmation == 'Y'): 
                    modified_item = self.manager.update_client( 
                        client_to_modify.id, 
                        fields['field_to_modify'], 
                        fields['new_value'] 
                    ) 
                    print(f"Le client a bien été modifié : \"{modified_item}\". ") 
                else: 
                    print('Vous avez annulé la modification, le département n\'a pas été modifié.') 
                    return False 
            else: 
                print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
                return False 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Modifies one contract ==== # 
        if self.dashboard.ask_for_action == '9': 
            self.dashboard.ask_for_action = None 

            if self.user_session == 'COMMERCE': 
                print('\nModifier un contrat') 
                contract_to_select = self.views.input_select_entity('contract') 
                contract_to_modify = self.manager.select_one_contract( 
                    contract_to_select['chosen_field'], 
                    contract_to_select['old_value'] 
                ) 

                fields = self.views.input_modify_contract(contract_to_modify) 
                # print('fields avant changemt (controller 9) : ', fields) 
                fields[fields['field_to_modify']] = fields['new_value'] 
                # print('fields après changemt (controller 9) : ', fields) 

                # Confirmation : 
                confirmation = self.views.ask_for_confirmation('modifier', 'contract') 
                if (confirmation == 'y') | (confirmation == 'Y'): 
                    modified_item = self.manager.update_contract( 
                        contract_to_modify.id, 
                        fields['field_to_modify'], 
                        fields['new_value'] 
                    ) 
                    print(f"Le contrat a bien été modifié : \"{modified_item}\". ") 
                else: 
                    print('Vous avez annulé la modification, le département n\'a pas été modifié.') 
                    return False 
            else: 
                print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
                return False 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Modifies one event ==== # 
        if self.dashboard.ask_for_action == '10': 
            self.dashboard.ask_for_action = None 

            if self.user_session == 'GESTION': 
                print('\nModifier un événement') 
                event_to_select = self.views.input_select_entity('event') 
                # user_to_select = self.views.input_select_user() 
                event_to_modify = self.manager.select_one_event( 
                    event_to_select['chosen_field'], 
                    event_to_select['old_value'] 
                ) 

                fields = self.views.input_modify_event( 
                    event_to_modify, 
                    gestion=True 
                ) 
                # print('fields avant changemt (controller 10) : ', fields) 
                fields[fields['field_to_modify']] = fields['new_value'] 
                # print('fields après changemt (controller 10) : ', fields) 

                # Confirmation : 
                confirmation = self.views.ask_for_confirmation('modifier', 'event') 
                if (confirmation == 'y') | (confirmation == 'Y'): 
                    modified_item = self.manager.update_event( 
                        event_to_modify.id, 
                        fields['field_to_modify'], 
                        fields['new_value'] 
                    ) 
                    print(f"L'événement {modified_item.id} a bien été modifié : \"{modified_item}\". ") 
                else: 
                    print('Vous avez annulé la modification, le département n\'a pas été modifié.') 
                    return False 
            else: 
                print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
                return False 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Deletes one user ==== # 
        if self.dashboard.ask_for_action == '11': 
            self.dashboard.ask_for_action = None 

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

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Displays all departments ==== # 
        if self.dashboard.ask_for_action == '12': 
            self.dashboard.ask_for_action = None 

            if self.user_session == 'GESTION': 
                self.display_all_entities('depts') 
            else: 
                print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
                return False 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Displays all users ==== # 
        if self.dashboard.ask_for_action == '13': 
            self.dashboard.ask_for_action = None 

            if self.user_session == 'GESTION': 
                self.display_all_entities('isers') 
            else: 
                print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
                return False 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Displays all clients ==== # 
        if self.dashboard.ask_for_action == '14': 
            self.dashboard.ask_for_action = None 

            if (self.user_session == 'GESTION') | (self.user_session == 'COMMERCE') | (self.user_session == 'SUPPORT'): 
                self.display_all_entities('clients') 
            else: 
                print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
                return False 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Displays all contracts ==== # 
        if self.dashboard.ask_for_action == '15': 
            self.dashboard.ask_for_action = None 

            if (self.user_session == 'GESTION') | (self.user_session == 'COMMERCE') | (self.user_session == 'SUPPORT'): 
                self.display_all_entities('contracts') 
            else: 
                print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
                return False 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Displays all events ==== # 
        if self.dashboard.ask_for_action == '16': 
            self.dashboard.ask_for_action = None 

            if (self.user_session == 'GESTION') | (self.user_session == 'COMMERCE') | (self.user_session == 'SUPPORT'): 
                self.display_all_entities('events') 
            else: 
                print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
                return False 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Displays a department ==== # 
        if self.dashboard.ask_for_action == '17': 
            self.dashboard.ask_for_action = None 
            print('\nAfficher un département') 

            if (self.user_session == 'GESTION') | (self.user_session == 'COMMERCE') | (self.user_session == 'SUPPORT'): 
                dept_to_select = self.views.input_select_entity('dept') 
                dept = self.manager.select_one_dept(dept_to_select['chosen_field'], dept_to_select['old_value']) 
                self.views.display_entity([dept]) 
            else: 
                print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
                return False 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Displays a user ==== # 
        if self.dashboard.ask_for_action == '18': 
            self.dashboard.ask_for_action = None 
            print('\nAfficher un utilisateur') 

            if (self.user_session == 'GESTION') : 
                user_to_select = self.views.input_select_entity('user') 
                user = self.manager.select_one_user( 
                    user_to_select['chosen_field'], 
                    user_to_select['old_value'] 
                ) 
                self.views.display_entity([user]) 
            else: 
                print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
                return False 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Displays a client ==== # 
        if self.dashboard.ask_for_action == '19': 
            self.dashboard.ask_for_action = None 
            print('\nAfficher un client') 

            if (self.user_session == 'GESTION')  | (self.user_session == 'COMMERCE') | (self.user_session == 'SUPPORT'): 
                client_to_select = self.views.input_select_entity('client') 
                client = self.manager.select_one_client( 
                    client_to_select['chosen_field'], 
                    client_to_select['old_value'] 
                ) 
                self.views.display_entity([client]) 
            else: 
                print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
                return False 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Displays a contract ==== # 
        if self.dashboard.ask_for_action == '20': 
            self.dashboard.ask_for_action = None 
            print('\nAfficher un contrat') 

            if (self.user_session == 'GESTION')  | (self.user_session == 'COMMERCE') | (self.user_session == 'SUPPORT'): 
                contract_to_select = self.views.input_select_entity('contract') 
                contract = self.manager.select_one_contract( 
                    contract_to_select['chosen_field'], 
                    contract_to_select['old_value'] 
                ) 
                self.views.display_entity([contract]) 
            else: 
                print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
                return False 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Displays an event ==== # 
        if self.dashboard.ask_for_action == '21': 
            self.dashboard.ask_for_action = None 
            print('\nAfficher un événement') 

            if (self.user_session == 'GESTION')  | (self.user_session == 'COMMERCE') | (self.user_session == 'SUPPORT'): 
                event_to_select = self.views.input_select_entity('event') 
                event = self.manager.select_one_event( 
                    event_to_select['chosen_field'], 
                    event_to_select['old_value'] 
                ) 
                self.views.display_entity([event]) 
            else: 
                print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
                return False 

            self.press_enter_to_continue() 
            self.start(mode) 


        # ==== Displays events that don't have support contact ==== # 
        if self.dashboard.ask_for_action == '22': 
            self.dashboard.ask_for_action = None 
            print('\nAfficher les événements sans contact support') 

            if (self.user_session == 'GESTION'): 
                # event_to_select = self.views.input_select_entity('event') 
                events = self.manager.select_entities_with_criteria('events', 'without support', logged_user.id) 
                self.views.display_entity([event]) 
            else: 
                print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
                return False 

            self.press_enter_to_continue() 
            self.start(mode) 



        """ commerce 3, 5, 8, 9, 14, 15, 16, 18, 19, 20, 21, 23, 24, 25, 26 

        '8 : 
        '9 : 
        '14 : Afficher tous les client ', 
        '15 : Afficher tous les contrats ', 
        '16 : Afficher tous les événements ', 

        '18 : Afficher un utilisateur ', 
        '19 : Afficher un client ', 
        '20 : Afficher un contrat ', 
        '21 : Afficher un événement ', 

        '23 : Afficher les clients d\'un utilisateur commercial ', 
        '24 : Afficher les contrats d\'un utilisateur commercial ', 
        '25 : Afficher les contrats non finis de payer ', 
        '26 : Afficher les contrats non signés ', 

        """ 



        """ Command to quit the application """ 
        if self.dashboard.ask_for_action == '0': 
            self.dashboard.ask_for_action = None 
            self.close_the_app() 




    def display_all_entities(self, entities): 
        print(f'\nAfficher tous les {entities_dict[entities]}') 

        entities_dict = { 
            'depts': 'départements', 
            'users': 'utilisateurs', 
            'clients': 'clients', 
            'contracts': 'contrats', 
            'events': 'événements' 
        } 
        objects = self.manager.select_all_entities(entities) 
        print(f"Voici la liste des {entities_dict[entities]} : ") 
        return self.views.display_entity(objects) 



    # ==== permissions GESTION ==== # 
    # def create_department(self, entity, fields): 
    #     if self.user_session == 'GESTION': 
    #         self.manager.add_entity(entity, fields) 
    #     else: 
    #         print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
    #         return False 


    # def create_user(self, entity, fields): 
    #     if self.user_session == 'GESTION': 
    #         self.manager.add_entity(entity, fields) 
    #     else: 
    #         print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
    #         return False 
    # ======== /session GESTION ======== # 


    # ======== Create ======== # 
    # # TODO: prompt data + retour dans l'application if False. 
    # def create_user(self, fields:dict): 
    #     """ Creates a new user, following the prompted data. 
    #         Permission: GESTION 
    #         Returns: 
    #             object User: The just created User instance, 
    #                 or false if the user does not have the permission to create it. 
    #     """ 
    #     if user_session == 'GESTION': 
    #         new_user = self.manager.add_user( 
    #             name=fields['name'], 
    #             email=fields['email'], 
    #             phone=fields['phone'], 
    #             department_name=fields['department_name']  
    #         ) 
    #         new_user_db = self.manager.select_one_user('name', fields[0]) 
    #         return new_user 
    #     else: 
    #         print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
    #         return False 

    # # TODO: prompt data + retour dans l'application if False. 
    # def create_client(self, fields:dict): 
    #     """ Creates a new client, following the prompted data. 
    #         Permission: COMMERCE 
    #         Returns: 
    #             object Client: The just created Client instance, 
    #                 or false if the user does not have the permission to create it. 
    #     """ 
    #     if user_session == 'COMMERCE': 
    #         new_client = self.manager.add_client( 
    #             name=fields['name'], 
    #             email=fields['email'], 
    #             phone=fields['phone'], 
    #             corporation_name=fields['corporation_name'], 
    #             sales_contact_name=logged_user.id 
    #         ) 
    #         new_client_db = self.manager.select_one_client('name', client_1['name']) 
    #         print(f'Le client {new_client_db.name} (id : {new_client_db.id}) a bien été créé.') 
    #         return new_client_db 
    #     else: 
    #         print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
    #         return False 

    # # TODO: prompt data + retour dans l'application if False. 
    # def create_contract(self, fields:dict): 
    #     """ Calls the manager.add_contract, sending the prompted data. 
    #         Permission: GESTION 
    #         Returns: 
    #             object Contract: The just created Contract instance, 
    #                 or false if the user does not have the permission to create it. 
    #     """ 
    #     if user_session == 'GESTION': 
    #         print('self.registered["contracts] CL149 create_contract : ', self.registered['contracts']) 
    #         contract_1 = self.registered['contracts'][0] 
    #         new_contract = self.manager.add_contract( 
    #             client_name=fields['client_name'], 
    #             amount=fields['amount'], 
    #             paid_amount=fields['paid_amount'], 
    #             is_signed=fields['is_signed'] 
    #         ) 
    #         new_contract_db = self.manager.select_one_contract('id', 1) 
    #         # new_client_db = self.manager.select_one_client('name', 'client 1') 
    #         print(f'Le contrat {new_contract_db.id} (du client {new_contract_db.client_name}) a bien été créé.') 
    #         return new_contract_db 
    #     else: 
    #         print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
    #         return False 

    # # TODO: prompt data + retour dans l'application if False. 
    # def create_event(self, fields:dict): 
    #     """ Calls the manager.add_event, sending the prompted data. The 'support_contact_id' is let empty. 
    #         A Gestion user will fill it. 
    #         Permission: COMMERCE 
    #         Returns: 
    #             object Event: The just created Event instance, 
    #                 or false if the user does not have the permission to create it. 
    #     """ 
    #     if user_session == 'COMMERCE': 
    #         contract_db = self.manager.select_one_contract('id', 1) 
    #         if contract_db.is_signed != 1: 
    #             prin(f'Le contrat numéro {contract_db} n\'est pas signé. ') 
    #             new_event = self.manager.add_event( 
    #                 name=fields['name'], 
    #                 contract_id=fields['contract_id'], 
    #                 start_datetime=fields['start_datetime'], 
    #                 end_datetime=fields['end_datetime'], 
    #                 location=fields['location'], 
    #                 attendees=fields['attendees'], 
    #                 notes=fields['notes'] 
    #             ) 
    #             new_event_db = self.manager.select_one_event('id', 1) 
    #             # new_client_db = self.manager.select_one_client('name', 'client 1') 
    #             print(f'L\'événement {new_event_db.name} (id : {new_event_db.id}) a bien été créé.') 
    #             return new_event_db 
    #         else: 
    #             print(f'Le contrat numéro {contract_db.id} n\'est pas signé, recontactez le client avant de créer l\'événement.') 
    #             return False 
    #     else: 
    #         print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
    #         return False 





    # ======== Modify ======== # 
    # # TODO: prompt data + retour dans l'application if False. 
    # def modify_user(self, id, field, new_value): 
    #     """ Modifies a user, following the prompted data. 
    #         Permission: GESTION 
    #         paparms: 
    #             id (int): The id of the user to modify. 
    #             field (str): The name of the field to modify. 
    #             new_value (str): The new value to register. 
    #         Returns: 
    #             object User: The just modified User instance, 
    #                 or false if the user does not have the permission to modify it. 
    #     """ 
    #     if user_session == 'GESTION': 
    #         # TODO: to put into the menu 
    #         user_to_modify = self.manager.select_one_user('name', 'support_user 1') 
    #         confirmation = session.prompt(f'\nVoulez-vous modifier l\'utilisateur {user_to_modify.name} (id : {user_to_modify.id}) ? (y/n) ') 
    #         modified_user = self.manager.update_user(user_to_modify.id, 'email', 'support_user_1@mail.org') 
    #         if confirmation: 
    #             modified_user_db = self.manager.select_one_user('id', user_to_modify.id) 
    #             print(f'L\'utilisateur {modified_user_db.id} été modifié.') 
    #             return modified_user_db 
    #         else: 
    #             print('Vous avez annulé la modification, l\'utilisateur n\'a pas été modifié.') 
    #     else: 
    #         print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
    #         return False 


    # # TODO: prompt data + retour dans l'application if False. 
    # def modify_client(self, id, field, new_value): 
    #     """ Modifies a client, following the prompted data. 
    #         Permission: COMMERCE, who is referenced as the client's contact. 
    #         paparms: 
    #             id (int): The id of the client to modify. 
    #             field (str): The name of the field to modify. 
    #             new_value (str): The new value to register. 
    #         Returns: 
    #             object Client: The just modified Client instance, 
    #                 or false if the user does not have the permission to modify it. 
    #     """ 
    #     if user_session == 'COMMERCE': 
    #         client_to_modify = self.manager.select_one_client('id', 1) 
    #         if client_to_modify.sales_contact_id == logged_user.id: 
    #             # TODO: to put into the menu 
    #             # user_name = session.prompt('\nQuel est le nom complet de l\'utilisateur à modifier ? ') 
    #             # user_to_modify = self.manager.select_one_user('name', user_name) 
    #             confirmation = session.prompt(f'\nVoulez-vous modifier le client {client_to_modify.name} (id : {client_to_modify.id}) ? (y/n) ') 
    #             modified_client = self.manager.update_client(client_to_modify.id, 'sales_user_name', 'sales_user_1') 
    #             if confirmation: 
    #                 modified_client_db = self.manager.select_one_client('id', client_to_modify.id) 
    #                 print(f'Le client {modified_client_db.id} été modifié.') 
    #                 return modified_client_db 
    #             else: 
    #                 print('Vous avez annulé la modification, le client n\'a pas été modifié.') 
    #             modified_client_db = self.manager.select_one_client('id', client_to_modify.id) 
    #             return modified_client_db 
    #         else: 
    #             print('Vous n\'avez pas l\'autorisation d\'effectuer cette action (département Commerce).') 
    #             return False 
    #     else: 
    #         print('Vous n\'avez pas l\'autorisation d\'effectuer cette action (Commercial responsable du client).') 
    #         return False 


    # # TODO: prompt data + retour dans l'application if False. 
    # def modify_contract(self, id, field, new_value): 
    #     """ Modifies a contract, following the prompted data. 
    #         Permission: COMMERCE, who is referenced as the client's contact. 
    #         paparms: 
    #             id (int): The id of the contract to modify. 
    #             field (str): The name of the field to modify. 
    #             new_value (str): The new value to register. 
    #         Returns: 
    #             object Contract: The just modified Contract instance, 
    #                 or false if the user does not have the permission to modify it. 
    #     """ 
    #     if user_session == 'COMMERCE': 
    #         contract_to_modify = self.manager.select_one_contract('id', 1) 
    #         contract_to_modify_sales_contact = contract_to_modify.client_id.sales_contact_id 
    #         if contract_to_modify_sales_contact == logged_user.id: 
    #             confirmation = session.prompt(f'\nVoulez-vous modifier le contrat numéro {contract_to_modify.id} ? (y/n) ') 
    #             modified_client = self.manager.update_client(contract_to_modify.id, 'paid_amount', 700) 
    #             if confirmation: 
    #                 modified_contract_db = self.manager.select_one_contract('id', contract_to_modify.id) 
    #                 print(f'Le contrat {modified_contract_db.id} été modifié.') 
    #                 return modified_contract_db 
    #             else: 
    #                 print('Vous avez annulé la modification, le contrat n\'a pas été modifié.') 
    #         else: 
    #             print('Vous n\'avez pas l\'autorisation d\'effectuer cette action (département Commerce).') 
    #             return False 
    #     else: 
    #         print('Vous n\'avez pas l\'autorisation d\'effectuer cette action (Commercial responsable du client).') 
    #         return False 


    # # TODO: prompt data + retour dans l'application if False. 
    # def modify_event(self, id, field, new_value):  # TODO 
        # """ Modifies a event, following the prompted data. 
        #     Permission: GESTION. 
        #     paparms: 
        #         id (int): The id of the event to modify. 
        #         field (str): The name of the field to modify. 
        #         new_value (str): The new value to register. 
        #     Returns: 
        #         object Contract: The just modified Event instance, 
        #             or false if the user does not have the permission to modify it. 
        # """ 
        # if (user_session == 'GESTION') | (user_session == 'SUPPORT'): 
        #     event_to_modify = self.manager.select_one_event('id', 1) 
        #     confirmation = session.prompt(f'\nVoulez-vous modifier l\'événement {event_to_modify.name} (id : {event_to_modify.id}) ? (y/n) ') 
        #     if (confirmation != 'y') | (confirmation != 'Y'): 
        #         print('Vous avez annulé la modification, l\'événement n\'a pas été modifié.') 
        #     else: 
        #         # TODO: to put into the menu 
        #         modified_event = self.manager.update_event(contract_to_modify.id, 'support_contact_id', support_contact_id) 
        #         modified_event_db = self.manager.select_one_event('id', event_to_modify.id) 
        #         print(f'L\'événement {modified_event_db.name} été modifié.') 
        #         return modified_event_db 
        # else: 
        #     print('Vous n\'avez pas l\'autorisation d\'effectuer cette action (département Gestion).') 
        #     return False 



    # ========= View all entities ======== # 
    # TODO: prompt data + retour dans l'application if False. 
    def view_all_factory(self, entities): 
        """ View all instances of a model. 
            Permissions: Utilisateur enregistré et connecté. 
            Lecture seule. 
            Args: 
                entities (str): (In plural) The entity to select 
            Returns: 
                list: The retrieved instances. 
        """ 
        if user_session in ['GESTION', 'COMMERCE', 'SUPPORT']: 
            if entities == clients: 
                clients_db = self.manager.select_all_entities('clients') 
                # clients_db = self.manager.select_all_clients() 
                print(f'Clients trouvés : ') 
                for client in clients_db: 
                    print(f'{client.name} ({client.id}), {client.corporation_name}') 
                    print(f'{client.email}, {client.phone}') 
                    print(f'{client.users.name} (id : {client.sales_contact_id})') 
                return clients_db 
            elif entities == contracts: 
                contracts_db = self.manager.select_all_entities('contracts') 
                # contracts_db = self.manager.select_all_contracts() 
                print(f'Contrats trouvés : ') 
                for contract in contracts_db: 
                    print(f'{contract.id} {contract.client.name}') 
                return contracts_db 
            elif entities == events: 
                events_db = self.manager.select_all_entities('events') 
                # events_db = self.manager.select_all_events() 
                print(f'Evénements trouvés : ') 
                for event in events_db: 
                    print(f'{event.id} {event.name}') 
                return events_db 
            else: 
                print(f'Cet objet ({entities}) n\'existe pas.') 
                return false 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return false 

    
    def view_all_users(self): 
        """ View all users. Permission: Only Gestion users can do this. 
            Returns:
                list: The list of all the users registered. 
        """ 
        if user_session == 'GESTION': 
            users_db = self.manager.select_all_entities('users') 
            # users_db = self.manager.select_all_users() 
            if users_db is None: 
                print('Aucun utilisateur à afficher.') 
                return False 
            else: 
                print(f'Utilisateurs trouvés : ') 
                for user in users_db: 
                    print(f'{user.id} {user.name} {user.departement}') 
                return users_db 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return false 


    def view_all_departments(self): 
        """ View all departments. Permission: Only Gestion users can do this. 
            Returns:
                list: The list of all the departments registered. 
        """ 
        if self.user_session == 'GESTION': 
            depts_db = self.manager.select_all_entities('depts') 
            # depts_db = self.manager.select_all_depts() 
            if depts_db is None: 
                print('Aucun département à afficher.') 
                return False 
            else: 
                print(f'Départementss trouvés : ') 
                for dept in depts_db: 
                    print(f'{dept.id} {dept.name}.') 
                return depts_db 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return false 

    # ========= /View all entities ======== # 



    # TODO: à découper pour les menus : 
    # ========= View filtered entities ======== # 

    def view_events_without_support(self): 
        """ Select all the events those don't have a support contact. 
            Permission: Only gestion users can do this. 
            Returns:
                list: All the selected events. 
        """ 
        if user_session == 'GESTION': 
            events_db = self.manager.select_entities_with_criteria( 
                'events', 'without support', None 
            ) 
            if events_db is None: 
                print('Tous les événements ont un contact support.') 
                return False 
            else: 
                print(f'Evénements trouvés : ') 
                for event in events_db: 
                    print(f'{event.id} {event.name}') 
                return events_db 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return false 


    def view_sales_clients(self): 
        """ Select all the sales user's clients. 
            Permission: Only sales users can do this. 
            Returns:
                list: All the selected clients. 
        """ 
        if user_session == 'COMMERCE': 
            clients_db = self.manager.select_entities_with_criteria( 
                'clients', 'sales contact', self.user_session.id 
                # 'clients', 'sales contact', logged_user.id 
            ) 
            if clients_db is None: 
                print('Vous n\'avez aucun client.') 
                return False 
            else: 
                print(f'Clients trouvés : ') 
                for client in clients_db: 
                    print(f'{client.id} {client.name} contact commerce : {clients.sales_contact_id}') 
                return clients_db 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return false 


    def view_sales_contracts(self): 
        """ Select all the sales user's contracts. 
            Permission: Only sales users can do this. 
            Returns:
                list: All the selected contracts. 
        """ 
        if user_session == 'COMMERCE': 
            contracts_db = self.manager.select_entities_with_criteria( 
                'contracts', 'sales contact', self.user_session.id 
                # 'contracts', 'sales contact', logged_user.id 
            ) 
            if contracts_db is None: 
                print('Vous n\'avez aucun contrat.') 
                return False 
            else: 
                print(f'Contrats trouvés : ') 
                for contract in contracts_db: 
                    print(f'{contract.id} {contract.clients.name} contact commerce : {contract.clients.sales_contact_id}')  # *** 
                return contracts_db 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return false 

    #  + not signed contracts 
    def view_not_paid_contracts(self): 
        """ Select all the sales user's contracts those don't be entirely paid. 
            Permission: Only sales users can do this. 
            Returns:
                list: All the selected contracts. 
        """ 
        if user_session == 'COMMERCE': 
            contracts_db = self.manager.select_entities_with_criteria( 
                'contracts', 'not paid id', self.user_session.id 
                # 'contracts', 'not paid id', logged_user.id 
            ) 
            if contracts_db is None: 
                print('Tous vos clients ont réglé leurs contrats.') 
                return False 
            else: 
                print(f'Contrats trouvés : ') 
                for contract in contracts_db: 
                    print(f'{contract.id} {contract.clients.name} montant : {contract.amount}, montant payé : {contract.paid_amount}') 
                return contracts_db 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return false 


    def view_support_events(self): 
        """ Select all the support user's events. 
            Permission: Only support users can do this. 
            Returns:
                list: All the selected events. 
        """ 
        if user_session == 'SUPPORT': 
            events_db = self.manager.select_entities_with_criteria( 
                'events', 'support id', self.user_session.id 
                # 'events', 'support id', logged_user.id 
            ) 
            if events_db is None: 
                print('Vous n\'avez aucun événement.') 
                return False 
            else: 
                print(f'Evénements trouvés : ') 
                for event in events_db: 
                    print(f'{event.id} {event.name} contact support : {event.support_contact_id}') 
                return events_db 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return false 

    # ========= /View filtered entities ======== # 


    # # ========= delete entities ======== # 
    # def delete_one_entity(self, entity, id): 
    #     if self.user_session.dept != 'GESTION': 
    #         print(f'Vous n\'avez pas l\'autorisation d\'effectuer cette action. Contactez un admin.') 
    #     else: 
    #         if entity == 'users': 
    #             entity_to_delete = self.manager.select_one_( 
    #                 'user', 
    #                 'id', 
    #                 id 
    #             ) 
    #             # entity_to_delete = self.manager.select_one_user('id', id) 
    #             confirmation = session.prompt(f'Êtes-vous sûr de vouloir supprimer cet objet {entity_to_delete} ? Y/N ') 
    #             if (confirmation != 'y') | (confirmation != 'Y'): 
    #                 print(f'Vous avez annulé la suppression, l\'objet {entity_to_delete} n\'a pas été supprimé.') 
    #             else: 
    #                 self.manager.delete_user('id', id) 
    #                 # all_users_db = self.manager.select_all_users() 
    #                 self.view_all_factory('users') 
    #         if entity == 'departments': 
    #             entity_to_delete = self.manager.select_one_( 
    #                 'dept', 
    #                 'id', 
    #                 id 
    #             ) 
    #             # entity_to_delete = self.manager.select_one_dept('id', id) 
    #             users_impacted = self.manager.select_entities_with_criteria('users', 'department', id) 
    #             print(f'! ATTENTION ! Cette action entraînera la suppression d\'utilisateurs.') 
    #             confirmation = session.prompt(f''' 
    #                 Êtes-vous sûr de vouloir supprimer ce département {entity_to_delete} et les utilisateurs {users_impacted} ? Y/N 
    #                 ''') 
    #             if (confirmation != 'y') | (confirmation != 'Y'): 
    #                 print(f'Vous avez annulé la suppression, le département et les utilisateurs {entity_to_delete} n\'ont pas été supprimés.') 
    #             else: 
    #                 self.manager.delete_dept('id', id) 
    #                 # all_users_db = self.manager.select_all_users() 
    #                 self.view_all_factory('departments') 

    # # ========= /delete entities ======== # 


    # === actions ==== # 
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




    @staticmethod 
    def press_enter_to_continue(): 
        session.prompt('Appuyez sur entrée pour continuer ') 

    """ Command to quit the application """ 
    @staticmethod 
    def close_the_app(): 
        print('\nFermeture de l\'application. Bonne fin de journée !') 

    # === /actions ==== # 







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




