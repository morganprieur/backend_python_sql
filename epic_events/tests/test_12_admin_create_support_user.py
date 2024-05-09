
from epic_events.manager import Manager 
from helpers_te_ts import ConnectTest 

import unittest 
import json 
import os 
from datetime import datetime 


class SuperuserTest(unittest.TestCase): 
	""" Config test files. 
	""" 
	@classmethod 
	def setUp(cls): 
		cls.manager = Manager() 
		cls.manager.connect() 
		cls.manager.create_session() 
		cls.helpers = ConnectTest('admin') 
		cls.helpers.connect_user() 


	@classmethod
	def test_2_getting_support_dept(cls): 
	    """ Test getting support dept, if permission is 'GESTION'. 
	        Expect one department's name is 'support'. 
		""" 
	    if cls.helpers.permission == 'GESTION': 
	        suppDept_db = cls.manager.select_all_entities('depts') 
	        assert len(suppDept_db) == 3 
	        cls.last_dept_db = suppDept_db.pop() 
	        assert cls.last_dept_db.name == 'support' 

	@classmethod
	def test_3_creation_support_user(cls): 
		""" Test adding one support user, if permission is 'GESTION'. 
	        Expect his name is the one that has been given to register. 
		""" 
		if cls.helpers.permission == 'GESTION': 
		    suppDept_db = cls.manager.select_one_dept('name', 'support') 
		    # testUser = cls.manager.add_entity( 'user', { 
		    #     'name': 'support_user 2', 
		    #     'email': 'support_2@mail.org', 
		    #     'entered_password': 'pass_user4', 
		    #     'phone': '06 34 56 79 81', 
		    #     'department_name': suppDept_db.name 
		    # }) 
		    testUser = cls.manager.add_entity( 'user', { 
		        'name': 'support_user 1', 
		        'email': 'support_1@mail.org', 
		        'entered_password': 'pass_user3', 
		        'phone': '06 34 56 78 91', 
		        'department_name': suppDept_db.name 
		    }) 

		    items_db = cls.manager.select_all_entities('users') 
		    # assert len(items_db) == 4 
		    assert len(items_db) == 3 
		    testSupport_db = items_db.pop() 
		    print('DEBUG : ', testSupport_db) 
		    # assert testSupport_db.name == 'support_user 2' 
		    assert testSupport_db.name == 'support_user 1' 

