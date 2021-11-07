import unittest
from unittest.mock import Mock, MagicMock, patch
# from freezegun import freeze_time
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../controller"))
)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../model")))


from tests.TestApp import TestApp
from model import CoursePreq
from model import Course



class TestCoursePreq(TestApp):

    def test_get_course(self):
        # course2 = Course.Course("How to Train Your Dragon", "Description here")
        # course2.id = 1
        # course2.
        # course = CoursePreq.CoursePreq().get_course(1)
        pass

def suite():
    """This defines all the tests of a module"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCoursePreq))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
