
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


    # ==== generics ==== # 
    def add_entity(self, entity, fields:dict): 
        """ Generic method that creates an entity. 
            Args:
                entity (str): The table in which to create an item. 
                fields (dict): The data to register. 
            Returns:
                entity object: The just created entity item. 
        """ 
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
                # print('entity => dept') 
                itemName = entities_dict[entity](**fields) 
                self.session.add(itemName) 
                self.session.commit() 
                items_db = self.select_all_entities('depts') 

            elif entity == 'user': 
                # get token: 
                # fields['token'] = self.get_token(2, { 
                token = self.get_token(2, entity.email, { 
                    'email': fields['email'], 
                    'pass': fields['password'], 
                    'dept': fields['department_id']} 
                ) 
                
                itemName = entities_dict[entity](**fields) 
                self.session.add(itemName) 
                self.session.commit() 
                items_db = self.select_all_entities('users') 

            elif entity == 'client': 
                # print('entity => client') 
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
                # print('entity => contract') 
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
                # print('entity => event') 
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
            return False 


    def select_all_entities(self, entity): 
        """ Generic method that selects all items of one table. /!\ entity in plural /!\ 
            Args:
                entity (str): The table to select, in plural. 
            Returns:
                list or False: The items selected, of False if the entity name doesn't exist. 
        """ 
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
            return False 


    def select_entities_with_criteria(self, entities, criteria, contact_id): 
        """ Select entity instances with criteria. 
            Possible criteria: 
                'without support' (events, for gestion)  
                'support contact' (events, for support) 
                'sales clients' (clients / contracts, for commerce) 
                'not signed' (contracts, for commerce) 
                'not paid' (contracts, for commerce) 
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
            elif criteria == 'support contact': 
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
        # itemName = self.select_one_dept('name', old_name) 
        if itemName is None: 
            print('itemName is none ML236') 
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
    # ==== /department methods ==== # 


    # ==== user ==== # 
    # def update_user(self, id, field, new_value): 
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
        print('update_user') 
        # itemName = self.select_one_user('id', id) 
        if field == 'name': 
            itemName.name = new_value 
        elif field == 'email': 
            itemName.email = new_value 
        elif field == 'password': 
            hashed_password = self.hash_pw(new_value, 12) 
            itemName.password = hashed_password 
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
        else: 
            print('no field recognized (manager.select_one_client)') 
        if client_db is None: 
            # TODO : afficher de nouveau la question précédente ? 
            print('Aucun client avec ces informations (manager.select_one_client)') 
            return False 
        else: 
            # print(f'user trouvé (manager.select_one_client) : {user_db.name}, id : {user_db.id}, mail : {user_db.email}, pass : {user_db.password}, départemt : (id : {user_db.department.id}) name : {user_db.department.name}.') 
            return client_db 


    # def update_client(self, id, field, new_value): 
    def update_client(self, itemName, field, new_value): 
        """ Modifies a field of a Client instance, following its id. 
            Possible fields: 
                name
                email
                phone
                corporation_name
                sales_contact_name 
            Args:
                # id (int): The id of the registered Client instance. 
                itemName (object): The registered Client instance to modify. 
                field (string): The name of the field to modify. 
                new_value (string): The new value to register. 
            Returns:
                object Client: The just updated Client instance. 
        """ 
        # itemName = self.select_one_user('id', id) 
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
        if contract_db is None: 
            # TODO : afficher de nouveau la question précédente ? 
            print('Aucun utilisateur avec ces informations (manager.select_one_user)') 
            return False 
        else: 
            # print(f'user trouvé (manager.select_one_user) : {user_db.name}, id : {user_db.id}, mail : {user_db.email}, pass : {user_db.password}, départemt : (id : {user_db.department.id}) name : {user_db.department.name}.') 
            return contract_db 


    # def update_contract(self, id, field, new_value): 
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
        # itemName = self.select_one_user('id', id) 
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
    # ==== /contract ==== # 


    # ==== event ==== # 
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
        print('select_one_event (manager)') 
        print('field (manager) : ', field) 
        print('value (manager) : ', value) 
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
            print('no field recognized (manager.select_one_event)') 
        # if event_db is None: 
        #     # TODO : afficher de nouveau la question précédente ? 
        #     print('Aucun événement avec ces informations (manager.select_one_event)') 
        #     return False 
        # else: 
        #     # print(f'event trouvé (manager.select_one_user) : {event_db.name}, id : {event_db.id}, mail : {event_db.email}, pass : {event_db.password}, départemt : (id : {user_db.department.id}) name : {user_db.department.name}.') 
        #     print(f'event trouvé (manager.select_one_event) : {event_db.name} (id : {event_db.id}), contrat : {event_db.contract_id}, début : {event_db.start_datetime}, fin : {event_db.end_datetime}, contact support {event_db.user.name} (ID : {support_contact_id}, lieu : {event_db.location}, invités : {event_db.attendees}, notes : {event_db.notes}).' ) 
        return event_db 


    # def update_event(self, id, field, new_value): 
    def update_event(self, itemName, field, new_value): 
        """ Modifies a field of an Event instance, following its id. 
            Possible fields: 
                id 
                name 
                contract_id 
            Args:
                # id (int): The id of the registered Event instance. 
                itemName (object): The registered Event instance to modify. 
                field (string): The name of the field to modify. 
                new_value (string): The new value to register. 
            Returns:
                object Event: The just updated Event instance. 
        """ 
        print('update_event') 
        # itemName = self.select_one_event('id', id) 
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
        self.session.commit() 
        return itemName 
    # ==== /event ==== # 


    # ================ Utils ================ # 
    
    def get_token(self, delta:int, email, data:dict): 
        """ Creates a token for the new user, that indicates his.her department, 
            with X hours before expiration. 
            Args:
                delta (int): The number of seconds before expiration. 
                username (str): The name of the user. 
                data (dict): The payload data for the creation of the token: 
                    email, pass, dept (name). 
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

        if not self.export_token(encoded_jwt): 
            return False 
        else: 
            return True  
        # return encoded_jwt 


    def export_token(self, token, email): 
        # Register the token in a crypted file 
        # file deepcode ignore PT: local project 
        # f = open(os.environ.get('TOKEN_PATH'),'r') 
        # # f.write(token) 
        # f.write(userToken) 
        # f.close() 

        # key generation 
        key = Fernet.generate_key() 
        # regsiters the key in a file
        # with open('filekey.key', 'wb') as filekey:
        with open(os.environ.get('JWT_KEY_PATH'), 'wb') as filekey: 
            filekey.write(key) 

        userToken = {} 
        userToken['email'] = email 
        userToken['token'] = new_token 


        # opens the key
        with open(os.environ.get('JWT_KEY_PATH'), 'rb') as keyfile:
            key = keyfile.read()
        
        # uses the generated key
        cipher_suite = Fernet(key)
        
        # opens the original file to encrypt
        # with open('nba.csv', 'rb') as file:
        with open(os.environ.get('TOKEN_PATH'), 'rb') as file:
            registered = file.read()
            
        # encrypts the file 
        if type(registered) == str: 
            encrypted = cipher_suite.encrypt(str(registered).encode('utf-8')) 
        elif type(registered) == byte: 
            encrypted = cipher_suite.encrypt(registered) 
        
        # opens the file in write mode and
        # writes the encrypted data
        with open(os.environ.get('TOKEN_PATH'), 'wb') as encrypted_file:
            encrypted_file.write(encrypted) 


        # # with open(os.environ.get('TOKEN_PATH'), "r") as file: 
        # with open(os.environ.get('TOKEN_PATH'), "rb") as file: 
        #     registered = json.load(file) 
        #     print('registered 1 : ', registered) 
        #     users = registered['users'] 
        #     for reg in users: 
        #         print('reg : ', reg) 
        #         if email in reg['email']: 
        #             users.pop(users.index(reg)) 
        #     users.append(userToken) 
        #     print('registered 2 : ', registered) 
        # with open(os.environ.get('TOKEN_PATH'), "w") as file: 
        #     json.dump(registered, file, indent=4) 
        # return True 


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
                print("pw ok (manager)") 
                return True 
            else: 
                print('pw not ok (manager)') 
                return False 

    # ======== /Utils ======== # 

