from flask import jsonify
from typing import List

from api.course import get_prereq_courses
from api.error import throw_error

from main import db
from model.Class import Class
from model.Course import Course
from model.Enrolment import Enrolment
from model.LoginSession import LoginSession
import dateutil.parser
import datetime
import pytz


def get_approved_enrolments(user_id):
    enrolment_list: Enrolment = Enrolment.query.filter_by(user_id=user_id).all()
    time_now = datetime.datetime.now(pytz.utc)
    upcoming = []
    ongoing = []
    past = []

    for each_enrol in enrolment_list:
        if each_enrol.is_approved:
            a_class: Class = Class.query.filter_by(class_id=each_enrol.class_id).first()
            class_start = dateutil.parser.parse(a_class.class_start_date)
            class_end = dateutil.parser.parse(a_class.class_end_date)

            # if a_class is None:
            #     error_type = "Class"
            #     message = "Invalid Class id"
            #     return throw_error(type=error_type, message=message)

            course: Course = Course.query.filter_by(id=a_class.course_id).first()
            #serialise = course.to_dict()

            if time_now < class_start:
                upcoming.append(
                    {
                        "course_name": course.name,
                        "class_id": a_class.class_id,
                        "progress": each_enrol.course_progress,
                        "class_start_date": a_class.class_start_date,
                        "class_end_date": a_class.class_end_date,
                    }
                )

            elif time_now >= class_start and time_now < class_end:
                ongoing.append(
                    {
                        "course_name": course.name,
                        "class_id": a_class.class_id,
                        "progress": each_enrol.course_progress,
                        "class_start_date": a_class.class_start_date,
                        "class_end_date": a_class.class_end_date,
                    }
                )

            elif time_now > class_end:
                past.append(
                    {
                        "course_name": course.name,
                        "class_id": a_class.class_id,
                        "progress": each_enrol.course_progress,
                        "class_start_date": a_class.class_start_date,
                        "class_end_date": a_class.class_end_date,
                    }
                )

    return {"upcoming": upcoming, "ongoing": ongoing, "past": past}
