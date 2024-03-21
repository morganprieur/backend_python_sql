
from manager import Manager 
from models import Base, Client, Contract, Department, Event, User  
from views import Views 

from sqlalchemy.orm import sessionmaker 

import json 
import os 
from datetime import datetime 
import bcrypt 
from prompt_toolkit import PromptSession 
session = PromptSession() 


class Controller(): 
    print(f'hello controller') 

    def start(self, mode): 
        view = Views() 
        manager = Manager() 
        manager.connect() 
        manager.create_tables() 
        manager.create_session() 
        newDept = manager.add_department(['vente']) 
        # DEBUG: 
        # dept_db = manager.select_one_dept('name', 'vente') 
        updatedDept = manager.update_dept('commerce', ['vente']) 
        upd_dept_db = manager.select_one_dept('name', 'commerce') 
        # DEBUG: Check if the old name doesn't exist anymore: 
        # upd_dept_db_none = manager.select_one_dept('vente')  # None ok 

        superAdmin = manager.add_user(['super_admin', 'admin@mail.org', os.environ.get('USER_1_PW'), '06 12 34 56 78', 1]) 

        if mode == 'pub': 
            # Type the required credentials: 
            userConnect = view.input_user_connection() 
            checked = manager.check_pw(userConnect['email'], userConnect['password']) 
        else:  
            # file deepcode ignore PT: local project 
            # Get the required credentials from the json data: 
            with open(os.environ.get('FILE_PATH'), 'r') as jsonfile: 
                registered = json.load(jsonfile) 
            userConnect = registered['users'][0] 
            password = os.environ.get('USER_1_PW') 
            checked = manager.check_pw(userConnect['email'], password) 

        # print(checked) 
        if not checked: 
            print('not connected user') 
        else: 
            logged_user = manager.select_one_user('email', userConnect['email'])  
            print('logged_user : ', logged_user) 


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


# if __name__ == "__main__": 
#     # main('pub') 
#     main('dev') 

