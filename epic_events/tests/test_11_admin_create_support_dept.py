
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

    @classmethod
    def test_2_not_already_support_dept(cls): 
        """ Test getting one dept with name 'support', if permission is 'GESTION'. 
            Expect 2 deptartments registered into the DB 
            and the none of them's name is 'support'. 
    	""" 
        if cls.permission == 'GESTION': 
            depts_db = cls.manager.select_all_entities('depts') 
            assert len(depts_db) == 2 
            depts_names_list = [] 
            for dept in depts_db: 
                depts_names_list.append(dept.name) 
            assert 'support' not in depts_names_list 

    @classmethod
    def test_3_creation_support_dept(cls): 
        """ Test adding one dept, if permission is 'GESTION'. 
            Expect 3 deptartments registered into the DB 
            and the last's name is 'support'. 
    	""" 
        if cls.permission == 'GESTION': 
            suppDept = cls.manager.add_entity('dept', { 
                'name': 'support' 
            }) 
            items_db = cls.manager.select_all_entities('depts') 
            assert len(items_db) == 3 
            last_dept = items_db.pop() 
            assert last_dept.name == 'support' 

