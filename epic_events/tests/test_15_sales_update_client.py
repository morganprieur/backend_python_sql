
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
	def test_2_get_client(cls): 
		""" Test getting one client, 
            if permission is 'COMMERCE' 
            and if client's contact is the connected user. 
			Expect to get one client, and its sales_contact_id is cls.connectUser.id. 
		""" 
		if cls.permission == 'COMMERCE': 
			salesUser_db = cls.manager.select_one_user('email', 'sales_1@mail.org') 
			clients_db = cls.manager.select_entities_with_criteria( 
				'clients', 
				'sales contact', 
				salesUser_db.id 
			) 
			assert len(clients_db) == 1 
			lastClient_db = clients_db.pop() 
			assert lastClient_db.user.name == salesUser_db.name 
		else: 
			assert not cls.permission 

	@classmethod
	def test_3_update_client(cls): 
		""" Test updating one client, 
            if permission is 'COMMERCE'. 
			Expect the new value of corporation_name is 'Enterprise 1'. 
		""" 
		if cls.permission == 'COMMERCE': 
			salesUser_db = cls.manager.select_one_user('email', 'sales_1@mail.org') 
			client_db = cls.manager.select_one_client('name', 'client 1') 
			edited_client = cls.manager.update_client( 
                client_db, 
                'corporation_name', 
                'Enterprise 1' 
            )
			client_db = cls.manager.select_one_client('name', 'client 1') 
			assert client_db.corporation_name == 'Enterprise 1' 
		else: 
			assert not cls.permission 

