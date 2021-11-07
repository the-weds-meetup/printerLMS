"""
TestClassController.py

Done by Chung Keng Yao
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
from freezegun import freeze_time
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../controller"))
)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../model")))


from tests.TestApp import TestApp
from controller import ClassController

class TestClassController(TestApp):

    # Currently, database (TestApp.py) have 7 classes but all classes's enrolment_end_date are before current date so there is 0 enrollable class now. 
    # If we change any of the classes's enrolement_end_date to any date after current date, it will appear as enrollable class.
    def test_get_all_enrollable_classes(self):
        enrollable_classes = ClassController.ClassController().get_all_enrollable_classes()
        self.assertEqual(len(enrollable_classes),0)

    # Get class by id = 1. 
    def test_get_class_pass1(self):
        classes1 = ClassController.ClassController().get_class(1)
        self.assertEqual(
            classes1,
            {
                "id": 1,
                "course_id": 1,
                "class_id": 1,
                "max_capacity": 20,
                "class_start_date":  '2021-10-05T16:00:00.000Z',
                "class_end_date":  '2021-10-12T16:00:00.000Z',
                "enrolment_start_date": '2021-10-04T00:00:00.000Z',
                "enrolment_end_date": '2021-10-05T04:00:00.000Z',
                "learners" : [],
                "current_capacity" : 0,
                "course_name" : 'Introduction to Programming',
            },
        )
    
    # Get class by id = 2. 
    def test_get_class_pass2(self):
        classes2 = ClassController.ClassController().get_class(2)
        self.assertEqual(
            classes2,
            {
                "id": 2,
                "course_id": 2,
                "class_id": 1,
                "max_capacity": 20,
                "class_start_date":  '2021-10-05T16:00:00.000Z',
                "class_end_date":  '2021-10-12T16:00:00.000Z',
                "enrolment_start_date": '2021-10-04T00:00:00.000Z',
                "enrolment_end_date": '2021-10-05T04:00:00.000Z',
                "learners" : [],
                "current_capacity" : 0,
                "course_name" : 'Information Systems and Innovation',
            },
        )

    # Since there are 7 classes now in TestApp.py, putting 0 class will raise an exception.
    def test_get_class_fail1(self):
        self.assertRaises(Exception, ClassController.ClassController().get_class, 0)


    # Since there are 7 classes now in TestApp.py, any number above 7 will raise an exception.
    def test_get_class_fail2(self):
        self.assertRaises(Exception, ClassController.ClassController().get_class, 10)

    # Get number of learners in class_id: 3 which will return 1. 
    # There is only one learner enrol into class_id: 3 so it should return 1. 
    def test_get_class_learners1(self):
        get_learners1 = ClassController.ClassController().get_class_learners(3)
        self.assertEqual(len(get_learners1), 1)
    
    # Get number of learners in class_id: 4 which will return 1. 
    # Even though there are two learners enrol into class_id: 4 , one is_approved = True while another one is_approved = False. 
    # This means that there will only be one learner in class_id: 4
    def test_get_class_learners2(self):
        get_learners2 = ClassController.ClassController().get_class_learners(4)
        self.assertEqual(len(get_learners2), 1)
            
    # Get a list of learners who are eligible for the course,but have yet to be enrolled or is not current taking any of the class right now.
    def test_get_class_non_enrolled_learners(self):
        get_non_enrolled_learners = ClassController.ClassController().get_class_non_enrolled_learners(7)
        self.assertEqual(len(get_non_enrolled_learners), 1)



if __name__ == "__main__":
    unittest.main()