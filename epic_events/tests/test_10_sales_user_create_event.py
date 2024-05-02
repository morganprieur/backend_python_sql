
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
	def test_2_creation_event(cls): 
		""" Test adding one event, 
			if permission is 'COMMERCE' and if contract is signed. 
			Expect to get one contract, and its is_signed field is True. 
		""" 
		if cls.helpers.permission == 'COMMERCE': 
			contract_db = cls.manager.select_all_entities('contracts').pop() 
			assert contract_db.client.sales_contact_id == cls.helpers.connectUser.id 
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
			# assert 1 == 2 

