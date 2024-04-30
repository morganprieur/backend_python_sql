
from epic_events.manager import Manager 
from helpers_te_ts import ConnectTest 

import unittest 
import json 
import os 
from datetime import datetime 


class SalesuserTest(unittest.TestCase): 
	""" Config test files. 
	""" 
	@classmethod 
	def setUp(cls): 
		cls.manager = Manager() 
		cls.manager.connect() 
		cls.manager.create_session() 
		cls.helpers = ConnectTest('sales') 
		cls.helpers.connect_user() 


	@classmethod 
	def test_2_creation_client(cls): 
			""" Test adding one client, if user connected. 
				Expect one client into the db, 
				and his name is 'testClient'. 
			""" 
			if cls.helpers.permission == 'COMMERCE': 
				# print(cls.helpers.permission) 
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

