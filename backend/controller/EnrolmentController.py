from typing import Any, List
from main import db

from model.Course import Course
from model.Class import Class
from model.Enrolment import Enrolment
from model.Learner import Learner

from controller.LearnerController import LearnerController

import dateutil.parser
import datetime
import pytz


class EnrolmentController:
    def add_enrolment(self, learner_id: int, class_id: int, is_approved: bool = False):
        """Manual Enrolments by admin is automatically approved"""
        a_class: Class = Class.query.filter_by(id=class_id).first()
        enrolment: Enrolment = Enrolment.query.filter_by(
            user_id=learner_id, class_id=class_id
        ).first()
        is_eligible = LearnerController().is_learner_eligible_for_enrolment(
            learner_id, a_class.course_id
        )

        if is_eligible == False:
            return "not_eligible"

        if enrolment != None:
            enrolment.is_approved = True
        else:
            # add enrolment object
            enroll: Enrolment = Enrolment(learner_id, class_id, is_approved=is_approved)
            db.session.add(enroll)

        db.session.commit()
        return True

    def check_learners_class_enrolment_status(self, learner_id: int, class_id: int):
        status = "no_enroll"

        enrolment: Enrolment = Enrolment.query.filter_by(
            user_id=learner_id, class_id=class_id
        ).first()
        if enrolment != None:
            if enrolment.is_approved:
                status = "approve"
            else:
                status = "awaiting_approval"

        return status

    def get_learners_awaiting_class_approval(self, class_id: int):
        learners: List[Learner] = []
        awaiting_enrolment: List[Enrolment] = Enrolment.query.filter_by(
            class_id=class_id, is_approved=False
        ).all()

        for awaiting in awaiting_enrolment:
            learner: Learner = Learner.query.filter_by(id=awaiting.user_id).first()
            learners.append(learner)

        return learners

    def get_approved_enrolments(self, learner_id: int):
        # get all approved enrolments of a learner first
        # for each class enrolment, get class details along with its corresponding course name
        enrolment_list: Enrolment = Enrolment.query.filter_by(user_id=learner_id).all()
        time_now = datetime.datetime.now(pytz.utc)
        upcoming = []
        ongoing = []
        past = []

        for each_enrol in enrolment_list:
            if each_enrol.is_approved:
                a_class: Class = Class.query.filter_by(id=each_enrol.class_id).first()
                class_start = dateutil.parser.parse(a_class.class_start_date)
                class_end = dateutil.parser.parse(a_class.class_end_date)

                course: Course = Course.query.filter_by(id=a_class.course_id).first()

                if time_now < class_start:
                    upcoming.append(
                        {
                            "course_name": course.name,
                            "class_name": a_class.class_id,
                            "progress": each_enrol.course_progress,
                            "class_start_date": a_class.class_start_date,
                            "class_end_date": a_class.class_end_date,
                        }
                    )

                elif time_now >= class_start and time_now < class_end:
                    ongoing.append(
                        {
                            "course_name": course.name,
                            "class_name": a_class.class_id,
                            "progress": each_enrol.course_progress,
                            "class_start_date": a_class.class_start_date,
                            "class_end_date": a_class.class_end_date,
                        }
                    )

                elif time_now > class_end:
                    past.append(
                        {
                            "course_name": course.name,
                            "class_name": a_class.class_id,
                            "progress": each_enrol.course_progress,
                            "class_start_date": a_class.class_start_date,
                            "class_end_date": a_class.class_end_date,
                        }
                    )

        return {"upcoming": upcoming, "ongoing": ongoing, "past": past}
