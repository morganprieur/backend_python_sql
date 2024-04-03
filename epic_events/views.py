
from getpass import getpass 
from prompt_toolkit import PromptSession 
session = PromptSession() 


class Views(): 
    print('hello view') 
    def input_user_connection(self): 
        user = {} 
        user['email'] = session.prompt('\nAdresse mail : ') 
        user['password'] = getpass('\nMot de passe : ') 
        # user['email'] = getpass('\nAdresse mail : ') 
        # user['password'] = session.prompt('\nMot de passe : ') 
        return user 


    def input_create_dept(self): 
        dept = {} 
        dept['name'] = session.prompt('\nNom du département : ') 
        return dept 
    






