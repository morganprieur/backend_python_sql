
# import this 

from controller import Controller 
from manager import Manager 
# from controller import Controller 
from sqlalchemy.orm import sessionmaker 

import json 
import os 
from datetime import datetime 
import bcrypt 
from prompt_toolkit import PromptSession 
session = PromptSession() 


def main(mode='pub'): 

    print(f'hello main {datetime.now()}') 
    controller = Controller() 
    controller.start(mode) 
    # view = Views() 
    # manager = Manager() 
    # manager.connect() 
    # manager.create_tables() 
    # manager.create_session() 
    # newDept = manager.add_department_item(['vente']) 
    # # DEBUG: 
    # # dept_db = manager.select_one_dept('name', 'vente') 
    # updatedDept = manager.update_dept_item('commerce', ['vente']) 
    # upd_dept_db = manager.select_one_dept('name', 'commerce') 
    # # DEBUG: Check if the old name doesn't exist anymore: 
    # # upd_dept_db_none = manager.select_one_dept('vente')  # None ok 

    # superAdmin = manager.add_user(['super_admin', 'admin@mail.org', os.environ.get('USER_1_PW'), '06 12 34 56 78', 1]) 

    # if mode == 'pub': 
    #     # Type the required credentials: 
    #     userConnect = view.input_user_connection() 
    #     checked = manager.check_pw(userConnect['email'], userConnect['password']) 
    # else:  
    #     # file deepcode ignore PT: local project 
    #     # Get the required credentials from the json data: 
    #     with open(os.environ.get('FILE_PATH'), 'r') as jsonfile: 
    #         registered = json.load(jsonfile) 
    #     userConnect = registered['users'][0] 
    #     password = os.environ.get('USER_1_PW') 
    #     checked = manager.check_pw(userConnect['email'], password) 

    # # print(checked) 
    # if not checked: 
    #     print('not connected user') 
    # else: 
    #     logged_user = manager.select_one_user('email', userConnect['email'])  
    #     print('logged_user : ', logged_user) 



if __name__ == "__main__": 
    # main('pub') 
    main('dev') 

