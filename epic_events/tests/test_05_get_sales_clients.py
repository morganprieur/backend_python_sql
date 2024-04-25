
# from epic_events.helpers import decorator_verify_jwt 
from epic_events.manager import Manager 

import unittest 
import json 
import os 
from datetime import datetime 



class Sales3Test(unittest.TestCase): 
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

        connectUser = self.manager.select_one_user( 
        	'email', connectEmail) 
        if self.manager.verify_if_token_exists(connectEmail): 
        	permission = self.manager.verify_token( 
        		connectEmail, 
        		connectUser.department.name 
        	) 
        	assert self.permission == 'COMMERCE' 


    def test_2_get_sales_user(self): 
        """ Test getting the sales user, 
            if the sales user is connected 
            and if he wants to get his own informations. 
            Expect getting one user and his email is equal to 'sales_1@mail.org'. 
    	""" 
        self.salesUser_db = self.manager.select_one_user('name', 'sales_user 1') 
        if (self.permission == 'COMMERCE') & (self.salesUser_db.email == 'sales_1@mail.org'): 
            assert len(self.salesUser_db) == 1 
            assert self.salesUser_db[0].email == 'sales_1@mail.org' 


    def test_3_get_sales_user_s_clients(self): 
        """ Test getting the sales user's clients. 
            Expect getting one client and his email is equal to 'client1@mail.com'. 
    	""" 
        salesClients_db = self.manager.select_entities_with_criteria( 
            'clients', 
            'sales clients', 
            self.salesUser_db.id 
        ) 
        assert len(salesClients_db) == 1 
        assert salesClients_db[0].email == 'client1@mail.com' 

