
# import sys
# print(sys.path)

from pathlib import Path
import sys
path_root = Path(__file__).parents[1]
# path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
print(sys.path)
# # import src.c.d

from manager import Manager 
# from epic_events.manager import Manager 
# from ..manager import Manager 
# from epic_events.models import Department, User 

import unittest 
import json 
import os 


# from server import loadClubs, loadCompetitions 

# from server import app 
# import unittest 


# competitions = loadCompetitions()
# clubs = loadClubs() 


class MyTest(unittest.TestCase): 
	""" 
		Config test files. 
	""" 
	def setUp(self): 
	# 	self.app = app 
	# 	self.app_ctxt = self.app.app_context() 
	# 	self.app_ctxt.push() 
	# 	self.client = self.app.test_client() 

		# # view = Views() 
		self.manager = Manager() 
		self.manager.connect() 
		# manager.create_tables() 
		self.manager.create_session() 

	def test_creation_dept(self): 
		""" Test adding one department.""" 
		# manager = Manager() 
		# manager.connect() 
		# # manager.create_tables() 
		# manager.create_session() 

		# file = os.environ.get('FILE_PATH') 
		# with open(file, 'r') as jsonfile: 
		# 	registered = json.load(jsonfile) 
		# 	users = [item for item in registered['users']] 
		# 	emailList = [item['email'] for item in users] 
		# print('emailList : ', emailList) 

		# print(dir(self)) 
		testDept = self.manager.add_department(['testTable']) 
		testDept_db = self.manager.select_one_dept('name', 'testTable') 
		assert testDept.name == 'testTable' 
		items_db = self.manager.select_all_depts() 
		assert len(items_db) == 2 


	def test_creation_user(self): 
		""" Test adding one user.""" 
		testDept_db = self.manager.select_one_dept('name', 'testTable') 
		testUser = self.manager.add_user( 
            ['user test', 'test@mail.org', 'test_password', 
            '01 23 45 67 89', testDept_db.id] 
        ) 
		testUser_db = self.manager.select_one_user( 
			'email', 'test@mail.org') 
		testUser_db = self.manager.update_user( 
			testUser_db.id, 'department_id', 
			testUser_db.department_id, 1) 

		dept_id = testUser_db.department_id 
		assert testUser_db.name == 'user test' 
		assert testUser_db.department_id == 1 

		testUser_db = self.manager.update_user( 
			testUser_db.id, 'department_id', 1, dept_id) 
		assert testUser_db.name == 'user test' 
		assert testUser_db.department_id == dept_id 


	def test_deletion_dept_and_user(self): 
		""" Test deletiing one department and the user with relationship.""" 
		testUser_db = self.manager.select_one_user( 
			'email', 'test@mail.org') 
		self.manager.delete_dept('name', 'testTable') 
		all_depts = self.manager.select_all_depts() 
		dept_names_list = [] 
		for dept in all_depts: 
			dept_names_list.append(dept) 
		assert testUser_db.name not in dept_names_list 

		# self.manager.delete_user('name', 'user test') 




	# # ==== tuto blent.ai ==== 
	# def argmax(liste):
	# 	if len(liste) == 0:
	# 		return None

	# 	idx_max = 0
	# 	value_max = liste[0]
	# 	for i, x in enumerate(liste):
	# 		if x > value_max:
	# 			value_max = x
	# 			idx_max = i
	# 	return idx_max

	# def test_argmax():
	# 	assert argmax([5, 8, 2, 9, 6, 3]) == 3
	# 	assert argmax([7]) == 0
	# 	assert argmax([]) is None
	# # ==== /tuto blent.ai ==== 
