
from sqlalchemy import create_engine 
import psycopg2 
from models import Base, Client, Contract, Department, Event, User   
from sqlalchemy.orm import sessionmaker 

import os 
import bcrypt 
from datetime import datetime, timedelta 
import json 
import jwt 
from jwt.exceptions import ExpiredSignatureError
import re 
# from prompt_toolkit import PromptSession 
# prompt_session = PromptSession() 


class Manager(): 
    print('hello manager') 
    def __init__(self): 
        self.db_user = os.environ.get('POSTGRES_USER') 
        self.db_password = os.environ.get("POSTGRES_PASSWORD") 
        self.db_host = os.environ.get("POSTGRES_HOST") 
        self.db_port = os.environ.get("DB_PORT") 
        self.db_name = os.environ.get("POSTGRES_DB") 
        self.db_url = f"postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}" 

    def connect(self): 
        self.engine = create_engine(self.db_url) 
        # print(conn.info.encoding) 

    def create_session(self): 
        Session = sessionmaker(bind=self.engine) 
        self.session = Session() 


    # ==== department methods ==== # 
    # def add_department(self, fields:dict): 
    #     """ Creates and registers a department. 
    #         Args: 
    #             fields (list): The unique field must be: 'name' as a string. 
    #         Returns: 
    #             object Department: The just created department. 
    #     """
    #     itemName = Department(name=fields['name']) 
    #     self.session.add(itemName) 
    #     self.session.commit() 
    #     return itemName 

    def update_dept(self, new_value, name): 
        """ Modifies a registered department with the new name. 
            Args:
                new_value (string): The new name to register. 
                name (string): The name to replace by the new_value. 
            Returns:
                object Department: The updated instance of Department. 
        """ 
        itemName = self.select_one_dept('name', name) 
        itemName.name = new_value 
        self.session.commit() 
        return itemName 


    def select_one_dept(self, field, value): 
        """ Selects one department following the given field and value. 
            Possible fields: 'id', 'name'. 
            Args:
                field (string): The field on wich select the item. 
                value (string): The value to select it. 
            Returns:
                object Department: The selected instance of Department. 
        """ 
        if field == 'id': 
            item_db = self.session.query(Department).filter( 
                Department.id==int(value)).first() 
        elif field == 'name': 
            item_db = self.session.query( 
                Department).filter(Department.name==value).first() 
        else: 
            print(f'Ce champ "{field}" n\'existe pas.')  
        # print(f'département trouvé (manager.select_one_dept) : {item_db.name}, id : {item_db.id}.') 
        return item_db 



    # def select_all_depts(self): 
    #     """ Returns:
    #             list: All the departments in a list of isntances. 
    #     """ 
    #     items_db = self.session.query(Department).all() 
    #     for item in items_db:
    #         print(f'département trouvé  (manager.select_all_depts) : {item.name}, id : {item.id}.') 
    #     return items_db 


    # TODO: retour dans l'appli si 'N' 
    def delete_dept(self, field, value): 
        """ Delete one registered department, following a unique field. 
            Args:
                field (string): The field name on which select the item. 
                value (string): The field value to select the item to delete. 
        """ 
        print('delete_dept') 
        item_db = self.select_one_dept(field, value) 
        self.session.delete(item_db) 
        self.session.commit() 
        print(f'Le département {item_db.name} (id : {item_db.id}) été supprimé.') 



    # ==== user ==== # 
    # def add_user(self, fields:dict): 
    #     """ Creates a user in the DB. 
    #         Args:
    #             fields (list): [name, email, hashed password, phone, department's name] 
    #         Returns:
    #             object User: The just created User instance. 
    #     """ 
    #     dept_db_id = self.select_one_dept('name', fields[4]).id 

    #     # Hash pass 
    #     hashed_password = self.hash_pw(fields[2], 12) 

    #     # Get token JWT 
    #     delta = 2*3600  # <-- for 'exp' JWT claim, en secondes 
    #     data = { 
    #         'email': fields['email'], 
    #         'pass': fields['pass'], 
    #         'dept': fields['dept'], 
    #     } 
    #     user_token = self.get_token(delta, data) 
    #     userName = User( 
    #         name=fields['name'], 
    #         email=fields['email'], 
    #         password=hashed_password, 
    #         phone=fields['phone'], 
    #         department_id=dept_db_id, 
    #         token=user_token, 
    #     ) 
    #     self.session.add(userName) 
    #     self.session.commit() 
    #     item_db = self.select_all_users().last() 
    #     return item_db 
    #     # return userName 


    def update_user(self, id, field, new_value): 
        """ Modifies a field of a user instance, following its id. 
            Args:
                id (int): The id of the registered user instance. 
                field (string): The name of the field to modify. 
                new_value (string): The new value to register. 
            Returns:
                object User: The just updated User instance. 
        """ 
        print('update_user') 
        itemName = self.select_one_user('id', id) 
        if field == 'name': 
            itemName.name = new_value 
        elif field == 'email': 
            itemName.email = new_value 
        elif field == 'phone': 
            itemName.phone = new_value 
        elif field == 'department_id': 
            itemName.department_id = new_value 
        elif field == 'token': 
            itemName.token = new_value 
        else: 
            print('no value (manager.update_user)') 
        self.session.commit() 
        return itemName 


    def select_one_user(self, field, value): 
        """ Select one user instance following a unique field. 
            Possible fields : 
                'id' 
                'name' 
                'email'. 
            Args:
                field (string): The name of the field to look for. 
                value (string): The value for select the User instance. 
            Returns:
                object User: The selected User instance. 
        """ 
        print('select_one_user') 
        # user_db = User() 
        if field == 'id': 
            user_db = self.session.query(User).filter( 
                User.id==int(value)).first() 
            # self.session.query(Client).filter( 
            #     Client.id==int(value)).first() 
            print('manager user_db : ', user_db) 
            return user_db 
        elif field == 'name': 
            user_db = self.session.query(User).filter( 
                User.name==value).first() 
            # users_db = self.session.query(User).all() 
            return user_db 
        elif field == 'email': 
            user_db = self.session.query(User).filter( 
                User.email==value).first() 
        else: 
            print('no field recognized (manager.select_one_user)') 
        if user_db is None: 
            # TODO : afficher de nouveau la question précédente ? 
            print('Aucun utilisateur avec ces informations (manager.select_one_user)') 
            return False 
        else: 
            # print(f'user trouvé (manager.select_one_user) : {user_db.name}, id : {user_db.id}, mail : {user_db.email}, pass : {user_db.password}, départemt : (id : {user_db.department.id}) name : {user_db.department.name}.') 
            return user_db 
        # print(f'user events.attendees ML206 : {item_db.events}') 
        return user_db 


    # def select_all_users(self): 
    #     """ Returns:
    #             list: All the user instances in a list. 
    #     """ 
    #     items_db = self.session.query(User).all() 
    #     for item in items_db:
    #         print(f'user trouvé  (manager.select_all_users) : {item.name}, id : {item.id}.') 
    #     return items_db 


    def delete_user(self, field, value): 
        """ Delete one registered user, following a unique field. 
            Args:
                field (string): The field name on which select the item. 
                value (string): The field value to select the item to delete. 
        """ 
        print('delete_user') 
        item_db = self.select_one_user(field, value) 
        print('user to delete LM249 : ', item_db) 
        self.session.delete(item_db) 
        self.session.commit() 
        print(f'L\'utilisateur {item_db.name} (id : {item_db.id}) a été supprimé.') 



    # ==== client ==== # 
    # def add_client(self, fields:dict): 
    #     """ Creates a Client instance, giving the data to register. 
    #         The datetime fields are automatically filled. 
    #         Fields: 
    #             name 
    #             email 
    #             phone 
    #             corporation_name 
    #             sales_contact_id*. 
    #         * The "sales_contact_id" is the connected user's id. 
    #         Args:
    #             fields (list): The data to register, or the data to retreive another data to register. 
    #         Returns: 
    #             (object Client): The just created Client instance. 
    #     """ 
    #     print(fields) 
    #     sales_contact = self.select_one_user('name', 'sales_user 1') 
    #     print('sales_contact_id : ', sales_contact.id) 
    #     itemName = Client( 
    #         name=fields['name'], 
    #         email=fields['email'], 
    #         phone=fields['phone'], 
    #         corporation_name=fields['corporation_name'], 
    #         created_at=datetime.now(), 
    #         updated_at=datetime.now(), 
    #         sales_contact_id=sales_contact.id 
    #     ) 
    #     self.session.add(itemName) 
    #     self.session.commit() 
    #     items_list_db = self.select_all_clients()  # .last() 
    #     item_db = items_list_db.pop() 
    #     return item_db 
    #     # return itemName 


    # # TODO : rester dans l'application si pas de client à retourner.  
    def select_one_client(self, field, value): 
        """ Select one client instance following a unique field. 
            Possible fields : 
                'id' 
                'name' 
                'email' 
                'phone' 
            Args:
                field (string): The name of the field to look for. 
                value (string): The value for select the Client instance. 
            Returns:
                object Client: The selected client instance. 
        """ 
        client_db = Client() 
        if field == 'id': 
            client_db = self.session.query(Client).filter( 
                Client.id==int(value)).first() 
        elif field == 'name': 
            client_db = self.session.query(Client).filter( 
                Client.name==value).first() 
        elif field == 'email': 
            client_db = self.session.query(Client).filter( 
                Client.email==value).first() 
        elif field == 'phone': 
            client_db = self.session.query(Client).filter( 
                Client.phone==value).first() 
        else: 
            print('no field recognized (manager.select_one_client)') 
        if client_db is None: 
            # TODO : afficher de nouveau la question précédente ? 
            print('Aucun client avec ces informations (manager.select_one_client)') 
            return False 
        else: 
            # print(f'user trouvé (manager.select_one_client) : {user_db.name}, id : {user_db.id}, mail : {user_db.email}, pass : {user_db.password}, départemt : (id : {user_db.department.id}) name : {user_db.department.name}.') 
            return client_db 

        # user = relationship('User', back_populates="clients") 
        # contract = relationship("Contract", back_populates="clients") 


    def update_client(self, id, field, new_value): 
        """ Modifies a field of a Client instance, following its id. 
            Possible fields: 
                name
                email
                phone
                corporation_name
                sales_contact_name 
            Args:
                id (int): The id of the registered Client instance. 
                field (string): The name of the field to modify. 
                new_value (string): The new value to register. 
            Returns:
                object Client: The just updated Client instance. 
        """ 
        itemName = self.select_one_user('id', id) 
        if field == 'name': 
            itemName.name = new_value 
        elif field == 'email': 
            itemName.email = new_value 
        elif field == 'phone': 
            itemName.phone = new_value 
        elif field == 'corporation_name': 
            itemName.corporation_name = new_value 
        elif field == 'sales_contact_name': 
            sales_contact_db = self.select_one_user('name', new_value) 
            itemName.sales_contact_id = sales_contact_db.id 
        else: 
            print('no value (manager.update_client)') 
        self.session.commit() 
        return itemName 


    # def select_all_clients(self): 
    #     """ Returns:
    #             list: All the Client instances in a list. 
    #     """ 
    #     print('select_all_clients ML348') 
    #     items_db = self.session.query(Client).all() 
    #     # print(items_db) 
    #     for item in items_db:
    #         print(f'client trouvé  (manager.select_all_clients) : {item.name}, id : {item.id}.') 
    #     return items_db 


    # TODO: retour dans l'appli si 'N' 
    def delete_client(self, field, value): 
        """ Delete a Client following a unique field. 
            Args:
                field (string): The field name to select. 
                value (string): The field value to select for deleting. 
        """ 
        item_db = self.select_one_client(field, value) 
        self.session.delete(item_db) 
        self.session.commit() 
        print(f'Le client {item_db.name} (id : {item_db.id}) été supprimé.') 
        


    # ==== contract ==== # 
    # def add_contract(self, fields:dict): 
    #     """ Creates a Contract instance, giving the data to register. The datetime field is automatically filled. 
    #         Args:
    #             fields (list): [ 
    #                 'client_name',
    #                 'amount',
    #                 'paid_amount',
    #                 'is_signed' 
    #             ] 
    #         Returns: 
    #             (object Contract): The just created Contract instance. 
    #     """ 
    #     client_db = self.select_one_client('name', fields['name']) 
    #     itemName = Contract( 
    #         client_id=client_db.id, 
    #         amount=fields['amount'], 
    #         paid_amount=fields['paid_amount'], 
    #         is_signed=fields['is_signed'], 
    #         created_at=datetime.now() 
    #     ) 
    #     self.session.add(itemName) 
    #     self.session.commit() 
    #     item_db = self.select_all_contracts().last() 
    #     return item_db 
    #     # return itemName 


    # # TODO : rester dans l'application si pas de contrat à retourner. 
    def select_one_contract(self, field, value): 
        """ Select one contract instance following a unique field. 
            Possible field: 
                'id' 
            Args:
                field (string): The name of the field to look for. 
                value (string): The value for select the Contract instance. 
            Returns:
                object Contract: The selected Contract instance. 
        """ 
        contract_db = Contract() 
        if field == 'id': 
            contract_db = self.session.query(Contract).filter( 
                Contract.id==int(value)).first() 
        else: 
            print('no field recognized (manager.select_one_contract)') 
        if contract_db is None: 
            # TODO : afficher de nouveau la question précédente ? 
            print('Aucun utilisateur avec ces informations (manager.select_one_user)') 
            return False 
        else: 
            # print(f'user trouvé (manager.select_one_user) : {user_db.name}, id : {user_db.id}, mail : {user_db.email}, pass : {user_db.password}, départemt : (id : {user_db.department.id}) name : {user_db.department.name}.') 
            return contract_db 


    # TODO : rester dans l'application si pas de contrat à retourner. 
    def select_last_contract(self, client_name): 
        """ Select the last contract of a client created. 
            One possible field: 
                'client_name' 
            Args: 
                value (string): The value for select the Contract instance. 
            Returns:
                object Contract: The selected Contract instance. 
        """ 
        contract_db = Contract() 
        client_db = self.select_one_client('name', client_name) 
        # last_contract_db = self.session.query(Contract).filter( 
        #     Contract.client_id==client_db.id).last() 
        contracts_db = self.session.query(Contract).filter( 
            Contract.client_id==client_db.id) 
        print('contracts_db ML447 : ', contracts_db) 
        # last_contract_db = contracts_db.last() 
        if contract_db is None: 
            # TODO : afficher de nouveau la question précédente ? 
            print('Aucun utilisateur avec ces informations (manager.select_one_user)') 
            return False 
        else: 
            # print(f'user trouvé (manager.select_one_user) : {user_db.name}, id : {user_db.id}, mail : {user_db.email}, pass : {user_db.password}, départemt : (id : {user_db.department.id}) name : {user_db.department.name}.') 
            return contract_db 


    def update_contract(self, id, field, new_value): 
        """ Modifies a field of a Contract instance, following its id. 
            Possible fields: 
                amount 
                paid_amount 
                is_signed 
            Args:
                id (int): The id of the registered Contract instance. 
                field (string): The name of the field to modify. 
                new_value (string): The new value to register. 
            Returns:
                object Contract: The just updated Contract instance. 
        """ 
        itemName = self.select_one_user('id', id) 
        if field == 'amount': 
            itemName.amount = new_value 
        elif field == 'paid_amount': 
            itemName.paid_amount = new_value 
        elif field == 'is_signed': 
            itemName.is_signed = new_value 
        elif field == 'department_id': 
            itemName.department_id = new_value 
        else: 
            print('no value (manager.update_contract)') 
        self.session.commit() 
        return itemName 


    # def select_all_contracts(self): 
    #     """ Returns:
    #             list: All the Contract instances in a list. 
    #     """ 
    #     items_db = self.session.query(Contract).all() 
    #     for item in items_db:
    #         print(f'contract trouvé  (manager.select_all_contracts) : {item.name}, id : {item.id}.') 
    #     return items_db 


    # TODO: retour dans l'appli si 'N' 
    def delete_contract(self, field, value): 
        """ Delete a Contract following a unique field. 
            Args:
                field (string): The field name to select. 
                value (string): The field value to select for deleting. 
        """ 
        item_db = self.select_one_contract(field, value) 
        # Verifier client.name *** 
        self.session.delete(item_db) 
        self.session.commit() 
        print(f'Le contrat {item_db.id} été supprimé.') 



    # ==== event ==== # 
    # def add_event(self, fields:list): 
    #     """ Creates an Event instance, giving the data to register. 
    #         The 'support_contact_id' is let empty. A Gestion user will fill it. 
    #         Args:
    #             fields (list): [ 
    #                 'name',
    #                 'contract_id',
    #                 'start_datetime',
    #                 'end_datetime' 
    #                 'location' 
    #                 'attendees' 
    #                 'notes' 
    #             ] 
    #         Returns: 
    #             object Event: The just created Event instance. 
    #     """ 
    #       print('add_event') 
    #     # client_db = self.select_one_client('name', fields[4]) 
    #     user_db = self.select_one_user('name', fields[4]) 
    #     itemName = Event( 
    #         name=fields[0], 
    #         contract_id=fields[1], 
    #         start_datetime=fields[2], 
    #         end_datetime=fields[3], 
    #         # support_contact_id=fields[user_db.id], 
    #         location=fields[4], 
    #         attendees=fields[5], 
    #         notes=fields[6] 
    #     ) 
    #     self.session.add(itemName) 
    #     self.session.commit() 
    #     item_db = self.select_all_events().last() 
    #     return item_db  
    #     # return itemName 


    # # TODO : rester dans l'application si pas d'événemt à retourner. 
    def select_one_event(self, field, value): 
        """ Select one Event instance following a unique field. 
            Possible fields: 
                'id' 
                'contract_id', 
            Args:
                field (string): The name of the field to look for. 
                value (string): The value for select the Event instance. 
            Returns:
                object Event: The selected Event instance. 
        """ 
        print('select_one_event') 
        event_db = Event() 
        if field == 'id': 
            event_db = self.session.query(Event).filter( 
                Event.id==int(value)).first() 
        elif field == 'contract_id': 
            event_db = self.session.query(Event).filter( 
                Event.contract_id==value).first() 
        else: 
            print('no field recognized (manager.select_one_event)') 
        if event_db is None: 
            # TODO : afficher de nouveau la question précédente ? 
            print('Aucun événement avec ces informations (manager.select_one_event)') 
            return False 
        else: 
            # print(f'event trouvé (manager.select_one_user) : {user_db.name}, id : {user_db.id}, mail : {user_db.email}, pass : {user_db.password}, départemt : (id : {user_db.department.id}) name : {user_db.department.name}.') 
            return event_db 


    # def update_event(self, id, field, new_value): 
    #     """ Modifies a field of an Event instance, following its id. 
    #         Possible fields: 
    #             name 
    #             contract_id 
    #             support_contact_id 
    #             location 
    #             attendees 
    #             notes 
    #         Args:
    #             id (int): The id of the registered Event instance. 
    #             field (string): The name of the field to modify. 
    #             new_value (string): The new value to register. 
    #         Returns:
    #             object Event: The just updated Event instance. 
    #     """ 
    #     print('update_event') 
    #     itemName = self.select_one_event('id', id) 
    #     if field == 'name': 
    #         itemName.name = new_value 
    #     elif field == 'contract_id': 
    #         itemName.contract_id = new_value 
    #     elif field == 'support_contact_name': 
    #         support_contact_db = self.select_one_user('name', new_value) 
    #         itemName.support_contact_id = support_contact_db.id 
    #     elif field == 'location': 
    #         itemName.location = new_value 
    #     elif field == 'attendees': 
    #         itemName.attendees = int(new_value) 
    #     elif field == 'notes': 
    #         itemName.notes = new_value 
    #     else: 
    #         print('no value (manager.update_event)') 
    #     self.session.commit() 
    #     return itemName 


    # def select_all_events(self): 
    #     """ Returns:
    #             list: All the Event instances in a list. 
    #     """ 
    #       print('select_all_events') 
    #     items_db = self.session.query(Event).all() 
    #     for item in items_db:
    #         print(f'Event trouvé  (manager.select_all_events) : {item.name}, id : {item.id}.') 
    #     return items_db 
    # ==== /event ==== # 


    # ==== generics ==== # 
    # TODO: ajouter les autres entiés 
    def add_entity(self, entity, fields:dict): 
        print('add_entity') 
        entities_dict = { 
            'dept': Department, 
            'user': User, 
            'client': Client, 
            'contract': Contract, 
            'event': Event, 
        } 
        items_db = [] 
        if entity in entities_dict: 

            if entity == 'dept': 
                print('entity => dept') 
                itemName = entities_dict[entity](**fields) 
                self.session.add(itemName) 
                self.session.commit() 
                items_db = self.select_all_entities('depts') 
                # print('items_db : ', items_db) 
                # last_item_db = items_db.pop() 
                # return last_item_db 

            elif entity == 'user': 
                print(f'entity => user') 
                itemName = entities_dict[entity](**fields) 
                self.session.add(itemName) 
                self.session.commit() 
                items_db = self.select_all_entities('users') 

            elif entity == 'client': 
                print('entity => client') 
                sales_contact = self.select_one_user('name', fields['sales_contact_name']) 
                fields.pop('sales_contact_name') 
                itemName = entities_dict[entity]( 
                    sales_contact_id=sales_contact.id, 
                    **fields 
                ) 
                self.session.add(itemName) 
                self.session.commit() 
                items_db = self.select_all_entities('clients') 

            elif entity == 'contract': 
                print('entity => contract') 
                client = self.select_one_client('name', fields['client_name']) 
                fields.pop('client_name') 
                itemName = entities_dict[entity]( 
                    client_id=client.id, 
                    **fields 
                ) 
                self.session.add(itemName) 
                self.session.commit() 
                items_db = self.select_all_entities('contracts') 

            elif entity == 'event': 
                print('entity => event') 
                contracts_db = self.select_all_entities('contracts') 
                last_contract_db = contracts_db.pop() 
                itemName = entities_dict[entity]( 
                    contract_id=last_contract_db.id, 
                    **fields 
                ) 
                self.session.add(itemName) 
                self.session.commit() 
                items_db = self.select_all_entities('events') 

            last_item_db = items_db.pop() 
            return last_item_db 
        else: 
            print(f'Cet objet ({entity}) n\'existe pas (manager.add_entity 729).') 
            return false 


    def select_all_entities(self, entity): 
        print('select_all_entities') 
        entities_dict = { 
            'depts': Department, 
            'users': User, 
            'clients': Client, 
            'contracts': Contract, 
            'events': Event 
        } 
        if entity in entities_dict.keys(): 
            items_list_db = self.session.query(entities_dict[entity]).all() 
            for item in items_list_db: 
                print(f'{entity} trouvé  (manager.select_all_entities) : {item}.') 
            return items_list_db 
        else: 
            print(f'Cet objet ({entity}) n\'existe pas ML748.') 
            return false 
    

    # def select_one_entity(self, entity, field, value): 
    #     """ Select one entity instance following a unique field. 
    #         Possible entities: 
    #             'dept' (for department), 
    #             'user', 
    #             'client', 
    #             'contract', 
    #             'event' 
    #         Possible fields (depending entity): 
    #             'id' 
    #             'name', 
    #             'email', 
    #             'phone', 
    #             'client_name', 
    #             'contract_id', 
    #         Args:
    #             entity (string): The name of the model to select. 
    #             field (string): The name of the field to look for. 
    #             value (string): The value for select the entity instance. 
    #         Returns:
    #             object entity: The selected entity instance. 
    #     """ 
    #     # event_db = Event() 
    #     entities_dict = { 
    #         'dept': Department, 
    #         'user': User, 
    #         'client': Client, 
    #         'contract': Contract, 
    #         'event': Event 
    #     } 
    #     fields_list = [ 
    #         'id', 
    #         'name', 
    #         'email', 
    #         'phone', 
    #         'client_name', 
    #         'contract_id' 
    #     ] 
    #     # fields_dict = { 
    #     #     'id': entities_dict[entity].id, 
    #     #     'name': entities_dict[entity].name, 
    #     #     'email': entities_dict[entity].email, 
    #     #     'phone': entities_dict[entity].phone, 
    #     #     'client_name': entities_dict[entity].client_name, 
    #     #     'contract_id': entities_dict[entity].contract_id 
    #     # } 
    #     print('entity ML715 : ', entity) 
    #     if entity in entities_dict.keys(): 
    #         # if field in fields_dict.keys(): 
    #         for f in fields_list: 
    #         #     if f == field: 
    #             print(f'field : ', field) 
    #             if field == 'id': 
    #                 entity_db = self.session.query(entities_dict[entity]).filter( 
    #                     entities_dict[entity].id==int(value)).first() 
    #                 print(f'entité trouvée (ML688) : ', entity_db) 
    #                 return entity_db 
    #             elif field == 'contract_id': 
    #                 entity_db = self.session.query(entities_dict[entity]).filter( 
    #                     entities_dict[entity].value==int(value)).first() 
    #                 print(f'entité trouvée (ML693) : ', entity_db) 
    #                 return entity_db 
    #             elif field == 'name': 
    #                 entity_db = self.session.query(entities_dict[entity]).filter( 
    #                     entities_dict[entity].name==value).first() 
    #                 print(f'entité trouvée (ML698) : ', entity_db) 
    #                 return entity_db 
    #     else: 
    #         print(f'Cet objet ({entity}) n\'existe pas.') 
    #         return false 

    # ==== /generics ==== # 


    def select_entities_with_criteria(self, entities, criteria, contact_id): 
        """ Select entity instances with criteria. 
            Args:
                entities (str): (in plural) The name of the objects to look for. 
                criteria (str): The criteria to follow for filtering the instances. 
            Returns:
                list: The instances that respect the criteria. 
        """ 
        if entities == 'events': 
            if criteria == 'without support': 
                events_db = self.session.query(Event).filter( 
                    Event.support_contact_id==null)  # *** null *** 
                if events_db is None: 
                    print('Aucun événement avec ces informations (manager without support)') 
                    return False 
                else: 
                    return events_db 
            elif criteria == 'support id': 
                events_db = self.session.query(Event).filter( 
                    Event.support_contact_id==contact_id) 
                if events_db is None: 
                    print('Aucun événement avec ces informations (manager.select_entities_with_criteria)') 
                    return False 
                else: 
                    return events_db 
        elif entities == 'contracts': 
            if criteria == 'sales contact': 
                contracts_db = self.session.query(Contract).filter( 
                    Contract.sales_contact_id==id) 
                if contracts_db is None: 
                    print('Aucun contrat avec ces informations (manager.select_entities_with_criteria)') 
                    return False 
                else: 
                    return contracts_db 
            if criteria == 'not signed': 
                contracts_db = self.session.query(Contract).filter( 
                    Contract.is_signed==0) 
                if contracts_db is None: 
                    print('Aucun contrat avec ces informations (manager.select_entities_with_criteria)') 
                    return False 
                else: 
                    return contracts_db 
            elif criteria == 'not paid': 
                contracts_db = self.session.query(Contract).filter( 
                    Contract.amount-Contract.paid_amount!=0) 
                if contracts_db is None: 
                    print('Aucun contrat avec ces informations (manager.select_entities_with_criteria)') 
                    return False 
                else: 
                    return contracts_db 
        elif field == 'clients': 
            if criteria == 'sales contact': 
                clients_db = self.session.query(Client).filter( 
                    Client.sales_contact_id==id)
                if clients_db is None: 
                    print('Aucun client avec ces informations (manager.select_entities_with_criteria)') 
                    return False 
                else: 
                    return clients_db 
        elif field == 'users': 
            if criteria == 'department': 
                users_db = self.session.query(Client).filter( 
                    Client.department_id==id)
                if users_db is None: 
                    print('Aucun utilisateur impacté par la suppression de ce département (manager.select_entities_with_criteria).') 
                    return False 
                else: 
                    return users_db 
        else: 
            print('no field recognized (manager.select_entities_with_criteria)') 



    # # TODO: retour dans l'appli si 'N' 
    # def delete_event(self, field, value): 
    #     """ Delete an Event following a unique field. 
    #         Args:
    #             field (string): The field name to select. 
    #             value (string): The field value to select for deleting. 
    #     """ 
    #       print('delete_event') 
    #     item_db = self.select_one_event(field, value) 
    #     # Vérifier contract_id.clients.name *** 
    #     self.session.delete(item_db) 
    #     self.session.commit() 
    #     print(f'L\'événement {item_db.name} (id : {item_db.id}) été supprimé.') 

    # user = relationship("User", back_populates="events") 
    # contracts = relationship("Contract", back_populates="events") 





    # def select_many(self, item): 
    #     users_db = self.session.query(User).filter(User.department==item) 
    #     # users_db = self.session.query(User).filter(User.department==vente) 
    #     for user in users_db: 
    #         print(f'User trouvé : {user.name}, id : {user.id}, departement : {user.department.name}') 

    #     clients_saler_1 = self.session.query(Client).filter(Client.sales_contact_id==item) 
    #     for client in clients_saler_1: 
    #         print(f'Client trouvé : {client.name}, id : {client.id}, contact commercial : {client.sales_contact_id, }, créé le {client.created_at}.') 


    # ======== # ======== Utils ======== # ======== # 
    
    def get_token(self, delta:int, data:dict): 
        """ Creates a token for the new user, that indicates his.her department, 
            with X hours before expiration. 
            Args:
                delta (int): The number of seconds before expiration. 
                data (dict): The payload data for the creation of the token. 
            Returns:
                string: The token to register for later use. 
        """ 
        print('get_token') 
        payload = { 
            'email': data['email'], 
            'pass': data['pass'], 
            'dept': data['dept'], 
            'exp': datetime.now()+timedelta(seconds=delta) 
        } 
        secret = os.environ.get('JWT_SECRET') 
        algo = os.environ.get('JWT_ALGO') 
        encoded_jwt = jwt.encode(payload, secret, algo) 
        return encoded_jwt 


    def verify_token(self, connectEmail, connectPass, connectDept): 
        """ Check if the user and department are those registered in the db. 
                If yes: 
                    Store the role's name of the user. 
                    Check the token's expiration time. 
                    if it is NOT past: 
                        Return the role's permission name for creation user_session by the Controller. 
                    else: 
                        Call get_token() for refreshing the token. 
                        Return tne role's permission for creation of the user_session by the Controller. 
                else: 
                    return "None". 
            Args:
                connectEmail (string): The email entered by the connected user. 
                connectPass (string): The password entered by the connected user. 
                connectDept (string): The name of the department which is registered the user. 

            Returns:
                string: The name of the user's role. 
        """ 
        registeredToken = self.select_one_user('email', connectEmail).token 
        secret = os.environ.get('JWT_SECRET') 
        algo = os.environ.get('JWT_ALGO') 

        # userDecode = {} 
        try: 
            userDecode = jwt.decode(registeredToken, secret, algorithms=[algo]) 
            print('userDecode ML784 : ', userDecode) 
            userDecode_exp = int(userDecode.pop('exp'))-3600 
            permission = '' 
            if userDecode['dept'] == 'gestion': 
                permission = 'GESTION' 
            elif userDecode['dept'] == 'commerce': 
                permission = 'COMMERCE' 
            if userDecode['dept'] == 'support': 
                permission = 'SUPPORT' 
            return permission 
        except ExpiredSignatureError as expired: 
            print(expired) 
            # print('userDecode ML788 : ', userDecode) 
            return 'past' 

        # connectedToken = { 
        #     'email': connectEmail, 
        #     'pass': connectPass, 
        #     'dept': connectDept, 
        #     'exp': datetime.now().timestamp() 
        # } 
        # exp = re.sub('\.\d+', '', str(connectedToken['exp'])) 
        # print('connectedToken : ', connectedToken) 
        # connectedToken['exp'] = exp 
        # connectedToken_exp = connectedToken.pop('exp') 

        # # Check login+hash_pw+dept.name: 
        # if userDecode == connectedToken: 
        #     print('connected : ', userDecode["email"], userDecode["pass"], userDecode["dept"], ' registered : ' , connectedToken) 
        #     print('Token user + dept ok. Check for exp time...') 

        #     # Check the expiration time: 
        #     if int(userDecode_exp) < int(connectedToken_exp): 
        #         print('Past token time', userDecode, userDecode_exp, connectedToken, connectedToken_exp) 
        #         return 'past' 
        #     else: 
        #         print('ok token time', userDecode, userDecode_exp, connectedToken, connectedToken_exp) 
        #         if userDecode['dept'] == 'gestion': 
        #             permission = 'GESTION' 
        #             print('OK token gestion (manager)') 
        #         elif userDecode['dept'] == 'commerce': 
        #             permission = 'COMMERCE' 
        #             print('OK token commerce (manager)') 
        #         elif userDecode['dept'] == 'support': 
        #             permission = 'SUPPORT' 
        #             print('OK token support (manager)') 
        #         else: 
        #             permission = None 
        #             print('token inconnu (manager)') 
        #         return permission 
        # else: 
        #     # ok 
        #     print('connected : ', userDecode["email"], userDecode["pass"], userDecode["dept"], ' registered : ' , connectedToken["email"], connectedToken["pass"], connectedToken["dept"]) 
        #     print('NO token checked (manager)') 
        #     return None 


    def hash_pw(self, password, nb:int): 
        """ Hash the given password before register it into the DB. 
            Params: 
                password (string): the readable password to hash. 
                nb (int): the number of characters for the salt. 
            Returns the hashed password. 
        """ 
        salt = bcrypt.gensalt(nb)
        hashed_password = bcrypt.hashpw( 
            password.encode('utf-8'), 
            salt 
        ).decode('utf-8') 
        return hashed_password 


    def check_pw(self, userEmail, pw): 
        user_db = self.select_one_user('email', userEmail) 
        if user_db is None: 
            print('user is none') 
            return False 
        else: 
            hashed = user_db.password 
            if bcrypt.checkpw(pw.encode('utf-8'), hashed.encode('utf-8')): 
                print("pw ok (manager)") 
                return True 
            else: 
                print('pw not ok (manager)') 
                return False 

    # ======== /Utils ======== # 



    def other(self, item): 
        print('other') 
        #     # # tuto simpletech 
        #     # stock_query = session.query(Stock).join(Warehouse).join(Product) 
        #     # stock_chaussure_entrepot_a = stock_query.filter(Product.name=='chaussure', Warehouse.name=='entreprot A').first() 
        #     # print(f'Le stock de {stock_chaussure_entrepot_a.product.name} dans {stock_chaussure_entrepot_a.warehouse.name} est de {stock_chaussure_entrepot_a.quantity}.') 

        #     # conn.commit() 

        # except Exception as ex: 
        #     print(ex) 

        # Voir si engine s'en occupe ? 
        # if conn is not None: 
        #     conn.close() 
        #     print('connex closed') 

        # return self.engine 

