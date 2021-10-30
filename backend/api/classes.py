from main import db
from model.Class import Class
from model.Learner import Learner
from model.Trainer import Trainer
from model.LearnerCourseCompletion import LearnerCourseCompletion
from flask import jsonify
from api.error import throw_error


# get class of the course along with the learners that has passed the class
def get_class(class_id: int):
    a_class: Class = Class.query.filter_by(class_id=class_id).first()

    if a_class is None:
        error_type = "Class"
        message = "Invalid Class id"
        return throw_error(type=error_type, message=message)

    serialise = a_class.to_dict()

    past_learners = []
    for each_past_learner in get_past_learners(class_id):
        learner: Learner = Learner.query.filter_by(id=each_past_learner.user_id).first()
        learner_name = learner.fullName()
        past_learners.append(
            {
                "user_id": each_past_learner.user_id,
                "name": learner_name,
            }
        )

    serialise["past_learners"] = past_learners

    response = {
        "success": True,
        "result": {"type": "Class", "records": serialise},
    }

    return jsonify(response), 200


def get_past_learners(class_id):
    past_learners: List[
        LearnerCourseCompletion
    ] = LearnerCourseCompletion.query.filter_by(class_id=class_id).all()

    return past_learners


def add_trainer(user_id, id):
    # queries a class according to what has been selected in AssignTrainers form
    a_class: Class = Class.query.filter_by(id=id).first()
    response = a_class.add_trainer(user_id)

    return jsonify(response), 200