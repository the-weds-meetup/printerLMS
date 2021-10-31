from flask import jsonify
from typing import List

from api.course import get_prereq_courses
from api.error import throw_error

from main import db
from model.Class import Class as CClass
from model.Course import Course
from model.Enrolment import Enrolment
from model.Learner import Learner
from model.LearnerCourseCompletion import LearnerCourseCompletion
from model.LoginSession import LoginSession


def response_self_enrolment(class_id: int, learner_id: int):
    the_class: CClass = CClass.query.filter_by(id=class_id).first()
    if the_class is None:
        return throw_error("Authorisation", "Not Authorised", 403)

    try:
        results = add_enrolment(learner_id=learner_id, class_id=class_id)
        if results == "not_eligible":
            response = {
                "success": False,
                "results": {
                    "type": "enrolment_status",
                    "msg": "Does not fulfil pre-requisites",
                },
            }
            return jsonify(response), 401

        response = {
            "success": True,
            "results": {
                "type": "enrolment_status",
                "msg": "OK",
            },
        }
        return jsonify(response), 200

    except Exception as e:
        print(e, flush=True)
        return throw_error(type="enroll_class", message=str(e), status_code=400)


def response_manual_enrolment(class_id: int, learner_id_list: List[int]):
    the_class: CClass = CClass.query.filter_by(id=class_id).first()
    non_enrolled_names: List[str] = []

    if the_class is None:
        return throw_error("Authorisation", "Not Authorised", 403)

    try:
        for learner_id in learner_id_list:
            results = add_enrolment(
                learner_id=learner_id, class_id=class_id, is_approved=True
            )
            if results == "not_eligible":
                learner: Learner = Learner.query.filter_by(id=learner_id).first()
                non_enrolled_names.append(learner.fullName())

        if len(non_enrolled_names) > 0:
            response = {
                "success": True,
                "results": {
                    "type": "class_enrolment_status",
                    "status": "Partially Failed",
                    "records": non_enrolled_names,
                },
            }
        else:
            response = {
                "success": True,
                "results": {
                    "type": "class_enrolment_status",
                    "status": "OK",
                },
            }
        return jsonify(response), 200

    except Exception as e:
        print(e, flush=True)
        return throw_error(type="enroll_class", message=str(e), status_code=400)


def is_learner_eligible_for_enrolment(learner_id: int, course_id: int):
    prereq_courses = get_prereq_courses(course_id)

    if len(prereq_courses) == 0:
        return True

    completed_class: List[
        LearnerCourseCompletion
    ] = LearnerCourseCompletion.query.filter_by(user_id=learner_id).all()

    # get list of course completed by learner
    completed_count = 0
    for complete in completed_class:
        class_details: CClass = CClass.query.filter_by(id=complete.class_id).first()
        course_completed: Course = Course.query.filter_by(
            id=class_details.course_id
        ).first()

        for course in prereq_courses:
            if course_completed.id == course.id:
                completed_count += 1
                break

    return len(prereq_courses) == completed_count


def check_learner_course_valid(token: str, course_id: int):
    session: LoginSession = LoginSession.query.filter_by(token=token).first()
    learner = session.get_learner()

    if learner is None:
        return throw_error("Authorisation", "Not Authorised", 403)

    if is_learner_eligible_for_enrolment(learner.id, course_id):
        # check if learner has completed
        is_completed = False
        completed_course: List[
            LearnerCourseCompletion
        ] = LearnerCourseCompletion.query.filter_by(user_id=learner.id).all()

        for completion in completed_course:
            completed_class: CClass = CClass.query.filter_by(
                id=completion.class_id
            ).first()
            if completed_class.course_id == course_id:
                is_completed = True
                break

        # check if completed
        response = {
            "success": True,
            "results": {
                "type": "enrolment_status",
                "msg": "OK",
                "completed": is_completed,
            },
        }
        return jsonify(response), 200

    response = {
        "success": False,
        "results": {
            "type": "enrolment_status",
            "msg": "Does not fulfil pre-requisites",
        },
    }
    return jsonify(response), 200


def add_enrolment(learner_id: int, class_id: int, is_approved: bool = False):
    the_class: CClass = CClass.query.filter_by(id=class_id).first()
    is_eligible = is_learner_eligible_for_enrolment(learner_id, the_class.course_id)

    if is_eligible == False:
        return "not_eligible"

    # add enrolment object
    enroll: Enrolment = Enrolment(learner_id, class_id, is_approved=is_approved)
    db.session.add(enroll)
    db.session.commit()
    return "OK"


def class_enrolment_status(token: str, class_id: int):
    session: LoginSession = LoginSession.query.filter_by(token=token).first()
    selected_class: CClass = CClass.query.filter_by(id=class_id).first()
    learner = session.get_learner()

    if learner is None or selected_class is None:
        return throw_error("Authorisation", "Not Authorised", 403)

    status = "no_enroll"
    enrolment: Enrolment = Enrolment.query.filter_by(
        user_id=learner.id, class_id=class_id
    ).first()
    if enrolment != None:
        if enrolment.is_approved:
            status = "approve"
        else:
            status = "awaiting_approval"

    response = {
        "success": True,
        "results": {
            "type": "class_enrolment_status",
            "status": status,
        },
    }
    return jsonify(response), 200
