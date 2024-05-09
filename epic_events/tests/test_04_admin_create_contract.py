
from epic_events.manager import Manager 
from helpers_te_ts import ConnectTest 

import unittest 
import json 
import os 
from datetime import datetime 


class SuperuserTest(unittest.TestCase): 
	""" Config test files. 
	""" 
	@classmethod 
	def setUp(cls): 
		cls.manager = Manager() 
		cls.manager.connect() 
		cls.manager.create_session() 
		cls.helpers = ConnectTest('admin') 
		cls.helpers.connect_user() 


	@classmethod 
	def test_2_creation_contract(cls): 
	    """ Test adding one contract, if the admin user is connected. 
	        Expect one contract is registered into the DB, 
	        and its client name is 'testClient'.        
	    """ 
	    if cls.helpers.permission == 'GESTION': 
	        testContract = cls.manager.add_entity( 'contract', { 
	            "client_name": "client 1", 
	            "amount": 1000, 
	            "paid_amount": 350, 
	            "is_signed": 0 
	        }) 
	        items_db = cls.manager.select_all_entities('contracts') 
	        assert len(items_db) == 1 
	        last_contract_db = items_db.pop() 
	        assert last_contract_db.client.name == "client 1" 
	    else: 
	        assert not cls.helpers.permission 


