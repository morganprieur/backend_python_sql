
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
	def test_2_not_already_support_dept(cls): 
	    """ Test getting one dept with name 'support', if permission is 'GESTION'. 
	        Expect 2 deptartments registered into the DB 
	        and the none of them's name is 'support'. 
		""" 
	    if cls.helpers.permission == 'GESTION': 
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
	    if cls.helpers.permission == 'GESTION': 
	        suppDept = cls.manager.add_entity('dept', { 
	            'name': 'support' 
	        }) 
	        items_db = cls.manager.select_all_entities('depts') 
	        assert len(items_db) == 3 
	        last_dept = items_db.pop() 
	        assert last_dept.name == 'support' 
	        # assert 1 == 2 

