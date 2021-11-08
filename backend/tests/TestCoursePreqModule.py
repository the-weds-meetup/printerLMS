"""
TestCoursePreqModule.py
Done by: Djulian Naval
Email ID: dbnaval.2019
"""


import unittest

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
        # get the only prereq couse in sqlite
        precourse: CoursePreq = CoursePreq.CoursePreq.query.filter_by(
            course_id=3
        ).first()
        course_compare = Course.Course(
            "Web Application Development I",
            "In this course, students be equipped with the knowledge and skill to develop a database-driven web application. PHP will be used as the vehicle of exploration. Other related topics like HTTP, HTML, CSS, Javascript will be covered as well. Students will learn the concepts gradually in the 13 weeks of the semester while building a web application of medium complexity.",
        )
        course_compare.id = 3
        self.assertEqual(precourse.get_course().__repr__(), course_compare.__repr__())

    def test_get_prereq_course(self):
        # get the only prereq couse in sqlite
        precourse: CoursePreq = CoursePreq.CoursePreq.query.filter_by(
            course_id=3
        ).first()
        course_compare = Course.Course(
            "Introduction to Programming",
            "This course is intended for any student who wishes to gain some programming fundamentals, also known as the building blocks of Information Systems. The course introduces students to fundamental programming concepts and constructs, explains the process of developing a basic software application, and explains the basic concepts of object orientation. The student will experience the implementation of a basic software application. Python, a widely-used, high-level, general-purpose and interactive programming language, is used as the vehicle of exploration in this course.",
        )
        course_compare.id = 1
        self.assertEqual(
            precourse.get_prereq_course().__repr__(), course_compare.__repr__()
        )

    def test_serialise(self):
        precourse: CoursePreq = CoursePreq.CoursePreq.query.filter_by(
            course_id=3
        ).first()
        precourse_expected = CoursePreq.CoursePreq(3, 1)
        precourse_expected.id = 1
        self.assertEqual(precourse.serialise(), precourse_expected.serialise())

    def test_empty_preqcourse_serialise(self):
        with self.assertRaises(Exception):
            CoursePreq.CoursePreq().serialise()


if __name__ == "__main__":
    unittest.main()
