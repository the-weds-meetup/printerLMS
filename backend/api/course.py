from flask import jsonify
from typing import List

from main import db
from model.Course import Course
from api.error import throw_error


def get_courses():
    course_list = Course.query.all()
    if len(course_list):
        return jsonify(
            {"code": 200, "data": [course.serialise() for course in course_list]}
        )
    return jsonify({"code": 404, "message": "There are no courses"}), 404


def getCourseCatalog(is_retired=False):
    """
    Gets all courses which are either retired or still ongoing
    """
    courses: List[Course] = Course.query.filter_by(is_retired=is_retired).all()

    serialised_courses = []
    for course in courses:
        serialised_courses.append(course.to_dict())

    status_code = 200
    response = {
        "success": True,
        "result": {"type": "Course", "records": serialised_courses},
    }

    return jsonify(response), status_code
