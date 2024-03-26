
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
	# def setUp(self): 
	# 	self.app = app 
	# 	self.app_ctxt = self.app.app_context() 
	# 	self.app_ctxt.push() 
	# 	self.client = self.app.test_client() 

		# # view = Views() 
		# manager = Manager() 
		# manager.connect() 
		# # manager.create_tables() 
		# manager.create_session() 

	# tester 2 mails des secrétaires 
	def test_showSummary_club_1(self): 
		""" Test one registered email, to get the email displayed on the page."""  
		manager = Manager() 
		manager.connect() 
		# manager.create_tables() 
		manager.create_session() 
		file = os.environ.get('FILE_PATH') 
		with open(file, 'r') as jsonfile: 
			registered = json.load(jsonfile) 
			# print('registered : ', registered) 
			users = [item for item in registered['users']] 
			# print('users : ', users) 
			emailList = [item['email'] for item in users] 
			# club = [club for club in clubs if club['email'] == request.form['email']][0] 
		print('emailList : ', emailList)  # ok 
		data = {"email": "john@simplylift.co"} 

		newDept = manager.add_department(['testTable']) 
		testTable_db = manager.select_one_dept('name', 'testTable') 
		assert testTable_db.name == 'testTable' 
		items_db = manager.select_all_depts() 
		assert len(items_db) == 2 

		testUser = manager.add_user(['user test', 'test@mail.org', 'test_password', '01 23 45 67 89', testTable_db.id]) 
		testUser_db = manager.select_one_user('email', 'test@mail.org') 
		testUser_db = manager.update_user(6, 'department_id', 1, 12) 
		assert testUser_db.name == 'user test' 
		assert testUser_db.department_id == 12 

		manager.delete_dept('name', 'testTable') 
		# manager.delete_user('name', 'user test') 




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
