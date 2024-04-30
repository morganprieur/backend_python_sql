
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
		# # view = Views() 
		cls.manager = Manager() 
		cls.manager.connect() 
		cls.manager.create_session() 
		cls.helpers = ConnectTest('admin') 
		cls.helpers.connect_user() 


	@classmethod 
	def test_1_verify_admin_token(cls): 
		""" Test the admin user's token. 
			Expect his permission dept == 'GESTION'. 
		""" 
		registered = cls.manager.decrypt_token() 

		connectEmail = 'admin@mail.org' 
		connectPass = cls.manager.hash_pw(os.environ.get('USER_1_PW')) 
		connectUser = cls.manager.select_one_user( 
			'email', 
			'admin@mail.org' 
		) 
		row = cls.manager.verify_if_token_exists(connectEmail) 
		if row: 
			cls.permission = cls.manager.verify_token( 
				connectEmail, 
				connectUser.department.name, 
				row 
			) 
			assert cls.permission == 'GESTION' 
		else: 
			row = cls.manager.verify_if_token_exists(connectEmail) 
			if row is None: 
				# assert row is None 
				token = cls.manager.get_token(120, { 
					'email': connectEmail, 
					'dept': connectUser.department.name 
				}) 
				cls.manager.register_token(connectEmail, token) 
				row = cls.manager.verify_if_token_exists(connectEmail) 
				cls.permission = cls.manager.verify_token( 
					connectEmail, 
					connectUser.department.name, 
					row 
				) 
				assert cls.permission == 'GESTION' 
			else: 
				cls.permission = cls.manager.verify_token( 
					connectEmail, 
					connectUser.department.name, 
					row 
				) 
				if cls.permission == 'past': 
					check_pass = cls.manager.check_pw(connectEmail, connectPass) 
					if check_pass: 
						token = cls.manager.get_token(120, { 
							'email': connectEmail, 
							'dept': connectUser.department.name 
						}) 
						cls.manager.register_token(connectEmail, token) 
						row = cls.manager.verify_if_token_exists(connectEmail) 
						cls.permission = cls.manager.verify_token( 
							connectEmail, 
							connectUser.department.name, 
							row 
						) 
						assert cls.permission == 'GESTION' 
					else: 
						assert cls.permission == 'past' 

