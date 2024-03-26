
from sqlalchemy import create_engine 
import psycopg2 
from models import Base, Client, Contract, Department, Event, User   
from sqlalchemy.orm import sessionmaker 
# from helpers import decorator_hash_pass, hash_pw 

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

    # ==== department methods ==== # 
    def add_department(self, fields:list): 
        itemName = Department(name=fields[0]) 
        self.session.add(itemName) 
        self.session.commit() 
        return itemName 

    def update_dept(self, new_value, name): 
        itemName = self.select_one_dept('name', name) 
        itemName.name = new_value 
        self.session.commit() 
        return itemName 

    # TODO: suppr print 
    def select_one_dept(self, field, value): 
        if field == 'id': 
            item_db = self.session.query(Department).filter( 
                Department.id==int(value)).first() 
        elif field == 'name': 
            item_db = self.session.query( 
                Department).filter(Department.name==value).first() 
        else: 
            print(f'Ce champ "{field}" n\'existe pas.')  
        print(f'département trouvé (manager.select_one_dept) : {item_db.name}, id : {item_db.id}.') 
        return item_db 

    def select_all_depts(self): 
        items_db = self.session.query(Department).all() 
        for item in items_db:
            print(f'département trouvé  (manager.select_all_depts) : {item.name}, id : {item.id}.') 
        return items_db 

    def delete_dept(self, field, value): 
        item_db = self.select_one_dept(field, value) 
        self.session.delete(item_db) 
        self.session.commit() 

    # ==== user ==== # 
    def add_user(self, fields:list): 
        dept_db_id = self.select_one_dept('name', fields[4]).id 

        # Hash pass 
        hashed_password = self.hash_pw(fields[2], 12) 

        # Get token JWT 
        delta = 2*3600  # <-- for 'exp' JWT claim, en secondes 
        data = { 
            'email': fields[1], 
            'pass': fields[2], 
            'dept': fields[4], 
        } 
        user_token = self.get_token(delta, data) 
        userName = User( 
            name=fields[0], 
            email=fields[1], 
            password=hashed_password, 
            phone=fields[3], 
            department_id=dept_db_id, 
            token=user_token, 
        ) 
        self.session.add(userName) 
        self.session.commit() 
        return userName 


    # def get_token(self, data:dict): 
    def get_token(self, delta:int, data:dict): 
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

        userDecode = jwt.decode(registeredToken, secret, algorithms=[algo]) 
        print('userDecode ML152 : ', userDecode) 
        userDecode_exp = int(userDecode.pop('exp'))-3600 

        connectedToken = { 
            'email': connectEmail, 
            'pass': connectPass, 
            'dept': connectDept, 
            'exp': datetime.now().timestamp() 
        } 
        exp = re.sub('\.\d+', '', str(connectedToken['exp'])) 
        print('connectedToken : ', connectedToken) 
        connectedToken['exp'] = exp 
        connectedToken_exp = connectedToken.pop('exp') 

        # Check login+hash_pw+dept.name: 
        if userDecode == connectedToken: 
            print('connected : ', userDecode["email"], userDecode["pass"], userDecode["dept"], ' registered : ' , connectedToken) 
            print('Token user + dept ok. Check for exp time...') 

            # Check the expiration time: 
            if int(userDecode_exp) < int(connectedToken_exp): 
                print('Past token time', userDecode, userDecode_exp, connectedToken, connectedToken_exp) 
                return 'past' 
            else: 
                print('ok token time', userDecode, userDecode_exp, connectedToken, connectedToken_exp) 
                if userDecode['dept'] == 'gestion': 
                    permission = 'GESTION' 
                    print('OK token gestion (manager)') 
                elif userDecode['dept'] == 'commerce': 
                    permission = 'COMMERCE' 
                    print('OK token commerce (manager)') 
                elif userDecode['dept'] == 'support': 
                    permission = 'SUPPORT' 
                    print('OK token support (manager)') 
                else: 
                    permission = None 
                    print('token inconnu (manager)') 
                return permission 
        else: 
            # ok 
            print('connected : ', userDecode["email"], userDecode["pass"], userDecode["dept"], ' registered : ' , connectedToken["email"], connectedToken["pass"], connectedToken["dept"]) 
            print('NO token checked (manager)') 
            return None 


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


    def update_user(self, id, field, new_value): 
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


    # TODO: suppr print 
    def select_one_user(self, field, value): 
        user_db = User() 
        if field == 'id': 
            user_db = self.session.query(User).filter( 
                User.id==int(value)).first() 
        elif field == 'name': 
            user_db = self.session.query(User).filter( 
                User.name==value).first() 
        elif field == 'email': 
            user_db = self.session.query(User).filter( 
                User.email==value).first() 
        elif field == 'department_id': 
            user_db = self.session.query(User).filter( 
                User.department_id==value).first() 
        else: 
            print('no field recognized (manager.select_one_user)') 
        if user_db is None: 
            # TODO : afficher de nouveau la question précédente ? 
            print('Aucun utilisateur avec ces informations (manager.select_one_user)') 
            return False 
        else: 
            print(f'user trouvé (manager.select_one_user) : {user_db.name}, id : {user_db.id}, mail : {user_db.email}, pass : {user_db.password}, départemt : (id : {user_db.department.id}) name : {user_db.department.name}.') 
        return user_db 


    def select_all_users(self): 
        items_db = self.session.query(User).all() 
        for item in items_db:
            print(f'user trouvé  (manager.select_all_users) : {item.name}, id : {item.id}.') 
        return items_db 


    def delete_user(self, field, value): 
        item_db = self.select_one_user(field, value) 
        self.session.delete(item_db) 
        self.session.commit() 


    # def select_many(self, item): 
    #     users_db = self.session.query(User).filter(User.department==item) 
    #     # users_db = self.session.query(User).filter(User.department==vente) 
    #     for user in users_db: 
    #         print(f'User trouvé : {user.name}, id : {user.id}, departement : {user.department.name}') 

    #     clients_saler_1 = self.session.query(Client).filter(Client.sales_contact_id==item) 
    #     for client in clients_saler_1: 
    #         print(f'Client trouvé : {client.name}, id : {client.id}, contact commercial : {client.sales_contact_id, }, créé le {client.created_at}.') 

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

