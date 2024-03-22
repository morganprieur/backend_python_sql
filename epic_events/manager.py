
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

    def create_tables(self): 
        try: 
            Base.metadata.drop_all(bind=self.engine) 
            Base.metadata.create_all(bind=self.engine) 
        except Exception as ex: 
            print(ex) 

    def create_session(self): 
            Session = sessionmaker(bind=self.engine) 
            self.session = Session() 

    def add_required(self): 
        """ Register the 'gestion' department and the superuser, 
            who will add the other departments and users. 
        """ 
        # file deepcode ignore PT: local project 
        with open(os.environ.get('FILE_PATH'), 'r') as jsonfile: 
            registered = json.load(jsonfile) 
        admin_dept = registered['department'][0] 
        # print(admin_dept) 
        super_admin = registered['users'][0] 

        gestion_dept = Department(name=admin_dept['name']) 
        self.session.add(gestion_dept) 
        self.session.commit() 

        # superAdmin_dept_name = session.query(Department).get(Department.id==1) 
        # vente.name = 'commerce' 
        # session.commit() 

        # ==== hash admin pass ==== # 
        password = os.environ.get('USER_1_PW') 
        print(password) 
        salt = bcrypt.gensalt(16)
        hash_password = bcrypt.hashpw( 
            password.encode('utf-8'), 
            salt 
        ).decode('utf-8') 

        # ==== get token ==== # 
        dept_name = admin_dept['name'] 

        payload = { 
            'email': super_admin['email'], 
            'pass': os.environ.get('USER_1_PW'), 
            'dept': dept_name, 
        } 
        secret = os.environ.get('JWT_SECRET') 
        algo = os.environ.get('JWT_ALGO') 
        encoded_jwt = jwt.encode(payload, secret, algo) 
        # print(encoded_jwt) 
        # return encoded_jwt 

        superAdmin = User( 
            name=super_admin['name'], 
            email=super_admin['email'], 
            password=hash_password, 
            phone=super_admin['phone'], 
            department_id=super_admin['department_id'], 
            token=encoded_jwt 
        ) 
        self.session.add(superAdmin) 
        self.session.commit() 



        # sales_user = User( 
        #     name='sales 1', 
        #     email='sales_1@mail.com', 
        #     password='S3cr3tp4ss', 
        #     phone='01 23 45 67 89', 
        #     department=vente 
        # ) 
        # self.session.add(sales_user) 
        # self.session.commit() 


    # ==== department ==== # 
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
        # print(field) 
        # print(type(field)) 
        if field == 'id': 
            item_db = self.session.query(Department).filter(Department.id==int(value)).first() 
        if field == 'name': 
            item_db = self.session.query(Department).filter(Department.name==value).first() 
        else: 
            print('Ce champ n\'existe pas.')  
            # item_db = self.session.query(Department).filter(Department.name==value).first() 
        print(f'département trouvé : {item_db.name}, id : {item_db.id}.') 
        return item_db 

    def select_all_depts(self): 
        items_db = self.session.query(Department).all() 
        for item in items_db:
            print(f'département trouvé : {item.name}, id : {item.id}.') 
        return items_db 

    def delete_dept(self, field, value): 
        item_db = self.select_one_dept(field, value) 
        self.session.delete(item_db) 
        self.session.commit() 

    # ==== user ==== # 
    # Essai décorateur jwt_gestion 
    # @jwt_gestion
    def add_user(self, fields:list): 
        print(fields) 
        dept_db = self.select_one_dept('id', fields[4])  
        userName = User( 
            name=fields[0], 
            email=fields[1], 
            password='password', 
            # password=fields[2], 
            phone=fields[3], 
            department_id=dept_db.id, 
            token='st.ri.ng', 
        ) 
        userName.password = self.hash_pw(fields[2], 12) 
        # Get token JWT 
        # delta = 2  # <-- for 'exp' JWT claim 
        data = { 
            'email': fields[1], 
            'pass': fields[2], 
            'dept': dept_db.name, 
        } 
        # userName.token = self.get_token(delta, data) 
        userName.token = self.get_token(data) 
        self.session.add(userName) 
        self.session.commit() 
        return userName 

    # def get_token(self, delta:int, data:dict): 
    def get_token(self, data:dict): 
        payload = { 
            'email': data['email'], 
            'pass': data['pass'], 
            'dept': data['dept'], 
        } 
        secret = os.environ.get('JWT_SECRET') 
        algo = os.environ.get('JWT_ALGO') 
        encoded_jwt = jwt.encode(payload, secret, algo) 
        # print(encoded_jwt) 
        return encoded_jwt 
        # tuto : eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg 

    def verify_token(self, connectEmail, connectPass, connectDept): 
        registeredToken = self.select_one_user('email', connectEmail).token 
        # print('registeredToken : ', registeredToken) 
        secret = os.environ.get('JWT_SECRET') 
        algo = os.environ.get('JWT_ALGO') 

        userDecode = jwt.decode(registeredToken, secret, algorithms=[algo]) 

        connectedToken = { 
            'email': connectEmail, 
            'pass': connectPass, 
            'dept': connectDept, 
        } 
        if {userDecode['email'], userDecode['pass'], userDecode['dept']} == {connectedToken['email'], connectedToken['pass'], connectedToken['dept']}: 
            # ok 
            print('OK token') 
            return True 
        else: 
            # ok 
            print('NO token') 
            return False 

    def hash_pw(self, password, nb:int): 
        salt = bcrypt.gensalt(nb)
        hash_password = bcrypt.hashpw( 
            password.encode('utf-8'), 
            salt 
        ).decode('utf-8') 
        return hash_password 

    def check_pw(self, userEmail, pw): 
        user_db = self.select_one_user('email', userEmail) 
        if user_db is None: 
            print('user is none') 
            return False 
        else: 
            hashed = user_db.password 
            if bcrypt.checkpw(pw.encode('utf-8'), hashed.encode('utf-8')): 
                print("pw ok") 
                return True 
            else: 
                print('pw not ok') 
                return False 

    def update_user(self, id, field, value, new_value): 
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
            print('no value') 
        self.session.commit() 
        return itemName 

    # TODO: suppr print 
    def select_one_user(self, field, value): 
        print('field : ', field) 
        print('value : ', value) 
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
            print('no field') 
        if user_db is None: 
            # TODO : afficher de nouveau la question précédente ? 
            print('Aucun utilisateur avec ces informations') 
            # return False 
        else: 
            print(f'user trouvé : {user_db.name}, id : {user_db.id}, mail : {user_db.email}, pass : {user_db.password}, départemt : (id : {user_db.department.id}) name : {user_db.department.name}.') 
        return user_db 

    def select_all_users(self): 
        items_db = self.session.query(User).all() 
        for item in items_db:
            print(f'user trouvé in all : {item.name}, id : {item.id}.') 
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
