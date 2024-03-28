
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
                if logged_user.departments.name == 'gestion': 
                    self.user_session = 'GESTION' 
                if logged_user.departments.name == 'commerce': 
                    self.user_session = 'COMMERCE' 
                if logged_user.departments.name == 'support': 
                    self.user_session = 'SUPPORT' 
                print(self.user_session) 
            else: 
                print(self.user_session) 

            action = session.prompt('\nVoir tous les clients ? ') 
            if (action == 'y') | (action == 'Y'): 
                all_clients = self.manager.select_all_clients() 
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
    #                 Attendees=fields['Attendees'], 
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
                # new_entity_db = self.manager.select_one_user('name', fields['name']) 
                print(f'L\'utilisateur {new_user.name} (id : {new_user.id}) a été créé.') 
                return new_user 
            elif entity == 'contract': 
                new_contract = self.manager.add_contract( 
                    client_name=fields['client_name'], 
                    amount=fields['amount'], 
                    paid_amount=fields['paid_amount'], 
                    is_signed=fields['is_signed'] 
                ) 
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
                    sales_contact_id=logged_user.id 
                ) 
                # new_entity_db = self.manager.select_one_client('name', fields['name']) 
                print(f'Le client {new_client.name} (id : {new_client.id}) a été créé.') 
                return new_client 
            elif entity == 'event':  # TODO 
                new_event = self.manager.add_event( 
                    name=fields['name'], 
                    contract_id=fields['contract_id'], 
                    start_datetime=fields['start_datetime'], 
                    end_datetime=fields['end_datetime'], 
                    location=fields['location'], 
                    Attendees=fields['Attendees'], 
                    notes=fields['notes'] 
                ) 
                # new_entity_db = self.manager.select_one_event('name', fields['name']) 
                print(f'L\'événement {new_event.name} (id : {new_event.id}) a été créé.') 
                return new_event 
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
        """ Modifies a event, following the prompted data. 
            Permission: GESTION. 
            paparms: 
                id (int): The id of the event to modify. 
                field (str): The name of the field to modify. 
                new_value (str): The new value to register. 
            Returns: 
                object Contract: The just modified Event instance, 
                    or false if the user does not have the permission to modify it. 
        """ 
        if (user_session == 'GESTION') | (user_session == 'SUPPORT'): 
            event_to_modify = self.manager.select_one_event('id', 1) 
            confirmation = session.prompt(f'\nVoulez-vous modifier l\'événement {event_to_modify.name} (id : {event_to_modify.id}) ? (y/n) ') 
            modified_event = self.manager.update_event(contract_to_modify.id, 'support_contact_id', support_contact_id) 
            if confirmation: 
                # TODO: to put into the menu 
                modified_event_db = self.manager.select_one_event('id', event_to_modify.id) 
                print(f'L\'événement {modified_event_db.name} été modifié.') 
                return modified_event_db 
            else: 
                print('Vous avez annulé la modification, l\'événement n\'a pas été modifié.') 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action (département Gestion).') 
            return False 



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
        if user_session == 'GESTION': 
            if entity == 'user': 
                entity_to_modify = self.manager.select_one_user('id', 1) 
                confirmation = session.prompt(f'\nVoulez-vous modifier l\'utilisateur {entity_to_modify.name} (id : {entity_to_modify.id}) ? (y/n) ') 
                if (confirmation != 'y') | (confirmation != 'Y'): 
                    print('Vous avez annulé la modification, l\'utilisateur n\'a pas été modifié.') 
                else: 
                    modified_entity = self.manager.update_user(id, field, new_value) 
                    modified_entity_db = self.manager.select_one_user('id', id) 
                    print(f'L\'utilisateur {id} été modifié.') 
                    return modified_entity_db 
            elif entity == 'event': 
                entity_to_modify = self.manager.select_one_event(field, value) 
                confirmation = session.prompt(f'\nVoulez-vous modifier l\'événement {entity_to_modify.name} (id : {entity_to_modify.id}) ? (y/n) ') 
                if (confirmation != 'y') | (confirmation != 'Y'): 
                    print('Vous avez annulé la modification, l\'événement n\'a pas été modifié.') 
                else: 
                    modified_entity = self.manager.update_event(id, 'support_contact_id', new_value) 
                    modified_entity_db = self.manager.select_one_event('id', id) 
                    print(f'L\'événement {modified_entity_db.name} (id : {modified_entity_db.id}) été modifié.') 
                    return modified_entity_db 
            else: 
                print(f'Cet objet ({entity}) n\'existe pas.') 
                return false 
        elif user_session != 'COMMERCE': 
            if entity == 'client': 
                responsible_sales_contact = self.manager.select_one_client('id', 1).sales_contact_id 
                if responsible_sales_contact != logged_user.id: 
                    print('Vous n\'avez pas l\'autorisation d\'effectuer cette action (Commercial responsable du client).') 
                    return False 
                else: 
                    confirmation = session.prompt(f'\nVoulez-vous modifier le client {entity_to_modify.name} (id : {entity_to_modify.id}) ? (y/n) ') 
                    if (confirmation != 'y') | (confirmation != 'Y'): 
                        print('Vous avez annulé la modification, le client n\'a pas été modifié.') 
                    else: 
                        modified_entity = self.manager.update_client(id, field, new_value) 
                        modified_entity_db = self.manager.select_one_user('id', id) 
                        print(f'L\'utilisateur {modified_entity_db.name} (id : {id}) été modifié.') 
                        return modified_entity_db 
            elif entity == 'contract': 
                responsible_sales_contact = self.manager.select_one_contract('id', 1).clients.sales_contact_id 
                if responsible_sales_contact != logged_user.id: 
                    print('Vous n\'avez pas l\'autorisation d\'effectuer cette action (Commercial responsable du client).') 
                    return False 
                else: 
                    confirmation = session.prompt(f'\nVoulez-vous modifier le contrat {entity_to_modify.id} concernant le client {entity_to_modify.clients.name}) ? (y/n) ') 
                    if (confirmation != 'y') | (confirmation != 'Y'): 
                        print('Vous avez annulé la modification, le contrat n\'a pas été modifié.') 
                    else: 
                        modified_entity = self.manager.update_contract(id, field, new_value) 
                        modified_entity_db = self.manager.select_one_user('id', id) 
                        print(f'Le contrat numéro {id} été modifié.') 
                        return modified_entity_db 
            else: 
                print(f'Cet objet ({entity}) n\'existe pas.') 
                return false 
        
        elif user_session == 'SUPPORT': 
            if entity == 'event': 
                responsible_support_contact = self.manager.select_one_event('id', id).support_contact_id 
                if responsible_support_contact != user_session.id: 
                    print('Vous n\'avez pas l\'autorisation d\'effectuer cette action (Support responsable de l\'événement).') 
                    return False 
                else: 
                    confirmation = session.prompt(f'\nVoulez-vous modifier l\'événement {entity_to_modify.name} (id : {entity_to_modify.id}) ? (y/n) ') 
                    if (confirmation != 'y') | (confirmation != 'Y'): 
                        print('Vous avez annulé la modification, l\'événement n\'a pas été modifié.') 
                    else: 
                        modified_entity = self.manager.update_event(id, field, new_value) 
                        modified_entity_db = self.manager.select_one_event('id', id) 
                        print(f'L\'événement {id} été modifié.') 
                        return modified_entity_db 
            else: 
                print(f'Cet objet ({entity}) n\'existe pas.') 
                return false 
        else: 
            print('Vous n\'avez pas l\'autorisation d\'effectuer cette action.') 
            return false 
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
                clients_db = self.manager.select_all_clients() 
                print(f'Clients trouvés : ') 
                for client in clients_db: 
                    print(f'{client.name} ({client.id}), {client.corporation_name}') 
                    print(f'{client.email}, {client.phone}') 
                    print(f'{client.users.name} (id : {client.sales_contact_id})') 
                return clients_db 
            elif entities == contracts: 
                contracts_db = self.manager.select_all_contracts() 
                print(f'Contrats trouvés : ') 
                for contract in contracts_db: 
                    print(f'{contract.id} {contract.client.name}') 
                return contracts_db 
            elif entities == events: 
                events_db = self.manager.select_all_events() 
                print(f'Evénements trouvés : ') 
                for event in events_db: 
                    print(f'{event.id} {event.name}') 
                return events_db 
            else: 
                print(f'Cet objet ({entities}) n\'existe pas.') 
                return false 
    # ========= /View all entities ======== # 
 
    # TODO: à découper pour les menus : 
    # ========= View filtered entities ======== # 
    def select_entities_with_criteria(self, entities, criteria): 
        if user_session == 'GESTION': 
            if entities == 'users': 
                users_db = self.manager.select_all_users() 
                if users_db is None: 
                    print('Aucun utilisateur avec ces informations.') 
                    return False 
                else: 
                    print(f'Utilisateurs trouvés : ') 
                    for user in users_db: 
                        print(f'{user.id} {user.name} {user.departement}') 
                    return users_db 
            if entities == 'events': 
                if criteria == 'without support': 
                    events_db = self.manager.select_entities_with_criteria('events', 'without support', None) 
                    if events_db is None: 
                        print('Aucun événement avec ces informations.') 
                        return False 
                    else: 
                        print(f'Evénements trouvés : ') 
                        for event in events_db: 
                            print(f'{event.id} {event.name} {event.support_contact_id}') 
                        return events_db 
                elif criteria == 'support id': 
                    events_db = self.manager.select_entities_with_criteria('events', 'support id', logged_user.id) 
                    if events_db is None: 
                        print('Aucun événement avec ces informations.') 
                        return False 
                    else: 
                        print(f'Evénements trouvés : ') 
                        for event in events_db: 
                            print(f'{event.id} {event.name} contact support : {event.support_contact_id}') 
                        return events_db 

        elif user_session == 'COMMERCE': 
            if entities == 'clients': 
                clients_db = self.manager.select_entities_with_criteria('clients', 'sales id', logged_user.id) 
                if clients_db is None: 
                    print('Aucun client avec ces informations.') 
                    return False 
                else: 
                    print(f'Clients trouvés : ') 
                    for client in clients_db: 
                        print(f'{client.id} {client.name} contact commerce : {clients.sales_contact_id}') 
                    return clients_db 
            elif entities == 'contracts': 
                if criteria == 'sales id': 
                    contracts_db = self.manager.select_entities_with_criteria('contracts', 'sales id', logged_user.id) 
                    if clients_db is None: 
                        print('Aucun contrat avec ces informations.') 
                        return False 
                    else: 
                        print(f'Contrats trouvés : ') 
                        for contract in contracts_db: 
                            print(f'{contract.id} {contract.clients.name} contact commerce : {contract.clients.sales_contact_id}') 
                        return contracts_db 
                if criteria == 'not paid': 
                    contracts_db = self.manager.select_entities_with_criteria('contracts', 'not paid id', None) 
                    if clients_db is None: 
                        print('Aucun client avec ces informations.') 
                        return False 
                    else: 
                        print(f'Contrats trouvés : ') 
                        for contract in contracts_db: 
                            print(f'{contract.id} {contract.clients.name} montant : {contract.amount}, montant payé : {contract.paid_amount}') 
                        return contracts_db 

        elif user_session == 'SUPPORT': 
            if entities == 'events': 
                if criteria == 'support id': 
                    events_db = self.manager.select_entities_with_criteria('events', 'support id', logged_user.id) 
                    if events_db is None: 
                        print('Aucun événement avec ces informations.') 
                        return False 
                    else: 
                        print(f'Evénements trouvés : ') 
                        for event in events_db: 
                            print(f'{event.id} {event.name} contact support : {event.support_contact_id}') 
                        return events_db 
    # ========= /View filtered entities ======== # 









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

