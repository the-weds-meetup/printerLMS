from main import db
from model.Class import Class
from flask import jsonify

# get all classes
def get_classes():
    class_list = Class.query.all()
    if len(class_list):
        return jsonify(
            {
                "code": 200,
                "data": [each_class.serialise() for each_class in class_list],
            }
        )
    return jsonify({"code": 404, "message": "There are no classes"}), 404


# get classes by course
def get_classes_by_course(course_id):
    class_list = Class.query.filter_by(course_id=course_id)
    if class_list:
        return jsonify(
            {
                "code": 200,
                "data": [each_class.serialise() for each_class in class_list],
            }
        )
    return jsonify({"code": 404, "message": "There are no classes"}), 404