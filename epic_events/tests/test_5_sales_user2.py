
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

    
	def test_3_creation_event(self): 
		""" Test adding one event. 
		""" 
		# retrouver les contracts du client testClient 
        # créer un événement pour le dernier contrat 
		client_db = self.manager.select_one_client('name', 'testClient') 
		contract_db = self.manager.select_all_entities('contracts').pop() 
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


