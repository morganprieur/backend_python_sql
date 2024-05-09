
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
	def test_2_get_not_signed_sales_user_s_contracts(cls): 
	    """ Test getting the sales user's not signed contracts. 
	        Expect getting one contract 
	        and his id is equal to the last registered contract's id. 
		""" 
	    if cls.helpers.permission == 'COMMERCE': 
	    	user_db = cls.manager.select_one_user( 
	    		'email', 
	    		'sales_1@mail.org' 
	    	) 
	    	notSignedContracts_db = cls.manager.select_entities_with_criteria( 
	    		'contracts', 
	    		'not signed', 
	    		user_db.id 
	    	) 
	    	assert len(notSignedContracts_db) == 1 
	    	items_db = cls.manager.select_all_entities('contracts') 
	    	lastContract_db = items_db.pop() 
	    	assert notSignedContracts_db[0].id == lastContract_db.id 
	    	# assert 1 == 2 
	    else: 
	    	assert cls.helpers.permission != 'COMMERCE' 
	    	# assert 2 == 3 

