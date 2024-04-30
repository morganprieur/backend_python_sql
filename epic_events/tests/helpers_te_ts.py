
from epic_events.manager import Manager 

import unittest 
import json 
import os 
from datetime import datetime 


# class ConnectTest(unittest.TestCase): 
class ConnectTest(): 
    """ Config file. 
    """ 
    @classmethod 
    # def setUp(cls): 
    def __init__(cls, role:str): 
        cls.manager = Manager() 
        cls.manager.connect() 
        cls.manager.create_session() 
        cls.role = role 

    @classmethod 
    # def test_1_verify_admin_token(cls): 
    def connect_user(cls): 
        """ Test the admin user's token. 
        	Expect his permission dept == 'GESTION'. 
        """ 
        # registered = cls.manager.decrypt_token() 
        role_dict = { 
            'admin': { 
                'email': 'admin@mail.org', 
                'pass': os.environ.get('USER_1_PW'), 
            } 
        } 
        # connectEmail = 'admin@mail.org' 
        # connectPass = cls.manager.hash_pw(os.environ.get('USER_1_PW')) 
        connectUser = cls.manager.select_one_user( 
        	'email', 
        	role_dict[cls.role]['email'] 
        ) 
        row = cls.manager.verify_if_token_exists(role_dict[cls.role]['email']) 
        if row: 
        	cls.permission = cls.manager.verify_token( 
        		role_dict[cls.role]['email'], 
        		connectUser.department.name, 
        		row 
        	) 
        	assert cls.permission == 'GESTION' 
        else: 
        	row = cls.manager.verify_if_token_exists(role_dict[cls.role]['email']) 
        	if row is None: 
        		# assert row is None 
        		token = cls.manager.get_token(120, { 
        			'email': role_dict[cls.role]['email'], 
        			'dept': connectUser.department.name 
        		}) 
        		cls.manager.register_token(role_dict[cls.role]['email'], token) 
        		row = cls.manager.verify_if_token_exists(role_dict[cls.role]['email']) 
        		cls.permission = cls.manager.verify_token( 
        			role_dict[cls.role]['email'], 
        			connectUser.department.name, 
        			row 
        		) 
        		assert cls.permission == 'GESTION' 
        	else: 
        		cls.permission = cls.manager.verify_token( 
        			role_dict[cls.role]['email'], 
        			connectUser.department.name, 
        			row 
        		) 
        		if cls.permission == 'past': 
        			check_pass = cls.manager.check_pw( 
                        role_dict[cls.role]['email'], 
                        role_dict[cls.role]['pass'] 
                    ) 
        			if check_pass: 
        				token = cls.manager.get_token(120, { 
        					'email': role_dict[cls.role]['email'], 
        					'dept': connectUser.department.name 
        				}) 
        				cls.manager.register_token( 
                            role_dict[cls.role]['email'], 
                            token 
                        ) 
        				row = cls.manager.verify_if_token_exists( 
                            role_dict[cls.role]['email']) 
        				cls.permission = cls.manager.verify_token( 
        					role_dict[cls.role]['email'], 
        					connectUser.department.name, 
        					row 
        				) 
        				assert cls.permission == 'GESTION' 
        			else: 
        				assert cls.permission == 'past' 

