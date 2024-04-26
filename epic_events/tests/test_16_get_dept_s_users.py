
# from epic_events.helpers import decorator_verify_jwt 
from epic_events.manager import Manager 

import unittest 
import json 
import os 
from datetime import datetime 



class SuperUser4Test(unittest.TestCase): 
    """ Config test files. 
    """ 
    def setUp(self): 
        # # view = Views() 
        self.manager = Manager() 
        self.manager.connect() 
        self.manager.create_session() 


    def test_01_get_dept(self): 
        """ Test getting the department with name 'commerce'. 
            Expect getting one department. 
    	""" 
        self.salesDept_db = self.manager.select_one_dept('name', 'commerce') 
        assert len(self.salesDept_db) == 1 


    def test_02_get_dept_s_users(self): 
        """ Test getting the dept's users. 
            Expect getting one user and his email is 'sales_1@mail.org'. 
    	""" 
        deptUser_db = self.manager.select_entities_with_criteria( 
            'users', 
            'department', 
            self.salesDept_db.id 
        ) 
        assert len(deptUser_db) == 1 
        assert deptUser_db[0].name == 'sales_user 1' 

