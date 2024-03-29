
# import sys
# print(sys.path)

from pathlib import Path
import sys
path_root = Path(__file__).parents[1]
# path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
print(sys.path)
# # import src.c.d

from sqlalchemy import create_engine 
import psycopg2 
# from models import Base, Client, Contract, Department, Event, User   
from sqlalchemy.orm import sessionmaker 

from manager import Manager 
from models import Client, Contract, Department, Event, User 
# from epic_events.manager import Manager 
# from ..manager import Manager 
# from epic_events.models import Department, User 

import unittest 
import json 
import os 



class Sales_userTest(unittest.TestCase): 
	""" 
		Config test files. 
	""" 

	def setUp(self): 
		# # view = Views() 
		self.manager = Manager() 
		self.manager.connect() 
		self.manager.create_session() 


	def test_creation_dept(self): 
		""" Test adding one department.""" 
		testDept = self.manager.add_department(['testTable']) 
		testDept_db = self.manager.select_one_dept('name', 'testTable') 
		assert testDept.name == 'testTable' 
		items_db = self.manager.select_all_depts() 
		assert len(items_db) == 4 


	def test_creation_user(self): 
		""" Test adding one user.""" 
		testUser = self.manager.add_user([ 
			'user test', 
			'test@mail.org', 
			'test_password', 
            '01 23 45 67 89', 
			'testTable' 
		]) 
		testUser_db = self.manager.select_one_user( 
			'email', 'test@mail.org') 
		dept_id = testUser_db.department_id 

		testUser_update = self.manager.update_user( 
			testUser_db.id, 'department_id', 
			testUser_db.department_id, 1) 
		assert testUser_db.name == 'user test' 
		assert testUser_db.department_id == 1 

		testUser_update = self.manager.update_user( 
			testUser_db.id, 'department_id', 1, dept_id) 
		testUser_update_db = self.manager.select_one_user('email', 'test@mail.org') 
		assert testUser_update_db.name == 'user test' 
		assert testUser_update_db.department_id == dept_id 


	def test_deletion_dept_and_user(self): 
		""" Test deletiing one department and the user with relationship.""" 
		testDept_db = self.manager.select_one_dept('name', 'testTable') 
		testUser_db = self.manager.select_one_user( 
			'email', 'test@mail.org') 
		print(testUser_db) 

		self.manager.delete_dept('name', 'testTable') 

		all_depts = self.manager.select_all_depts() 
		depts_names_list = [] 
		for dept in all_depts: 
			depts_names_list.append(dept) 
		assert testDept_db.name not in depts_names_list 

		all_users = self.manager.select_all_users() 
		users_names_list = [] 
		for user in all_users: 
			users_names_list.append(user) 
		assert testUser_db.name not in depts_names_list 

		# self.manager.delete_user('name', 'user test') 


	# User gestion : 
	# userConnect = registered['users'][0] 
	# password = os.environ.get('USER_1_PW') 
	# User commerce : 
	# userConnect = registered['users'][1] 
	# password = os.environ.get('U_2_PW') 
