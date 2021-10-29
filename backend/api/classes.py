from flask import jsonify, request
from typing import List
from main import db
from model.Class import Class


def add_class(request_data: dict[str, any]):

    course_id = request_data["course_id"]
    class_id = request_data["class_id"]
    max_capacity = request_data["max_capacity"]
    class_start_date = request_data["class_start_date"]
    class_end_date = request_data["class_end_date"]
    enrolment_start_date = request_data["enrolment_start_date"]
    enrolment_end_date = request_data["enrolment_end_date"]

    classes: Class = Class(course_id,class_id,max_capacity,class_start_date,class_end_date,enrolment_start_date,enrolment_end_date)
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
