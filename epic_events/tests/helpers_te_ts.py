
from epic_events.manager import Manager 

import unittest 
import json 
import os 
from datetime import datetime 


class ConnectTest(): 
    """ Set the role of the user to test. 
    """ 
    @classmethod 
    def __init__(cls, role:str): 
        cls.manager = Manager() 
        cls.manager.connect() 
        cls.manager.create_session() 
        cls.role = role 

    @classmethod 
    def connect_user(cls): 
        """ Test the user's token. 
        """ 
        # registered = cls.manager.decrypt_token() 
        role_dict = { 
            'admin': { 
                'email': 'admin@mail.org', 
                # file deepcode ignore NoHardcodedPasswords/test: local project 
                'pass': 'pass_superuser1', 
                'dept': 'GESTION' 
            }, 
            'sales': { 
                'email': 'sales_1@mail.org', 
                # file deepcode ignore NoHardcodedPasswords/test: local project 
                'pass': 'pass_user2', 
                'dept': 'COMMERCE' 
            }, 
            'support': { 
                'email': 'support_1@mail.org', 
                # file deepcode ignore NoHardcodedPasswords/test: local project 
                'pass': 'pass_user3', 
                'dept': 'SUPPORT' 
            } 
        } 
        connectUser = cls.manager.select_one_user( 
        	'email', 
        	role_dict[cls.role]['email'] 
        ) 

        row = cls.manager.verify_if_token_exists(role_dict[cls.role]['email']) 
        if row is not None: 
        	cls.permission = cls.manager.verify_token( 
        		role_dict[cls.role]['email'], 
        		connectUser.department.name, 
        		row 
        	) 
        	if cls.permission == 'past': 
        	    pw_check = cls.manager.check_pw( 
        	        role_dict[cls.role]['email'], 
        	        role_dict[cls.role]['pass'] 
        	    ) 
        	    if pw_check: 
        	        new_token = cls.manager.get_token(120, { 
        	            'email': role_dict[cls.role]['email'], 
        	            'dept': connectUser.department.name 
        	        }) 
        	        cls.manager.register_token( 
        	            role_dict[cls.role]['email'], 
        	            new_token 
        	        ) 

        	        row = cls.manager.verify_if_token_exists( 
        	            role_dict[cls.role]['email'] 
        	        ) 
        	        cls.permission = cls.manager.verify_token( 
        	            role_dict[cls.role]['email'], 
        	            connectUser.department.name, 
        	            row 
        	        ) 
        	        assert cls.permission == role_dict[cls.role]['dept'] 
        	        # assert 1 == 2 
        	    else: 
        	        assert not cls.permission 
        	        assert 2 == 3 
        else: 
            pw_check = cls.manager.check_pw( 
                role_dict[cls.role]['email'], 
                role_dict[cls.role]['pass'] 
            ) 
            if pw_check: 
                new_token = cls.manager.get_token(120, { 
                    'email': role_dict[cls.role]['email'], 
                    'dept': connectUser.department.name 
                }) 
                cls.manager.register_token( 
                    role_dict[cls.role]['email'], 
                    new_token 
                ) 

                row = cls.manager.verify_if_token_exists( 
                    role_dict[cls.role]['email'] 
                ) 
                cls.permission = cls.manager.verify_token( 
                    role_dict[cls.role]['email'], 
                    connectUser.department.name, 
                    row 
                ) 
                assert cls.permission == role_dict[cls.role]['dept'] 
                assert 3 == 4 
            else: 
                assert not cls.permission 
                assert 4 == 5 

			# if cls.permission in ['GESTION', 'COMMERCE', 'SUPPORT']: 
