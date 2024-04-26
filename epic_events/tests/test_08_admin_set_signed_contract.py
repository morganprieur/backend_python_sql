
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
    	cls.connectUser = cls.manager.select_one_user('email', 'admin@mail.org') 
    	if cls.manager.verify_if_token_exists(connectEmail): 
    		cls.permission = cls.manager.verify_token( 
    			connectEmail, 
    			cls.connectUser.department.name 
    		) 
    		assert cls.permission == 'GESTION' 


    @classmethod
    def test_2_get_last_contract_not_signed(cls): 
        """ Test last contract is not signed, if the connected user is admin. 
            Expect is_signed is none. 
        """ 
        if (cls.permission == 'GESTION') | (cls.permission == 'COMMERCE'): 
            contracts_db = cls.manager.select_all_entities('contracts') 
            cls.lastContract_db = contracts_db.pop() 
            assert cls.lastContract_db.client.name == 'client 1' 
            assert cls.lastContract_db.amount == 1000 
            assert cls.lastContract_db.paid_amount == 400 
            assert cls.lastContract_db.is_signed == False 
        else: 
            assert cls.permission == 'SUPPORT' 


    def test_3_set_signed_contract(cls): 
        """ Test set last contract's is_signed field to True, 
            if the connected user is admin or sales user. 
            Expect is_signed is True. 
        """ 
        if (cls.permission == 'COMMERCE') | (cls.permission == 'GESTION'): 
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


    def test_4_contract_signed(cls): 
        """ Test last contract's is_signed field is False, 
            if the connected user is admin or sales user. 
            Expect is_signed is True. 
        """ 
        if (cls.permission == 'COMMERCE') | (cls.permission == 'GESTION'): 
            items_db = cls.manager.select_all_entities('contracts') 
            assert len(items_db) == 1 
            last_db = items_db.pop()  
            assert last_db.is_signed == True 

