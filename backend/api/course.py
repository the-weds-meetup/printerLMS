from flask import jsonify
from typing import List

from main import db
from model.Course import Course
from model.CoursePreq import CoursePreq
from model.Learner import Learner
from model.LoginSession import LoginSession
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

    status_code = 200
    serialise = course.to_dict()

    enrolment = []
    ongoing = []
    prereqs = []

    for a_class in course.get_class_enrolment():
        enrolment.append(a_class.serialise())

    for a_class in course.get_class_ongoing():
        ongoing.append(a_class.serialise())

    serialise["class"] = {
        "enrolling": enrolment,
        "ongoing": ongoing,
    }

    for prereq_course in get_prereq_courses(course_id):
        prereqs.append(
            {
                "id": prereq_course.id,
                "name": prereq_course.name,
            }
        )

    serialise["prerequisites"] = prereqs

    response = {
        "success": True,
        "result": {"type": "Course", "records": serialise},
    }

    return jsonify(response), status_code


def add_course(request_data: dict[str, any]):

    session: LoginSession = LoginSession.query.filter_by(
        token=request_data["token"]
    ).first()

    learner: Learner = session.get_learner()

    if learner.isAdmin() == False:
        return throw_error("Authorisation", "Not Authorised", 403)

    name = request_data["name"]
    description = request_data["description"]
    is_retired = request_data["is_retired"]
    coursePreReqs: List[int] = request_data["prerequisites"]

    course: Course = Course(name, description, is_retired)
    db.session.add(course)
    db.session.flush()

    if len(coursePreReqs) > 0:
        add_course_prereqs(course.id, coursePreReqs)

    db.session.commit()

    response = {
        "success": True,
        "result": {"type": "course_add", "msg": "Added a new course"},
    }

    return jsonify(response), 200


def add_course_prereqs(course_id: int, course_prereqs: List[int]):
    for prereq_id in course_prereqs:
        pre_reqs: CoursePreq = CoursePreq(course_id, prereq_id)
        db.session.add(pre_reqs)


def get_all_courses():
    """Return non retired courses"""
    course_list: List[Course] = Course.query.filter_by(is_retired=False).all()
    courses_serialised = []

    for course in course_list:
        courses_serialised.append(course.to_dict())
    status_code = 200

    response = {
        "success": True,
        "result": {"type": "Course", "records": courses_serialised},
    }

    return jsonify(response), status_code


def get_prereq_courses(course_id: int):
    prereqs_list: List[CoursePreq] = CoursePreq.query.filter_by(
        course_id=course_id, is_active=True
    ).all()
    prereq_courses: List[Course] = []

    for prereq in prereqs_list:
        print(prereq)
        prereq_courses.append(prereq.get_prereq_course())

    return prereq_courses
