from flask import jsonify
from typing import List

from main import db
from model.Class import Class
from model.Course import Course
from model.CoursePreq import CoursePreq
from model.Learner import Learner
from model.LearnerCourseCompletion import LearnerCourseCompletion
from model.LoginSession import LoginSession
from api.error import throw_error


def get_course(course_id: int):
    """
    Get course and ongoing and upcoming classes
    """
    course: Course = Course.query.filter_by(id=course_id).first()

    if course is None:
        error_type = "Course"
        message = "Invalid course id"
        return throw_error(type=error_type, message=message)

    serialise = course.to_dict()
    serialise["class"] = get_course_classes(course)

    prereqs = []
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

    return jsonify(response), 200


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


def get_all_courses(is_retired: bool):
    """Return non retired courses"""
    course_list: List[Course] = Course.query.filter_by(is_retired=is_retired).all()
    courses_serialised = []

    for course in course_list:
        serialise = course.to_dict()
        serialise["class"] = get_course_classes(course)
        courses_serialised.append(serialise)

    response = {
        "success": True,
        "result": {"type": "Course", "records": courses_serialised},
    }

    return jsonify(response), 200


def get_course_classes(course: Course):
    enrolling = []
    ongoing = []

    for a_class in course.get_class_enrolment():
        enrolling.append(a_class.serialise())

    for a_class in course.get_class_ongoing():
        ongoing.append(a_class.serialise())

    return {"enrolling": enrolling, "ongoing": ongoing}


def get_prereq_courses(course_id: int):
    prereqs_list: List[CoursePreq] = CoursePreq.query.filter_by(
        course_id=course_id, is_active=True
    ).all()
    prereq_courses: List[Course] = []

    for prereq in prereqs_list:
        print(prereq)
        prereq_courses.append(prereq.get_prereq_course())

    return prereq_courses


def check_learner_course_valid(token: str, course_id: int):
    session: LoginSession = LoginSession.query.filter_by(token=token).first()
    learner = session.get_learner()

    if learner.isAdmin() == False:
        return throw_error("Authorisation", "Not Authorised", 403)

    # check preq courses
    prereq_course = get_prereq_courses(course_id)

    if len(prereq_course) == 0:
        response = {
            "success": True,
            "results": {"type": "enrolment_status", "msg": "OK"},
        }
        return response, 200

    # get learner completed courses
    completed_class: List[
        LearnerCourseCompletion
    ] = LearnerCourseCompletion.query.filter_by(user_id=learner.id).all()

    completed_course: List[Course] = []
    for complete in completed_class:
        class_details: Class = Class.query.filter_by(id=complete.class_id).first()
        course: Course = Course.query.filter_by(id=class_details.course_id).first()
        if course_id in prereq_course:
            completed_course.append(course)

    if len(completed_class) != len(completed_course):
        response = {
            "success": False,
            "results": {
                "type": "enrolment_status",
                "msg": "Does not fulfil pre-requisites",
            },
        }
        return response, 200

    response = {
        "success": True,
        "results": {
            "type": "enrolment_status",
            "msg": "OK",
        },
    }

    return response, 200
