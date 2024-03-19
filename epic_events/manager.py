
from sqlalchemy import create_engine 
import psycopg2 
from models import Base, Client, Contract, Department, Event, User   
from sqlalchemy.orm import sessionmaker 

import os 
import bcrypt 
import jwt 


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
        # db_user = os.environ.get('POSTGRES_USER') 
        # db_password = os.environ.get("POSTGRES_PASSWORD") 
        # db_host = os.environ.get("POSTGRES_HOST") 
        # db_port = os.environ.get("DB_PORT") 
        # db_name = os.environ.get("POSTGRES_DB") 
        # db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}" 
        # print(db_url) 
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

    def add_department_item(self, fields:list): 
        itemName = Department(name=fields[0]) 
        self.session.add(itemName) 
        self.session.commit() 
        return itemName 

    def update_dept_item(self, new_value, fields:list): 
        itemName = self.select_one_dept('name', fields[0]) 
        itemName.name = new_value 
        self.session.commit() 
        return itemName 

    def select_one_dept(self, field, value): 
        if field == 'name': 
            item_db = self.session.query(Department).filter(Department.name==value).first() 
        else: 
            item_db = self.session.query(Department).filter(Department.name==value).first() 
        print(f'département trouvé : {item_db.name}, id : {item_db.id}.') 
        return item_db 

    def add_user(self, fields:list): 
        print(fields) 
        userName = User( 
            name=fields[0], 
            email=fields[1], 
            password=fields[2], 
            phone=fields[3], 
            department_id=fields[4], 
        ) 
        # userName.password = bcrypt.hashpw(fields[2].encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8') 
        userName.password = self.hash_pw(fields[2], 12) 
        # userName.password = self.hash_pw(fields[2]) 
        print('userName.password : ', userName.password) 
        # print('userName.department_id : ', userName.department_id) 
        self.session.add(userName) 
        self.session.commit() 
        return userName 
    #     # hashed_password = flask_bcrypt.generate_password_hash('hash3_for_password').decode('utf-8')  
    #     # print(hashed_password) 

    def hash_pw(self, password, nb:int): 
        salt = bcrypt.gensalt(nb)
        hash_password = bcrypt.hashpw( 
            password.encode('utf-8'), 
            salt 
            # bcrypt.gensalt(12) 
        ).decode('utf-8') 
        return hash_password 

    def select_one_user(self, field, value): 
        if field == 'id': 
            user_db = self.session.query(User).filter(User.id==int(value)).first() 
        elif field == 'name': 
            user_db = self.session.query(User).filter(User.name==value).first() 
        print(f'user trouvé : {user_db.name}, id : {user_db.id}, mail : {user_db.email}, pass : {user_db.password}, départemt : (id : {user_db.department.id}) name : {user_db.department.name}.') 
        return user_db 


    def check_pw(self, pw, user_id): 
        user_db = self.select_one_user('id', 1) 
        hashed = user_db.password 
        if bcrypt.checkpw(pw.encode('utf-8'), hashed.encode('utf-8')): 
            print("pw ok") 
        else: 
            print('pw not ok') 



    # def select_one(self, itemName, model, value): 
    #     # vente = Department(name='vente') 
    #     # session.add(vente) 
    #     # session.commit() 

    #     # vente.name = 'commerce' 
    #     # self.session.commit() 

    #     # sales_user = User( 
    #     #     name='sales 1', 
    #     #     email='sales_1@mail.com', 
    #     #     password='S3cr3tp4ss', 
    #     #     phone='01 23 45 67 89', 
    #     #     department=item 
    #     #     # department=vente 
    #     # ) 
    #     # self.session.add(sales_user) 
    #     # self.session.commit() 

    #     print('itemName : ', itemName, ' model : ', model, ' value : ', value) 
    #     item = model.select_one_item(self, itemName, value) 
    #     print(item) 
    #         # itemName = session.query(model).filter(model.attribute==value).first() 
    #     # vente_db = self.session.query(Department).filter(Department.id==1).first() 
    #     # print(f'département trouvé : {vente_db.name}, id : {vente_db.id}.') 

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

# print('hello manager') 

        # Voir si engine s'en occupe ? 
        # if conn is not None: 
        #     conn.close() 
        #     print('connex closed') 

        # return self.engine 


# if __name__ == "__main__": 
#     main() 

