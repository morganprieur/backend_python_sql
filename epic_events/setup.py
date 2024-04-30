
from sqlalchemy import create_engine 
import psycopg2 
from manager import Manager 
from models import Base, Client, Contract, Department, Event, User 
from sqlalchemy.orm import sessionmaker 

from cryptography.fernet import Fernet 
from datetime import datetime, timedelta 
import json 
import os 


class Setup(): 
    print('hello setup') 
    def __init__(self): 
        self.manager = Manager() 
        self.manager.connect() 
        try: 
            Base.metadata.drop_all(bind=self.manager.engine) 
            Base.metadata.create_all(bind=self.manager.engine) 
            print('DB connection ok') 
        except Exception as ex: 
            print(ex) 
        self.manager.create_session() 


    def add_required(self): 
        """ Register the departments and the superuser, 
            who will be able to add the other users and update departments. 
            Returns bool: True if it's done. 
        """ 
        # file deepcode ignore PT: local project 
        with open(os.environ.get('FILE_PATH'), 'r') as jsonfile: 
            registered = json.load(jsonfile) 
        admin_dept = registered['departments'][0] 
        super_admin = registered['users'][0] 

        # ==== add departments ==== # 
        self.manager.add_entity('dept', {'name': admin_dept['name']}) 

        # DEBUG 
        superAdmin_dept_name = self.manager.session.query(Department).filter(Department.id==1).first() 
        print('DEBUG superAdmin_dept_name : ', superAdmin_dept_name) 
        # ==== /add department ==== # 

        # ==== tokens management ==== # 
        """ Generate a key and regsiter it into a file. 
            Returns:
                bool: True if the process has been done. 
        """ 
        # key generation 
        key = Fernet.generate_key() 
        # regsiters the key in a file 
        with open(os.environ.get('JWT_KEY_PATH'), 'wb') as filekey: 
            filekey.write(key) 
        # ==== /token management ==== # 

        # ==== add superAdmin user ==== # 
        # ==== hash pass ==== # 
        password = os.environ.get('USER_1_PW') 
        hash_password_SA = self.manager.hash_pw(password) 
        # print(password) 

        # ==== register user ==== # 
        superAdmin = { 
            'name': super_admin['name'], 
            'email': super_admin['email'], 
            'password': hash_password_SA, 
            'phone': super_admin['phone'], 
            'department_name': 'gestion'  # , 
        } 
        adminUser = self.manager.add_user_setup(superAdmin) 
        print('DEBUG adminUser : ', adminUser) 
        # ==== /register user ==== # 

        # ==== register empty file for tokens ==== # 
        userToken = { 
            "users": [ 
            ] 
        } 
        # Encrypt the token 
        self.manager.first_register_token(userToken) 
        debug = self.manager.decrypt_token() 
        print('debug decrypt_token :', debug) 
        return True 
        # ==== /register empty file for tokens ==== # 


if __name__ == "__main__": 
    setup = Setup() 
    setup.add_required() 

