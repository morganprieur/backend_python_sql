
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
		testUser_update = self.manager.update_user( 
			testUser_db.id, 'department_id', 
			testUser_db.department_id, 1) 

		dept_id = testUser_db.department_id 
		# print('dept_id : ', dept_id) 
		assert testUser_db.name == 'user test' 
		assert testUser_db.department_id == 1 

		testUser_update = self.manager.update_user( 
			testUser_db.id, 'department_id', 1, dept_id) 
		assert testUser_update.name == 'user test' 
		assert testUser_update.department_id == dept_id 
		# assert testUser_update.department_id == dept_id 


	def test_deletion_dept_and_user(self): 
		""" Test deletiing one department and the user with relationship.""" 
		testDept_db = self.manager.select_one_dept('name', 'testTable') 
		testUser_db = self.manager.select_one_user( 
			'email', 'test@mail.org') 

		self.manager.delete_dept('name', 'testTable') 

		all_depts = self.manager.select_all_depts() 
		depts_names_list = [] 
		for dept in all_depts: 
			depts_names_list.append(dept) 
		assert testDept_db.name not in depts_names_list 

		all_users = self.manager.select_all_users() 
		users_names_list = [] 
		for user in all_users: 
			users_names_list.append(user) 
		assert testUser_db.name not in depts_names_list 

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
