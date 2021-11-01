from typing import Any, List

from model.Course import Course
from model.Class import Class
from model.Enrolment import Enrolment
from model.Learner import Learner

from controller.CourseController import CourseController
from controller.LearnerController import LearnerController


class ClassController:
    def get_all_enrollable_classes(self):
        course_list: List[Course] = Course.query.all()
        enrolling_class = []

        for course in course_list:
            enrolling: List[Class] = CourseController.get_enrolling_classes_course(
                course.id
            )

            # check if class is full
            for enrol_class in enrolling:
                # check that class is not full
                current_learners = self.get_class_learners(enrol_class.id)
                if len(current_learners) < enrol_class.max_capacity:
                    serialise = enrol_class.serialise()
                    serialise["current_capacity"] = len(current_learners)
                    serialise["course_name"] = course.name
                    enrolling_class.append(self.get_class(enrol_class.id))

        return enrolling_class

    def get_class(self, class_id: int):
        a_class: Class = Class.query.filter_by(id=class_id).first()
        learners = []

        if a_class is None:
            raise Exception("Class", "Invalid ClassID")

        serialise = a_class.to_dict()
        for learner in self.get_class_learners(class_id):
            learners.append(learner.serialise())

        serialise["learners"] = learners
        serialise["current_capacity"] = len(learners)
        serialise["course_name"] = a_class.get_course().name
        return serialise

    def get_class_learners(self, class_id: int):
        enrolments: List[Enrolment] = Enrolment.query.filter_by(
            class_id=class_id, is_approved=True, is_withdrawn=False
        ).all()
        learners: List[Learner] = []

        for enrolment in enrolments:
            learner: Learner = Learner.query.filter_by(id=enrolment.user_id).first()
            learners.append(learner)
        return learners

    def get_class_non_enrolled_learners(self, class_id: int):
        """
        Get a list of learners who are eligible for the course,
        but have yet to be enrolled or is not current taking any of the class right now
        """
        current_class: Class = Class.query.filter_by(id=class_id).first()
        incompleted_learners = CourseController.get_course_incompleted_learners(
            current_class.get_course().id
        )
        course_id = current_class.get_course().id
        ongoing_learners = self.get_class_learners(class_id)
        nonstarted_learners: List[Learner] = []

        for learner in incompleted_learners:
            is_match = False
            for ongoing_learner in ongoing_learners:
                if ongoing_learner.id == learner.id:
                    is_match = True
                    break

            if (
                is_match == False
                and LearnerController.is_learner_eligible_for_enrolment(
                    learner.id, course_id
                )
            ):
                nonstarted_learners.append(learner)

        return nonstarted_learners
