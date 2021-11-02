from flask import jsonify
from typing import List

from api.error import throw_error
from controller.LearnerController import LearnerController
from controller.EnrolmentController import EnrolmentController

from main import db
from model.Class import Class
from model.Learner import Learner

import dateutil.parser
import datetime
import pytz


def get_approved_enrolments(user_id):
    enrolment_list: Enrolment = Enrolment.query.filter_by(user_id=user_id).all()
    time_now = datetime.datetime.now(pytz.utc)
    upcoming = []
    ongoing = []
    past = []

    for each_enrol in enrolment_list:
        if each_enrol.is_approved:
            a_class: Class = Class.query.filter_by(class_id=each_enrol.class_id).first()
            class_start = dateutil.parser.parse(a_class.class_start_date)
            class_end = dateutil.parser.parse(a_class.class_end_date)

            # if a_class is None:
            #     error_type = "Class"
            #     message = "Invalid Class id"
            #     return throw_error(type=error_type, message=message)

            course: Course = Course.query.filter_by(id=a_class.course_id).first()
            #serialise = course.to_dict()

            if time_now < class_start:
                upcoming.append(
                    {
                        "course_name": course.name,
                        "class_id": a_class.class_id,
                        "progress": each_enrol.course_progress,
                        "class_start_date": a_class.class_start_date,
                        "class_end_date": a_class.class_end_date,
                    }
                )

            elif time_now >= class_start and time_now < class_end:
                ongoing.append(
                    {
                        "course_name": course.name,
                        "class_id": a_class.class_id,
                        "progress": each_enrol.course_progress,
                        "class_start_date": a_class.class_start_date,
                        "class_end_date": a_class.class_end_date,
                    }
                )

            elif time_now > class_end:
                past.append(
                    {
                        "course_name": course.name,
                        "class_id": a_class.class_id,
                        "progress": each_enrol.course_progress,
                        "class_start_date": a_class.class_start_date,
                        "class_end_date": a_class.class_end_date,
                    }
                )

    return {"upcoming": upcoming, "ongoing": ongoing, "past": past}


def response_self_enrolment(class_id: int, learner_id: int):
    the_class: Class = Class.query.filter_by(id=class_id).first()
    if the_class is None:
        return throw_error("Authorisation", "Not Authorised", 403)

    try:
        results = EnrolmentController().add_enrolment(
            learner_id=learner_id, class_id=class_id
        )
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
            results = EnrolmentController().add_enrolment(
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
