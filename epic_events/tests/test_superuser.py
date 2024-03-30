
# from pathlib import Path
# import sys
# # print(sys.path) 
# path_root = Path(__file__).parents[1]
# # path_root = Path(__file__).parents[2]
# sys.path.append(str(path_root))
# print(sys.path)
# # # import src.c.d

from epic_events.manager import Manager 

import unittest 
import json 
import os 



class SuperuserTest(unittest.TestCase): 
	""" Config test files. 
	""" 
	def setUp(self): 
		# # view = Views() 
		self.manager = Manager() 
		self.manager.connect() 
		self.manager.create_session() 


	def test_connexion_superuser(self): 
		""" Tests connexion, verify password and token 
		""" 
		print('test_connex') 
		# file deepcode ignore PT: local project 
		with open(f"../epic_events/{os.environ.get('FILE_PATH')}", 'r') as jsonfile: 
			self.registered = json.load(jsonfile) 
			# print('self.registered test_superuser L36 : ', self.registered) 
			print('self.registered["users"] test_superuser L37 : ', self.registered['users']) 
			userConnect = self.registered['users'][0] 

			# # Verify password 
			# userConnect['password'] = os.environ.get('USER_1_PW') 
			# checked = self.manager.check_pw( 
			# 	userConnect['email'], 
			# 	userConnect['password'] 
			# ) 
			# user_db = self.manager.select_one_user('name', 'super_admin') 
			# assert checked == user_db.password 




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


	def test_creation_dept(self): 
		""" Test adding one department. 
		""" 
		testDept = self.manager.add_entity('dept', {'name': 'testDept'}) 
		# testDept_db = self.manager.select_one_dept('name', 'testTable') 
		assert testDept.name == 'testDept' 
		items_db = self.manager.select_all_depts() 
		assert len(items_db) == 4 

		self.manager.delete_dept('name', 'testDept') 


	# Essai select generique manager L657 : 
	def test_select_entity(self): 
		""" Test adding one client and select it with select_one_entity. 
		""" 
		testUser = self.manager.select_one_entity('user', 'name', 'sales_user 1') 
		assert testUser.id == 2 
		testclient = self.manager.add_client({ 
			'name': "testClient", 
			'email': "client1@mail.com", 
			'phone': "06 09 87 65 43", 
			'corporation_name': "Entreprise 1", 
			'sales_contact_name': "sales_user 1" 
		}) 
		all_clients = self.manager.select_all_clients() 
		last_client = all_clients.pop() 
		testclient_db = self.manager.select_one_entity('client', 'name', 'testClient') 
		assert testclient_db.id == last_client.id 
		items_db = self.manager.select_all_clients() 
		assert len(items_db) == 1 

		self.manager.delete_client('id', last_client.id) 



	


	# 	def test_update_user(self): 
	# 		testUser = self.manager.add_user([ 
	# 			'user test', 
	# 			'test@mail.org', 
	# 			'test_password', 
	# 			'01 23 45 67 89', 
	# 			'testTable' 
	# 		]) 
	# 		testUser_db = self.manager.select_one_user('email', 'test@mail.org') 
	# 		assert testUser_db.id == 2 
	# 		assert testUser_db.name == 'user test' 
	# 		assert testUser_db.department_id == 2 
	# 		commerceDept = testUser_db.department_id 

	# 		# Change user test's department: 
	# 		gestionDept = self.manager.select_one_dept('name', 'gestion') 
	# 		testUser_update = self.manager.update_user( 
	# 			testUser_db.id, 
	# 			'department_id', 
	# 			gestionDept 
	# 		) 
	# 		assert testUser_db.department_id == 1 

	# 		# Reset user test's original department: 
	# 		testUser_update = self.manager.update_user( 
	# 			testUser_db.id, 
	# 			'department_id', 
	# 			commerceDept 
	# 		) 
	# 		testUser_update_db = self.manager.select_one_user('email', 'test@mail.org') 
	# 		assert testUser_update_db.name == 'user test' 
	# 		assert testUser_update_db.department_id == commerceDept 





	# def test_creation_user(self): 
	# 	""" Test adding one user.""" 
	# 	testUser = self.manager.add_user([ 
	# 		'user test', 
	# 		'test@mail.org', 
	# 		'test_password', 
    #         '01 23 45 67 89', 
	# 		'testTable' 
	# 	]) 
	# 	testUser_db = self.manager.select_one_user( 
	# 		'email', 'test@mail.org') 
	# 	dept_id = testUser_db.department_id 

	# 	testUser_update = self.manager.update_user( 
	# 		testUser_db.id, 'department_id', 
	# 		testUser_db.department_id, 1) 
	# 	assert testUser_db.name == 'user test' 
	# 	assert testUser_db.department_id == 1 

	# 	testUser_update = self.manager.update_user( 
	# 		testUser_db.id, 'department_id', 1, dept_id) 
	# 	testUser_update_db = self.manager.select_one_user('email', 'test@mail.org') 
	# 	assert testUser_update_db.name == 'user test' 
	# 	assert testUser_update_db.department_id == dept_id 


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



