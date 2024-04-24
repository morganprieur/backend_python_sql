
# from epic_events.helpers import decorator_verify_jwt 
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


	def test_1_creation_dept(self): 
		""" Test adding one department. 
		""" 
		print(datetime.now()) 
		testDept = self.manager.add_entity('dept', {'name': 'commerce'}) 
		print('DEBUG testDept : ', testDept) 
		assert testDept.name == 'commerce' 
		items_db = self.manager.select_all_entities('depts') 
		assert len(items_db) == 2 


	def test_2_creation_user(self): 
		""" Test adding one user. 
		""" 
		testUser = self.manager.add_entity( 'user', { 
			'name': 'sales_user 1', 
            'email': 'sales_1@mail.org', 
            'entered_password': os.environ.get('USER_2_PW'), 
            'phone': '06 23 45 67 89', 
            'department_name': 'commerce' 
		}) 

		testUser_db = self.manager.select_one_user('name', 'sales_user 1') 
		assert testUser_db.name == 'sales_user 1' 
		print('DEBUG : ', testUser_db) 
		items_db = self.manager.select_all_entities('users') 
		assert len(items_db) == 2 


	# def test_4_creation_contract(self): 
	# 	""" Test adding one contract. 
	# 	""" 
	# 	testContract = self.manager.add_entity( 'contract', { 
	# 		"client_name": "testClient", 
	# 		"amount": "1000", 
	# 		"paid_amount": "350", 
	# 		"is_signed": 1 
	# 	}) 
	# 	testContracts_db = self.manager.select_all_entities('contracts') 
	# 	last_contract_db = testContracts_db.pop() 
	# 	assert last_contract_db.id == testContract.id 
	# 	items_db = self.manager.select_all_entities('contracts') 
	# 	assert len(items_db) == 1 


	# def test_5_creation_event(self): 
	# 	""" Test adding one event. 
	# 	""" 
	# 	contract_id = self.manager.select_all_entities('contracts').pop().id 
	# 	testEvent = self.manager.add_entity( 'event', { 
	# 		"name": "Anniversaire 15 ans d'Oren", 
	# 		"contract_id": contract_id, 
	# 		"start_datetime": "2024-04-27 10:00", 
	# 		"end_datetime": "2024-04-27 19:00", 
	# 		"location": "Pizzéria, rue Desnouettes, Paris 15", 
	# 		"attendees": 30, 
	# 		"notes": "Parking à 1 km : place Herbier. \nArrivées à partir de 11h30, départs doivent être terminés à 18h." 
	# 	}) 
	# 	last_event_db = self.manager.select_all_entities('events').pop() 
	# 	assert testEvent.id == last_event_db.id 
	# 	items_db = self.manager.select_all_entities('events') 
	# 	assert len(items_db) == 1 


	# def test_6_deletion_dept_and_user(self): 
	# 	""" Test deletiing one user.""" 
	# 	testDept_db = self.manager.select_one_dept('name', 'testDept') 
	# 	testUser_db = self.manager.select_one_user( 
	# 		'email', 'test_user_2@email.org') 
	# 	print('DEBUG testUser_db : ', testUser_db) 

	# 	self.manager.delete_dept('name', 'testDept') 

	# 	all_depts = self.manager.select_all_entities('depts') 
	# 	depts_names_list = [] 
	# 	for dept in all_depts: 
	# 		depts_names_list.append(dept) 
	# 	assert testDept_db.name not in depts_names_list 

	# 	all_clients = self.manager.select_all_entities('clients') 
	# 	assert all_clients == [] 

	# 	all_events = self.manager.select_all_entities('events') 
	# 	assert all_events == [] 


