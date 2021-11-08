"""
TestCourseController.py
Authored by: Teng Zhi Ming Brandan
"""

import unittest
from freezegun import freeze_time
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../controller"))
)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../model")))


from tests.TestApp import TestApp
from controller import CourseController


class TestCourseController(TestApp):

    # Test if classes are returned as expected
    def testPrereq(self):
        self.assertEqual(
            len(CourseController.CourseController().get_prereq_courses(3)),
            1,
        )
        
    @freeze_time("2021-10-22") #needed
    def testPastClassesCourses(self):
        self.assertEqual(
            len(CourseController.CourseController().get_past_classes_courses(1)),
            1,
        )

    @freeze_time("2021-10-22") #needed
    def testEnrollingClassesCourses(self):
        self.assertEqual(
            len(CourseController.CourseController().get_enrolling_classes_course(1)),
            1,
        )

    def testOngoingClassesCourses(self):
        self.assertEqual(
            len(CourseController.CourseController().get_ongoing_classes_course(1)),
            1,
        )
        
    def testCourseCompletedLearners(self):
        self.assertEqual(
            len(CourseController.CourseController().get_course_completed_learners(1)),
            1,
        )
        
    def testCourseIncompletedLearners(self):
        self.assertEqual(
            len(CourseController.CourseController().get_course_incompleted_learners(1)),
            2,
        )

    # Test Exceptions
    def testPrereqException(self):
        with self.assertRaises(Exception):
            CourseController.CourseController().get_prereq_courses('string')



if __name__ == "__main__":
    unittest.main()
