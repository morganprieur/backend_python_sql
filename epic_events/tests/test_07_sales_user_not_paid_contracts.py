
# from epic_events.helpers import decorator_verify_jwt 
from epic_events.manager import Manager 

import unittest 
import json 
import os 
from datetime import datetime 



class Sales5Test(unittest.TestCase): 
    """ Config test files. 
    """ 
    def setUp(self): 
        # # view = Views() 
        self.manager = Manager() 
        self.manager.connect() 
        self.manager.create_session() 


    def test_1_connect_sales_user(self): 
    	""" Test connect a sales user. 
    		Expect permission is 'COMMERCE'. 
    	""" 
    	connectEmail = 'sales_1@mail.org' 
    	# connectPass = os.environ.get('USER_2_PW') 
    	# print('connectPass -10 test25 :', connectPass[:10]) 

    	self.connectUser = self.manager.select_one_user( 
    		'email', connectEmail) 
    	if self.manager.verify_if_token_exists(connectEmail): 
    		permission = self.manager.verify_token( 
    			connectEmail, 
    			connectUser.department.name 
    		) 
    		assert self.permission == 'COMMERCE' 
    	else: 
    	    assert not self.permission 


    def test_02_get_not_paid_sales_user_s_contracts(self): 
        """ Test getting the sales user-s not paid contracts. 
            Expect getting one contract 
            and his id is equal to the last registered contract's id. 
    	""" 
        if self.connectUser: 
            if self.permission == 'COMMERCE': 
                notPaidContracts_db = self.manager.select_entities_with_criteria( 
                    'contracts', 
                    'not signed', 
                    self.salesUser_db.id 
                ) 
                assert len(notPaidContracts_db) == 1 
                items_db = self.manager.select_all_entities('contracts') 
                lastContract_db = items_db.pop() 
                assert notPaidContracts_db.id == lastContract_db.id 
            else: 
                assert permission != 'COMMERCE' 

