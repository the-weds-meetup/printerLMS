"""To get courses, and details of its respective classs"""
from typing import Any, List
import dateutil.parser
import datetime
import pytz

from model.Course import Course
from model.CoursePreq import CoursePreq
from model.Class import Class
from model.Enrolment import Enrolment
from model.Learner import Learner
from model.LearnerCourseCompletion import LearnerCourseCompletion

from controller.ClassController import ClassController


class CourseController:
    def get_prereq_courses(self, course_id: int):
        prereqs_list: List[CoursePreq] = CoursePreq.query.filter_by(
            course_id=course_id, is_active=True
        ).all()
        prereq_courses: List[Course] = []

        for prereq in prereqs_list:
            prereq_courses.append(prereq.get_prereq_course())

        return prereq_courses

    def get_past_classes_courses(self, course_id: int):
        classes: List[Class] = Class.query.filter_by(course_id=course_id).all()
        past_class: List[Class] = []
        time_now = datetime.datetime.now(pytz.utc)

        if len(classes) == 0:
            return classes

        # determine which classes are completed
        # current time > class_end_date
        for a_class in classes:
            end_date = dateutil.parser.parse(a_class.class_end_date)

            if time_now >= end_date:
                past_class.append(a_class)

        return past_class

    def get_enrolling_classes_course(self, course_id: int):
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

    def get_ongoing_classes_course(self, course_id: int):
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

    def get_course_completed_learners(self, course_id: int):
        learner_completed: List[Learner] = []
        completed_classes = self.get_past_classes_courses(course_id=course_id)

        all_learner_completed: List[
            LearnerCourseCompletion
        ] = LearnerCourseCompletion.query.all()

        completed_classes_id_list = []
        for cclass in completed_classes:
            completed_classes_id_list.append(cclass.id)

        for learner in all_learner_completed:
            if learner.class_id in completed_classes_id_list:
                match_learner: Learner = Learner.query.filter_by(
                    id=learner.user_id
                ).first()
                learner_completed.append(match_learner)

        return learner_completed

    def get_course_incompleted_learners(self, course_id: int):
        """Return learners who either taking the course now or not enrolled in the course"""
        learner_incompleted: List[Learner] = []
        learner_completed = self.get_course_completed_learners(course_id=course_id)

        learners: List[Learner] = Learner.query.filter_by(department_id=2).all()

        completed_learner_id = []
        for learner in learner_completed:
            completed_learner_id.append(learner.id)

        for learner in learners:
            if learner.id not in completed_learner_id:
                learner_incompleted.append(learner)

        return learner_incompleted
