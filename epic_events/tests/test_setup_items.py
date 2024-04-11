
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


	# def test_created_depts(self): 
	# 	""" Test departments created by the setup.py script.""" 
	# 	dept_gestion_db = self.manager.select_one_dept('name', 'gestion') 
	# 	dept_commerce_db = self.manager.select_one_dept('name', 'commerce') 
	# 	dept_support_db = self.manager.select_one_dept('name', 'support') 
	# 	assert dept_gestion_db.name == 'gestion' 
	# 	assert dept_commerce_db.name == 'commerce' 
	# 	assert dept_support_db.name == 'support' 
	# 	items_db = self.manager.select_all_depts() 
	# 	assert len(items_db) == 3 


	# def test_created_user(self): 
	# 	""" Test user created by the setup.py script.""" 
	# 	testUser_db = self.manager.select_one_user( 
	# 		'email', 'admin@mail.org' 
	# 	) 
	# 	assert testUser_db.id == 1 
	# 	assert testUser_db.name == 'super_admin' 
	# 	assert testUser_db.department_id == 1 


	def test_encrypted_token(self): 
		with open(os.environ.get('JWT_KEY_PATH'), 'rb') as keyfile:
			key = keyfile.read() 
			print('key : ', key) 
		# uses the registered key
		cipher_suite = Fernet(key) 
		# file deepcode ignore PT/test: local project 
		with open(os.environ.get('TOKEN_PATH'), 'rb') as file: 
			registered = file.read() 
			print(registered) 
			print(type(registered))  # csv.reader 
		# déchiffrer les données de file 
		# plain_text = cipher_suite.decrypt(cipher_text) 
		plain_text = cipher_suite.decrypt(registered).decode('utf-8') 
		# plain_text = list(plain_text) 
		print('plain_text : ', plain_text) 
		print('type(plain_text) : ', type(plain_text)) 

		plain_text_split = plain_text.split('\n') 
		for row in plain_text_split: 
			print(row) 
			row_split = row.split(',') 
			for i in range(len(row_split)): 
				if i == 2: 
					print(row_split[10:]) 
					# assert row_split[1] == 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQG1haWwub3JnIiwicGFzcyI6Imhhc2gucGFzcy53b3JkIiwiZGVwdCI6Imdlc3Rpb24iLCJleHAiOjE3MTI3NzczNTR9.baKJaIzWocCWjtJxFAID5VTdHCs3F0WzFbjaGJHaeFg' 
					assert part[10:] == 'bjaGJHaeFg' 

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
