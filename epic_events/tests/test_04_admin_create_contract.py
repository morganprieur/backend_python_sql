
# from epic_events.helpers import decorator_verify_jwt 
from epic_events.manager import Manager 

import unittest 
import json 
import os 
from datetime import datetime 



class Superuser2Test(unittest.TestCase): 
    """ Config test files. 
    """ 
    def setUp(self): 
        # # view = Views() 
        self.manager = Manager() 
        self.manager.connect() 
        self.manager.create_session() 



    def test_1_verify_admin_token(self): 
    	""" Test the admin user's token. 
    		Expect his permission dept == 'GESTION'. 
    	""" 
    	registered = self.manager.decrypt_token() 

    	connectEmail = 'admin@mail.org' 
    	connectPass = self.manager.hash_pw(os.environ.get('USER_1_PW')) 
    	self.connectUser = self.manager.select_one_user('email', 'admin@mail.org') 
    	if self.manager.verify_if_token_exists(connectEmail): 
    		self.permission = self.manager.verify_token( 
    			connectEmail, 
    			self.connectUser.department.name 
    		) 
    		assert self.permission == 'GESTION' 
    	else: 
    	    assert not self.permission 


    def test_2_creation_contract(self): 
        """ Test adding one contract, if the admin user is connected. 
            Expect one contract is registered into the DB, 
            and its client name is 'testClient'.        
        """ 
        if self.permission == 'GESTION': 
            testContract = self.manager.add_entity( 'contract', { 
                "client_name": "testClient", 
                "amount": 1000, 
                "paid_amount": 350, 
                "is_signed": 0 
            }) 
            items_db = self.manager.select_all_entities('contracts') 
            assert len(items_db) == 1 
            last_contract_db = testContracts_db.pop() 
            assert last_contract_db.client.name == "testClient" 
        else: 
            assert not self.permission 


