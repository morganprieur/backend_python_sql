
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
	def test_2_get_last_contract_not_signed(cls): 
	    """ Test last contract is not signed, if the connected user is admin. 
	        Expect is_signed is none. 
	    """ 
	    if (cls.helpers.permission == 'GESTION') | (cls.helpers.permission == 'COMMERCE'): 
	        contracts_db = cls.manager.select_all_entities('contracts') 
	        cls.lastContract_db = contracts_db.pop() 
	        assert cls.lastContract_db.client.name == 'client 1' 
	        assert cls.lastContract_db.amount == 1000 
	        assert cls.lastContract_db.paid_amount == 350 
	        assert cls.lastContract_db.is_signed == False 
	        # assert 1 == 2 
	    else: 
	        assert cls.permission == 'SUPPORT' 
	        assert 2 == 3 

	@classmethod
	def test_3_set_signed_contract(cls): 
	    """ Test set last contract's is_signed field to True, 
	        if the connected user is admin or sales user. 
	        Expect is_signed is True. 
	    """ 
	    if (cls.helpers.permission == 'COMMERCE') | (cls.helpers.permission == 'GESTION'): 
	        edited_contract = cls.manager.update_contract( 
	            cls.lastContract_db, 
	            'is_signed', 
	            # False 
	            True 
	        ) 
	        items_db = cls.manager.select_all_entities('contracts') 
	        assert len(items_db) == 1 
	        last_db = items_db.pop() 
	        assert last_db.client.name == "client 1" 

	@classmethod
	def test_4_contract_signed(cls): 
	    """ Test last contract's is_signed field is False, 
	        if the connected user is admin or sales user. 
	        Expect is_signed is True. 
	    """ 
	    if (cls.helpers.permission == 'COMMERCE') | (cls.helpers.permission == 'GESTION'): 
	        items_db = cls.manager.select_all_entities('contracts') 
	        assert len(items_db) == 1 
	        last_db = items_db.pop()  
	        assert last_db.is_signed == True 

