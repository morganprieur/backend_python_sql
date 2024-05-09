
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
	def test_2_get_client(cls): 
		""" Test getting one client, 
            if permission is 'COMMERCE' 
            and if client's contact is the connected user. 
			Expect to get one client, and its sales_contact_id is cls.connectUser.id. 
		""" 
		if cls.helpers.permission == 'COMMERCE': 
			# salesUser_db = cls.manager.select_one_user('email', 'sales_1@mail.org') 
			clients_db = cls.manager.select_entities_with_criteria( 
				'clients', 
				'sales contact', 
				cls.helpers.connectUser.id 
			) 
			assert len(clients_db) == 1 
			lastClient_db = clients_db.pop() 
			assert lastClient_db.user.name == cls.helpers.connectUser.name 
		else: 
			assert not cls.permission 

	@classmethod
	def test_3_update_client(cls): 
		""" Test updating one client, 
            if permission is 'COMMERCE'. 
			Expect the new value of corporation_name is 'Enterprise 1'. 
		""" 
		if cls.helpers.permission == 'COMMERCE': 
			# salesUser_db = cls.manager.select_one_user('email', 'sales_1@mail.org') 
			print('cls.helpers.connectUser.name :', cls.helpers.connectUser.name) 
			clients_db = cls.manager.select_entities_with_criteria( 
				'clients', 
				'sales contact', 
				cls.helpers.connectUser.id 
			) 
			client_db = clients_db.pop() 
			edited_client = cls.manager.update_client( 
                client_db, 
                'corporation_name', 
                'Enterprise 1' 
            ) 
			client_db = cls.manager.select_one_client( 
				'name', 
				'client 1' 
			) 
			assert client_db.corporation_name == 'Enterprise 1' 
		else: 
			assert not cls.permission 

