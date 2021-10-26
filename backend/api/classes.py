from main import db
from model.Class import Class
from model.Learner import Learner
from model.Trainer import Trainer
from model.LearnerCourseCompletion import LearnerCourseCompletion
from flask import jsonify
from api.error import throw_error

# get all classes
def get_classes():
    class_list = Class.query.all()
    if len(class_list):
        return jsonify(
            {
                "code": 200,
                "data": [each_class.serialise() for each_class in class_list],
            }
        )
    return jsonify({"code": 404, "message": "There are no classes"}), 404


# get classes by course
def get_classes_by_course(course_id):
    class_list = Class.query.filter_by(course_id=course_id).all()
    if len(class_list):
        return jsonify(
            {
                "code": 200,
                "data": [each_class.serialise() for each_class in class_list],
            }
        )
    return jsonify({"code": 404, "message": "There are no classes"}), 404


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
        "result": {"type": "Course", "records": serialise},
    }

    return jsonify(response), 200


def get_past_learners(class_id):
    past_learners: List[
        LearnerCourseCompletion
    ] = LearnerCourseCompletion.query.filter_by(class_id=class_id).all()

    return past_learners


def add_trainer(user_id, class_id):
    # trainer: Trainer = trainer
    a_class: Class = Class.query.filter_by(class_id=class_id).first()
    response = a_class.add_trainer(user_id)

    return jsonify(response), 200