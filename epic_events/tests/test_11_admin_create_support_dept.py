
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


    def test_01_not_already_support_dept(self): 
        """ Test getting one dept with name 'support', if permission is 'GESTION'. 
            Expect 2 deptartments registered into the DB 
            and the none of them's name is 'support'. 
    	""" 
        if self.permission == 'GESTION': 
            depts_db = self.manager.select_all_entities('depts') 
            assert len(items_db) == 2 
            depts_names_list = [] 
            for dept in depts_db: 
                depts_names_list.append(dept.name) 
            assert 'support' not in depts_names_list 
        else: 
            assert not self.permission 


    def test_01_creation_support_dept(self): 
        """ Test adding one dept, if permission is 'GESTION'. 
            Expect 3 deptartments registered into the DB 
            and the last's name is 'support'. 
    	""" 
        if self.permission == 'GESTION': 
            suppDept = self.manager.add_entity('dept', { 
                'name': 'support' 
            }) 
            items_db = self.manager.select_all_entities('depts') 
            assert len(items_db) == 3 
            last_dept = items_db.pop() 
            assert last_dept.name == 'support' 
        else: 
            assert not self.permission 

