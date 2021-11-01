from typing import Any, List
import dateutil.parser
import datetime
import pytz
from backend.api import learner

from model.Course import Course
from model.Class import Class
from model.Enrolment import Enrolment
from model.Learner import Learner
from model.LoginSession import LoginSession
from model.LearnerCourseCompletion import LearnerCourseCompletion

from controller.AuthController import AuthController
from controller.CourseController import CourseController


class LearnerController:
    def get_learner(self, token: str) -> Learner:
        isValid = AuthController.validate_token(token)
        if isValid == None:
            raise Exception("Invalid Token")

        session: LoginSession = AuthController.return_login_session(token)
        learner: Learner = session.get_learner()

        if learner == None:
            raise Exception("Invalid LearnerID")

        return learner

    def is_learner_eligible_for_enrolment(
        self, learner_id: int, course_id: int
    ) -> bool:
        prereq_courses = CourseController.get_prereq_courses(course_id)
        completed_class: List[
            LearnerCourseCompletion
        ] = LearnerCourseCompletion.query.filter_by(user_id=learner_id).all()

        # get list of course completed by learner
        completed_count = 0
        for complete in completed_class:
            class_details: Class = Class.query.filter_by(id=complete.class_id).first()
            course_completed: Course = Course.query.filter_by(
                id=class_details.course_id
            ).first()

            for course in prereq_courses:
                if course_completed.id == course.id:
                    completed_count += 1
                    break

        return len(prereq_courses) == completed_count

    def check_learner_finish_course(self, learner_id: int, course_id: int):
        if self.is_learner_eligible_for_enrolment():
            # check if learner has completed
            is_completed = False
            completed_course: List[
                LearnerCourseCompletion
            ] = LearnerCourseCompletion.query.filter_by(user_id=learner_id).all()

            for completion in completed_course:
                completed_class: Class = Class.query.filter_by(
                    id=completion.class_id
                ).first()
                if completed_class.course_id == course_id:
                    is_completed = True
                    break

            return is_completed

        # success, msg
        return "Does not fulfil pre-requisites"
