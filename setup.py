
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

        # ==== /add users ==== # 
        # superAdmin 
        # ==== hash admin pass ==== # 
        password = os.environ.get('USER_1_PW') 
        # print(password) 
        salt = bcrypt.gensalt(16)
        hash_password_SA = bcrypt.hashpw( 
            password.encode('utf-8'), 
            salt 
        ).decode('utf-8') 

        # ==== get token admin ==== # 
        dept_name = admin_dept['name'] 
        payload = { 
            'email': super_admin['email'], 
            'pass': os.environ.get('USER_1_PW'), 
            'dept': dept_name, 
            'exp': datetime.now()+timedelta(seconds=5) 
        } 
        secret = os.environ.get('JWT_SECRET') 
        algo = os.environ.get('JWT_ALGO') 
        encoded_jwt = jwt.encode(payload, secret, algo) 
        print(encoded_jwt) 

        admin_department = self.session.query(Department).filter(Department.name==super_admin['department_name']).first() 

        # ==== register admin user ==== # 
        superAdmin = User( 
            name=super_admin['name'], 
            email=super_admin['email'], 
            password=hash_password_SA, 
            phone=super_admin['phone'], 
            department_id=admin_department.id, 
            token=encoded_jwt 
        ) 
        self.session.add(superAdmin) 
        self.session.commit() 

        # DEBUG 
        superadmin_dept_db = self.session.query(Department).filter( 
            Department.id==1).first()
        print('superadmin_dept_db SL108 : ', superadmin_dept_db) 
        # /superAdmin 

        # salesUser  # à retirer 
        # ==== hash salesUser pass ==== # 
        password = os.environ.get('U_2_PW') 
        salt = bcrypt.gensalt(16)
        hash_password_SU = bcrypt.hashpw( 
            password.encode('utf-8'), 
            salt 
        ).decode('utf-8') 

        # ==== get token admin ==== # 
        sales_dept_name = sales_dept['name'] 
        payload = { 
            'email': user_commerce['email'], 
            'pass': os.environ.get('U_2_PW'), 
            'dept': sales_dept_name, 
            'exp': datetime.now()+timedelta(seconds=5) 
        } 
        secret = os.environ.get('JWT_SECRET') 
        algo = os.environ.get('JWT_ALGO') 
        su_encoded_jwt = jwt.encode(payload, secret, algo) 
        print(su_encoded_jwt) 

        salesUser_department = self.session.query(Department).filter( 
            Department.name==user_commerce['department_name']).first() 

        # ==== register admin user ==== # 
        salesUser = User( 
            name=user_commerce['name'], 
            email=user_commerce['email'], 
            password=hash_password_SU, 
            phone=user_commerce['phone'], 
            department_id=salesUser_department.id, 
            token=su_encoded_jwt 
        ) 
        self.session.add(salesUser) 
        self.session.commit() 
        # /salesUser  # à retirer 


if __name__ == "__main__": 
    setup = Setup() 
    setup.connect() 
    setup.create_tables() 
    setup.create_session() 
    setup.add_required() 

