
# from pathlib import Path
# import sys
# print(sys.path)
# path_root = Path(__file__).parents[1]
# # path_root = Path(__file__).parents[2]
# sys.path.append(str(path_root))
# print(sys.path)
# # # import src.c.d

from sqlalchemy import create_engine 
import psycopg2 
from sqlalchemy.orm import sessionmaker 

from manager import Manager 
from models import Client, Contract, Department, Event, User 

from cryptography.fernet import Fernet 
import unittest 
import json 
import os 



class SetupTest(unittest.TestCase): 
	""" 
		Config test files. 
	""" 

	def setUp(self): 
		# # view = Views() 
		self.manager = Manager() 
		self.manager.connect() 
		self.manager.create_session() 


	def test_1_created_depts(self): 
		""" Test departments created by the setup.py script.""" 
		dept_gestion_db = self.manager.select_one_dept('name', 'gestion') 
		assert dept_gestion_db.name == 'gestion' 
		items_db = self.manager.select_all_entities('depts') 
		assert len(items_db) == 1 

	def test_2_created_user(self): 
		""" Test user created by the setup.py script.""" 
		testUser_db = self.manager.select_one_user( 
			'email', 'admin@mail.org' 
		) 
		assert testUser_db.id == 1 
		assert testUser_db.name == 'super_admin' 
		assert testUser_db.department_id == 1 


	# def test_3_decrypt_token(self): 
	# 	decrypted = self.manager.decrypt_token() 
	# 	assert type(decrypted) == dict 
	# 	assert type(decrypted['users']) == list 
	# 	assert decrypted['users'][0]['email'] == 'admin@mail.org' 
	# 	# assert decrypted is True 


	def test_4_verify_token(self): 
		registered = self.manager.decrypt_token() 

		connectEmail = 'admin@mail.org' 
		connectPass = self.manager.hash_pw(os.environ.get('USER_1_PW')) 
		connectDept = self.manager.select_one_user('email', 'admin@mail.org').department.name 
		self.manager.verify_token(connectEmail, connectPass, connectDept) 



		# users = registered['users'] 
		# for row in users: 
		# 	print('row test_setup72 : ', row) 
		# 	if connectEmail in row: 
		# 		print('présent : ', row['email'], row['token']) 
		# 		assert connectEmail == row['email'] 
		# 	else: 
		# 		print('non présent : ', row['email'], row['token']) 
		# 		assert connectEmail not in row 


