
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
	def test_2_creation_dept(cls): 
		""" Test adding one department if the admin is connected. 
			Expect one department created and its name is 'commerce'. 
		""" 
		# print(datetime.now()) 
		if cls.helpers.permission == 'GESTION': 
			assert cls.helpers.permission == 'GESTION' 
			testDept = cls.manager.add_entity( 
				'dept', { 
					'name': 'commerce' 
				} 
			) 
			print('DEBUG testDept : ', testDept) 
			assert testDept.name == 'commerce' 
			items_db = cls.manager.select_all_entities('depts') 
			assert len(items_db) == 2 
		else: 
			assert not cls.permission 


	@classmethod 
	def test_3_creation_user(cls): 
		""" Test adding one user if the admin is connected. 
			Expect 2 users into the DB and its name is 'sales_user 1'. 
		""" 
		if cls.helpers.permission == 'GESTION': 
			testUser = cls.manager.add_entity( 'user', { 
				'name': 'sales_user 1', 
				'email': 'sales_1@mail.org', 
				'entered_password': os.environ.get('USER_2_PW'), 
				'phone': '06 23 45 67 89', 
				'department_name': 'commerce' 
			}) 

			testUser_db = cls.manager.select_one_user('name', 'sales_user 1') 
			assert testUser_db.name == 'sales_user 1' 
			print('DEBUG : ', testUser_db) 
			items_db = cls.manager.select_all_entities('users') 
			assert len(items_db) == 2 
		else: 
			assert not cls.permission 

