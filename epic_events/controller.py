
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
        self.views = Views() 
        self.manager = Manager() 
        self.manager.connect() 
        self.manager.create_session() 

        self.user_session = None 


    # def start(self, mode, user_session=None): 
    def start(self, mode): 
        # self.user_session = None 
        test_prompt = session.prompt('test controller : ') 
        print(test_prompt) 

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
            logged_user = self.manager.select_one_entity( 
                'user',  
                'email', 
                userConnect['email'] 
            ) 
            # logged_user = self.manager.select_one_user( 
            #     'email', userConnect['email']) 

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
                updated_user_db = self.manager.select_one_entity( 
                    'user', 
                    'email', 
                    logged_user.email 
                ) 
                # updated_user_db = self.manager.select_one_user('email', logged_user.email) 
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

            action = session.prompt('\nVoir tous les clients ? ') 
            if (action == 'y') | (action == 'Y'): 
                all_clients = self.manager.select_all_entities('clients') 
                # all_clients = self.manager.select_all_clients() 
                if all_clients == []: 
                    print(f'Aucun client') 
                else: 
                    for client in all_clients: 
                        print(f'client : {client}') 



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


    # ========= creation factory ======== # 
    # TODO: prompt data + retour dans l'application if False. 
    def create_factory(self, entity, fields:dict): 
        """ Creates a new 'entity', following the prompted data. 
            Returns: 
                object 'entity': The just created 'entity' instance, 
                    or false if the user does not have the permission to create it. 
        """ 
        if user_session == 'GESTION': 
            if entity == 'user': 
                new_user = self.manager.add_user( 
                    name=fields['name'], 
                    email=fields['email'], 
                    phone=fields['phone'], 
                    department_name=fields['department_name']  
                ) 
                new_entity_db = self.manager.select_one_entity( 
                    'user', 
                    'name', 
                    fields['name'] 
                ) 
                # new_entity_db = self.manager.select_one_user('name', fields['name']) 
                print(f'L\'utilisateur {new_entity_db.name} (id : {new_entity_db.id}) a été créé.') 
                return new_user 
            elif entity == 'contract': 
                new_contract = self.manager.add_contract( 
                    client_name=fields['client_name'], 
                    amount=fields['amount'], 
                    paid_amount=fields['paid_amount'], 
                    is_signed=fields['is_signed'] 
                ) 
                # new_entity_db = self.manager.select_last_entity('contract')  # value : client_name 
                # new_entity_db = self.manager.select_last_contract(value)  # value : client_name 
                print(f'Le contrat {new_contract.name} (id : {new_contract.id}) a été créé.') 
                return new_contract 
            else: 
                print(f'Cet objet ({entity}) n\'existe pas.') 
                return false 
        elif user_session == 'COMMERCE': 
            if entity == 'client': 
                new_client = self.manager.add_client( 
                    name=fields['name'], 
                    email=fields['email'], 
                    phone=fields['phone'], 
                    corporation_name=fields['corporation_name'], 
                    sales_contact_id=self.user_session.id 
                    # sales_contact_id=logged_user.id 
                ) 
                new_entity_db = self.manager.select_one_entity( 
                    'client', 
                    'name', 
                    fields['name'] 
                ) 
                new_entity_db = self.manager.select_one_entity( 
                    'client', 
                    'name', 
                    fields['name'] 
                ) 
                # new_entity_db = self.manager.select_one_client('name', fields['name']) 
                print(f'Le client {new_entity_db.name} (id : {new_entity_db.id}) a été créé.') 
                return new_entity_db 
            elif entity == 'event':  # TODO 
                new_event = self.manager.add_event( 
                    name=fields['name'], 
                    contract_id=fields['contract_id'], 
                    start_datetime=fields['start_datetime'], 
                    end_datetime=fields['end_datetime'], 
                    location=fields['location'], 
                    attendees=fields['attendees'], 
                    notes=fields['notes'] 
                ) 
                new_entity_db = self.manager.select_one_entity( 
                    'event', 
                    'name', 
                    fields['name'] 
                ) 
                # new_entity_db = self.manager.select_one_event('name', fields['name']) 
                print(f'L\'événement {new_entity_db.name} (id : {new_entity_db.id}) a été créé.') 
                return new_entity_db 
            else: 
                print(f'Cet objet ({entity}) n\'existe pas.') 
                return false 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return False 
    # ========= /creation factory ======== # 




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



    # ========= modify factory ======== # 
    # TODO: prompt data + retour dans l'application if False. 
    def modify_factory(self, entity, id, field, new_value): 
        """ Creates a 'modify' request on an 'entity', following the prompted data, and check the 'permission'. 
            Permission: regarding to the entity, and who is referenced/or not as the entity's contact. 
            paparms: 
                entity (str): model of the instance to modify. 
                id (int): The id of the instance to modify. 
                field (str): The name of the field to modify. 
                new_value (str): The new value to register instead. 
            Returns: 
                object 'entity': The just modified 'entity' instance, 
                    or false if the user does not have the permission to modify it. 
        """ 
        # TODO 
        if user_session == 'GESTION': 
            gestion_entities_dict = { 
                'dept': self.manager.select_one_entity('department', 'id', id), 
                # 'dept': self.manager.select_one_dept('id', id), 
                'user': self.manager.select_one_user('user', 'id', id), 
                # 'user': self.manager.select_one_user('id', id), 
                'event': self.manager.select_one_event('event', 'id', id) 
                # 'event': self.manager.select_one_event('id', id) 
            } 
            if entity not in gestion_entities_dict.keys(): 
                print(f'Cet objet ({entity}) n\'existe pas.') 
                return false 
            else: 
                for entity in gestion_entities_dict.keys(): 
                    entity_to_modify = gestion_entities_dict[entity] 
                    confirmation = session.prompt(f'\nVoulez-vous modifier l\'enregistrement {entity_to_modify} ? (y/n) ') 
                    if (confirmation != 'y') | (confirmation != 'Y'): 
                        print('Vous avez annulé la modification, l\'enregistrement n\'a pas été modifié.') 
                    else: 
                        modified_entity = self.manager.update_entity(id, field, new_value) 
                        modified_entity_db = self.select_one_entity('id', id) 
                        return modified_entity_db 
        elif user_session == 'COMMERCE': 
            sales_entities_dict = { 
                'client': self.manager.select_one_entity( 
                    'client', 
                    'id', 
                    id 
                ), 
                # 'client': self.manager.select_one_client('id', id), 
                'contract': self.manager.select_one_entity( 
                    'contract', 
                    'id', 
                    id 
                ), 
                # 'contract': self.manager.select_one_contract('id', id), 
            } 
            if entity not in sales_entities_dict.keys(): 
                print(f'Cet objet ({entity}) n\'existe pas.') 
                return false 
            else: 
                for entity in sales_entities_dict.keys(): 
                    entity_to_modify = sales_entities_dict[entity] 
                    confirmation = session.prompt(f'\nVoulez-vous modifier l\'enregistrement {entity_to_modify} ? (y/n) ') 
                    if (confirmation != 'y') | (confirmation != 'Y'): 
                        print('Vous avez annulé la modification, l\'enregistrement n\'a pas été modifié.') 
                    else: 
                        modified_entity = self.manager.update_entity(id, field, new_value) 
                        modified_entity_db = self.select_one_entity('id', id) 
                        return modified_entity_db 
        elif user_session == 'SUPPORT': 
            support_entities_dict = { 
                'event': self.manager.select_one_entity( 
                    'event', 
                    'id', 
                    id 
                ) 
                # 'event': self.manager.select_one_event('id', id) 
            } 
            if entity not in support_entities_dict.keys(): 
                print(f'Cet objet ({entity}) n\'existe pas.') 
                return false 
            else: 
                for entity in support_entities_dict.keys(): 
                    entity_to_modify = support_entities_dict[entity] 
                    confirmation = session.prompt(f'\nVoulez-vous modifier l\'enregistrement {entity_to_modify} ? (y/n) ') 
                    if (confirmation != 'y') | (confirmation != 'Y'): 
                        print('Vous avez annulé la modification, l\'enregistrement n\'a pas été modifié.') 
                    else: 
                        modified_entity = self.manager.update_entity(id, field, new_value) 
                        modified_entity_db = self.select_one_entity('id', id) 
                        return modified_entity_db 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return false 

        # if user_session == 'GESTION': 
        #     if entity == 'user': 
        #         entity_to_modify = self.manager.select_one_user('id', 1) 
        #         confirmation = session.prompt(f'\nVoulez-vous modifier l\'utilisateur {entity_to_modify.name} (id : {entity_to_modify.id}) ? (y/n) ') 
        #         if (confirmation != 'y') | (confirmation != 'Y'): 
        #             print('Vous avez annulé la modification, l\'utilisateur n\'a pas été modifié.') 
        #         else: 
        #             modified_entity = self.manager.update_user(id, field, new_value) 
        #             modified_entity_db = self.manager.select_one_user('id', id) 
        #             print(f'L\'utilisateur {modified_entity_db} été modifié.') 
        #             return modified_entity_db 
        #     elif entity == 'event': 
        #         entity_to_modify = self.manager.select_one_event(field, value) 
        #         confirmation = session.prompt(f'\nVoulez-vous modifier l\'événement {entity_to_modify.name} (id : {entity_to_modify.id}) ? (y/n) ') 
        #         if (confirmation != 'y') | (confirmation != 'Y'): 
        #             print('Vous avez annulé la modification, l\'événement n\'a pas été modifié.') 
        #         else: 
        #             modified_entity = self.manager.update_event(id, 'support_contact_id', new_value) 
        #             modified_entity_db = self.manager.select_one_event('id', id) 
        #             print(f'L\'événement {modified_entity_db.name} (id : {modified_entity_db.id}) été modifié : contact support id {modified_entity_db.support_contact_id}, nom {modified_entity_db.users.name}.') 
        #             return modified_entity_db 
            # else: 
            #     print(f'Cet objet ({entity}) n\'existe pas.') 
            #     return false 
        # elif user_session == 'COMMERCE': 
        #     if entity == 'client': 
        #         entity_to_modify = self.manager.select_one_client('id', id) 
        #         responsible_sales_contact = entity_to_modify.sales_contact_id 
        #         if responsible_sales_contact != self.user_session.id: 
        #         # if responsible_sales_contact != logged_user.id: 
        #             print('Vous n\'avez pas l\'autorisation d\'effectuer cette action (Commercial responsable du client).') 
        #             return False 
        #         else: 
        #             confirmation = session.prompt(f'\nVoulez-vous modifier le client {entity_to_modify.name} (id : {entity_to_modify.id}) ? (y/n) ') 
        #             if (confirmation != 'y') | (confirmation != 'Y'): 
        #                 print('Vous avez annulé la modification, le client n\'a pas été modifié.') 
        #             else: 
        #                 modified_entity = self.manager.update_client(id, field, new_value) 
        #                 modified_entity_db = self.manager.select_one_client('id', id) 
        #                 print(f'Le client {modified_entity_db.name} (id : {id}) été modifié.') 
        #                 return modified_entity_db 
        #     elif entity == 'contract': 
        #         entity_to_modify = self.manager.select_one_contract('id', id) 
        #         client_contract_id = entity_to_modify.client_id 
        #         client_db = self.manager.select_one_client('id', client_contract_id) 
        #         responsible_sales_contact = client_db.sales_contact_id 
        #         # responsible_sales_contact = self.manager.select_one_contract('id', 1).clients.sales_contact_id 
        #         if responsible_sales_contact != self.user_session.id: 
        #         # if responsible_sales_contact != logged_user.id: 
        #             print('Vous n\'avez pas l\'autorisation d\'effectuer cette action (Commercial responsable du client).') 
        #             return False 
        #         else: 
        #             confirmation = session.prompt(f'\nVoulez-vous modifier le contrat {entity_to_modify} concernant le client {entity_to_modify.clients.name}) ? (y/n) ') 
        #             if (confirmation != 'y') | (confirmation != 'Y'): 
        #                 print('Vous avez annulé la modification, le contrat n\'a pas été modifié.') 
        #             else: 
        #                 modified_entity = self.manager.update_contract(id, field, new_value) 
        #                 modified_entity_db = self.manager.select_one_contract('id', id) 
        #                 print(f'Le contrat numéro {modified_entity_db} été modifié.') 
        #                 return modified_entity_db 
            # else: 
            #     print(f'Cet objet ({entity}) n\'existe pas.') 
            #     return false 
        
        # elif user_session == 'SUPPORT': 
        #     if entity == 'event': 
        #         entity_to_modify = self.manager.select_one_event('id', id) 
        #         responsible_support_contact = entity_to_modify.support_contact_id 
        #         if responsible_support_contact != user_session.id: 
        #             print('Vous n\'avez pas l\'autorisation d\'effectuer cette action (Support responsable de l\'événement).') 
        #             return False 
        #         else: 
        #             confirmation = session.prompt(f'\nVoulez-vous modifier l\'événement {entity_to_modify.name} (id : {entity_to_modify.id}) ? (y/n) ') 
        #             if (confirmation != 'y') | (confirmation != 'Y'): 
        #                 print('Vous avez annulé la modification, l\'événement n\'a pas été modifié.') 
        #             else: 
        #                 modified_entity = self.manager.update_event(id, field, new_value) 
        #                 modified_entity_db = self.manager.select_one_event('id', id) 
        #                 print(f'L\'événement {modified_entity_db} été modifié.') 
        #                 return modified_entity_db 
        #     else: 
        #         print(f'Cet objet ({entity}) n\'existe pas.') 
        #         return false 
        # else: 
        #     print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
        #     return false 
    # ========= /modify factory ======== # 


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


    # ========= View one entity ======== # 
    def view_one_entity(self, entity, field, value): 
        """ View one entity, selected with one unique field. All the users can do this, as "read only" displaying. 
            Args:
                entity (str): The entity to view. 
                field (str): The unique field on which to select the entity. 
                value (str): The value to look for. 
            Returns:
                object instance: The entity instance retrieved or None. 
        """ 
        permissions = ['GESTION', 'COMMERCE', 'SUPPORT'] 
        if self.user_session.dept not in permissions: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action, contactez un admin. ') 
            return false 
        else: 
            if entity == 'department': 
                if self.user_session.dept != permissions['0']: 
                    print('Vous n\'avez pas l\'autorisation d\'effectuer cette action, contactez un admin. ') 
                    return false 
                else: 
                    dept_db = self.manager.select_one_entity( 
                        'dept', 
                        field, 
                        value 
                    ) 
                    # dept_db = self.manager.select_one_dept(field, value) 
                    if dept_db is None: 
                        print(f'Il n\'y a pas de département avec ces informations. ') 
                    else: 
                        print(f'Département trouvé : {dept_db}') 
            if entity == 'user': 
                if self.user_session.dept != 'GESTION': 
                    print('Vous n\'avez pas l\'autorisation d\'effectuer cette action, contactez un admin. ') 
                    return false 
                else: 
                    user_db = self.manager.select_one_entity( 
                        'user', 
                        field, 
                        value 
                    ) 
                    # user_db = self.manager.select_one_user(field, value) 
                    if user_db is None: 
                        print(f'Il n\'y a pas d\'utilisateur avec ces informations. ') 
                    else: 
                        print(f'Utilisateur trouvé : {user_db}') 
            if entity == 'client': 
                client_db = self.manager.select_one_entity( 
                    'client', 
                    field, 
                    value 
                ) 
                # client_db = self.manager.select_one_client(field, value) 
                if client_db is None: 
                    print(f'Il n\'y a pas de client avec ces informations. ') 
                else: 
                    print(f'Client trouvé : {client_db}') 
            if entity == 'contract': 
                contract_db = self.manager.select_one_entity( 
                    'contract', 
                    field, 
                    value 
                ) 
                # contract_db = self.manager.select_one_contract(field, value) 
                if contract_db is None: 
                    print(f'Il n\'y a pas de contract avec ces informations. ') 
                else: 
                    print(f'Contract trouvé : {contract_db}') 
            if entity == 'event': 
                event_db = self.manager.select_one_( 
                    'contract', 
                    field, 
                    value 
                ) 
                # event_db = self.manager.select_one_contract(field, value) 
                if event_db is None: 
                    print(f'Il n\'y a pas d\'événement avec ces informations. ') 
                else: 
                    print(f'Evénement trouvé : {event_db}') 
            else: 
                print(f'Cet objet ({entity}) n\'existe pas.') 
                return false 
    # ========= /View one entity ======== # 
 

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


    # ========= delete entities ======== # 
    def delete_one_entity(self, entity, id): 
        if self.user_session.dept != 'GESTION': 
            print(f'Vous n\'avez pas l\'autorisation d\'effectuer cette action. Contactez un admin.') 
        else: 
            if entity == 'users': 
                entity_to_delete = self.manager.select_one_( 
                    'user', 
                    'id', 
                    id 
                ) 
                # entity_to_delete = self.manager.select_one_user('id', id) 
                confirmation = session.prompt(f'Êtes-vous sûr de vouloir supprimer cet objet {entity_to_delete} ? Y/N ') 
                if (confirmation != 'y') | (confirmation != 'Y'): 
                    print(f'Vous avez annulé la suppression, l\'objet {entity_to_delete} n\'a pas été supprimé.') 
                else: 
                    self.manager.delete_user('id', id) 
                    # all_users_db = self.manager.select_all_users() 
                    self.view_all_factory('users') 
            if entity == 'departments': 
                entity_to_delete = self.manager.select_one_( 
                    'dept', 
                    'id', 
                    id 
                ) 
                # entity_to_delete = self.manager.select_one_dept('id', id) 
                users_impacted = self.manager.select_entities_with_criteria('users', 'department', id) 
                print(f'! ATTENTION ! Cette action entraînera la suppression d\'utilisateurs.') 
                confirmation = session.prompt(f''' 
                    Êtes-vous sûr de vouloir supprimer ce département {entity_to_delete} et les utilisateurs {users_impacted} ? Y/N 
                    ''') 
                if (confirmation != 'y') | (confirmation != 'Y'): 
                    print(f'Vous avez annulé la suppression, le département et les utilisateurs {entity_to_delete} n\'ont pas été supprimés.') 
                else: 
                    self.manager.delete_dept('id', id) 
                    # all_users_db = self.manager.select_all_users() 
                    self.view_all_factory('departments') 

    # ========= /delete entities ======== # 









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

