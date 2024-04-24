
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


    def test_01_creation_support_dept(self): 
        """ Test adding one dept. 
    	""" 
        supp_dept = self.manager.add_entity('dept', { 
            'name': 'support' 
        }) 
        items_db = self.manager.select_all_entities('depts') 
        assert len(items_db) == 3 
        last_dept = items_db.pop() 
        assert last_dept.name == 'support' 


    def test_02_creation_support_user(self): 
    	""" Test adding one user. 
    	""" 
    	print('get password :', os.environ.get('U_3_PW')) 
    	testUser = self.manager.add_entity( 'user', { 
    		'name': 'support_user 1', 
            'email': 'support_1@mail.org', 
            'entered_password': 'pass_user3', 
            'phone': '06 34 56 78 91', 
            'department_name': 'support' 
    	}) 

    	items_db = self.manager.select_all_entities('users') 
    	assert len(items_db) == 3 
    	testSupport_db = items_db.pop() 
    	print('DEBUG : ', testSupport_db) 
    	assert testSupport_db.name == 'support_user 1' 


    def test_03_set_support_to_event(self): 
    	""" Test setting a support contact to one event. 
    	""" 
    	support_db = self.manager.select_one_user('name', 'support_user 1') 
    	events_db = self.manager.select_all_entities('events') 
    	event_to_modify = events_db.pop() 
    	edited_event = self.manager.update_event( 
            event_to_modify, 
            'support_contact_name', 
            'support_user 1' 
        ) 

    	items_db = self.manager.select_all_entities('events') 
    	assert len(items_db) == 1 
    	last_event_db = items_db.pop() 
    	assert last_event_db.support_contact_id != 'NULL' 


	# def test_6_deletion_dept_and_user(self): 
	# 	""" Test deletiing one user.""" 
	# 	testDept_db = self.manager.select_one_dept('name', 'testDept') 
	# 	testUser_db = self.manager.select_one_user( 
	# 		'email', 'test_user_2@email.org') 
	# 	print('DEBUG testUser_db : ', testUser_db) 

	# 	self.manager.delete_dept('name', 'testDept') 

	# 	all_depts = self.manager.select_all_entities('depts') 
	# 	depts_names_list = [] 
	# 	for dept in all_depts: 
	# 		depts_names_list.append(dept) 
	# 	assert testDept_db.name not in depts_names_list 

	# 	all_clients = self.manager.select_all_entities('clients') 
	# 	assert all_clients == [] 

	# 	all_events = self.manager.select_all_entities('events') 
	# 	assert all_events == [] 


