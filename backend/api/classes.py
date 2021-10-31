from flask import jsonify, request
from typing import Any, List

from api.course import get_course_incompleted_learners
from api.enrolment import is_learner_eligible_for_enrolment
from api.error import throw_error

from main import db
from model.Course import Course
from model.LearnerCourseCompletion import LearnerCourseCompletion
from model.Class import Class
from model.Enrolment import Enrolment
from model.Learner import Learner
from model.Trainer import Trainer


def response_get_class_learners(class_id: int):
    learners = get_class_learners(class_id)
    learners_serialised = []

    for learner in learners:
        learners_serialised.append(learner.serialise())

    response = {
        "sucess": True,
        "results": {"type": "Class", "records": learners_serialised},
    }
    return jsonify(response), 200


def response_get_non_enrolled_learners(class_id):
    learners = get_class_non_enrolled_learners(class_id)
    learners_serialised = []

    for learner in learners:
        learners_serialised.append(learner.serialise())

    response = {
        "success": True,
        "results": {"type": "class_enrolment", "records": learners_serialised},
    }
    return jsonify(response), 200


def get_class_learners(class_id: int):
    enrolments: List[Enrolment] = Enrolment.query.filter_by(class_id=class_id).all()
    learners: List[Learner] = []

    for enrolment in enrolments:
        learner: Learner = Learner.query.filter_by(id=enrolment.user_id).first()
        learners.append(learner)
    return learners


def add_class(request_data: dict[str, any]):
    course_id = request_data["course_id"]
    max_capacity = request_data["max_capacity"]
    class_start_date = request_data["class_start_date"]
    class_end_date = request_data["class_end_date"]
    enrolment_start_date = request_data["enrolment_start_date"]
    enrolment_end_date = request_data["enrolment_end_date"]
    trainer_id = request_data["trainer_id"]

    # get latest class id
    all_classes: list[Class] = Class.query.filter_by(course_id=course_id).all()
    new_class_id = len(all_classes) + 1

    classes: Class = Class(
        course_id=course_id,
        class_id=new_class_id,
        max_capacity=max_capacity,
        class_start_date=class_start_date,
        class_end_date=class_end_date,
        enrolment_start_date=enrolment_start_date,
        enrolment_end_date=enrolment_end_date,
    )
    db.session.add(classes)
    db.session.flush()

    # add trainer id
    if trainer_id != None:
        classes.add_trainer(trainer_id)
    else:
        db.session.commit()

    response = {
        "success": True,
        "result": {"type": "class_add", "msg": "Added a new class"},
    }

    return jsonify(response), 200


def edit_class(request_data: dict[str, any]):
    class_id = request_data["class_id"]
    max_capacity = request_data["max_capacity"]
    class_start_date = request_data["class_start_date"]
    class_end_date = request_data["class_end_date"]
    enrolment_start_date = request_data["enrolment_start_date"]
    enrolment_end_date = request_data["enrolment_end_date"]
    trainer_id = request_data["trainer_id"]

    a_class: Class = Class.query.filter_by(id=class_id).first()

    if trainer_id is None:
        raise ("Missing Trainer ID")

    if a_class is None:
        raise ("Missing Class ID")

    a_class.max_capacity = max_capacity
    a_class.class_start_date = class_start_date
    a_class.class_end_date = class_end_date
    a_class.enrolment_start_date = enrolment_start_date
    a_class.enrolment_end_date = enrolment_end_date
    a_class.add_trainer(trainer_id)
    db.session.commit()

    response = {
        "success": True,
        "result": {"type": "class_edit", "msg": "Edited Class"},
    }

    return jsonify(response), 200


def get_all_class():
    class_list = Class.query.all()
    response = Class(class_list)
    class_serialised = []

    for classes in class_list:
        serialise = classes.to_dict()
        class_serialised.append(serialise)

    response = {
        "success": True,
        "result": {"type": "Course", "records": class_serialised},
    }
    return jsonify(response), 200


# get class of the course along with the learners that has passed the class
def get_class(id: int):
    a_class: Class = Class.query.filter_by(id=id).first()

    if a_class is None:
        error_type = "Class"
        message = "Invalid Class id"
        return throw_error(type=error_type, message=message)

    serialise = a_class.to_dict()

    learners = []
    for learner in get_learners(id):
        learner: Learner = Learner.query.filter_by(id=learner.user_id).first()
        learner_name = learner.fullName()
        learners.append(
            {
                "user_id": learner.user_id,
                "name": learner_name,
            }
        )

    serialise["learners"] = learners

    response = {
        "success": True,
        "result": {"type": "Class", "records": serialise},
    }

    return jsonify(response), 200


def get_learners(class_id):
    past_learners: List[
        LearnerCourseCompletion
    ] = LearnerCourseCompletion.query.filter_by(class_id=class_id).all()

    return past_learners


def add_trainer(user_id, class_id):
    # queries a class according to what has been selected in AssignTrainers form
    a_class: Class = Class.query.filter_by(id=class_id).first()
    response = a_class.add_trainer(user_id)

    return jsonify(response), 200


def get_class_non_enrolled_learners(class_id: int):
    current_class: Class = Class.query.filter_by(id=class_id).first()
    incompleted_learners = get_course_incompleted_learners(
        current_class.get_course().id
    )
    course_id = current_class.get_course().id
    ongoing_learners = get_class_learners(class_id)
    nonstarted_learners: List[Learner] = []

    for learner in incompleted_learners:
        is_match = False
        for ongoing_learner in ongoing_learners:
            if ongoing_learner.id == learner.id:
                is_match = True
                break

        if is_match == False and is_learner_eligible_for_enrolment(
            learner.id, course_id
        ):
            nonstarted_learners.append(learner)

    return nonstarted_learners
