from flask import jsonify
from typing import List

from main import db
from model.Course import Course
from api.error import throw_error


def getCourseCatalog(is_retired=False):
    """
    Gets all courses which are either retired or still ongoing
    """
    courses: List[Course] = Course.query.filter_by(is_retired=is_retired).all()

    serialised_courses = []
    for course in courses:
        seralise = course.to_dict()
        seralise["current_class_enroll"] = len(course.get_class_ongoing_enrolment())
        serialised_courses.append(seralise)

    status_code = 200
    response = {
        "success": True,
        "result": {"type": "Course", "records": serialised_courses},
    }

    return jsonify(response), status_code
