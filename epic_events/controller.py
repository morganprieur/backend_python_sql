
from manager import Manager 
from models import Base, Client, Contract, Department, Event, User  
from views import Views 
from utils.helpers import test_fct 

from sqlalchemy.orm import sessionmaker 

# from getpass import getpass 
import bcrypt 
from datetime import datetime, timedelta 
import json 
from jwt.exceptions import ExpiredSignatureError 
import os 
import time 

from prompt_toolkit import PromptSession 
session = PromptSession() 


class Controller(): 
    print(f'hello controller') 
    # test_fct() 

    def start(self, mode): 
        view = Views() 
        manager = Manager() 
        manager.connect() 
        manager.create_tables() 
        manager.create_session() 
        newDept = manager.add_department(['vente']) 
        # DEBUG: 
        # dept_db = manager.select_one_dept('name', 'vente') 
        updatedDept = manager.update_dept('commerce', 'vente') 
        upd_dept_db = manager.select_one_dept('name', 'commerce') 

        superAdmin = manager.add_user( 
            ['super_admin', 
            'admin@mail.org', 
            os.environ.get('USER_1_PW'), 
            '06 12 34 56 78', 
            upd_dept_db.id 
        ]) 

        # time.sleep(5) 
        # print('pause') 

        if mode == 'pub': 
            # Type the required credentials: 
            userConnect = view.input_user_connection() 
            # Verify password 
            checked = manager.check_pw( 
                userConnect['email'], 
                userConnect['password'] 
            ) 
        else:  
            # file deepcode ignore PT: local project 
            with open(os.environ.get('FILE_PATH'), 'r') as jsonfile: 
                registered = json.load(jsonfile) 
            userConnect = registered['users'][0] 
            password = os.environ.get('USER_1_PW') 
            # Verify password 
            checked = manager.check_pw(userConnect['email'], password) 
        # TODO: sortie propre après l'erreur de saisie 
        if not checked: 
            print('Les informations saisies ne sont pas bonnes, merci de réessayer.') 
        else: 
            logged_user = manager.select_one_user( 
                'email', userConnect['email']) 
            # Verify JWT 
            tokened = manager.verify_token( 
                userConnect['email'], 
                password, 
                logged_user.department.name 
            ) 
            # TODO: sortie propre après l'échec du token 
            if not tokened: 
                print('Vous n\'avez pas la permission \'effectuer cette action') 
            else: 
                permission = True 
                print('permission ok') 
                return permission 




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

