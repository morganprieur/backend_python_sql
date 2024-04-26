
from epic_events.manager import Manager 

import unittest 
import json 
import os 
from datetime import datetime 



class SalesuserTest(unittest.TestCase): 
	""" Config test files. 
	""" 

	def setUp(self): 
		# # view = Views() 
		self.manager = Manager() 
		self.manager.connect() 
		self.manager.create_session() 


	def test_1_connect_sales_user(self): 
		""" Test connect a sales user. 
			Expect permission is 'COMMERCE'. 
		""" 
		connectEmail = 'sales_1@mail.org' 
		# connectPass = os.environ.get('USER_2_PW') 
		# print('connectPass -10 test25 :', connectPass[:10]) 

		self.connectUser = self.manager.select_one_user( 
			'email', connectEmail) 
		if self.manager.verify_if_token_exists(connectEmail): 
			permission = self.manager.verify_token( 
				connectEmail, 
				self.connectUser.department.name 
			) 
			assert self.permission == 'COMMERCE' 
		else: 
			assert not self.permission 


	def test_1_get_client(self): 
		""" Test getting one client, 
            if permission is 'COMMERCE' 
            and if client's contact is the connected user. 
			Expect to get one client, and its sales_contact_id is self.connectUser.id. 
		""" 
		if self.permission == 'COMMERCE': 
			self.client_db = self.manager.select_entities_with_criteria('clients', 'sales clients', self.connectUser.id) 
			assert self.client_db.user.name == self.connectUser.name 
			assert len(self.client_db) == 1 
		else: 
			assert not self.permission 


	def test_2_update_client(self): 
		""" Test updating one client, 
            if permission is 'COMMERCE'. 
			Expect the new value of corporation_name is 'Enterprise 1'. 
		""" 
		if self.permission == 'COMMERCE': 
		    edited_client = self.manager.update_client( 
                self.client_db, 
                'corporation_name', 
                'Enterprise 1' 
            )
		    client_db = self.manager.select_one_client('name', 'client 1') 
		    assert client_db.attendees == 40 
		else: 
			assert not self.permission 

