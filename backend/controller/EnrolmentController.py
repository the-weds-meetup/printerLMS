"""To get courses, and details of its respective classs"""
from typing import Any, List
import dateutil.parser
import datetime
import pytz

from model.Course import Course
from model.Class import Class
from model.Enrolment import Enrolment
from model.Learner import Learner


class EnrolmentController:
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
