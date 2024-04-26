
# from epic_events.helpers import decorator_verify_jwt 
from epic_events.manager import Manager 

import unittest 
import json 
import os 
from datetime import datetime 



class Sales3Test(unittest.TestCase): 
    """ Config test files. 
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


    # @classmethod 
    # def test_2_get_sales_user(cls): 
    #     """ Test getting the sales user, 
    #         if the sales user is connected 
    #         and if he wants to get his own informations. 
    #         Expect getting one user and his email is equal to 'sales_1@mail.org'. 
    # 	""" 
    #     cls.salesUser_db = cls.manager.select_one_user('name', 'sales_user 1') 
    #     if (cls.permission == 'COMMERCE') & (cls.salesUser_db.email == 'sales_1@mail.org'): 
    #         assert len(cls.salesUser_db) == 1 
    #         assert cls.salesUser_db[0].email == 'sales_1@mail.org' 


    @classmethod 
    def test_3_get_sales_user_s_clients(cls): 
        """ Test getting the sales user's clients. 
            Expect getting one client and his email is equal to 'client1@mail.com'. 
    	""" 
        all_clients = cls.manager.select_all_entities('clients') 
        salesClients_db = cls.manager.select_entities_with_criteria( 
            'clients', 
            'sales contact', 
            cls.connectUser.id 
        ) 
        assert len(salesClients_db) == 1 
        assert salesClients_db[0].email == 'client1@mail.com' 

