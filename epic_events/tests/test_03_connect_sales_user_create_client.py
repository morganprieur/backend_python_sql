
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
			assert cls.permission == 'COMMERCE' 
		else: 
			assert not cls.permission 


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

