from flask import jsonify

from main import db
from model.Class import Class

from controller.ClassController import ClassController
from controller.TrainerController import TrainerController
from controller.EnrolmentController import EnrolmentController


def response_get_class_learners(class_id: int):
    learners = ClassController().get_class_learners(class_id)
    print(learners, flush=True)
    learners_serialised = []

    for learner in learners:
        learners_serialised.append(learner.serialise())

    response = {
        "sucess": True,
        "results": {"type": "Class", "records": learners_serialised},
    }
    return jsonify(response), 200


def response_get_non_enrolled_learners(class_id):
    learners = ClassController().get_class_non_enrolled_learners(class_id)
    learners_serialised = []

    for learner in learners:
        learners_serialised.append(learner.serialise())

    response = {
        "success": True,
        "results": {"type": "class_non_enrolment", "records": learners_serialised},
    }
    return jsonify(response), 200


def response_get_all_enrollable_classes():
    enrolling_class = ClassController().get_all_enrollable_classes()
    response = {
        "success": True,
        "results": {
            "type": "get_enrollable_class",
            "records": enrolling_class,
        },
    }
    return jsonify(response), 200


def response_get_all_waiting_learners(class_id: int):
    serialise_learners = []
    learners = EnrolmentController().get_learners_awaiting_class_approval(class_id)
    for learner in learners:
        serialise_learners.append(learner.serialise())

    response = {
        "success": True,
        "results": {
            "type": "class_waiting_list",
            "records": serialise_learners,
        },
    }
    return jsonify(response), 200


def response_get_class_details(class_id: int):
    serialised_class = ClassController().get_class(class_id)
    response = {
        "success": True,
        "result": {"type": "Class", "records": serialised_class},
    }
    return jsonify(response), 200


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


def add_trainer_response(user_id: int, class_id: int):
    # queries a class according to what has been selected in AssignTrainers form
    a_class: Class = Class.query.filter_by(id=class_id).first()
    response = a_class.add_trainer(user_id)

    return jsonify(response), 200


def get_all_learner_courses(user_id: int):
    learner = {}
    trainer = {}
    # merge code with upcoming methods
    # get all enrolled courses here

    # get trainer courses here

    if TrainerController().is_trainer(user_id):
        trainer = {
            "past": TrainerController().get_past_classes_serialise(user_id),
            "current": TrainerController().get_current_classes_serialise(user_id),
            "future": TrainerController().get_future_classes_serialise(user_id),
        }

    response = {
        "success": True,
        "results": {
            "type": "my_courses",
            "records": {"learner": learner, "trainer": trainer},
        },
    }

    return jsonify(response), 200
