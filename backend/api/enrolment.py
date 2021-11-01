from flask import jsonify
from typing import List

from api.error import throw_error
from controller.LearnerController import LearnerController
from controller.EnrolmentController import EnrolmentController

from main import db
from model.Class import Class
from model.Enrolment import Enrolment
from model.Learner import Learner


def response_self_enrolment(class_id: int, learner_id: int):
    the_class: Class = Class.query.filter_by(id=class_id).first()
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
    the_class: Class = Class.query.filter_by(id=class_id).first()
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


def check_learners_class_enrolment_status(learner_id: int, course_id: int):
    status = LearnerController().check_learner_finish_course(learner_id, course_id)
    success = type(status) == bool
    response = {
        "success": success,
        "results": {
            "type": "enrolment_status",
            "completed": status,
        },
    }
    return jsonify(response), 200


def add_enrolment(learner_id: int, class_id: int, is_approved: bool = False):
    the_class: Class = Class.query.filter_by(id=class_id).first()
    enrolment: Enrolment = Enrolment.query.filter_by(
        user_id=learner_id, class_id=class_id
    ).first()
    is_eligible = LearnerController().is_learner_eligible_for_enrolment(
        learner_id, the_class.course_id
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
    return "OK"


def learner_class_enrolment_status(learner_id: int, class_id: int):
    selected_class: Class = Class.query.filter_by(id=class_id).first()

    if selected_class is None:
        raise Exception("Missing ClassID")

    status = EnrolmentController().check_learners_class_enrolment_status(
        learner_id, class_id
    )

    response = {
        "success": True,
        "results": {
            "type": "class_enrolment_status",
            "status": status,
        },
    }
    return jsonify(response), 200
