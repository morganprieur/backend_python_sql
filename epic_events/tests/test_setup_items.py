
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


	def test_created_depts(self): 
		""" Test departments created by the setup.py script.""" 
		dept_gestion_db = self.manager.select_one_dept('name', 'gestion') 
		dept_commerce_db = self.manager.select_one_dept('name', 'commerce') 
		dept_support_db = self.manager.select_one_dept('name', 'support') 
		assert dept_gestion_db.name == 'gestion' 
		assert dept_commerce_db.name == 'commerce' 
		assert dept_support_db.name == 'support' 
		items_db = self.manager.select_all_entities('depts') 
		assert len(items_db) == 4 


	def test_created_user(self): 
		""" Test user created by the setup.py script.""" 
		testUser_db = self.manager.select_one_user( 
			'email', 'admin@mail.org' 
		) 
		assert testUser_db.id == 1 
		assert testUser_db.name == 'super_admin' 
		assert testUser_db.department_id == 1 

	
	def decrypt_token(self, email, token): 
		# opens the key 
		# file deepcode ignore PT: local project 
		with open(os.environ.get('JWT_KEY_PATH'), 'rb') as keyfile:
			key = keyfile.read() 
			# print('key : ', key) 
		# uses the registered key
		cipher_suite = Fernet(key) 
		# with open(os.environ.get('TOKEN_PATH'), 'rb') as file: 
		with open('../users2.csv', 'rb') as file: 
			registered_bytes = file.read() 
			print("registered_bytes : ", registered_bytes) 
			# print(type(registered_bytes)) 
			plain_text = cipher_suite.decrypt(registered_bytes) 
			print("plain_text : ", plain_text) 
			# print(type(plain_text)) 
			# registered = ast.literal_eval(a.decode('utf-8'))
			registered = ast.literal_eval(plain_text.decode('utf-8'))
			# registered = json.loads(plain_text.decode('utf-8')) 
			print("registered : ", registered)  # dict 
			# print(type(registered)) 
			# déchiffrer les données de file 
			# plain_text = cipher_suite.decrypt(cipher_text) 
			# plain_text = cipher_suite.decrypt(registered).decode('utf-8') 
			# [x.decode("utf8") for x in data.split(b"\x00") if len(x)] 
			# plaint_text_list = [x.decode("utf8") for x in plain_text.split(b"\x00") if len(x)] 

			users = registered['users'] 
			for row in users: 
				print(row) 
				if email in row: 
					print('présent : ', row['email'], row['token']) 
					assert email == row['email'] 
				else: 
					print('non présent : ', row['email'], row['token']) 
					assert email not in row 
					assert token not in row 



	# def test_deletion_dept_and_user(self): 
	# 	""" Test deletiing one department and the user with relationship.""" 
	# 	testDept_db = self.manager.select_one_dept('name', 'testTable') 
	# 	testUser_db = self.manager.select_one_user( 
	# 		'email', 'test@mail.org') 
	# 	print(testUser_db) 

	# 	self.manager.delete_dept('name', 'testTable') 

	# 	all_depts = self.manager.select_all_depts() 
	# 	depts_names_list = [] 
	# 	for dept in all_depts: 
	# 		depts_names_list.append(dept) 
	# 	assert testDept_db.name not in depts_names_list 

	# 	all_users = self.manager.select_all_users() 
	# 	users_names_list = [] 
	# 	for user in all_users: 
	# 		users_names_list.append(user) 
	# 	assert testUser_db.name not in depts_names_list 

	# 	# self.manager.delete_user('name', 'user test') 


	# User gestion : 
	# userConnect = registered['users'][0] 
	# password = os.environ.get('USER_1_PW') 
	# User commerce : 
	# userConnect = registered['users'][1] 
	# password = os.environ.get('U_2_PW') 
