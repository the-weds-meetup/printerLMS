import unittest
from flask.app import Flask
import flask_testing
import os, sys

from main import app, db
from model import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestApp(flask_testing.TestCase):
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {}
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    def create_app(self):
        db.init_app(app)
        return app

    def setUp(self):
        db.create_all()
        self.init_db()
        db.session.flush()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def init_db(self):
        db.session.add(Department.Department("Human Resource and Admin"))
        db.session.add(Department.Department("Engineers"))
        db.session.commit()

        # Add Learners
        db.session.add(
            Learner.Learner("admin@lms.com", "p@ssword", "Phris", "Coskitt", 1)
        )
        db.session.add(
            Learner.Learner("engineer1@lms.com", "p@ssword", "Engineer 1", "Loh", 2)
        )
        db.session.add(
            Learner.Learner("engineer2@lms.com", "p@ssword", "Engineer 2", "Minh", 2)
        )
        db.session.add(
            Learner.Learner("engineer3@lms.com", "p@ssword", "Engineer 2", "Loo", 2)
        )
        db.session.commit()

        # Add Admins
        db.session.add(Administrator.Administrator(1))
        db.session.commit()

        # Add Courses
        db.session.add(
            Course.Course(
                "Introduction to Programming",
                "This course is intended for any student who wishes to gain some programming fundamentals, also known as the building blocks of Information Systems. The course introduces students to fundamental programming concepts and constructs, explains the process of developing a basic software application, and explains the basic concepts of object orientation. The student will experience the implementation of a basic software application. Python, a widely-used, high-level, general-purpose and interactive programming language, is used as the vehicle of exploration in this course.",
            )
        )
        db.session.add(
            Course.Course(
                "Information Systems and Innovation",
                "In this course, you will get an overview of fundamental business concepts with an emphasis on the challenges and opportunities that arise from technology and how information systems can be used to create business value and innovations.",
            )
        )
        db.session.add(
            Course.Course(
                "Web Application Development I",
                "In this course, students be equipped with the knowledge and skill to develop a database-driven web application. PHP will be used as the vehicle of exploration. Other related topics like HTTP, HTML, CSS, Javascript will be covered as well. Students will learn the concepts gradually in the 13 weeks of the semester while building a web application of medium complexity.",
            )
        )
        db.session.commit()

        # Add Course Prereqs
        db.session.add(CoursePreq.CoursePreq(3, 1))
        db.session.commit()

        # Add Classes (Past)
        db.session.add(
            Class.Class(
                1,
                1,
                20,
                "2021-10-05T16:00:00.000Z",
                "2021-10-12T16:00:00.000Z",
                "2021-10-04T00:00:00.000Z",
                "2021-10-05T04:00:00.000Z",
            )
        )
        db.session.add(
            Class.Class(
                2,
                1,
                20,
                "2021-10-05T16:00:00.000Z",
                "2021-10-12T16:00:00.000Z",
                "2021-10-04T00:00:00.000Z",
                "2021-10-05T04:00:00.000Z",
            )
        )

        # Add Classes (Present)
        db.session.add(
            Class.Class(
                1,
                2,
                20,
                "2021-10-21T16:00:00.000Z",
                "2021-11-01T16:00:00.000Z",
                "2021-10-15T00:00:00.000Z",
                "2021-10-21T04:00:00.000Z",
            )
        )
        db.session.add(
            Class.Class(
                2,
                2,
                20,
                "2021-10-21T16:00:00.000Z",
                "2021-11-01T16:00:00.000Z",
                "2021-10-15T00:00:00.000Z",
                "2021-10-21T04:00:00.000Z",
            )
        )

        # Add Classes (Present - Enrolment/ Future)
        db.session.add(
            Class.Class(
                1,
                3,
                20,
                "2021-11-01T16:00:00.000Z",
                "2021-11-20T16:00:00.000Z",
                "2021-10-15T00:00:00.000Z",
                "2021-10-31T04:00:00.000Z",
            )
        )
        db.session.add(
            Class.Class(
                2,
                3,
                20,
                "2021-11-01T16:00:00.000Z",
                "2021-11-20T16:00:00.000Z",
                "2021-10-15T00:00:00.000Z",
                "2021-10-31T04:00:00.000Z",
            )
        )
        db.session.flush()

        # Add Trainer
        db.session.add(Trainer.Trainer(2, 1))
        db.session.add(Trainer.Trainer(2, 2))
        db.session.add(Trainer.Trainer(2, 3))
        db.session.add(Trainer.Trainer(2, 4))
        db.session.add(Trainer.Trainer(2, 5))
        db.session.add(Trainer.Trainer(2, 6))
        db.session.commit()

        # Add Enrolment (Engineer2 and 3)
        db.session.add(
            Enrolment.Enrolment(
                3, 3, enrolment_date="2021-10-21T16:00:00.000Z", is_approved=True
            )
        )
        db.session.add(
            Enrolment.Enrolment(
                3, 4, enrolment_date="2021-10-21T16:00:00.000Z", is_approved=True
            )
        )
        db.session.add(
            Enrolment.Enrolment(
                4, 4, enrolment_date="2021-10-21T16:00:00.000Z", is_approved=False
            )
        )
        db.session.commit()

        # Add Learner Course Completion
        db.session.add(
            LearnerCourseCompletion.LearnerCourseCompletion(
                2, 1, completion_date="2021-10-11T12:00:00.000Z"
            )
        )
        db.session.add(
            LearnerCourseCompletion.LearnerCourseCompletion(
                2, 2, completion_date="2021-10-11T12:00:00.000Z"
            )
        )
        db.session.commit()


        # id = 7
        db.session.add(
            Class.Class(
                3,
                1,
                20,
                "2021-11-01T16:00:00.000Z",
                "2021-11-20T16:00:00.000Z",
                "2021-10-15T00:00:00.000Z",
                "2021-10-31T04:00:00.000Z",
            )
        )
        db.session.commit()


if __name__ == "__main__":
    unittest.main()
