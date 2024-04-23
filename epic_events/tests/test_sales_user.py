
from epic_events.manager import Manager 

import unittest 
import json 
import os 
from datetime import datetime 



class SalesuserTest(unittest.TestCase): 
	""" Config test files. 
	""" 

	def setUp(self): 
		# # view = Views() 
		self.manager = Manager() 
		self.manager.connect() 
		self.manager.create_session() 


	def test_1_connect_sales_user(self): 
		connectEmail = 'sales_1@mail.org' 
		connectPass = self.manager.hash_pw(os.environ.get('USER_2_PW')) 
		print('connectPass -10 test25 :', connectPass[:10]) 
		connectDept = self.manager.select_one_user('email', connectEmail) 
		logged_user = self.manager.check_pw(connectEmail, connectPass) 

		permission = self.manager.verify_token( 
			connectEmail, 
			connectPass, 
			connectDept 
		) 

		assert permission == 'COMMERCE' 


	# def test_2_creation_client(self): 
	# 		""" Test adding one client. 
	# 		""" 
	# 		testClient = self.manager.add_entity( 'client', { 
	# 			'name': 'testClient', 
	# 	        'email': 'test_client@email.com', 
	# 	        'phone': '06 13 45 67 89', 
	# 	        'corporation_name': 'Entreprise 2', 
	# 	        'sales_contact_name': 'sales_user 1' 
	# 		}) 
	# 		testClient_db = self.manager.select_one_client('name', 'testClient') 
	# 		assert testClient_db.name == 'testClient' 
	# 		items_db = self.manager.select_all_entities('clients') 
	# 		assert len(items_db) == 1 

