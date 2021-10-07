from main import db
from model.Course import Course
from flask import jsonify

def get_courses():
    course_list = Course.query.all()
    if len(course_list):
        return jsonify(
            {"code": 200, "data": [course.serialise() for course in course_list]}
        )
    return jsonify({"code": 404, "message": "There are no courses"}), 404