
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

    
	def test_1_creation_event(self): 
		""" Test adding one event, 
			if permission is 'COMMERCE' and if contract is signed. 
			Expect to get one contract, and its is_signed field is True. 
		""" 
		if self.permission == 'COMMERCE': 
			contract_db = self.manager.select_all_entities('contracts').pop() 
			assert contract_db.client.sales_contact_id == self.connectUser.id 
			assert contract_db.is_signed is None 
			testEvent = self.manager.add_entity( 'event', { 
				"name": "Anniversaire 15 ans d'Oren", 
				"contract_id": contract_db.id, 
				"start_datetime": "2024-04-27 10:00", 
				"end_datetime": "2024-04-27 19:00", 
				"location": "Pizzéria, rue Desnouettes, Paris 15", 
				"attendees": 30, 
				"notes": "Parking à 1 km : place Herbier. \nArrivées à partir de 11h30, départs doivent être terminés à 18h." 
			}) 

			items_db = self.manager.select_all_entities('events') 
			assert len(items_db) == 1 
			last_event_db = items_db.pop() 
			assert last_event_db.name == "Anniversaire 15 ans d'Oren" 

