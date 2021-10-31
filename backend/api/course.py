from flask import jsonify
from typing import List
import dateutil.parser
import datetime
import pytz

from main import db
from model.Class import Class
from model.Course import Course
from model.CoursePreq import CoursePreq
from model.Enrolment import Enrolment
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
    serialise["class"] = get_course_classes(course_id)

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

    for a_class in get_enrolling_classes_course(course_id=course_id):
        enrolling.append(a_class.serialise())

    for a_class in get_ongoing_classes_course(course_id=course_id):
        ongoing.append(a_class.serialise())

    for a_class in get_past_classes_courses(course_id=course_id):
        past.append(a_class.serialise())

    return {"enrolling": enrolling, "ongoing": ongoing, "past": past}


def get_past_classes_courses(course_id: int):
    classes: List[Class] = Class.query.filter_by(course_id=course_id).all()
    past_class: List[Class] = []
    time_now = datetime.datetime.now(pytz.utc)

    if len(classes) == 0:
        return classes

    for a_class in classes:
        end_date = dateutil.parser.parse(a_class.class_end_date)

        if time_now >= end_date:
            past_class.append(a_class)

    return past_class


def get_completed_classes_courses(course_id: int):
    classes: List[Class] = Class.query.filter_by(course_id=course_id).all()
    completed_class: List[Class] = []
    time_now = datetime.datetime.now(pytz.utc)

    if len(classes) == 0:
        return completed_class

    # determine which classes are completed
    # current time > class_end_date
    for a_class in classes:
        enrolment_end = dateutil.parser.parse(a_class.class_end_date)

        if time_now > enrolment_end:
            completed_class.append(a_class)

    return completed_class


def get_enrolling_classes_course(course_id: int):
    classes: List[Class] = Class.query.filter_by(course_id=course_id).all()
    enrolment_class: List[Class] = []
    time_now = datetime.datetime.now(pytz.utc)

    if len(classes) == 0:
        return enrolment_class

    # determine which classes are ongoing enrolment
    # ongoing enrolment start <= current time < ongoing enrolment end
    for a_class in classes:
        enrolment_start = dateutil.parser.parse(a_class.enrolment_start_date)
        enrolment_end = dateutil.parser.parse(a_class.enrolment_end_date)

        if time_now >= enrolment_start and time_now < enrolment_end:
            enrolment_class.append(a_class)

    return enrolment_class


def get_ongoing_classes_course(course_id: int):
    classes: List[Class] = Class.query.filter_by(course_id=course_id).all()
    enrolment_class: List[Class] = []
    time_now = datetime.datetime.now(pytz.utc)

    if len(classes) == 0:
        return enrolment_class

    # determine which classes are being taught now
    # ongoing enrolment start <= current time < ongoing enrolment end
    for a_class in classes:
        enrolment_start = dateutil.parser.parse(a_class.enrolment_start_date)
        enrolment_end = dateutil.parser.parse(a_class.enrolment_end_date)

        if time_now >= enrolment_start and time_now < enrolment_end:
            enrolment_class.append(a_class)

    return enrolment_class


def get_prereq_courses(course_id: int):
    prereqs_list: List[CoursePreq] = CoursePreq.query.filter_by(
        course_id=course_id, is_active=True
    ).all()
    prereq_courses: List[Course] = []

    for prereq in prereqs_list:
        prereq_courses.append(prereq.get_prereq_course())

    return prereq_courses


def get_course_completed_learners(course_id: int):
    learner_completed: List[Learner] = []
    completed_classes = get_completed_classes_courses(course_id=course_id)

    all_learner_completed: List[
        LearnerCourseCompletion
    ] = LearnerCourseCompletion.query.all()

    completed_classes_id_list = []
    for cclass in completed_classes:
        completed_classes_id_list.append(cclass.id)

    for learner in all_learner_completed:
        if learner.class_id in completed_classes_id_list:
            match_learner: Learner = Learner.query.filter_by(id=learner.user_id).first()
            learner_completed.append(match_learner)

    return learner_completed


def get_course_incompleted_learners(course_id: int):
    """Return learners who either taking the course now or not enrolled in the course"""
    learner_incompleted: List[Learner] = []
    learner_completed = get_course_completed_learners(course_id=course_id)

    learners: List[Learner] = Learner.query.filter_by(department_id=2).all()

    completed_learner_id = []
    for learner in learner_completed:
        completed_learner_id.append(learner.id)

    for learner in learners:
        if learner.id not in completed_learner_id:
            learner_incompleted.append(learner)

    return learner_incompleted
