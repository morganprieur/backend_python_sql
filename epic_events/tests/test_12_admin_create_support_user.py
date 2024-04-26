
# from epic_events.helpers import decorator_verify_jwt 
from epic_events.manager import Manager 

import unittest 
import json 
import os 
from datetime import datetime 



class Superuser3Test(unittest.TestCase): 
    """ Config test files. 
    """ 
    def setUp(self): 
        # # view = Views() 
        self.manager = Manager() 
        self.manager.connect() 
        self.manager.create_session() 


    def test_1_verify_admin_token(self): 
    	""" Test the admin user's token. 
    		Expect his permission dept == 'GESTION'. 
    	""" 
    	registered = self.manager.decrypt_token() 

    	connectEmail = 'admin@mail.org' 
    	# connectPass = self.manager.hash_pw(os.environ.get('USER_1_PW')) 
    	self.connectUser = self.manager.select_one_user('email', 'admin@mail.org') 
    	if self.manager.verify_if_token_exists(connectEmail): 
    		self.permission = self.manager.verify_token( 
    			connectEmail, 
    			self.connectUser.department.name 
    		) 
    		assert self.permission == 'GESTION' 
    	else: 
    	    assert not self.permission 


    def test_2_getting_support_dept(self): 
        """ Test getting support dept, if permission is 'GESTION'. 
            Expect one department's name is 'support'. 
    	""" 
        if self.permission == 'GESTION': 
            self.suppDept_db = self.manager.select_one_dept('support') 
            assert len(self.suppDept_db) == 1 
        else: 
            assert not self.permission 


    def test_3_creation_support_user(self): 
    	""" Test adding one support user, if permission is 'GESTION'. 
            Expect his name is the one that has been given to register. 
    	""" 
    	if self.permission == 'GESTION': 
            # print('get password :', os.environ.get('U_3_PW'))  # bug vscode ? 
            testUser = self.manager.add_entity( 'user', { 
                'name': 'support_user 1', 
                'email': 'support_1@mail.org', 
                'entered_password': 'pass_user3', 
                'phone': '06 34 56 78 91', 
                'department_name': self.suppDept_db.name 
            }) 

            items_db = self.manager.select_all_entities('users') 
            assert len(items_db) == 3 
            testSupport_db = items_db.pop() 
            print('DEBUG : ', testSupport_db) 
            assert testSupport_db.name == 'support_user 1' 
    	else: 
            assert not self.permission 

