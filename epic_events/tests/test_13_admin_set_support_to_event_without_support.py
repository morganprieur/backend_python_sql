
# from epic_events.helpers import decorator_verify_jwt 
from epic_events.manager import Manager 

import unittest 
import json 
import os 
from datetime import datetime 



class Superuser3Test(unittest.TestCase): 
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


    def test_2_get_events_without_support(self): 
    	""" Test getting events without a support contact, if permission is 'GESTION'. 
            Excpect getting one event and his name is "Anniversaire 15 ans d'Oren". 
    	""" 
    	if self.permission == 'GESTION': 
            events_db = self.manager.select_entities_with_criteria('events', 'without support', None) 
            assert len(events_db) == 1 
            self.lastEvent_db = events_db.pop() 
            assert self.lastEvent_db.name == "Anniversaire 15 ans d'Oren" 
    	else: 
            assert not self.permission 


    def test_3_set_support_to_event(self): 
    	""" Test setting a support contact to one event. 
            Expect there is only one event, 
            and its support_id is equal to the id of the just registered support user. 
    	""" 
    	if self.permission == 'GESTION': 
            edited_event = self.manager.update_event( 
                self.lastEvent_db, 
                'support_contact_name', 
                'support_user 1' 
            ) 
            items_db = self.manager.select_all_entities('events') 
            assert len(items_db) == 1 
            last_event_db = items_db.pop() 
            assert last_event_db.support_contact_id == self.connectUser.id 
    	else: 
            assert not self.permission 

