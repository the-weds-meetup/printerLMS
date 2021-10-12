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
        enrolment = []

        for a_class in course.get_class_enrolment():
            enrolment.append(a_class.serialise())

        seralise["class"] = {"enrolling": enrolment}
        serialised_courses.append(seralise)

    status_code = 200
    response = {
        "success": True,
        "result": {"type": "Course", "records": serialised_courses},
    }

    return jsonify(response), status_code


def getCourse(course_id: int):
    """
    Get course and ongoing and upcoming classes
    """
    course: Course = Course.query.filter_by(id=course_id).first()

    if course is None:
        error_type = "Course"
        message = "Invalid course id"
        return throw_error(type=error_type, message=message)

    print(course)

    status_code = 200
    seralise = course.to_dict()
    enrolment = []
    ongoing = []

    for a_class in course.get_class_enrolment():
        enrolment.append(a_class.serialise())

    for a_class in course.get_class_ongoing():
        ongoing.append(a_class.serialise())

    seralise["class"] = {
        "enrolling": enrolment,
        "ongoing": ongoing,
    }

    response = {
        "success": True,
        "result": {"type": "Course", "records": seralise},
    }

    return jsonify(response), status_code
