
from models import Base, Client, Contract, Department, Event, User   

import bcrypt 
import json 
import jwt 
import os 
import psycopg2 
import re 
# Abstract Syntax Trees 
import ast 

from cryptography.fernet import Fernet 
from datetime import datetime, timedelta 
from jwt.exceptions import ExpiredSignatureError
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker 
from time import time 



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

    def create_session(self): 
        Session = sessionmaker(bind=self.engine) 
        self.session = Session() 


    def add_user_setup(self, fields:dict): 
        print('\nadd_user_setup') 
        fields['department_id'] = self.select_one_dept('name', fields['department_name']).id 
        department_name = fields.pop('department_name') 
        itemName = User(**fields) 
        self.session.add(itemName) 
        self.session.commit() 

        items_db = self.select_all_entities('users') 
        last_item_db = items_db.pop() 
        return last_item_db 


    # ==== generics ==== # 
    def add_entity(self, entity_name, fields:dict): 
        """ Generic method that creates an entity. 
            Args: 
                entity_name (str): The table in which to create an item. 
                fields (dict): The data to register. 
            Returns: 
                entity object: The last created entity item. 
        """ 
        print('\nAdd_entity') 
        entities_dict = { 
            'dept': Department, 
            'user': User, 
            'client': Client, 
            'contract': Contract, 
            'event': Event, 
        } 
        items_db = [] 

        if entity_name in entities_dict: 
            if entity_name == 'dept': 
                # print('entity => dept') 

                itemName = entities_dict[entity_name](**fields) 
                self.session.add(itemName) 
                self.session.commit() 
                items_db = self.select_all_entities('depts') 

            elif entity_name == 'user': 
                """ A User instance needs to get the password hashed 
                    and registered into the DB. 
                """ 
                print('...Hashage du mot de passe, veuillez patienter...') 
                fields['department_id'] = self.select_one_dept( 
                    'name', fields['department_name']).id 
                department_name = fields.pop('department_name') 

                hashed = self.hash_pw(fields['entered_password']) 
                fields.pop('entered_password') 

                itemName = entities_dict[entity_name]( 
                    password=hashed, 
                    **fields) 
                self.session.add(itemName) 
                self.session.commit() 

                items_db = self.select_all_entities('users') 

            elif entity_name == 'client': 
                fields['created_at'] = datetime.now() 
                fields['updated_at'] = datetime.now() 
                itemName = entities_dict[entity_name]( 
                    **fields 
                ) 
                self.session.add(itemName) 
                self.session.commit() 
                items_db = self.select_all_entities('clients') 

            elif entity_name == 'contract': 
                client = self.select_one_client( 
                    'name', 
                    fields['client_name'] 
                ) 
                fields.pop('client_name') 
                if (fields['is_signed'] == 'Y') | (fields['is_signed'] == 'y'): 
                    fields['is_signed'] = True 
                else: 
                    fields['is_signed'] = False 
                fields['created_at'] = datetime.now() 
                itemName = entities_dict[entity_name]( 
                    client_id=client.id, 
                    **fields 
                ) 
                self.session.add(itemName) 
                self.session.commit() 
                items_db = self.select_all_entities('contracts') 

            elif entity_name == 'event': 
                # print('entity => event') 
                itemName = entities_dict[entity_name](**fields) 
                self.session.add(itemName) 
                self.session.commit() 
                items_db = self.select_all_entities('events') 

            last_item_db = items_db.pop() 
            return last_item_db 
        else: 
            print(f'Cet objet ({entity}) n\'existe pas (manager.add_entity 729).') 
            return False 

    def select_all_entities(self, entity_name): 
        """ Generic method that selects all items of one table. /!/ entity in plural /!/ 
            Args:
                entity (str): The table to select, in plural. 
            Returns:
                list or False: The items selected, of False if the entity name doesn't exist. 
        """ 
        # print('select_all_entities') 
        entities_dict = { 
            'depts': Department, 
            'users': User, 
            'clients': Client, 
            'contracts': Contract, 
            'events': Event 
        } 

        # file deepcode ignore UpdateAPI: local project 
        if entity_name in entities_dict.keys(): 
            items_list_db = self.session.query(entities_dict[entity_name]).all() 
            return items_list_db 
        else: 
            print(f'Cet objet ({entity_name}) n\'existe pas ML161.') 
            return False 

    def select_entities_with_criteria(self, entities, criteria, contact_id): 
        """ Select entity instances with criteria. 
            Possible criteria: 
                'without support' (events, for gestion)  
                'support contact' (events, for support) 
                'sales clients' (clients / contracts, for commerce) 
                'client' (contracts, for commerce) 
                'not signed' (contracts, for commerce) 
                'not paid' (contracts, for commerce) 
            Args: 
                entities (str): (in plural) The name of the objects to look for. 
                criteria (str): The criteria to follow for filtering the instances. 
                contact_id (int): The ID of the logged user, if needed. 
            Returns: 
                list: The instances that respect the criteria. 
        """ 
        if entities == 'events': 
            if criteria == 'without support': 
                events_db = self.session.query(Event).filter( 
                    # file deepcode ignore change_to_is: SQLAlchemy syntax: '== None' 
                    Event.support_contact_id == None).all() 
                if events_db is None: 
                    print('Aucun événement avec ces informations (manager, without support)') 
                    return False 
                else: 
                    return events_db 
            elif criteria == 'support contact': 
                events_db = self.session.query(Event).filter( 
                    Event.support_contact_id==contact_id).all() 
                if events_db is None: 
                    print('Aucun événement avec ces informations (manager.select_entities_with_criteria)') 
                    return False 
                else: 
                    return events_db 
        elif entities == 'contracts': 
            if criteria == 'not signed': 
                contracts_db = self.session.query(Contract).filter( 
                    Contract.is_signed=='f').all() 
                if contracts_db is None: 
                    print('Aucun contrat avec ces informations (manager.select_entities_with_criteria)') 
                    return False 
                else: 
                    return contracts_db 
            elif criteria == 'not paid': 
                contracts_db = self.session.query(Contract).filter( 
                    Contract.amount-Contract.paid_amount!=0).all() 
                if contracts_db is None: 
                    print('Aucun contrat avec ces informations (manager.select_entities_with_criteria)') 
                    return False 
                else: 
                    return contracts_db 
            elif criteria == 'client': 
                contracts_db = self.session.query(Contract).filter( 
                    Contract.client_id==contact_id).all() 
                if contracts_db is None: 
                    print('Aucun contrat avec ces informations (manager.select_entities_with_criteria)') 
                    return False 
                else: 
                    return contracts_db 
        elif entities == 'clients': 
            if criteria == 'sales contact': 
                clients_db = self.session.query(Client).filter( 
                    Client.sales_contact_id==contact_id).all() 
                if clients_db is None: 
                    print('Aucun client avec ces informations (manager.select_entities_with_criteria)') 
                    return False 
                else: 
                    return clients_db 
        elif entities == 'users': 
            if criteria == 'department': 
                users_db = self.session.query(Client).filter( 
                    Client.department_id==id).all()
                if users_db is None: 
                    print('Aucun utilisateur impacté par la suppression de ce département (manager.select_entities_with_criteria).') 
                    return False 
                else: 
                    return users_db 
        else: 
            print('no entity recognized (manager.select_entities_with_criteria)') 
    # ==== /generics ==== # 


    # ==== department methods ==== # 
    def update_dept(self, itemName, old_name, new_value): 
        """ Modifies a registered department with the new value. 
            For the department table, it is possible to update only the name. 
            Args:
                itemName (object): The object (Department) to modify. 
                id (string): The ID to look for. 
                field (string): The field to replace by the new_value. 
                new_value (string): The new value to register. 
            Returns: 
                object Department: The updated instance of Department. 
        """ 
        if itemName is None: 
            print('itemName is none ML259') 
        else: 
            itemName.name = new_value 
            self.session.commit() 
            modified_item = self.select_one_dept('id', itemName.id) 
            return modified_item 

    def select_one_dept(self, field, value): 
        """ Selects one department following the given field and value. 
            Possible fields: 'id', 'name'. 
            Args:
                field (string): The field on wich select the item. 
                value (string): The value to select it. 
            Returns:
                object Department: The selected instance of Department. 
        """ 
        item_db = Department 
        if field == 'id': 
            item_db = self.session.query(Department).filter( 
                Department.id==int(value)).first() 
        elif field == 'name': 
            item_db = self.session.query( 
                Department).filter(Department.name==value).first() 
        else: 
            print(f'Ce champ "{field}" n\'existe pas.') 
        return item_db 

    def delete_dept(self, field, value): 
        """ Delete one registered department, following a unique field. 
            Args: 
                field (string): The field name on which select the item. 
                value (string): The field value to select the item to delete. 
        """ 
        print('\ndelete_dept') 
        item_db = self.select_one_dept(field, value) 
        print('dept to delete ML294 : ', item_db) 
        self.session.delete(item_db) 
        self.session.commit() 

    # ==== /department methods ==== # 


    # ==== user ==== # 
    def update_user(self, itemName, field, new_value): 
        """ Modifies a field of a user instance, following its id. 
            Args:
                # id (int): The id of the registered user instance. 
                itemName (object): The registered user object to modify. 
                field (string): The name of the field to modify. 
                new_value (string): The new value to register. 
            Returns:
                object User: The just updated User instance. 
        """ 
        print('\nUpdate_user') 
        if field == 'id': 
            itemName.id = new_value 
        elif field == 'name': 
            itemName.name = new_value 
        elif field == 'email': 
            itemName.email = new_value 
        elif field == 'password': 
            hashed_password = self.hash_pw(new_value) 
            itemName.password = hashed_password 
        elif field == 'phone': 
            itemName.phone = new_value 
        elif field == 'department_id': 
            itemName.department_id = new_value 
        else: 
            print('no value (manager.update_user)') 
        self.session.merge(itemName) 
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
        # print('\nSelect_one_user') 
        user_db = User() 
        if field == 'id': 
            user_db = self.session.query(User).filter( 
                User.id==int(value)).first() 
            return user_db 
        elif field == 'name': 
            user_db = self.session.query(User).filter( 
                User.name==value).first() 
            return user_db 
        elif field == 'email': 
            user_db = self.session.query(User).filter( 
                User.email==value).first() 
        else: 
            print('no field recognized (manager.select_one_user)') 
        if user_db is None: 
            print('Aucun utilisateur avec ces informations.') 
            return False 
        else: 
            return user_db 

    def delete_user(self, field, value): 
        """ Deletes one registered user, following a unique field. 
            Deletes also his token. 
            Args: 
                field (string): The field name on which select the item. 
                value (string): The field value to select the item to delete. 
        """ 
        print('\ndelete_user') 
        item_db = self.select_one_user(field, value) 
        email = item_db.email 
        # Get the decrypted tokens 
        self.decrypt_token() 
        # Retrieve and delete the user's token 
        self.delete_registered_token() 
        # Delete the user and register the data again 
        self.session.delete(item_db) 
        self.session.commit() 
        print(f'L\'utilisateur {item_db.name} (id : {item_db.id}) a été supprimé.') 
    # ==== /user ==== # 


    # ==== client ==== # 
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
        elif field == 'sales_contact_id': 
            client_db = self.session.query(Client).filter( 
                Client.sales_contact_id==7).all() 
        else: 
            print('no field recognized (manager.select_one_client)') 
        return client_db 

    def update_client(self, itemName, field, new_value): 
        """ Modifies a field of a given Client instance. 
            Possible fields: 
                name
                email
                phone
                corporation_name
                sales_contact_name 
            Args:
                itemName (object): The registered Client instance to modify. 
                field (string): The name of the field to modify. 
                new_value (string): The new value to register. 
            Returns:
                object Client: The just updated Client instance. 
        """ 
        if field == 'name': 
            itemName.name = new_value 
        elif field == 'email': 
            itemName.email = new_value 
        elif field == 'phone': 
            itemName.phone = new_value 
        elif field == 'corporation_name': 
            itemName.corporation_name = new_value 
        elif field == 'sales_contact_name': 
            sales_contact_db = self.select_one_user( 
                'name', 
                new_value 
            ) 
            itemName.sales_contact_id = sales_contact_db.id 
        else: 
            print('no value (manager.update_client)') 
        self.session.merge(itemName) 
        self.session.commit() 
        return itemName 
    # ==== /client ==== # 


    # ==== contract ==== # 
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
        return contract_db 

    def update_contract(self, itemName, field, new_value): 
        """ Modifies a field of a Contract instance, following its id. 
            Possible fields: 
                amount 
                paid_amount 
                is_signed 
            Args:
                # id (int): The id of the registered Contract instance. 
                itemName (object): The registered Contract instance to modify. 
                field (string): The name of the field to modify. 
                new_value (string): The new value to register. 
            Returns:
                object Contract: The just updated Contract instance. 
        """ 
        print('\nUpdate_contract') 
        if field == 'amount': 
            itemName.amount = new_value 
            self.session.commit() 
        elif field == 'paid_amount': 
            itemName.paid_amount = new_value 
        elif field == 'is_signed': 
            itemName.is_signed = new_value 
            self.session.commit() 
        else: 
            print('no value (manager.update_contract)') 
        self.session.merge(itemName) 
        self.session.commit() 
        return itemName 
    # ==== /contract ==== # 


    # ==== event ==== # 
    def select_one_event(self, field, value): 
        """ Select one Event instance following a unique field. 
            Possible fields: 
                'id' 
                'name' 
                'contract_id' 
            Args:
                field (string): The name of the field to look for. 
                value (string): The value for select the Event instance. 
            Returns:
                object Event: The selected Event instance. 
        """ 
        print('\nSelect_one_event (manager)') 
        event_db = Event() 
        if field == 'id': 
            event_db = self.session.query(Event).filter( 
                Event.id==int(value)).first() 
        elif field == 'name': 
            event_db = self.session.query(Event).filter( 
                Event.name==value).first() 
        elif field == 'contract_id': 
            event_db = self.session.query(Event).filter( 
                Event.contract_id==value).first() 
        else: 
            print(f'no field recognized ({field}) (manager.select_one_event)') 
        return event_db 

    def update_event(self, itemName, field, new_value): 
        """ Modifies a field of an Event instance, following its id. 
            Possible fields: 
                id 
                name 
                contract_id 
                support_contact_name 
            Args:
                # id (int): The id of the registered Event instance. 
                itemName (object): The registered Event instance to modify. 
                field (string): The name of the field to modify. 
                new_value (string): The new value to register. 
            Returns:
                object Event: The just updated Event instance. 
        """ 
        print('\nUpdate_event') 
        if field == 'name': 
            itemName.name = new_value 
        elif field == 'contract_id': 
            itemName.contract_id = new_value 
        elif field == 'support_contact_name': 
            support_contact_db = self.select_one_user('name', new_value) 
            itemName.support_contact_id = support_contact_db.id 
        elif field == 'location': 
            itemName.location = new_value 
        elif field == 'attendees': 
            itemName.attendees = int(new_value) 
        elif field == 'notes': 
            itemName.notes = new_value 
        else: 
            print('no value (manager.update_event)') 
            return False 
        self.session.merge(itemName) 
        self.session.commit() 
        return itemName 
    # ==== /event ==== # 


    # ================ Utils ================ # 
    # TODO: change timedelta seconds to hours *** 
    def get_token(self, delta:int, data:dict): 
        """ Creates a token for the new user, that indicates his.her department, 
            with <delta> seconds before expiration. 
            Args: 
                delta (int): The number of seconds before expiration. 
                data (dict): The payload data for the creation of the token: 
                    "email", 
                    "dept" (name). 
            Returns: 
                string: The token to register for later use. 
        """ 
        print('\nGet_token') 
        payload = { 
            'email': data['email'], 
            'dept': data['dept'], 
            'exp': datetime.now()+timedelta(seconds=delta) 
        } 
        secret = os.environ.get('JWT_SECRET') 
        algo = os.environ.get('JWT_ALGO') 
        encoded_jwt = jwt.encode(payload, secret, algo) 
        # print('token ML595 :', encoded_jwt) 
        return encoded_jwt 

    def first_register_token(self, data_to_encrypt:dict): 
        """ Register the admin token in a crypted file. 
            Process: 
                - Get the key for encrypt the data. 
                - Set the email/token as a dictionary. 
                - Encrypt the data. 
                - register the data into the file.  
            Args: 
                email (str): The email to register into the encrypted file. 
                token (str): The token to register. 
            Return: 
                Bool: True if it's done. 
        """ 
        # get key 
        # file deepcode ignore PT: local project  # Snyk 
        with open(os.environ.get('JWT_KEY_PATH'), 'rb') as keyfile:
            key = keyfile.read() 
        # use the registered key
        cipher_suite = Fernet(key) 

        # chiffrer le mail/token et l'enregistrer 
        # ouvrir le fichier users en écriture en bytes 
        # enregistrer le hash dans le fichier 
        # Encrypt the token 
        encrypted = cipher_suite.encrypt(str(data_to_encrypt).encode('utf-8')) 
        # Register the encrypted token 
        with open(os.environ.get('TOKEN_PATH'), 'wb') as encrypted_file:
            encrypted_file.write(encrypted) 
        return True 
    
    def decrypt_token(self): 
        """ Decrypts the encrypted file with the registered key. 
            Returns: 
                dict: The conent of the encrypted file. 
        """ 
        # open the key
        with open(os.environ.get('JWT_KEY_PATH'), 'rb') as keyfile:
            key = keyfile.read() 
            # print('key : ', key) 
        # use the registered key
        cipher_suite = Fernet(key) 

        # decrypt the file 
        with open(os.environ.get('TOKEN_PATH'), 'rb') as file: 
            registered_bytes = file.read() 
        plain_text = cipher_suite.decrypt(registered_bytes) 
        registered = ast.literal_eval(plain_text.decode('utf-8'))
        return registered 

    def delete_registered_token(self, connectEmail): 
        """ Selects the user to delete into the tokens decrypted data. 
            Delete his row from the data. 
            Encrypt and regsiter the data again. 
            Args: 
                connectEmail (str): The email to look for. 
            Returns: 
                bool: True if the data has been registered. 
        """ 
        print('\nDelete_registered_token') 
        # Get the decrypted tokens data 
        registeredData = self.decrypt_token() 
        users = registeredData['users'] 
        for row in users: 
            if connectEmail == row['email']: 
                users.pop(row) 

        registered['users'] = users 

        # Encrypt the token 
        encrypted = cipher_suite.encrypt(str(registered).encode('utf-8')) 
        # Register the encrypted token 
        with open(os.environ.get('TOKEN_PATH'), 'wb') as encrypted_file:
            encrypted_file.write(encrypted) 
        return True 

    def verify_if_token_exists(self, connectEmail): 
        """ Check if the user's token is registered into the encrypted file. 
            Args: 
                connectEmail (string): The email entered by the connected user. 
            Returns:
                dict: the dict of the registered user's data 
                    or None: if the user's token is not registered. 
        """ 
        print('\nVerify_if_token_exists') 
        # Get the decrypted token's content file 
        registeredData = self.decrypt_token() 
        users = registeredData['users'] 
        for row in users: 
            if connectEmail == row['email']: 
                return row 

    def verify_token(self, connectEmail, connectDept, row:dict): 
        """ Check if the user and department are those registered in the db. 
            If email ok: 
                Store the department's name of the user. 
                Verify the encrypted data: 
                - decrypt the data with the registered key. 
                - Loop through the decrypted data to look for the connectEmail. 
                IF token exists: check if the token complies with the given data. 
                    IF token ok: Check the token's expiration time. 
                        IF it is NOT PAST: 
                            Return the role's permission name 
                        IF it is past: 
                            return 'past' 
                    IF token NOT ok: 
                        return False. 
                IF token does NOT exist: 
                    return False. 
            IF email NOT ok: 
                return False. 
            Args: 
                connectEmail (string): The email entered by the connected user. 
                connectPass (string): The password entered by the connected user. 
                connectDept (string): The name of the department which is registered the user. 
            Returns:
                str: The name of the user's role 
                or message (str) 
                or None 
        """ 
        print('\nVerify_token') 
        if connectEmail == row['email']: 
            registeredToken = row['token'] 

        secret = os.environ.get('JWT_SECRET') 
        algo = os.environ.get('JWT_ALGO') 

        try: 
            self.userDecode = jwt.decode( 
                registeredToken, 
                secret, 
                algorithms=[algo] 
            ) 
            userDecode_exp = int(self.userDecode.pop('exp'))-3600 

            permission = '' 
            if self.userDecode['dept'] == 'gestion': 
                permission = 'GESTION' 
            elif self.userDecode['dept'] == 'commerce': 
                permission = 'COMMERCE' 
            elif self.userDecode['dept'] == 'support': 
                permission = 'SUPPORT' 
            return permission 

        except ExpiredSignatureError as expired: 
            print('Token expired, check password') 
            return 'past' 

        except InvalidToken as invalid: 
            print(invalid) 
            return False 

    def register_token(self, email, token): 
        """ Register the token in a crypted file. 
            Process: 
                - Get the key for encrypt/decrypt the data. 
                - Read the encrypted file. 
                - Decrypt the encrypted data. 
                - Convert bytes data to dictionary. 
                - Loop through the "users" data to look for the email. 
                    if found: replace the regsitered token by the given. 
                    else: add the email/token to the list of data. 
                - Encrypt the updated data. 
                - register the updated data into the file.  
            Args: 
                email (str): The email to find or register into the encrypted file. 
                token (str): The new token to register. 
            Return: 
                Bool: True if it's done. 
        """ 
        print('\nRegister_token') 
        # get key 
        # file deepcode ignore PT: local project  # Snyk 
        with open(os.environ.get('JWT_KEY_PATH'), 'rb') as keyfile:
            key = keyfile.read() 
        # use the registered key
        cipher_suite = Fernet(key) 

        # lire le fichier des données chiffrées 
        # Ouvrir le fichier key en lecture 
        # l'utiliser pour déchiffrer le fichier chiffré 
        # boucler pour chercher le mail de l'utilisateur 
        registered = self.decrypt_token() 

        users = registered['users'] 
        # SI le mail de l'utilisateur est dedans : 
        #   changer le token 
        # SINON : 
        #   ajouter le nouveau mail/token au fichier 
        presents = [] 
        for row in users: 
            if email == row['email']: 
                row['token'] = token 
                # Update the token 
                presents.append(row['email']) 

        if presents == []: 
            # print('presents is emplty : ', presents) 
            # Add the new user into the dict users 
            users.append({"email": email, "token": token}) 
        registered['users'] = users 

        # chiffrer registered mis à jour 
        # ouvrir le fichier users en écriture en bytes 
        # enregistrer le hash dans le fichier 
        # Encrypt the token 
        # encrypted = cipher_suite.encrypt(usersTokens) 
        encrypted = cipher_suite.encrypt(str(registered).encode('utf-8')) 
        # Register the encrypted token 
        with open(os.environ.get('TOKEN_PATH'), 'wb') as encrypted_file:
            encrypted_file.write(encrypted) 
        print('Token registered') 
        return True 


    def hash_pw(self, password): 
        """ Hash the given password before register it into the DB. 
            Params: 
                password (string): the password to hash. 
                nb (int): the number of characters for the salt. 
            Returns the hashed password. 
        """ 
        salt = bcrypt.gensalt(16)
        hashed_password = bcrypt.hashpw( 
            password.encode('utf-8'), 
            salt 
        ).decode('utf-8') 
        return hashed_password 

    def check_pw(self, userEmail, pw): 
        """ Verify if the hashed entered password is the same of the registered one. 
            params: 
                userEmail (str): the entered email 
                pw (str): the entered password 
            returns: 
            (bool): True if the user exists and the entered pw is correct, 
                    False else. 
        """ 
        user_db = self.select_one_user('email', userEmail) 
        if user_db is None: 
            print('user is none') 
            return False 
        else: 
            hashed = user_db.password 
            if bcrypt.checkpw(pw.encode('utf-8'), hashed.encode('utf-8')): 
                print("DEBUG pw ok ML842 (manager)") 
                return True 
            else: 
                print('pw not ok ML845 (manager)') 
                return False 

    # ======== /Utils ======== # 

