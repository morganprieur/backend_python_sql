
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
	def test_3_get_sales_user_s_clients(cls): 
	    """ Test getting the sales user's clients. 
	        Expect getting one client and his email is equal to 'client1@mail.com'. 
		""" 
	    all_clients = cls.manager.select_all_entities('clients') 
	    user_db = cls.manager.select_one_user( 
	        'email', 
	        'sales_1@mail.org' 
	    ) 
	    salesClients_db = cls.manager.select_entities_with_criteria( 
	        'clients', 
	        'sales contact', 
	        user_db.id 
	    ) 
	    assert len(salesClients_db) == 1 
	    assert salesClients_db[0].email == 'client1@mail.com' 

