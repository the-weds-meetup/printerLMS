from main import db
from model.Learner import Learner
from model.LearnerCourseCompletion import LearnerCourseCompletion
from flask import jsonify

# get learners by course
def get_learners_by_course(class_id):
    learners_complete_list = LearnerCourseCompletion.query.filter_by(
        class_id=class_id
    ).all()

    if len(learners_complete_list):
        return (
            jsonify(
                {
                    "success": True,
                    "result": {
                        "type": "Learner_Course_Completion",
                        "records": [
                            each_learner.to_dict()
                            for each_learner in learners_complete_list
                        ],
                    },
                }
            ),
            200,
        )
    return jsonify({"message": "There are no learners who completed this course"}), 404
