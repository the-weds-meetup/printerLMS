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

    #Currently, database (TestApp.py) have 7 classes but all classes's enrolment_end_date are before current date so there is 0 enrollable class now. 
    # If we change any of the classes's enrolement_end_date to any date after current date, it will appear as enrollable class.
    def test_get_all_enrollable_classes(self):
        classes = ClassController.ClassController().get_all_enrollable_classes()
        self.assertEqual(len(classes),0)

    #get class by class_id = 1
    def test_get_trainer_by_class_id(self):
        classes = ClassController.ClassController().get_class(1)
        print(classes)
        self.assertEqual(
            classes,
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
    
    def test_get_trainer_by_class_id_fail(self):
        self.assertRaises(Exception, ClassController.ClassController().get_class, 10)

    def test_get_class_learners(self):
        classes = ClassController.ClassController().get_class_learners(4)
        self.assertEqual(len(classes), 1)
            

    def test_get_class_non_enrolled_learners(self):
        classes = ClassController.ClassController(). get_class_non_enrolled_learners(7)
        self.assertEqual(len(classes), 1)



if __name__ == "__main__":
    unittest.main()
    unittest.main()
