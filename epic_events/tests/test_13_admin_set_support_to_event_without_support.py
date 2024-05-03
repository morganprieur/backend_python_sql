
from epic_events.manager import Manager 
from helpers_te_ts import ConnectTest 

import unittest 
import json 
import os 
from datetime import datetime 


class SuperuserTest(unittest.TestCase): 
	""" Config test files. 
	""" 
	@classmethod 
	def setUp(cls): 
		cls.manager = Manager() 
		cls.manager.connect() 
		cls.manager.create_session() 
		cls.helpers = ConnectTest('admin') 
		cls.helpers.connect_user() 


	@classmethod
	def test_2_get_events_without_support(cls): 
		""" Test getting events without a support contact, if permission is 'GESTION'. 
	        Excpect getting one event and his name is "Anniversaire 15 ans d'Oren". 
		""" 
		if cls.helpers.permission == 'GESTION': 
		    events_db = cls.manager.select_entities_with_criteria( 
		        'events', 
		        'without support', 
		        1 
		    ) 
		    assert len(events_db) == 1 
		    lastEvent_db = events_db.pop() 
		    assert lastEvent_db.name == "Anniversaire 15 ans d'Oren" 
		    assert lastEvent_db.support_contact_id is None 


	@classmethod
	def test_3_set_support_to_event(cls): 
		""" Test setting a support contact to one event. 
	        Expect there is only one event, 
	        and its support_id is equal to the id of the just registered support user. 
		""" 
		if cls.helpers.permission == 'GESTION': 
		    lastEvent_db = cls.manager.select_one_event( 
	            'name', 
	            "Anniversaire 15 ans d'Oren" 
	        ) 
		    edited_event = cls.manager.update_event( 
	            lastEvent_db, 
	            'support_contact_name', 
	            # NULL 
	            'support_user 1' 
	        ) 
		    items_db = cls.manager.select_all_entities('events') 
		    assert len(items_db) == 1 
		    last_event_db = items_db.pop() 
		    supportUser_db = cls.manager.select_one_user( 
	            'name', 
	            'support_user 1' 
	        ) 
		    assert last_event_db.support_contact_id == supportUser_db.id 
		    # assert 1 == 2 

