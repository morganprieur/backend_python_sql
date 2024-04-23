
# from pathlib import Path
# import sys
# path_root = Path(__file__).parents[1]
# sys.path.append(str(path_root))

from epic_events.manager import Manager 
import unittest 
import json 
import os 
from datetime import datetime 



class Sales_userTest(unittest.TestCase): 
	""" Config test files. 
	""" 

	def setUp(self): 
		# # view = Views() 
		self.manager = Manager() 
		self.manager.connect() 
		self.manager.create_session() 


	def connect_sales_user(self): 
		registered = self.manager.decrypt_token() 

		connectEmail = 'sales_1@mail.org' 
		connectPass = self.manager.hash_pw(os.environ.get('USER_2_PW')) 
		connectDept = self.manager.select_one_user('email', 'pass_user2')
		permission = self.manager.verify_token(connectEmail, connectPass, connectDept) 

		assert permission == 'COMMERCE' 

            # elif userDecode['dept'] == 'support': 
            #     permission = 'SUPPORT'

