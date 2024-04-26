
# from epic_events.helpers import decorator_verify_jwt 
from epic_events.manager import Manager 

import unittest 
import json 
import os 
from datetime import datetime 



class Superuser2Test(unittest.TestCase): 
    """ Config test files. 
    """ 
    @classmethod 
    def setUp(cls): 
        # # view = Views() 
        cls.manager = Manager() 
        cls.manager.connect() 
        cls.manager.create_session() 


    @classmethod 
    def test_1_verify_admin_token(cls): 
    	""" Test the admin user's token. 
    		Expect his permission dept == 'GESTION'. 
    	""" 
    	registered = cls.manager.decrypt_token() 

    	connectEmail = 'admin@mail.org' 
    	connectPass = cls.manager.hash_pw(os.environ.get('USER_1_PW')) 
    	cls.connectUser = cls.manager.select_one_user('email', 'admin@mail.org') 
    	if cls.manager.verify_if_token_exists(connectEmail): 
    		cls.permission = cls.manager.verify_token( 
    			connectEmail, 
    			cls.connectUser.department.name 
    		) 
    		assert cls.permission == 'GESTION' 
    	else: 
    	    assert not cls.permission 


    @classmethod 
    def test_2_creation_contract(cls): 
        """ Test adding one contract, if the admin user is connected. 
            Expect one contract is registered into the DB, 
            and its client name is 'testClient'.        
        """ 
        if cls.permission == 'GESTION': 
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
            assert not cls.permission 


