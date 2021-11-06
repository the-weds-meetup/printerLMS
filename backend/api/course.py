from flask import jsonify
from typing import List

from main import db
from model.Course import Course
from model.CoursePreq import CoursePreq
from model.Learner import Learner
from model.LoginSession import LoginSession

from controller.CourseController import CourseController


from api.error import throw_error


def response_get_completed_learners(course_id: int):
    learners = CourseController().get_course_completed_learners(course_id)
    learners_serialised = []

    for learner in learners:
        learners_serialised.append(learner.serialise())

    response = {
        "success": True,
        "result": {"type": "Course", "records": learners_serialised},
    }
    return jsonify(response), 200


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
    serialise["class"] = get_course_classes(course_id)

    prereqs = []
    for prereq_course in CourseController().get_prereq_courses(course_id):
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
        serialise["class"] = get_course_classes(course.id)
        courses_serialised.append(serialise)

    response = {
        "success": True,
        "result": {"type": "Course", "records": courses_serialised},
    }

    return jsonify(response), 200


def get_course_classes(course_id: int):
    enrolling = []
    ongoing = []
    past = []

    for a_class in CourseController().get_enrolling_classes_course(course_id=course_id):
        enrolling.append(a_class.serialise())

    for a_class in CourseController().get_ongoing_classes_course(course_id=course_id):
        ongoing.append(a_class.serialise())

    for a_class in CourseController().get_past_classes_courses(course_id=course_id):
        past.append(a_class.serialise())

    return {"enrolling": enrolling, "ongoing": ongoing, "past": past}
