
from sqlalchemy import create_engine 
import psycopg2 
from epic_events.models import Base, Client, Contract, Department, Event, User 
from sqlalchemy.orm import sessionmaker 

import bcrypt 
from datetime import datetime, timedelta 
import json 
import jwt 
import os 


class Setup(): 
    print('hello setup') 
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
        """ Register the departments and the superuser, 
            who will be able to add the other users and update departments. 
            Returns bool: True if it's done. 
        """ 
        # file deepcode ignore PT: local project 
        with open('epic_events/'+os.environ.get('FILE_PATH'), 'r') as jsonfile: 
            registered = json.load(jsonfile) 
        admin_dept = registered['departments'][0] 
        sales_dept = registered['departments'][1] 
        support_dept = registered['departments'][2] 
        super_admin = registered['users'][0] 
        user_commerce = registered['users'][1] 

        # ==== add departments ==== # 
        gestion_dept = Department(name=admin_dept['name']) 
        self.session.add(gestion_dept) 
        self.session.commit() 

        # DEBUG 
        superAdmin_dept_name = self.session.query(Department).filter(Department.id==1).first() 
        
        # sales dept 
        com_dept = Department(name=sales_dept['name']) 
        self.session.add(com_dept) 
        self.session.commit() 
        # /sales dept 

        # support dept 
        sup_dept = Department(name=support_dept['name']) 
        self.session.add(sup_dept) 
        self.session.commit() 
        # /support dept 
        # ==== /add departments ==== # 

        # ==== tokens management ==== # 
        # def get_key(): 
        #     """ Generate a key and regsiter it into a file. 
        #         Returns:
        #             bool: True if the process has been done. 
        #     """ 
        # key generation 
        key = Fernet.generate_key() 
        # regsiters the key in a file 
        with open(os.environ.get('JWT_KEY_PATH'), 'wb') as filekey: 
            filekey.write(key) 
                # return True 
        # ==== /tokens management ==== # 

        # ==== add users ==== # 
        # superAdmin 
        # ==== hash admin pass ==== # 
        password = os.environ.get('USER_1_PW') 
        # print(password) 
        salt = bcrypt.gensalt(16)
        hash_password_SA = bcrypt.hashpw( 
            password.encode('utf-8'), 
            salt 
        ).decode('utf-8') 

        # ==== register admin user ==== # 
        admin_department = self.session.query(Department).filter(Department.name==super_admin['department_name']).first() 
        superAdmin = User( 
            name=super_admin['name'], 
            email=super_admin['email'], 
            password=hash_password_SA, 
            phone=super_admin['phone'], 
            department_id=admin_department.id  # , 
            # token=encoded_jwt 
        ) 
        self.session.add(superAdmin) 
        self.session.commit() 
        # ==== /register admin user ==== # 

        # ==== get + register admin token ==== # 
        adminUser = self.session.query(User).filter(User.name==superAdmin['name']).first() 
        token = self.manager.get_token(2, { 
            'email': adminUser.email, 
            'pass': adminUser.password, 
            'dept': adminUser.departments.name, 
            'type': 'token' 
        }) 
        print(token) 

        usersTokens = { 
            "users": [ 
                { 
                    "email": adminUser.email, 
                    "token": token 
                } 
            ] 
        } 

        # Encrypt the token 
        # encrypted = cipher_suite.encrypt(usersTokens) 
        encrypted = cipher_suite.encrypt(str(usersTokens).encode('utf-8')) 
        # Register the encrypted token 
        with open(os.environ.get('TOKEN_PATH'), 'wb') as encrypted_file:
            encrypted_file.write(encrypted) 

        return True 

        # ==== /get + register admin token ==== # 


if __name__ == "__main__": 
    setup = Setup() 
    setup.connect() 
    setup.create_tables() 
    setup.create_session() 
    setup.add_required() 

