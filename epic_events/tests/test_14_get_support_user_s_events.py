
# from epic_events.helpers import decorator_verify_jwt 
from epic_events.manager import Manager 

import unittest 
import json 
import os 
from datetime import datetime 



class Support1Test(unittest.TestCase): 
    """ Config test files. 
    """ 
    @classmethod
    def setUp(cls): 
        # # view = Views() 
        cls.manager = Manager() 
        cls.manager.connect() 
        cls.manager.create_session() 
        # cls.permission = '' 

    @classmethod
    def test_1_connect_support_user(cls): 
    	""" Test connect a support user. 
    		Expect permission is 'SUPPORT'. 
    	""" 
    	connectEmail = 'support_1@mail.org' 
    	connectUser = cls.manager.select_one_user( 
    		'email', connectEmail) 
    	if cls.manager.verify_if_token_exists(connectEmail): 
            # print('if exists') 
            cls.permission = cls.manager.verify_token( 
            	connectEmail, 
            	connectUser.department.name 
            ) 
            if cls.permission in ['GESTION', 'COMMERCE', 'SUPPORT']: 
                assert cls.permission == 'SUPPORT' 
                # assert 1 == 2 
            elif cls.permission == 'past': 
            	pass_counter = 1 				
            	# file deepcode ignore NoHardcodedPasswords/test: Local project 
            	userEmail = connectEmail 
            	userPass = 'pass_user3' 
            	if cls.manager.check_pw(userEmail, userPass): 
            		user_db = cls.manager.select_one_user( 
                        'email', 
                        userEmail 
                    ) 
            		assert user_db.department.name == 'support' 
            		token = cls.manager.get_token(5, { 
            			'email': userEmail, 
            			'dept': user_db.department.name 
            		}) 
            		cls.manager.register_token(userEmail, 'token', token) 
            		cls.permission = user_db.department.name.upper() 
            		assert cls.permission == 'SUPPORT' 
    	else: 
            print('No token exists') 
            assert 3 == 4 
    	# print('not entered into if') 
    	# assert 0 == 1 


    @classmethod
    def test_2_get_support_user_s_events(cls): 
        """ Test getting the support user's events, if permission is 'SUPPORT'. 
            Expect getting one event and his name is "Anniversaire 15 ans d'Oren". 
    	""" 
        if cls.permission == 'SUPPORT': 
            supportUser = cls.manager.select_one_user('email', 'support_1@mail.org') 
            supportEvents_db = cls.manager.select_entities_with_criteria( 
                'events', 
                'support contact', 
                supportUser.id 
            ) 
            assert len(supportEvents_db) == 1 
            last_event_db = supportEvents_db.pop() 
            assert last_event_db.support_contact_id == supportUser.id 
            assert last_event_db.attendees == 30 


    @classmethod
    def test_3_support_update_event(cls): 
        """ Test updating one event, if permission is 'SUPPORT'. 
            Expect getting event.attendees is 40. 
    	""" 
        if cls.permission == 'SUPPORT': 
            item_db = cls.manager.select_one_event('name', "Anniversaire 15 ans d'Oren") 
            print('items_db 1 :', item_db) 
            edited_event = cls.manager.update_event( 
                item_db, 
                'attendees', 
                40 
            ) 
            item_db = cls.manager.select_one_event('name', "Anniversaire 15 ans d'Oren") 
            print('items_db 2 :', item_db) 
            assert item_db.attendees == 40 

