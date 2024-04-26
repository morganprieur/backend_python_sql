
# from epic_events.helpers import decorator_verify_jwt 
from epic_events.manager import Manager 

import unittest 
import json 
import os 
from datetime import datetime 



class Superuser3Test(unittest.TestCase): 
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
    	# connectPass = cls.manager.hash_pw(os.environ.get('USER_1_PW')) 
    	cls.connectUser = cls.manager.select_one_user('email', 'admin@mail.org') 
    	if cls.manager.verify_if_token_exists(connectEmail): 
    		cls.permission = cls.manager.verify_token( 
    			connectEmail, 
    			cls.connectUser.department.name 
    		) 
    		assert cls.permission == 'GESTION' 

    @classmethod
    def test_2_get_events_without_support(cls): 
    	""" Test getting events without a support contact, if permission is 'GESTION'. 
            Excpect getting one event and his name is "Anniversaire 15 ans d'Oren". 
    	""" 
    	if cls.permission == 'GESTION': 
            events_db = cls.manager.select_entities_with_criteria('events', 'without support', 1) 
            assert len(events_db) == 1 
            lastEvent_db = events_db.pop() 
            assert lastEvent_db.name == "Anniversaire 15 ans d'Oren" 
            assert lastEvent_db.support_contact_id == 'NULL' 

    @classmethod
    def test_3_set_support_to_event(cls): 
    	""" Test setting a support contact to one event. 
            Expect there is only one event, 
            and its support_id is equal to the id of the just registered support user. 
    	""" 
    	if cls.permission == 'GESTION': 
    	    lastEvent_db = cls.manager.select_one_event('name', "Anniversaire 15 ans d'Oren") 
    	    edited_event = cls.manager.update_event( 
                lastEvent_db, 
                'support_contact_name', 
                # NULL 
                # 'support_user 1' 
            ) 
    	    items_db = cls.manager.select_all_entities('events') 
    	    assert len(items_db) == 1 
    	    last_event_db = items_db.pop() 
    	    supportUser_db = cls.manager.select_one_user('name', 'support_user 1') 
    	    assert last_event_db.support_contact_id == supportUser_db.id 

