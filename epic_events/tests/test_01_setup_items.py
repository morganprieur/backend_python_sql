
# from pathlib import Path
# import sys
# print(sys.path)
# path_root = Path(__file__).parents[1]
# # path_root = Path(__file__).parents[2]
# sys.path.append(str(path_root))
# print(sys.path)
# # # import src.c.d

from sqlalchemy import create_engine 
import psycopg2 
from sqlalchemy.orm import sessionmaker 

from manager import Manager 
from models import Client, Contract, Department, Event, User 

from cryptography.fernet import Fernet 
import unittest 
import json 
import os 



class SetupTest(unittest.TestCase): 
	""" 
		Config test files. 
	""" 

	def setUp(self): 
		self.manager = Manager() 
		self.manager.connect() 
		self.manager.create_session() 


	def test_1_created_depts(self): 
		""" Test departments created by the setup.py script.""" 
		dept_gestion_db = self.manager.select_one_dept('name', 'gestion') 
		assert dept_gestion_db.name == 'gestion' 
		items_db = self.manager.select_all_entities('depts') 
		assert len(items_db) == 1 


	def test_2_created_user(self): 
		""" Test user created by the setup.py script.""" 
		testUser_db = self.manager.select_one_user( 
			'email', 'admin@mail.org' 
		) 
		assert testUser_db.id == 1 
		assert testUser_db.name == 'super_admin' 
		assert testUser_db.department_id == 1 

