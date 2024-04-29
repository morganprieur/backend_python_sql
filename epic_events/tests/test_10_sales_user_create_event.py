
from epic_events.manager import Manager 

import unittest 
import json 
import os 
from datetime import datetime, timedelta 



class SalesuserTest(unittest.TestCase): 
	""" Config test files. 
	""" 
	@classmethod
	def setUp(cls): 
		# # view = Views() 
		cls.manager = Manager() 
		cls.manager.connect() 
		cls.manager.create_session() 

	@classmethod
	def test_1_connect_sales_user(cls): 
		""" Test connect a sales user. 
			Expect permission is 'COMMERCE'. 
		""" 
		connectEmail = 'sales_1@mail.org' 
		# connectPass = os.environ.get('USER_2_PW') 
		# print('connectPass -10 test25 :', connectPass[:10]) 

		cls.connectUser = cls.manager.select_one_user( 
			'email', connectEmail) 
		if cls.manager.verify_if_token_exists(connectEmail): 
			cls.permission = cls.manager.verify_token( 
				connectEmail, 
				cls.connectUser.department.name 
			) 
			if cls.permission in ['GESTION', 'COMMERCE', 'SUPPORT']: 
				assert cls.permission == 'COMMERCE' 
			elif cls.permission == 'past': 
				pass_counter = 1 				
				# file deepcode ignore NoHardcodedPasswords/test: Local project 
				userEmail = 'sales_1@mail.org' 
				userPass = 'pass_user2' 
				if cls.manager.check_pw(userEmail, userPass): 
					user_db = cls.manager.select_one_user('email', userEmail) 
					assert user_db.department.name == 'commerce' 
					token = cls.manager.get_token(5, { 
						'email': userEmail, 
						'dept': user_db.department.name 
					}) 
					cls.manager.register_token(userEmail, 'token', token) 
					cls.permission = user_db.department.name.upper() 
					assert cls.permission == 'COMMERCE' 

	@classmethod
	def test_2_creation_event(cls): 
		""" Test adding one event, 
			if permission is 'COMMERCE' and if contract is signed. 
			Expect to get one contract, and its is_signed field is True. 
		""" 
		if cls.permission == 'COMMERCE': 
			contract_db = cls.manager.select_all_entities('contracts').pop() 
			assert contract_db.client.sales_contact_id == cls.connectUser.id 
			assert contract_db.is_signed is True 
			testEvent = cls.manager.add_entity( 'event', { 
				"name": "Anniversaire 15 ans d'Oren", 
				"contract_id": contract_db.id, 
				"start_datetime": "2024-04-27 10:00", 
				"end_datetime": "2024-04-27 19:00", 
				"location": "Pizzéria, rue Desnouettes, Paris 15", 
				"attendees": 30, 
				"notes": "Parking à 1 km : place Herbier. \nArrivées à partir de 11h30, départs doivent être terminés à 18h." 
			}) 

			items_db = cls.manager.select_all_entities('events') 
			assert len(items_db) == 1 
			last_event_db = items_db.pop() 
			assert last_event_db.name == "Anniversaire 15 ans d'Oren" 

