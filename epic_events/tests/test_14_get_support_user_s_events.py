
# from epic_events.helpers import decorator_verify_jwt 
from epic_events.manager import Manager 

import unittest 
import json 
import os 
from datetime import datetime 



class Support1Test(unittest.TestCase): 
    """ Config test files. 
    """ 
    def setUp(self): 
        # # view = Views() 
        self.manager = Manager() 
        self.manager.connect() 
        self.manager.create_session() 


    def test_1_connect_support_user(self): 
    	""" Test connect a support user. 
    		Expect permission is 'SUPPORT'. 
    	""" 
    	connectEmail = 'support_user 1' 
    	# connectPass = os.environ.get('USER_2_PW') 
    	# print('connectPass -10 test25 :', connectPass[:10]) 

    	self.connectUser = self.manager.select_one_user( 
    		'email', connectEmail) 
    	if self.manager.verify_if_token_exists(connectEmail): 
    		permission = self.manager.verify_token( 
    			connectEmail, 
    			self.connectUser.department.name 
    		) 
    		assert self.permission == 'SUPPORT' 
    	else: 
    	    assert not self.permission 


    def test_2_get_support_user_s_events(self): 
        """ Test getting the support user's events, if permission is 'SUPPORT'. 
            Expect getting one event and his name is "Anniversaire 15 ans d'Oren". 
    	""" 
        if self.permission == 'SUPPORT': 
            supportEvents_db = self.manager.select_entities_with_criteria( 
                'events', 
                'support contacts', 
                self.connectUser.id 
            ) 
            assert len(items_db) == 1 
            self.last_event_db = items_db.pop() 
            assert self.last_event_db.support_contact_id == self.connectUser.id 
        else: 
    	    assert not self.permission 


    def test_3_support_update_event(self): 
        """ Test updating one event, if permission is 'SUPPORT'. 
            Expect getting event.attendees is 40. 
    	""" 
        if self.permission == 'SUPPORT': 
            edited_event = self.manager.update_event( 
                self.last_event_db, 
                'attendees', 
                40 
            ) 
            item_db = self.manager.select_one_event('name', "Anniversaire 15 ans d'Oren") 
            assert item_db.attendees == 40 
        else: 
    	    assert not self.permission 



