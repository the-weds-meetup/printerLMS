from main import db
from model.Learner import Learner
from model.LearnerCourseCompletion import LearnerCourseCompletion
from flask import jsonify

# get learners by course
def get_learners_by_course(course_id):
    learners_complete_list = LearnerCourseCompletion.query.filter_by(
        course_id=course_id
    ).all()

    if len(learners_complete_list):
        return (
            jsonify(
                {
                    "data": [
                        each_learner.serialise()
                        for each_learner in learners_complete_list
                    ],
                }
            ),
            200,
        )
    return jsonify({"message": "There are no learners who completed this course"}), 404
