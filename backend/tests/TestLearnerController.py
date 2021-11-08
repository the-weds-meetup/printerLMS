"""
TestLearnerController
Authored by: Jasmine Lim Hui Shan
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
from controller import LearnerController
from model import LoginSession


class TestLearnerController(TestApp):
    def test_get_learner(self):
        session = LoginSession.LoginSession(1)
        session_serialise = session.serialise()
        print(session_serialise)
        # session_serialise["token"] = "fc361853-2529-4e6d-a18e-1d7bec47dfa7"

        # # session = AuthController.AuthController().login("admin@lms.com", "p@ssword")
        # # print(session)
        # learner = LearnerController.LearnerController().get_learner(
        #     session_serialise["token"]
        # )
        # print(learner)

        # self.assertEqual(
        #     learner.serialise(),
        #     {
        #         "id": 1,
        #         "email": "admin@lms.com",
        #         "first_name": "Phris",
        #         "middle_name": None,
        #         "last_name": "Coskitt",
        #         "full_name": "Phris Coskitt",
        #         "department": "Human Resource and Admin",
        #         "is_admin": True,
        #     },
        # )

    def test_get_learner_from_id(self):
        learner = LearnerController.LearnerController().get_learner_from_id(1)
        self.assertEqual(
            learner.serialise(),
            {
                "id": 1,
                "email": "admin@lms.com",
                "first_name": "Phris",
                "middle_name": None,
                "last_name": "Coskitt",
                "full_name": "Phris Coskitt",
                "department": "Human Resource and Admin",
                "is_admin": True,
            },
        )

    def test_get_learner_from_id_fail(self):
        self.assertRaises(
            Exception, LearnerController.LearnerController().get_learner_from_id, 5
        )

    def test_is_learner_eligible_for_enrolment_true(self):
        # test user id 2 who wants to take course 3
        # user id 2 has already taken course 1 which is a prereq to course 3, so is_eligible will be true
        is_eligible = (
            LearnerController.LearnerController().is_learner_eligible_for_enrolment(
                2, 3
            )
        )
        self.assertEqual(is_eligible, True)

    def test_is_learner_eligible_for_enrolment_false(self):
        # test user id 3 who wants to take course 3
        # user id 3 has not taken course 1 which is a prereq to course 3, so is_eligible will be false
        is_eligible = (
            LearnerController.LearnerController().is_learner_eligible_for_enrolment(
                3, 3
            )
        )
        self.assertEqual(is_eligible, False)

    def test_check_learner_finish_course(self):
        complete = LearnerController.LearnerController().check_learner_finish_course(
            2, 1
        )
        self.assertEqual(complete, True)

    def test_check_learner_finish_course_fail(self):
        complete = LearnerController.LearnerController().check_learner_finish_course(
            3, 1
        )
        self.assertEqual(complete, False)

    def test_is_learner_enrolled_and_approve(self):
        learner_enrol = (
            LearnerController.LearnerController().is_learner_enrolled_and_approve(3, 3)
        )

        self.assertEqual(learner_enrol, True)

    def test_is_learner_enrolled_and_approve_fail(self):
        learner_enrol = (
            LearnerController.LearnerController().is_learner_enrolled_and_approve(3, 6)
        )

        self.assertEqual(learner_enrol, False)


if __name__ == "__main__":
    unittest.main()