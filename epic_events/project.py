
from manager import Manager 
from models import Base, Client, Contract, Department, Event, User   
from sqlalchemy.orm import sessionmaker 

import os 
from datetime import datetime 
import bcrypt 

def main(): 

    print(f'hello main {datetime.now()}') 
    manager = Manager() 
    manager.connect() 
    manager.create_tables() 
    manager.create_session() 
    newDept = manager.add_department_item(['vente']) 
    # dept_db = manager.select_one_dept('name', 'vente') 
    updatedDept = manager.update_dept_item('commerce', ['vente']) 
    upd_dept_db = manager.select_one_dept('name', 'commerce') 
    # upd_dept_db_none = manager.select_one_dept('vente')  # None ok 

    newUser = manager.add_user(['user_1', 'user1@mail.fr', os.environ.get('USER_1_PW'), '06 12 34 56 78', 1]) 
    user1_db = manager.select_one_user('name', 'user_1') 
    checked = manager.check_pw('pass_us1', 1) 
    # get_token 


    # # print(newItem.__str__()) 
    # newSaler = manager.add_model_item('sales_user', User, 
    #     ['sales 1', 'sales_1@mail.com', 'S3cr3tp4ss', '01 23 45 67 89', newDept])
    # # manager.select_one(newDept) 
    # item = manager.select_one('vente_db', Department, 'vente') 
    # print(item) 
    # # manager.add_model_item('client', Client, [ 
    # #     'client 1', 
    # #     'client_1@mail.com', 
    # #     '01 32 45 67 89', 
    # #     'Entreprise 1', 
    # #     datetime.now(), 
    # #     datetime.now(), 
    # #     newClient 
    # # ]) 
    # # # manager.other(newSaler) 
    # # item = manager.select_one('vente_db', Department, 'name', 'vente') 


if __name__ == "__main__": 
    main() 

