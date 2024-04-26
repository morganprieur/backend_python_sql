
# from epic_events.helpers import decorator_verify_jwt 
from epic_events.manager import Manager 

import unittest 
import json 
import os 
from datetime import datetime 



class Sales7Test(unittest.TestCase): 
    """ Config test. 
    """ 
    @classmethod
    def setUp(cls): 
        # # view = Views() 
        cls.manager = Manager() 
        cls.manager.connect() 
        cls.manager.create_session() 

    @classmethod
    def test_1_connect_sales_user(cls): 
    	""" Test connect a sales user. 
    		Expect permission is 'COMMERCE'. 
    	""" 
    	connectEmail = 'sales_1@mail.org' 
    	# connectPass = os.environ.get('USER_2_PW') 
    	# print('connectPass -10 test25 :', connectPass[:10]) 

    	cls.connectUser = cls.manager.select_one_user( 
    		'email', connectEmail) 
    	if cls.manager.verify_if_token_exists(connectEmail): 
    		cls.permission = cls.manager.verify_token( 
    			connectEmail, 
    			cls.connectUser.department.name 
    		) 
    		assert cls.permission == 'COMMERCE' 


    @classmethod
    def test_2_get_not_paid_sales_user_s_contracts(cls): 
        """ Test getting the sales user's not paid contracts. 
            Expect getting one contract 
            and his id is equal to the last registered contract's id. 
    	""" 
        if cls.connectUser: 
            if cls.permission == 'COMMERCE': 
                notPaidContracts_db = cls.manager.select_entities_with_criteria( 
                    'contracts', 
                    'not signed', 
                    cls.connectUser.id 
                ) 
                assert len(notPaidContracts_db) == 1 
                items_db = cls.manager.select_all_entities('contracts') 
                lastContract_db = items_db.pop() 
                assert notPaidContracts_db[0].id == lastContract_db.id 
            else: 
                assert permission != 'COMMERCE' 

