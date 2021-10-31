from flask import jsonify, request
from typing import List
from main import db
from model.Class import Class
from model.Learner import Learner
from model.Trainer import Trainer
from model.LearnerCourseCompletion import LearnerCourseCompletion
from api.error import throw_error


def add_class(request_data: dict[str, any]):
    course_id = request_data["course_id"]
    max_capacity = request_data["max_capacity"]
    class_start_date = request_data["class_start_date"]
    class_end_date = request_data["class_end_date"]
    enrolment_start_date = request_data["enrolment_start_date"]
    enrolment_end_date = request_data["enrolment_end_date"]

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
    db.session.commit()

    response = {
        "success": True,
        "result": {"type": "class_add", "msg": "Added a new class"},
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

    past_learners = []
    for each_past_learner in get_past_learners(id):
        learner: Learner = Learner.query.filter_by(id=each_past_learner.user_id).first()
        learner_name = learner.fullName()
        past_learners.append(
            {
                "user_id": each_past_learner.user_id,
                "name": learner_name,
            }
        )

    serialise["past_learners"] = past_learners

    response = {
        "success": True,
        "result": {"type": "Class", "records": serialise},
    }

    return jsonify(response), 200


def get_past_learners(class_id):
    past_learners: List[
        LearnerCourseCompletion
    ] = LearnerCourseCompletion.query.filter_by(class_id=class_id).all()

    return past_learners


def add_trainer(user_id, id):
    # queries a class according to what has been selected in AssignTrainers form
    a_class: Class = Class.query.filter_by(id=id).first()
    response = a_class.add_trainer(user_id)

    return jsonify(response), 200
