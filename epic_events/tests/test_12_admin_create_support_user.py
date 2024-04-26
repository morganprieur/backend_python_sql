
# from epic_events.helpers import decorator_verify_jwt 
from epic_events.manager import Manager 

import unittest 
import json 
import os 
from datetime import datetime 



class Superuser3Test(unittest.TestCase): 
    """ Config test files. 
    """ 
    @classmethod
    def setUp(cls): 
        # # view = Views() 
        cls.manager = Manager() 
        cls.manager.connect() 
        cls.manager.create_session() 

    @classmethod
    def test_1_verify_admin_token(cls): 
    	""" Test the admin user's token. 
    		Expect his permission dept == 'GESTION'. 
    	""" 
    	registered = cls.manager.decrypt_token() 

    	connectEmail = 'admin@mail.org' 
    	# connectPass = cls.manager.hash_pw(os.environ.get('USER_1_PW')) 
    	cls.connectUser = cls.manager.select_one_user('email', 'admin@mail.org') 
    	if cls.manager.verify_if_token_exists(connectEmail): 
    		cls.permission = cls.manager.verify_token( 
    			connectEmail, 
    			cls.connectUser.department.name 
    		) 
    		assert cls.permission == 'GESTION' 

    @classmethod
    def test_2_getting_support_dept(cls): 
        """ Test getting support dept, if permission is 'GESTION'. 
            Expect one department's name is 'support'. 
    	""" 
        if cls.permission == 'GESTION': 
            suppDept_db = cls.manager.select_all_entities('depts') 
            assert len(suppDept_db) == 3 
            cls.last_dept_db = suppDept_db.pop() 
            assert cls.last_dept_db.name == 'support' 

    @classmethod
    def test_3_creation_support_user(cls): 
    	""" Test adding one support user, if permission is 'GESTION'. 
            Expect his name is the one that has been given to register. 
    	""" 
    	if cls.permission == 'GESTION': 
            # print('get password :', os.environ.get('U_3_PW'))  # bug vscode ? 
            suppDept_db = cls.manager.select_one_dept('name', 'support') 
            testUser = cls.manager.add_entity( 'user', { 
                'name': 'support_user 1', 
                'email': 'support_1@mail.org', 
                'entered_password': 'pass_user3', 
                'phone': '06 34 56 78 91', 
                'department_name': suppDept_db.name 
            }) 

            items_db = cls.manager.select_all_entities('users') 
            assert len(items_db) == 3 
            testSupport_db = items_db.pop() 
            print('DEBUG : ', testSupport_db) 
            assert testSupport_db.name == 'support_user 1' 

