
# from epic_events.helpers import decorator_verify_jwt 
from epic_events.manager import Manager 

import unittest 
import json 
import os 
from datetime import datetime 



class SuperuserTest(unittest.TestCase): 
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
		connectPass = cls.manager.hash_pw(os.environ.get('USER_1_PW')) 
		cls.connectUser = cls.manager.select_one_user('email', 'admin@mail.org') 
		if cls.manager.verify_if_token_exists(connectEmail): 
			cls.permission = cls.manager.verify_token( 
				connectEmail, 
				cls.connectUser.department.name 
			) 
			assert cls.permission == 'GESTION' 
			# return cls.permission 
		else: 
		    assert not cls.permission 


	def test_2_creation_dept(cls): 
		""" Test adding one department if the admin is connected. 
			Expect one department created and its name is 'commerce'. 
		""" 
		print(dir(cls)) 
		print(datetime.now()) 
		if cls.permission == 'GESTION': 
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
		if cls.permission == 'GESTION': 
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

