
# from epic_events.helpers import decorator_verify_jwt 
from epic_events.manager import Manager 

import unittest 
import json 
import os 
from datetime import datetime 



class Sales5Test(unittest.TestCase): 
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
    		if cls.permission in ['GESTION', 'COMMERCE', 'SUPPORT']: 
    			assert cls.permission == 'COMMERCE' 
    		elif cls.permission == 'past': 
    		    pass_counter = 1 				
    		    # file deepcode ignore NoHardcodedPasswords/test: Local project 
    		    userEmail = 'sales_1@mail.org' 
    		    userPass = 'pass_user2' 
    		    if cls.manager.check_pw(userEmail, userPass): 
    		        user_db = cls.manager.select_one_user('email', userEmail) 
    		        assert user_db.department.name == 'commerce' 
    		        token = cls.manager.get_token(5, { 
    		            'email': userEmail, 
    		            'dept': user_db.department.name 
    		        }) 
    		        cls.manager.register_token(userEmail, 'token', token) 
    		        cls.permission = user_db.department.name.upper() 
    		        assert cls.permission == 'COMMERCE' 


    @classmethod
    def test_2_get_not_signed_sales_user_s_contracts(cls): 
        """ Test getting the sales user's not signed contracts. 
            Expect getting one contract 
            and his id is equal to the last registered contract's id. 
    	""" 
        # print(dir(cls)) 
        if cls.connectUser: 
            if cls.permission == 'COMMERCE': 
                notSignedContracts_db = cls.manager.select_entities_with_criteria( 
                    'contracts', 
                    'not signed', 
                    cls.connectUser.id 
                ) 
                assert len(notSignedContracts_db) == 1 
                items_db = cls.manager.select_all_entities('contracts') 
                lastContract_db = items_db.pop() 
                assert notSignedContracts_db[0].id == lastContract_db.id 
                # assert 1 == 2 
            else: 
                assert permission != 'COMMERCE' 

