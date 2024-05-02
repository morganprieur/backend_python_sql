
from epic_events.manager import Manager 
from helpers_te_ts import ConnectTest 

import unittest 
import json 
import os 
from datetime import datetime 


class SupportuserTest(unittest.TestCase): 
	""" Config test files. 
	""" 
	@classmethod 
	def setUp(cls): 
		cls.manager = Manager() 
		cls.manager.connect() 
		cls.manager.create_session() 
		cls.helpers = ConnectTest('support') 
		cls.helpers.connect_user() 


	@classmethod
	def test_2_get_support_user_s_events(cls): 
	    """ Test getting the support user's events, if permission is 'SUPPORT'. 
	        Expect getting one event and his name is "Anniversaire 15 ans d'Oren". 
		""" 
	    if cls.helpers.permission == 'SUPPORT': 
	        supportEvents_db = cls.manager.select_entities_with_criteria( 
	            'events', 
	            'support contact', 
	            cls.helpers.connectUser.id 
	        ) 
	        assert len(supportEvents_db) == 1 
	        last_event_db = supportEvents_db.pop() 
	        assert last_event_db.support_contact_id == cls.helpers.connectUser.id 
	        assert last_event_db.attendees == 30 
	    else: 
	        assert not cls.helpers.permission 
	        assert 2 == 3 


	@classmethod
	def test_3_support_update_event(cls): 
	    """ Test updating one event, if permission is 'SUPPORT'. 
	        Expect getting event.attendees is 40. 
		""" 
	    if cls.helpers.permission == 'SUPPORT': 
	        item_db = cls.manager.select_one_event('name', "Anniversaire 15 ans d'Oren") 
	        print('item_db 1 :', item_db) 
	        edited_event = cls.manager.update_event( 
	            item_db, 
	            'attendees', 
	            40 
	        ) 
	        item_db = cls.manager.select_one_event('name', "Anniversaire 15 ans d'Oren") 
	        print('item_db 2 :', item_db) 
	        assert item_db.attendees == 40 
	        # assert 1 == 2 
	    else: 
	        assert not cls.helpers.permission 
	        # assert 2 == 3 

