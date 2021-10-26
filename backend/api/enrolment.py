from flask import jsonify
from typing import List

from api.course import get_prereq_courses
from api.error import throw_error

from main import db
from model.Class import Class as CClass
from model.Course import Course
from model.Enrolment import Enrolment
from model.LearnerCourseCompletion import LearnerCourseCompletion
from model.LoginSession import LoginSession


def is_learner_eligible_for_enrolment(learner_id: int, course_id: int):
    prereq_courses = get_prereq_courses(course_id)

    if len(prereq_courses) == 0:
        return True

    completed_class: List[
        LearnerCourseCompletion
    ] = LearnerCourseCompletion.query.filter_by(user_id=learner_id).all()

    # get list of course completed by learner
    completed_course: List[Course] = []
    for complete in completed_class:
        class_details: CClass = CClass.query.filter_by(id=complete.class_id).first()
        course: Course = Course.query.filter_by(id=class_details.course_id).first()
        if course_id in prereq_courses:
            completed_course.append(course)

    return len(completed_class) == len(completed_course)


def check_learner_course_valid(token: str, course_id: int):
    session: LoginSession = LoginSession.query.filter_by(token=token).first()
    learner = session.get_learner()

    if learner is None:
        return throw_error("Authorisation", "Not Authorised", 403)

    if is_learner_eligible_for_enrolment(learner.id, course_id):
        response = {
            "success": True,
            "results": {
                "type": "enrolment_status",
                "msg": "OK",
            },
        }
        return response, 200

    response = {
        "success": False,
        "results": {
            "type": "enrolment_status",
            "msg": "Does not fulfil pre-requisites",
        },
    }
    return response, 200


def add_enrolment(token: str, class_id: int):
    session: LoginSession = LoginSession.query.filter_by(token=token).first()
    the_class: CClass = CClass.query.filter_by(class_id=class_id)
    learner = session.get_learner()

    if learner is None or the_class is None:
        return throw_error("Authorisation", "Not Authorised", 403)

    is_eligible = is_learner_eligible_for_enrolment(learner.id, the_class.course_id)

    if is_eligible == False:
        response = {
            "success": False,
            "results": {
                "type": "enrolment_status",
                "msg": "Does not fulfil pre-requisites",
            },
        }
        return response, 401

    # add enrolment object
    enroll: Enrolment = Enrolment(learner.id, class_id)
    db.session.add(enroll)
    db.session.flush()
