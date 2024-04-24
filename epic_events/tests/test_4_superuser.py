
# from epic_events.helpers import decorator_verify_jwt 
from epic_events.manager import Manager 

import unittest 
import json 
import os 
from datetime import datetime 



class Superuser2Test(unittest.TestCase): 
    """ Config test files. 
    """ 
    def setUp(self): 
        # # view = Views() 
        self.manager = Manager() 
        self.manager.connect() 
        self.manager.create_session() 


    def test_04_creation_contract(self): 
        """ Test adding one contract. 
        """ 
        testContract = self.manager.add_entity( 'contract', { 
			"client_name": "testClient", 
			"amount": "1000", 
			"paid_amount": "350", 
			"is_signed": 0 
		}) 
        testContracts_db = self.manager.select_all_entities('contracts') 
        last_contract_db = testContracts_db.pop() 
        assert last_contract_db.client.name == "testClient" 
        items_db = self.manager.select_all_entities('contracts') 
        assert len(items_db) == 1 


    def test_05_contract_not_signed(self): 
        client_db = self.manager.select_one_client('name', 'testClient') 
        contract_db = self.manager.select_one_contract( 
            'client_id', 
            client_db.id 
        ) 
        assert contract_db.is_signed is None 


    def test_06_signature_contract(self): 
        """ Test adding one contract. 
        """ 
        client_db = self.manager.select_one_client('name', 'testClient') 
        contract_to_modify = self.manager.select_all_entities('contracts').pop() 
        edited_contract = self.manager.update_contract(contract_to_modify, 'is_signed', True) 

        items_db = self.manager.select_all_entities('contracts') 
        assert len(items_db) == 1 
        last_contract_db = items_db.pop() 
        assert last_contract_db.client.name == "testClient" 


    def test_07_contract_signed(self): 
        items_db = self.manager.select_all_entities('contracts') 
        last_contract_db = items_db.pop() 
        assert last_contract_db.is_signed == True 


	# def test_6_deletion_dept_and_user(self): 
	# 	""" Test deletiing one user.""" 
	# 	testDept_db = self.manager.select_one_dept('name', 'testDept') 
	# 	testUser_db = self.manager.select_one_user( 
	# 		'email', 'test_user_2@email.org') 
	# 	print('DEBUG testUser_db : ', testUser_db) 

	# 	self.manager.delete_dept('name', 'testDept') 

	# 	all_depts = self.manager.select_all_entities('depts') 
	# 	depts_names_list = [] 
	# 	for dept in all_depts: 
	# 		depts_names_list.append(dept) 
	# 	assert testDept_db.name not in depts_names_list 

	# 	all_clients = self.manager.select_all_entities('clients') 
	# 	assert all_clients == [] 

	# 	all_events = self.manager.select_all_entities('events') 
	# 	assert all_events == [] 


