from typing import Any, List
from main import db

from model.Class import Class
from model.Enrolment import Enrolment
from model.Learner import Learner

from controller.LearnerController import LearnerController


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
