
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
    	# connectPass = self.manager.hash_pw(os.environ.get('USER_1_PW')) 
    	self.connectUser = self.manager.select_one_user('email', 'admin@mail.org') 
    	if self.manager.verify_if_token_exists(connectEmail): 
    		self.permission = self.manager.verify_token( 
    			connectEmail, 
    			self.connectUser.department.name 
    		) 
    		assert self.permission == 'GESTION' 
    	else: 
    	    assert not self.permission 


    def test_2_get_last_contract_not_signed(self): 
        """ Test last contract is not signed, if the connected user is admin. 
            Expect is_signed is none. 
        """ 
        if (self.permission == 'GESTION') | (self.permission == 'COMMERCE'): 
            contracts_db = self.manager.select_all_entities('contracts') 
            self.lastContract_db = contracts_db.pop() 
            assert self.lastContract_db.client_name == 'testClient' 
            assert self.lastContract_db.amount == 1000 
            assert self.lastContract_db.paid_amount == 350 
            assert self.lastContract_db.is_signed is None 
        else: 
            assert self.permission == 'SUPPORT' 


    def test_3_set_signed_contract(self): 
        """ Test set last contract's is_signed field to True, 
            if the connected user is admin or sales user. 
            Expect is_signed is True. 
        """ 
        if (self.permission == 'COMMERCE') | (self.permission == 'GESTION'): 
            edited_contract = self.manager.update_contract( 
                self.lastContract_db, 
                'is_signed', 
                True 
            ) 
            items_db = self.manager.select_all_entities('contracts') 
            assert len(items_db) == 1 
            self.last_contract_db = items_db.pop() 
            assert last_contract_db.client.name == "testClient" 
        else: 
            assert self.permission == 'SUPPORT' 


    def test_4_contract_signed(self): 
        """ Test last contract's is_signed field is False, 
            if the connected user is admin or sales user. 
            Expect is_signed is True. 
        """ 
        if (self.permission == 'COMMERCE') | (self.permission == 'GESTION'): 
            assert last_contract_db.is_signed == True 
        else: 
            assert self.permission == 'SUPPORT' 

