
# from pathlib import Path
# import sys
# # print(sys.path) 
# path_root = Path(__file__).parents[1]
# # path_root = Path(__file__).parents[2]
# sys.path.append(str(path_root))
# print(sys.path)
# # # import src.c.d

from epic_events.helpers import decorator_verify_jwt 
from epic_events.manager import Manager 

import unittest 
import json 
import os 
from datetime import datetime 



class SuperuserTest(unittest.TestCase): 
	""" Config test files. 
	""" 
	def setUp(self): 
		# # view = Views() 
		self.manager = Manager() 
		self.manager.connect() 
		self.manager.create_session() 


	# def test_connexion_superuser(self): 
	# 	""" Tests connexion, verify password and token 
	# 	""" 
	# 	print('test_connex') 
	# 	# file deepcode ignore PT: local project 
	# 	with open(f"../epic_events/{os.environ.get('FILE_PATH')}", 'r') as jsonfile: 
	# 		self.registered = json.load(jsonfile) 
	# 		# print('self.registered test_superuser L36 : ', self.registered) 
	# 		print('self.registered["users"] test_superuser L37 : ', self.registered['users']) 
	# 		userConnect = self.registered['users'][0] 

	# 		# # Verify password 
	# 		# userConnect['password'] = os.environ.get('USER_1_PW') 
	# 		# checked = self.manager.check_pw( 
	# 		# 	userConnect['email'], 
	# 		# 	userConnect['password'] 
	# 		# ) 
	# 		# user_db = self.manager.select_one_user('name', 'super_admin') 
	# 		# assert checked == user_db.password 

			# if not checked: 
			# 	# TODO: retour formulaire + compteur (3 fois max) 
			# 	print('Les informations saisies ne sont pas bonnes, merci de réessayer.') 
			# else: 
			# 	logged_user = self.manager.select_one_user( 
			# 		'email', userConnect['email']) 

			# 	# Verify JWT 
			# 	# Check token pour utilisateur connecté + département 
			# 	self.user_session = self.manager.verify_token( 
			# 		logged_user.email, 
			# 		logged_user.password, 
			# 		logged_user.department.name 
			# 	) 
			# 	print('self.user_session CL65 : ', self.user_session) 
			# 	# # TODO: sortie propre après l'échec du token 
			# 	if self.user_session == 'past': 
			# 		print('self.user_session CL68 : ', self.user_session) 
			# 		print(logged_user.token) 
			# 		delta = 8*3600 
			# 		new_token = self.manager.get_token(delta, { 
			# 			'email': logged_user.email, 
			# 			'pass': logged_user.password, 
			# 			'dept': logged_user.department.name 
			# 		}) 
			# 		updated_logged_user = self.manager.update_user(logged_user.id, 'token', new_token) 
			# 		updated_user_db = self.manager.select_one_user('email', logged_user.email) 
			# 		print(updated_user_db.token) 
			# 		if logged_user.departments.name == 'gestion': 
			# 			self.user_session = 'GESTION' 
			# 		if logged_user.departments.name == 'commerce': 
			# 			self.user_session = 'COMMERCE' 
			# 		if logged_user.departments.name == 'support': 
			# 			self.user_session = 'SUPPORT' 
			# 		print(self.user_session) 
			# 	else: 
			# 		print(self.user_session) 


	# # @decorator_verify_jwt  # : essayer 
	def test_1_creation_dept(self): 
		""" Test adding one department. 
		""" 
		print(datetime.now()) 
		testDept = self.manager.add_entity('dept', {'name': 'testDept'}) 
		print('testDept : ', testDept) 
		# testDept_db = self.manager.select_one_dept('name', 'testTable') 
		assert testDept.name == 'testDept' 
		items_db = self.manager.select_all_entities('depts') 
		# items_db = self.manager.select_all_depts() 
		assert len(items_db) == 2 


	def test_2_creation_user(self): 
		""" Test adding one user. 
		""" 
		# Hash pass 
		hashed_password = self.manager.hash_pw('pw_testUser') 

		testUser = self.manager.add_entity( 'user', { 
			'name': 'testUser', 
            'email': 'test_user_2@email.org', 
            'password': hashed_password, 
            'phone': '06 08 97 65 43', 
            'department_name': 'gestion' 
            # 'token': user_token 
		}) 

		# # Get token JWT 
		# delta = 2*3600  # <-- for 'exp' JWT claim, en secondes 
		# data = { 
		#     'email': 'test_user_2@email.org', 
		#     'pass': hashed_password, 
		#     'dept': 'gestion', 
		# } 
		# user_token = self.manager.get_token(delta, data) 

		testUser_db = self.manager.select_one_user('name', 'testUser') 
		assert testUser_db.name == 'testUser' 
		print(testUser_db) 
		items_db = self.manager.select_all_entities('users') 
		assert len(items_db) == 2 


	def test_3_creation_client(self): 
		""" Test adding one client. 
		""" 
		testClient = self.manager.add_entity( 'client', { 
			'name': 'testClient', 
            'email': 'test_client@email.com', 
            'phone': '06 13 45 67 89', 
            'corporation_name': 'Entreprise 2', 
            'sales_contact_name': 'testUser' 
		}) 
		testClient_db = self.manager.select_one_client('name', 'testClient') 
		assert testClient_db.name == 'testClient' 
		items_db = self.manager.select_all_entities('clients') 
		assert len(items_db) == 1 


	def test_4_creation_contract(self): 
		""" Test adding one contract. 
		""" 
		testContract = self.manager.add_entity( 'contract', { 
			"client_name": "testClient", 
			"amount": "1000", 
			"paid_amount": "350", 
			"is_signed": 1 
		}) 
		testContracts_db = self.manager.select_all_entities('contracts') 
		last_contract_db = testContracts_db.pop() 
		assert last_contract_db.id == testContract.id 
		items_db = self.manager.select_all_entities('contracts') 
		assert len(items_db) == 1 


	def test_5_creation_event(self): 
		""" Test adding one event. 
		""" 
		testEvent = self.manager.add_entity( 'event', { 
			"name": "Anniversaire 15 ans d'Oren", 
			"start_datetime": "2024-04-27 10:00", 
			"end_datetime": "2024-04-27 19:00", 
			"location": "Pizzéria, rue Desnouettes, Paris 15", 
			"attendees": 30, 
			"notes": "Parking à 1 km : place Herbier. \nArrivées à partir de 11h30, départs doivent être terminés à 18h." 
		}) 
		last_event_db = self.manager.select_all_entities('events').pop() 
		assert testEvent.id == last_event_db.id 
		items_db = self.manager.select_all_entities('events') 
		assert len(items_db) == 1 


	def test_6_deletion_dept_and_user(self): 
		""" Test deletiing one user.""" 
		testDept_db = self.manager.select_one_dept('name', 'testDept') 
		testUser_db = self.manager.select_one_user( 
			'email', 'test_user_2@email.org') 
		print('testUser_db : ', testUser_db) 

		self.manager.delete_dept('name', 'testDept') 

		all_depts = self.manager.select_all_entities('depts') 
		depts_names_list = [] 
		for dept in all_depts: 
			depts_names_list.append(dept) 
		assert testDept_db.name not in depts_names_list 

		# all_users = self.manager.select_all_entities('users') 
		# users_names_list = [] 
		# for user in all_users: 
		# 	users_names_list.append(user) 
		# assert testUser_db.name not in depts_names_list 

		all_clients = self.manager.select_all_entities('clients') 
		assert all_clients == [] 
		assert all_clients is None 

	# 	# self.manager.delete_user('name', 'user test') 


