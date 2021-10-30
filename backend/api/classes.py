from flask import jsonify, request
from typing import List
from main import db
from model.Class import Class


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
