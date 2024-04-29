
from epic_events.manager import Manager 

import unittest 
import json 
import os 
from datetime import datetime 



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
	def test_2_creation_client(cls): 
			""" Test adding one client, if user connected. 
				Expect one client into the db, 
				and his name is 'testClient'. 
			""" 
			if cls.permission == 'COMMERCE': 
				testClient = cls.manager.add_entity( 'client', { 
					'name': 'client 1', 
					'email': 'client1@mail.com', 
					'phone': '06 13 45 67 89', 
					'corporation_name': 'Entreprise 2', 
					'sales_contact_name': 'sales_user 1' 
				}) 
				testClient_db = cls.manager.select_one_client( 
					'name', 'client 1') 
				assert testClient_db.email == 'client1@mail.com' 
				items_db = cls.manager.select_all_entities('clients') 
				assert len(items_db) == 1 
			else: 
				assert not cls.permission 

